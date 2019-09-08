from django.conf.urls import url
from django.contrib.auth import views as auth_view
from . import views
from django.contrib.auth.models import User

app_name='song'

urlpatterns = [
    url(r'^$', views.index, name='index'),
    # url(r'^login/$', auth_view.login, {'template_name':'song/login.html'}, name='login'),
    url(r'^login/$', auth_view.LoginView.as_view(template_name="song/login.html"), name='login'),
    # url(r'^logout/$', auth_view.LogoutView.as_view (template_name="song/logout.html"), name='logout'),
    url(r'^logout/$', auth_view.LogoutView.as_view(template_name="song/index.html"), name='logout'),
    url(r'^register/$', views.register, name='register'),
    url(r'^activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',views.activate, name='activate'),
    url(r'^dashboard/$', views.dashboard, name='dashboard'),
    url(r'^recommend/(?P<id>[0-9]+)/play/$', views.recommend, name = 'recommend'),
    url(r'^rate/(?P<id>[0-9]+)/$', views.rate, name = 'rate'),
]
