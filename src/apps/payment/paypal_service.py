import requests
from django.conf import settings

def get_paypal_api_base_url():
    """Returns sandbox or live base URL depending on settings."""
    if settings.PAYPAL_MODE == 'live':
        return "https://api-m.paypal.com"
    return "https://api-m.sandbox.paypal.com"

def get_paypal_access_token():
    """Fetches OAuth 2.0 access token using client ID and secret."""
    url = f"{get_paypal_api_base_url()}/v1/oauth2/token"
    headers = {
        "Accept": "application/json",
        "Accept-Language": "en_US",
    }
    data = {"grant_type": "client_credentials"}

    response = requests.post(
        url,
        headers=headers,
        data=data,
        auth=(settings.PAYPAL_CLIENT_ID, settings.PAYPAL_CLIENT_SECRET)
    )

    if response.status_code == 200:
        return response.json().get("access_token")
    else:
        raise Exception(f"Failed to get PayPal Access Token: {response.text}")

def create_paypal_order(amount, return_url, cancel_url, currency="USD"):
    """Creates a PayPal order via REST API v2."""
    access_token = get_paypal_access_token()
    url = f"{get_paypal_api_base_url()}/v2/checkout/orders"

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {access_token}",
    }

    payload = {
        "intent": "CAPTURE",
        "purchase_units": [
            {
                "amount": {
                    "currency_code": currency,
                    "value": f"{amount:.2f}",
                }
            }
        ],
        "application_context": {
            "return_url": return_url,
            "cancel_url": cancel_url,
            "user_action": "PAY_NOW"
        }
    }

    response = requests.post(url, json=payload, headers=headers)

    if response.status_code in (200, 201):
        data = response.json()
        approval_url = None
        for link in data.get("links", []):
            if link.get("rel") == "approve":
                approval_url = link.get("href")
                break
        return {"order_id": data.get("id"), "approval_url": approval_url}
    else:
        raise Exception(f"PayPal Order Creation Failed: {response.text}")

def capture_paypal_order(order_id):
    """Captures payment for an approved PayPal order."""
    access_token = get_paypal_access_token()
    url = f"{get_paypal_api_base_url()}/v2/checkout/orders/{order_id}/capture"

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {access_token}",
    }

    response = requests.post(url, headers=headers)

    if response.status_code in (200, 201):
        return response.json()
    else:
        raise Exception(f"PayPal Order Capture Failed: {response.text}")
