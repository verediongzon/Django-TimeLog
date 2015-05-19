from django.db import models
from django.contrib.auth.models import User
from datetime import datetime, timedelta


class Account(models.Model):
	
	user = models.OneToOneField(User, related_name='account')
	status = models.CharField(max_length=10, default='offline')
	employee_type = models.CharField(max_length=20)
	rate = models.IntegerField(default=0)

	@property
	def fullname(self):
		return '{0} {1}'.format(self.user.first_name, self.user.last_name)

	def __unicode__(self):
		return self.user.first_name


class History(models.Model):
	account = models.ForeignKey(Account, related_name='history')
	timein = models.DateTimeField(auto_now_add=True)
	timeout = models.DateTimeField(null=True)
	
	
	@property
	def totaltime(self):
		if not self.timeout:
			partial = timedelta(0)
			return partial

		
		time_difference = self.timeout - self.timein

		return time_difference

	def __unicode__(self):
		return '{0}' .format('Timelog')

class Total(models.Model):
	account = models.ForeignKey(Account, related_name='total')
	today_in = models.DateField(auto_now_add=True)
	today_total = models.CharField(max_length=100)

	@property
	def salarytotal(self):
		time =  str(self.today_total)
		print time
		daysalary =  int(time.split(":")[0]) * self.account.rate
		return daysalary

	def __unicode__(self):
		return '{0}' .format('Totals')