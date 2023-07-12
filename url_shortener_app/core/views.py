from django.shortcuts import render, reverse, redirect
import pyshorteners as pyshorteners
from django.http import HttpResponse, HttpResponseRedirect
from django.views.generic.edit import FormView
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from core.forms import LoginForm, ShortenUrlForm, RegisterForm


def redirect_home(request):
    return HttpResponseRedirect(reverse('core:home'))


def home(request, **kwargs):
    user_login_required = kwargs.get('login_required', False)
    return render(request, 'home.html', context={'login_required': user_login_required})


def login_required(request):
    return home(request, login_required=True)


class RegisterView(FormView):
    form_class = RegisterForm

    def get(self, request, *args, **kwargs):
        return HttpResponseRedirect(self.get_success_url())

    def get_success_url(self):
        return reverse('core:home')

    def form_valid(self, form):
        user = form.save()
        if user is not None:
            login(self.request, user)
            return redirect('core:home')

    def form_invalid(self, form):
        return render(self.request, 'home.html', {'register_form': form})


class LoginView(FormView):
    form_class = LoginForm

    def get(self, request, *args, **kwargs):
        return HttpResponseRedirect(self.get_success_url())

    def get_success_url(self):
        return reverse('core:home')

    def form_valid(self, form):
        user = authenticate(
            username=form.cleaned_data['mobile_number'],
            password=form.cleaned_data['password'],
        )
        if user is not None:
            login(self.request, user)
            return redirect('core:home')

    def form_invalid(self, form):
        return render(self.request, 'home.html', {'login_form': form})


class ShortenUrlView(LoginRequiredMixin, FormView):
    form_class = ShortenUrlForm

    def get(self, request, *args, **kwargs):
        return HttpResponseRedirect(self.get_success_url())

    def get_success_url(self):
        return reverse('core:home')

    def form_valid(self, form):
        url = form.cleaned_data['url']
        shortener = pyshorteners.Shortener()
        shortened_url = shortener.tinyurl.short(url)
        context = {'shortened_url': shortened_url,
                   'url': url}
        return render(self.request, 'home.html', context=context)

    def form_invalid(self, form):
        return render(self.request, 'home.html', {'url_form': form})


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse('core:home'))
