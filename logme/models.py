from django.db import models
from django.contrib.auth.models import User
from datetime import datetime, timedelta
import datetime
from datetime import datetime


class Account(models.Model):
	OJT = 'OJT'
	REG = 'RE'
	UNREG = 'URE'
	EMPLOYEE_CHOICE = (
		(OJT, 'OJT'),
		(REG, 'Regular'),
		(UNREG, 'Not Regular'),
	)


	classtype = models.CharField(max_length=5,
									choices = EMPLOYEE_CHOICE,
									default = REG)
	
	user = models.OneToOneField(User, related_name='account')

	status = models.CharField(max_length=10, default='offline')

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

		time_difference = (self.timeout - self.timein)
	
		return time_difference

	def __unicode__(self):
		return '{0}' .format('Timelog')

class Total(models.Model):
	account = models.ForeignKey(Account, related_name='total')
	today_in = models.DateField(auto_now_add=True)
	today_total = models.CharField(max_length=100)

	def __unicode__(self):
		return '{0}' .format('Totals')