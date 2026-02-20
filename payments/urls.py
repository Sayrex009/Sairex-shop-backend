from rest_framework import routers
from django.urls import path, include
from .views import PaymentViewSet, CreatePaymentIntentView, StripeWebhookView

router = routers.DefaultRouter()
router.register(r'', PaymentViewSet, basename='payment')

urlpatterns = [
	path('', include(router.urls)),
	path('create-intent/', CreatePaymentIntentView.as_view(), name='create-payment-intent'),
	path('webhook/', StripeWebhookView.as_view(), name='stripe-webhook'),
]
