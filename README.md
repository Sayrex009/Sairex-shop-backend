# Ecommerce Backend

Django + DRF ecommerce backend skeleton with production-friendly defaults: JWT, Celery, Redis, Postgres, Docker, Swagger.

See `.env.example` for env vars.

Stripe integration
- Set `STRIPE_API_KEY` and `STRIPE_WEBHOOK_SECRET` in `.env`.
- Create a payment intent:

```bash
curl -X POST http://localhost:8000/api/v1/payments/create-intent/ \
	-H "Authorization: Bearer <ACCESS_TOKEN>" \
	-H "Content-Type: application/json" \
	-d '{"amount":"100.00","currency":"usd","order_id":123}'
```

- Example webhook (Stripe CLI):

```bash
stripe listen --forward-to localhost:8000/api/v1/payments/webhook/
```

