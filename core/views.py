from django.shortcuts import HttpResponse, render, get_object_or_404, redirect
from django.views import View
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django.utils.decorators import method_decorator
from django.conf import settings
from django.contrib import messages
import mercadopago
import json
from .models import Subscription, Payment
from datetime import date
from dateutil.relativedelta import relativedelta

def index(request):
    return HttpResponse("Hello, World!")

class PaymentView(View):
    def get(self, request, public_id):
        subscription = get_object_or_404(Subscription, public_id=public_id)
        
        context = {
            'subscription': subscription,
            'gym': subscription.student.gym,
            'student': subscription.student,
            'plan': subscription.plan,
            'public_id': public_id,
        }
        
        return render(request, 'payment_page.html', context)

class CreatePaymentView(View):
    def post(self, request, public_id):
        subscription = get_object_or_404(Subscription, public_id=public_id)
        
        # Check if Mercado Pago access token is configured
        if not settings.MERCADO_PAGO_ACCESS_TOKEN:
            return JsonResponse({
                'success': False,
                'error': 'Mercado Pago access token not configured'
            }, status=500)
        
        # Initialize Mercado Pago SDK
        sdk = mercadopago.SDK(settings.MERCADO_PAGO_ACCESS_TOKEN)
        
        # Create payment data
        payment_data = {
            "transaction_amount": float(subscription.plan.monthly_fee),
            "description": f"Monthly subscription - {subscription.plan.name}",
            "payment_method_id": "pix",
            "payer": {
                "email": subscription.student.email or "noreply@paguefit.com",
                "first_name": subscription.student.full_name.split()[0],
                "last_name": " ".join(subscription.student.full_name.split()[1:]) if len(subscription.student.full_name.split()) > 1 else "",
            },
            "external_reference": str(subscription.public_id),
        }
        
        # Only add notification_url if we have a valid public URL
        webhook_url = settings.MERCADO_PAGO_WEBHOOK_URL
        if webhook_url and webhook_url.startswith('http'):
            payment_data["notification_url"] = webhook_url
        
        # Create payment
        try:
            payment_response = sdk.payment().create(payment_data)
            payment = payment_response["response"]
            
            # Log the full response for debugging
            print(f"Payment response status: {payment_response['status']}")
            print(f"Payment response: {payment_response}")
            
        except Exception as e:
            print(f"Error creating payment: {str(e)}")
            return JsonResponse({
                'success': False,
                'error': f'Payment creation failed: {str(e)}'
            }, status=400)
        
        if payment_response["status"] == 201:
            # Save payment record
            Payment.objects.create(
                subscription=subscription,
                amount_paid=subscription.plan.monthly_fee,
                external_payment_id=payment["id"],
                status='PENDING'
            )
            
            # Get PIX QR code and copy-paste code
            pix_data = {
                'qr_code': payment["point_of_interaction"]["transaction_data"]["qr_code"],
                'qr_code_base64': payment["point_of_interaction"]["transaction_data"]["qr_code_base64"],
                'payment_id': payment["id"],
                'amount': payment["transaction_amount"]
            }
            
            return JsonResponse({
                'success': True,
                'payment_data': pix_data
            })
        else:
            # Log the error response for debugging
            print(f"Payment creation failed. Status: {payment_response['status']}")
            print(f"Error response: {payment_response}")
            
            return JsonResponse({
                'success': False,
                'error': f'Failed to create payment. Status: {payment_response["status"]}'
            }, status=400)

@csrf_exempt
@require_http_methods(["POST"])
def payment_webhook(request):
    try:
        data = json.loads(request.body)
        
        # Check if it's a payment notification
        if data.get("type") == "payment":
            payment_id = data.get("data", {}).get("id")
            
            if payment_id:
                # Initialize Mercado Pago SDK
                sdk = mercadopago.SDK(settings.MERCADO_PAGO_ACCESS_TOKEN)
                
                # Get payment details
                payment_response = sdk.payment().get(payment_id)
                payment_data = payment_response["response"]
                
                if payment_response["status"] == 200:
                    # Find the payment record
                    try:
                        payment = Payment.objects.get(external_payment_id=payment_id)
                        
                        # Update payment status
                        if payment_data["status"] == "approved":
                            payment.status = "APPROVED"
                            payment.save()
                            
                            # Update subscription
                            subscription = payment.subscription
                            subscription.status = "ACTIVE"
                            subscription.next_due_date = date.today() + relativedelta(months=1)
                            subscription.save()
                            
                        elif payment_data["status"] in ["rejected", "cancelled"]:
                            payment.status = "REJECTED"
                            payment.save()
                            
                    except Payment.DoesNotExist:
                        pass
        
        return JsonResponse({"status": "ok"})
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=400)