from django.urls import path
from . import views

app_name = 'loans'

urlpatterns = [
    path('apply/', views.apply_loan, name='apply_loan'),
    path('loan/', views.loan_list, name='loan_list'),
    path('<int:loan_id>/', views.loan_detail, name='loan_detail'),
]
