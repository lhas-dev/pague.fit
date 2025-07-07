from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('pay/<uuid:public_id>/', views.PaymentView.as_view(), name='payment-page'),
]