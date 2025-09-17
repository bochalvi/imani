from django.urls import path
from . import views

app_name = 'accounts'

urlpatterns = [
    path('', views.account_list, name='account_list'),
    path('create/<int:member_id>/', views.create_account, name='create_account'),
    path('<int:account_id>/transactions/',
         views.transaction_history, name='transaction_history'),
    path('<int:account_id>/', views.account_detail, name='account_detail'),
    path('<int:account_id>/deposit/', views.deposit, name='deposit'),

]
