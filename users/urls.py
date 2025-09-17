from django.urls import path
from . import views
from .views import SignUpView, CreateInviteView
app_name = 'users'
urlpatterns = [
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('invite/', CreateInviteView.as_view(), name='create_invite'),
    path('signup/<uuid:token>/', SignUpView.as_view(),
         name='signup'),  # Token in URL
    path('forgot-password/', views.ForgotPassword,
         name='forgot-password'),
    path('reset-password/', views.ResetPassword, name='reset_password'),

    path('reset-password/<str:reset_id>/',
         views.ResetPassword, name='reset-password'),



]
