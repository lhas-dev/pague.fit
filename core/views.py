from django.shortcuts import HttpResponse, render
from django.views import View

def index(request):
    return HttpResponse("Hello, World!")

class PaymentView(View):
    def get(self, request, public_id):
        return render(request, 'payment_page.html', {'public_id': public_id})