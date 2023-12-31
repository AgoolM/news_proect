
from urllib import request
from django.shortcuts import redirect, render
from django.http import HttpResponse
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import UserCreationForm
from django.views import View
from django.contrib.auth.decorators import login_required
from config.settings import LOGIN_REDIRECT_URL
from .forms import LoginForm,UserRegistrationForm
from django.views.generic import CreateView
from django.urls import reverse_lazy
from .models import Profile
from .forms import UserEditForm,ProfileEditForm
from django.contrib.auth.models import User
from .models import Profile



def user_login(request):
  if request.method == "POST" :
    form =LoginForm(request.POST)
    if form.is_valid():
      data = form.cleaned_data
      user = authenticate(request, username=data['username'],password=data['password'])

      if user is not None:
        if user.is_active:
          login(request,user)
          return HttpResponse("Muoffaqiyatli login amalga oshirlidi ")
        else:
          return HttpResponse("Sizning parolingiz faol holatda emas")
      else:
        return HttpResponse("Login va parolda xatolik bor ")
  else:
    form =LoginForm()
    context={
      'form':form
    }
  return render(request, 'registration/login.html', context)

@login_required
def dashboard_view(request):
    user = request.user
    try:
        profile = Profile.objects.get(user=user)
    except Profile.DoesNotExist:
        profile = None

    context = {
        'user': user,
        'profile': profile
    }
    return render(request, 'pagest/user_profile.html', context)




def user_register(request):
    if request.method == "POST":
        user_form = UserRegistrationForm(request.POST)
        if user_form.is_valid():
            new_user = user_form.save(commit=False)
            new_user.set_password(user_form.cleaned_data["password"])
            new_user.save()
            Profile.objects.create(user=new_user)
            context = {"new_user": new_user}
            return render(request, 'account/register_done.html', context)
    else:
        user_form = UserRegistrationForm()
        context = {"user_form": user_form}
        return render(request, 'account/register.html', context)


class SingUpView(CreateView):
   form_class = UserCreationForm
   success_url = reverse_lazy('login_page')
   template_name = 'account/register.html'   
  

class SingupView(View):
   
   def get(self,request):
      user_form = UserRegistrationForm()
      context = {"user_form": user_form}
      return render(request, 'account/register.html', context)

   

   def post(self,request):
      if request.method == "POST":
        user_form = UserRegistrationForm(request.POST)
        if user_form.is_valid():
            new_user = user_form.save(commit=False)
            new_user.set_password(user_form.cleaned_data["password"])
            new_user.save()
            context = {"new_user": new_user}
            return render(request, 'account/register_done.html', context)
        



@login_required
def edit_user(request):
    try:
        profile = request.user.profile
    except Profile.DoesNotExist:
        profile = Profile.objects.create(user=request.user)

    if request.method == "POST":
        user_form = UserEditForm(instance=request.user, data=request.POST)
        profile_form = ProfileEditForm(instance=profile, data=request.POST, files=request.FILES)
        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save(commit=False)
            profile = profile_form.save(commit=False)
            user.save()
            profile.save()
    else:
        user_form = UserEditForm(instance=request.user)
        profile_form = ProfileEditForm(instance=profile)

    return render(request, 'account/profile_edit.html', {"user_form": user_form, "profile_form": profile_form})

class EditUserView(View):
   
   def get(self, request):
      
      user_form = UserEditForm(instance=request.user)
      profile_form = ProfileEditForm(instance=request.user.profile)

      return render(request, 'account/profile_edit.html', {"user_form": user_form, "profile_form": profile_form})
   
   def post(self, request):
       try:
        profile = request.user.profile
       except Profile.DoesNotExist:
        profile = Profile.objects.create(user=request.user)

       if request.method == "POST":
        user_form = UserEditForm(instance=request.user, data=request.POST)
        profile_form = ProfileEditForm(instance=profile, data=request.POST, files=request.FILES)
        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save(commit=False)
            profile = profile_form.save(commit=False)
            user.save()
            profile.save()
            return redirect('user_profile')