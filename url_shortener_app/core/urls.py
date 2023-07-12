from django.urls import path

from . import views

app_name = 'core'

urlpatterns = [
    path('', views.redirect_home, name='redirect_home'),
    path('home', views.home,  name='home'),
    # following url is used to redirect to home and show login_required error to the user
    path('accounts/login/', views.login_required, name='login-required'),
    path('auth/register', views.RegisterView.as_view(), name='register'),
    path('auth/login', views.LoginView.as_view(), name='login'),
    path('auth/logout', views.logout_view, name='logout'),
    path('shorten-url', views.ShortenUrlView.as_view(), name='shorten-url'),
]
