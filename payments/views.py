import stripe
from django.conf import settings
from django.http import JsonResponse
from django.views import View
from django.views.generic import TemplateView

from apps.website.models import Order

stripe.api_key = settings.STRIPE_SECRET_KEY


class CreateCheckoutSessionView(View):
    def post(self, request, *args, **kwargs):
        order_id = self.kwargs['order_id']
        order = Order.objects.get(id=order_id)
        YOUR_DOMAIN = "http://127.0.0.1:8000"
        checkout_session = stripe.checkout.Session.create(
            payment_method_types=['card'],
            line_items=[
                {
                    'price_data': {
                        'currency': 'usd',
                        'unit_amount': order.total_price * 100,
                        'product_data': {
                            'name': order.item.name
                        },
                    },
                    'quantity': 1,
                },
            ],
            metadata={
                "order_id": order.id
            },
            mode='payment',
            success_url=YOUR_DOMAIN + '/success-payment/',
            cancel_url=YOUR_DOMAIN + '/decline-payment/',
        )
        return JsonResponse({
            'id': checkout_session.id
        })


class SuccessView(TemplateView):
    template_name = "success-payment.html"


class CancelView(TemplateView):
    template_name = "decline-payment.html"
