from celery import shared_task
from django.conf import settings
from .models import Payment
from orders.models import Order


@shared_task(bind=True)
def process_stripe_event(self, event):
    """Process stripe webhook events asynchronously."""
    try:
        event_type = event['type']
        data = event['data']['object']

        if event_type == 'payment_intent.succeeded':
            pid = data.get('id')
            metadata = data.get('metadata', {})
            amount = data.get('amount') / 100.0 if data.get('amount') else 0

            payment, _ = Payment.objects.get_or_create(provider_payment_id=pid, defaults={
                'provider': 'stripe',
                'amount': amount,
                'currency': data.get('currency', 'usd'),
                'status': 'succeeded',
                'metadata': metadata,
            })
            payment.status = 'succeeded'
            payment.save()

            order_id = metadata.get('order_id')
            if order_id:
                try:
                    order = Order.objects.get(id=order_id)
                    order.status = 'paid'
                    order.save()
                except Order.DoesNotExist:
                    pass

        elif event_type in ('payment_intent.payment_failed', 'charge.failed'):
            pid = data.get('id')
            try:
                payment = Payment.objects.get(provider_payment_id=pid)
                payment.status = 'failed'
                payment.save()
            except Payment.DoesNotExist:
                pass

    except Exception as exc:
        raise self.retry(exc=exc, countdown=5)
