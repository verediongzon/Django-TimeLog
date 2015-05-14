from django.contrib import admin
from logme.models import Account, History, Total
from django.contrib.auth.models import User


class TotalInline(admin.TabularInline):
	readonly_fields = ['today_in', 'today_total']
	model = Total
	

class HistoryInline(admin.TabularInline):
	readonly_fields = ['timein', 'timeout', 'totaltime']
	model = History

class AccountAdmin(admin.ModelAdmin):

	list_display = ['classtype', 'user','fullname','status']
	inlines = [HistoryInline, TotalInline]
	

admin.site.register(Account, AccountAdmin)