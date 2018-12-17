from django.contrib.auth import login, authenticate
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.views import View
from .forms import *



# Logowanie użytkownika
class LoginUserView(View):

    def get(self, request):
        form = LoginUserForm()
        return render(request, 'wish_list/loginUser.html', {'form': form})

    def post(self, request):
        form = LoginUserForm(request.POST)
        if form.is_valid():
            user = authenticate(username=form.cleaned_data.get('email'), password=form.cleaned_data.get('password'))
            if user is not None:
                login(request, user)
                next = request.GET.get('next')
                if next is not None:
                    return redirect(next)
                return render(request, 'wish_list/loginUser.html')
            else:
                return HttpResponse("Login i/lub hasło jest niepoprawne")

