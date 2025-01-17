from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
from django.contrib.auth.views import LogoutView

urlpatterns = [
    path('', views.index, name='index'),
    path('merchandise/', views.merchandise, name='merchandise'),
    path('clients/', views.clients, name='clients'),
    path('merchandise/<int:category_id>/', views.categories, name='categories'),
    path('invoices/', views.invoices, name='invoices'),
    path('invoices/issued/', views.issued_invoices, name='issued_invoices'),
    path('invoices/received/', views.received_invoices, name='received_invoices'),
    path("invoices/issued/edit/<int:pk>/", views.edit_issued_invoice, name="edit_issued_invoice"),
    path('invoices/received/edit/<int:invoice_id>/', views.edit_received_invoice, name='edit_received_invoice'),
    path('invoices/create/', views.create_invoice, name='create_invoice'),
    path('register-invoice/', views.register_invoice, name='register_invoice'),
    path('transactions/', views.transactions, name='transactions'),
    path('login/', auth_views.LoginView.as_view(template_name='registration/login.html'), name='login'),
    path('logout/', views.custom_logout, name='logout'),
]
