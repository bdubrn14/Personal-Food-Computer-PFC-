from django.db import models
from django.contrib.postgres.fields import JSONField

# Create your models here.
class ParsedRecipe(models.Model):
	minute = models.IntegerField()
	phase = models.TextField()
	cycle = models.TextField()
	environment_name = models.TextField()
	environment_state = JSONField()

	# class Meta:
	# 	app_label = 'app'