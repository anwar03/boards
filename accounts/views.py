from django.contrib.auth import login as auth_login
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.generic import UpdateView, CreateView


from .forms import signUpForm, UserUpdateForm
# Create your views here.


class SignUp(CreateView):
    form_class = signUpForm
    template_name = 'signup.html'

    def form_valid(self, form):
        user = form.save()
        auth_login(self.request, user)
        return redirect('home')
    

class UserUpdateView(UpdateView):
    form_class = UserUpdateForm
    template_name = 'accounts.html'
    success_url = reverse_lazy('my_accounts')

    def get_object(self):
        return self.request.user

