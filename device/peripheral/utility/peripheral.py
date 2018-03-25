# Import python modules
import logging, time, threading

# Import all possible states & errors
from device.utility.states import States
from device.utility.errors import Errors


class Peripheral:
    """ Parent class for peripheral devices e.g. sensors and actuators. """

    # Initialize logger
    logger = logging.getLogger(__name__)

    # Initialize state and error lists
    states = States()
    errors = Errors()

    # Initialize state & error variables
    _state = None
    _error = None

    # Initialize timeing variables
    sampling_interval_sec = 2
    last_update_time = None


    def __init__(self, name, config, env, sys):
        """ Initializes SHT25. """
        self.name = name
        self.config = config
        self.env = env
        self.sys = sys

        # Initialize communication
        self.bus = config["comms"]["bus"]
        self.mux = config["comms"]["mux"]
        self.channel = config["comms"]["channel"]
        self.address = config["comms"]["address"]

        # Initialize peripheral specific config
        self.initialize_peripheral_config()

        # Set state & error values
        self.state = self.states.SETUP
        self.error = self.errors.NONE

        # Initialize thread object


    @property
    def state(self):
        """ Gets state value. """
        return self._state


    @state.setter
    def state(self, value):
        """ Safely updates peripheral state in system object each time
            it is changed. """
        self._state = value
        with threading.Lock():
            if self.name not in self.sys.peripheral_state:
                self.sys.peripheral_state[self.name] = {}
            self.sys.peripheral_state[self.name]["state"] = self._state


    def commanded_state(self):
        """ Gets the peripheral's commanded state. """
        if self.name in self.sys.peripheral_state and \
            "commanded_state" in self.sys.peripheral_state[self.name]:
            return self.sys.peripheral_state[self.name]["commanded_state"]
        else:
            return None


    @property
    def error(self):
        """ Gets error value. """
        return self._error


    @error.setter
    def error(self, value):
        """ Safely updates peripheral error in system object each time
            it is changed. """
        self._error= value
        with threading.Lock():
            if self.name not in self.sys.peripheral_state:
                self.sys.peripheral_state[self.name] = {}
            self.sys.peripheral_state[self.name]["error"] = self._error

    def spawn(self):
        """ Spawns peripheral thread. """
        self.thread = threading.Thread(target=self.state_machine)
        self.thread.daemon = True
        self.thread.start()


    def state_machine(self):
        """ Runs state machine. """
        self.logger.info("Starting state machine")
        while True:
            if self.state == self.states.SETUP:
                self.setup_state()
            elif self.state == self.states.INIT:
                self.init_state()
            elif self.state == self.states.NOS:
                self.nos_state()
            elif self.state == self.states.ERROR:
                self.error_state()
            elif self.state == self.states.RESET:
                self.reset_state()


    def setup_state(self):
        """ Runs setup state. Waits for system to enter initialization state 
            then transitions to initialization state. """
        self.logger.info("{} entered SETUP state".format(self.name))
        while self.sys.state != self.states.INIT:
            time.sleep(0.100) # 100ms
        self.state = self.states.INIT


    def init_state(self):
        """ Runs initialization state. Initializes sensor then transitions to 
            normal operating state. Transitions to error state on error. """
        self.logger.info("{} entered INIT state".format(self.name))
        self.initialize_peripheral()
        self.state = self.states.NOS


    def nos_state(self):
        """ Runs normal operation state. Gets temperature and humidity reading
            every <sampling_rate> seconds. Transitions to reset if commanded. 
            Transitions to error state on error. """
        self.logger.info("{} entered NOS state".format(self.name))
        self.last_update_time_sec = time.time()
        while True:
            if self.sampling_interval_sec < time.time() - self.last_update_time_sec:
                self.update_peripheral()
                self.last_update_time_sec = time.time()
            else:
                time.sleep(0.100) # 100ms

            if self.commanded_state() == self.states.RESET:
                self.state = self.commanded_state()
                continue
            elif self.state == self.states.ERROR:
                continue

    def error_state(self):
        """ Runs error state. Waits for commaned state to be set to reset,
            then transitions to reset state. """
        self.logger.info("{} entered ERROR state".format(self.name))
        while (self.sys.state != self.states.RESET and \
            self.commanded_state() != self.states.RESET):
            time.sleep(0.1) # 100ms
        self.state = self.states.RESET


    def reset_state(self):
        """ Runs reset state. Resets device state then transitions to 
            initialization state. """
        self.logger.info("{} entered RESET state".format(self.name))
        self.error = self.errors.NONE
        self.state = self.state.INIT
        self.reset_peripheral()