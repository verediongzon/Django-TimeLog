import datetime
from django.http import HttpResponseRedirect, HttpRequest
from django.views import generic
from django.contrib import auth
from django.shortcuts import render, redirect, render_to_response, get_object_or_404
from django.contrib.auth import authenticate, login, logout, forms as user_forms
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.models import User
from logme.models import Account, History, Total
from django.utils import timezone
from django.template import Context
from django.views.generic.edit import FormView
from datetime import timedelta
from django.core.exceptions import ObjectDoesNotExist
from django.core.urlresolvers import reverse


from logme.forms import RegistrationForm, PasswordChangeForm


class Index(generic.TemplateView):
    template_name = 'logme/form.html'

    def get(self, request):

        if request.user.is_authenticated():
            if request.user.is_superuser:
                return redirect('logat:admin')
            return redirect('logat:home')

        else:
            return self.render_to_response({})


    def post(self, request, *args, **kwargs):	
		username = request.POST.get('username', '')
		password = request.POST.get('password', '')
		user = auth.authenticate(username=username, password=password)


		if user is not None:

			if user.is_superuser:
				auth.login(request, user)
				return redirect('logat:admin')

			else:

				try:				
					account = Account.objects.get(user=user)
					count = user.account.total.filter(today_in=datetime.date.today()).count()
					

				except ObjectDoesNotExist:
					return render(request, 'logme/form.html', {
		            'error_message': "Please Contact the Administrator for Activation",
		        	})
			
				else:				
					auth.login(request,user)
					account.status='online'
					account.save()				
					log = History(account=account)
					log.save()

					if count == 0:
						todate=Total(account=account)
						todate.save()

					return redirect('logat:home')


		else:
			 return render(request, 'logme/form.html', {
            'error_message': "Username/Password Invalid. Please Try Again.",
        })



class Home_Page(generic.TemplateView):

    template_name = 'logme/home.html'


    def get(self, request):

		if request.user.is_authenticated():

			searching = request.GET.get('months')		

			getting_last_history = self.request.user.account.history.last()

			if searching:
				sorting_history = self.request.user.account.history.filter(timein__month=searching).order_by("-timein")

			else:
				sorting_history = self.request.user.account.history.order_by('-timein')

			getting_last_history.timeout = timezone.now()
			getting_last_history.save()

			timein = getting_last_history.timein
			str(timein)
			datenow = timein.strftime('%Y-%m-%d')

			filtered_history = self.request.user.account.history.filter(timein__startswith=datenow)

			

			today_total= timedelta(0)

			for total in filtered_history:
				today_total += total.totaltime

			
			today = self.request.user.account.total.last()
			
			today.today_total = today_total
			today.save()


			return self.render_to_response({'sorts':sorting_history, 'timein':timein,'today_total':today_total})

		return redirect("logat:index")

    def post(self, request):
		
		if request.POST.get('logout'):	


			logout=self.request.user.account.history.last()
			
			logout.timeout = timezone.now()			

			logout.save()

			getting_last_history = self.request.user.account.history.last()
			timein = getting_last_history.timein
			str(timein)
			datenow = timein.strftime('%Y-%m-%d')


			filtered_history = self.request.user.account.history.filter(timein__startswith=datenow)

			today_total = timedelta(0)

			for total in filtered_history:
				today_total += total.totaltime

			
			today = self.request.user.account.total.last()
			today.today_total = today_total
			today.save()


			out = Account.objects.get(user=self.request.user)
			out.status = 'offline'
			out.save()

			auth.logout(request)
			return redirect('logat:index')

		if request.POST.get('history'):

			return redirect('logat:history')

		if request.POST.get('cpass'):
			return redirect('logat:change_password')

		if request.POST.get('search2'):

			months = request.POST.get('month','')

			home_url = "{}?months={}".format(reverse('logat:home'), months)

			return HttpResponseRedirect(home_url)

			

class Register(SuccessMessageMixin, generic.FormView):
    template_name = 'logme/register.html'
    form_class = RegistrationForm
    success_url = '/'
    success_message = "Your account was created successfully. Wait for Admin confirmation."

    def post(self, request):
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        if form.is_valid():
            form.save()
            return self.form_valid(form)

        else:
            return self.form_invalid(form)
    


class Day_Total(generic.TemplateView):
	template_name = 'logme/history.html'

	def get(self, request):
		display = self.request.user.account.total.all()

		return self.render_to_response({'display':display})


class Admin_Home(generic.TemplateView):
	template_name = 'logme/homes.html'


	def get(self, request):
	 	if request.user.is_authenticated():

	 		host_display = Account.objects.all()


	 		return self.render_to_response({'display':host_display})

	 	else:
			return redirect('logat:index')


	def post(self, request):


		if request.POST.get('logout'):
			auth.logout(request)
			return redirect('logat:index')

		if request.POST.get('history'):
			selected_user = request.POST.get('naming','')

			return HttpResponseRedirect(reverse('logat:profile', args=[selected_user]))

		if request.POST.get('daytotal'):
			selected_user = request.POST.get('naming','')
			
			return HttpResponseRedirect(reverse('logat:daytotal', args=[selected_user]))


class Profile(generic.TemplateView):
	template_name = 'logme/profile.html'	
	
	def get(self, request, pk):

		u_account = Account.objects.get(pk=pk)
		u_history = u_account.history.order_by('-timein')
			
		return self.render_to_response({'show_history':u_history})


class Histories(generic.TemplateView):
	template_name = 'logme/histories.html'

	def get(self, request, pk):

		u_account = Account.objects.get(pk=pk)
		u_total = u_account.total.all() 

		return self.render_to_response({'u_total_show':u_total})


class ChangePassword(generic.TemplateView):
    template_name = 'logme/change_password.html'

    def get_context_data(self, *args, **kwargs):
        context = {}
        context['password_form'] = PasswordChangeForm(data=self.request.POST or None, user=self.request.user)
        return context

    def post(self, request):
        context = self.get_context_data()
        form = context['password_form']
        if form.is_valid():
            form.save()
            context['change'] = True
        return self.render_to_response(context)
