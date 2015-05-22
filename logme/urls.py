from django.conf.urls import patterns, url

from logme import views

urlpatterns = patterns('',
	url(r'^$', views.Index.as_view(), name = 'index'),
	url(r'^home/$', views.Home_Page.as_view(), name = 'home'),
	url(r'^register/$', views.Register.as_view(), name = 'register'),
	url(r'^history/$', views.Day_Total.as_view(), name = 'history'),
	url(r'^homes/$', views.Admin_Home.as_view(), name='admin'),
	url(r'^profile/(?P<pk>\d+)/$', views.Profile.as_view(), name='profile'),
	url(r'^daytotal/(?P<pk>\d+)/$', views.Histories.as_view(), name='daytotal'),
	url(r'^change/$', views.ChangePassword.as_view(), name='change_password'),
	url(r'^manage/$', views.Manage_User.as_view(), name = 'manage'),
)