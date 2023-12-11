from django.urls import path
from django.contrib.auth import views as auth_views
from django.contrib.auth.views import LoginView,LogoutView,\
    PasswordChangeView,PasswordChangeDoneView,PasswordResetView,\
    PasswordResetConfirmView,PasswordResetDoneView,PasswordResetCompleteView
from .views import  user_login,dashboard_view,user_register,SingUpView,edit_user,EditUserView

urlpatterns = [
    #path('login/',user_login, name='login_page'),
    path('login/',LoginView.as_view(),name='login_page'),
    path('out/',LogoutView.as_view(),name='logout_page'),
    path('password-change/',PasswordChangeView.as_view(), name='password_change'),
    path('password-done/', PasswordChangeDoneView.as_view(), name='password_change_done'),
    path('password-reset/', PasswordResetView.as_view(), name='password_reset'),
    path('password-reset/done/', PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('account/password-reset/<uidb64>/<token>/',auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('password-reset/complite/', PasswordResetCompleteView.as_view(), name='password_reset_complite'),
    path('profile/',dashboard_view, name='user_profile'),
    path('singup/',user_register, name='user_register'),
    #path('profile/edit/',EditUserView.as_view(), name='etit_user')
    path('profile/edit/',edit_user, name='etit_user')
    #path('singup/',SingUpView.as_view(), name='user_register'),

]
