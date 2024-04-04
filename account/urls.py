from django.urls import path
from .views import register_user, login_page, account_verify, ChangePass,LogoutView
from django.contrib.auth import views as auth_view
urlpatterns = [
    path('register_user/', register_user.as_view(), name='register_user'),
    path('login_page/', login_page.as_view(), name='login_page'),
    path('logout/', LogoutView.as_view(),
         name='logout'),
    path('verify/<email_token>', account_verify, name='verify'),
    path('password_reset/', auth_view.PasswordResetView.as_view(
        template_name='account/password_reset.html'), name='password_reset'),
    path('password_reset/done/', auth_view.PasswordResetDoneView.as_view(
        template_name='account/password_reset_done.html'), name='password_reset_done'),
    path('password_reset_confirm/<uidb64>/<token>/', auth_view.PasswordResetConfirmView.as_view(
        template_name='account/password_reset_confirm.html'), name='password_reset_confirm'),
    path('password-reset-complete/',
         auth_view.PasswordResetCompleteView.as_view(template_name='account/password_reset_complete.html'), name='password_reset_complete'),
    path('change_pass/', ChangePass.as_view(), name='change_pass')
]
