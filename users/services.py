import stripe

from djangoProjectDRF_1_0.settings import STRIPE_API_KEY

stripe.api_key = STRIPE_API_KEY


def create_stripe_price(payment_sum):
    """Создает цену в страйпе."""
    return stripe.Price.create(
        currency="rub",
        unit_amount=payment_sum * 100,
        product_data={"name": "Buy educational material"},
    )


def create_stripe_session(price):
    """Создает сессию на оплату страйпе."""
    session = stripe.checkout.Session.create(
        success_url="https://127.0.0.1:8000/",
        line_items=[{"price": price.get("id"), "quantity": 1}],
        mode="payment",
    )
    return session.get("id"), session.get("url")
