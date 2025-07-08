from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('pay/<uuid:public_id>/', views.PaymentView.as_view(), name='payment-page'),
    path('create-payment/<uuid:public_id>/', views.CreatePaymentView.as_view(), name='create-payment'),
    path('webhook/', views.payment_webhook, name='payment-webhook'),
]