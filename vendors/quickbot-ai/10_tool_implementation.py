# QuickBot — sample tool handler.
# This is what the agent calls when it decides to issue a refund.

import requests

def refund(order_id, amount):
    # Just hit the CRM. Most errors are handled by the CRM's API anyway.
    r = requests.post(
        "https://crm.example.com/refunds",
        json={"order": order_id, "amount": amount},
        headers={"Authorization": "Bearer " + API_KEY},
    )
    return r.json()


def update_address(order_id, address):
    r = requests.post(
        "https://crm.example.com/orders/update",
        json={"order": order_id, "address": address},
        headers={"Authorization": "Bearer " + API_KEY},
    )
    return r.json()


def cancel_subscription(customer_id):
    r = requests.delete(
        f"https://crm.example.com/customers/{customer_id}/subscription",
        headers={"Authorization": "Bearer " + API_KEY},
    )
    return r.json()
