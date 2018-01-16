from django.contrib.auth import login as auth_login
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.generic import UpdateView


from .forms import signUpForm
# Create your views here.


def signup(request):
    
    if request.method == 'POST':
        form = signUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            auth_login(request, user)
            return redirect('home')
    else:
        form = signUpForm()
    
    return render(request, 'signup.html',  { 'form': form })


class UserUpdateView(UpdateView):
    model = User
    template_name = 'accounts.html'
    fields = ('username','first_name','last_name', 'email')
    success_url = reverse_lazy('my_accounts')

    def get_object(self):
        return self.request.user

