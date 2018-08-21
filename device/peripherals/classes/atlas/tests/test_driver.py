# Import standard python libraries
import sys, os, pytest

# Import driver elements
from device.peripherals.classes.atlas.driver import AtlasDriver
from device.peripherals.classes.atlas.simulator import AtlasSimulator
from device.comms.i2c2.mux_simulator import MuxSimulator


def test_init():
    driver = AtlasDriver(
        name="Test",
        bus=2,
        address=0x64,
        simulate=True,
        mux_simulator=MuxSimulator(),
        Simulator=AtlasSimulator,
    )


def test_read_info():
    driver = AtlasDriver(
        "Test",
        2,
        0x64,
        simulate=True,
        mux_simulator=MuxSimulator(),
        Simulator=AtlasSimulator,
    )
    info = driver.read_info()
    assert info.sensor_type == "ec"
    assert info.firmware_version == "1.96"


def test_read_status():
    driver = AtlasDriver(
        "Test",
        2,
        0x64,
        simulate=True,
        mux_simulator=MuxSimulator(),
        Simulator=AtlasSimulator,
    )
    status = driver.read_status()
    assert status.prev_restart_reason == "Powered off"
    assert status.voltage == 3.655


def test_enable_protocol_lock():
    driver = AtlasDriver(
        "Test",
        2,
        0x64,
        simulate=True,
        mux_simulator=MuxSimulator(),
        Simulator=AtlasSimulator,
    )
    driver.enable_protocol_lock()


def test_disable_protocol_lock():
    driver = AtlasDriver(
        "Test",
        2,
        0x64,
        simulate=True,
        mux_simulator=MuxSimulator(),
        Simulator=AtlasSimulator,
    )
    driver.disable_protocol_lock()


def test_enable_led():
    driver = AtlasDriver(
        "Test",
        2,
        0x64,
        simulate=True,
        mux_simulator=MuxSimulator(),
        Simulator=AtlasSimulator,
    )
    driver.enable_led()


def test_disable_led():
    driver = AtlasDriver(
        "Test",
        2,
        0x64,
        simulate=True,
        mux_simulator=MuxSimulator(),
        Simulator=AtlasSimulator,
    )
    driver.disable_led()


def test_enable_sleep_mode():
    driver = AtlasDriver(
        "Test",
        2,
        0x64,
        simulate=True,
        mux_simulator=MuxSimulator(),
        Simulator=AtlasSimulator,
    )
    driver.enable_sleep_mode()
