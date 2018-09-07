from django.db import models

# Create your models here.

class Student(models.Model):
	name = models.CharField(max_length=128)

	def __str__(self):
		return self.name

class Section(models.Model):
	name = models.CharField(max_length=128)
	members = models.ManyToManyField(Student, through='Enrollment')

	def __str__(self):
		return self.name


class Enrollment(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    section = models.ForeignKey(Section, on_delete=models.CASCADE)

class Enrollment1(models.Model):    
	student = models.CharField(max_length=128)
	section = models.CharField(max_length=128)

 