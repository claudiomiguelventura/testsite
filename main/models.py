from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class ToDoList(models.Model):
	user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="todolist", null=True)
	name = models.CharField(max_length=200)

	def __str__(self):
		return self.name


class Item(models.Model):
	todolist = models.ForeignKey(ToDoList, on_delete=models.CASCADE)
	text = models.CharField(max_length=300)
	complete = models.BooleanField()

	def __str__(self):
		return self.text

class RainTable(models.Model):
	district = models.CharField(max_length=50)
	county = models.CharField(max_length=50)
	county_code = models.CharField(max_length=5)
	
	def __str__(self):
		return self.county

class RainDay(models.Model):
	rainTable = models.ForeignKey(RainTable, on_delete=models.CASCADE)
	rd_date = models.DateField()
	rd_minimum = models.FloatField()
	rd_maximum = models.FloatField()
	rd_range = models.FloatField()
	rd_mean = models.FloatField()
	rd_std = models.FloatField()

	def __str__(self):
		return "%s" % (str(self.rd_date))