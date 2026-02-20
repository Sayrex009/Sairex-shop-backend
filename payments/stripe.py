import stripe
from django.conf import settings


stripe.api_key = getattr(settings, 'STRIPE_API_KEY', '')


def create_payment_intent(amount, currency='usd', metadata=None):
    """Create a Stripe PaymentIntent and return the client secret."""
    if metadata is None:
        metadata = {}
    intent = stripe.PaymentIntent.create(
        amount=int(float(amount) * 100),
        currency=currency,
        metadata=metadata,
    )
    return intent


def construct_event(payload, sig_header):
    """Validate and construct a Stripe Event using webhook secret."""
    webhook_secret = getattr(settings, 'STRIPE_WEBHOOK_SECRET', '')
    if webhook_secret:
        return stripe.Webhook.construct_event(payload=payload, sig_header=sig_header, secret=webhook_secret)
    # If no secret configured, parse loosely (not recommended for production)
    return stripe.Event.construct_from(payload, stripe.api_key)
