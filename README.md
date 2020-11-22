API high-level flow overview
============================

## Entrypoint
Create the telegram account in the system with the source:
```bash
curl -X POST \
  https://smarted.store/api/v1/accounts/user/ \
  -H 'Content-Type: application/json' \
  -d '{
      "tg_id": 2147483647,
      "username": "petya1337",
      "first_name": "Petya",
      "last_name": "Ivanov",
      "source": "Space"
}'
```

## Telegram Account Refill

Let's assume that multiplier for 50,000 is 1.5, so:
- real balance = 50,000
- virtual balance = 25,000
- total balance = real balance + virtual balance = 75,000

Refilled amount immediately will be added to the invoice. Invoice creation logic:
```python
from decimal import Decimal

from core.apps.vendor.gambling import chc

amount = Decimal(75_000)
client = chc.CHCAPIClient()

invoice_id, transaction_id = client.create_invoice(amount)
balance, transaction_id = client.check_invoice(invoice_id)

assert balance == Decimal(amount) 

print(invoice_id)  # "79163678722265"

```  

When additional amount will be refilled, invoice will be updated:
```python
from decimal import Decimal

from core.apps.vendor.gambling import chc

additional_amount = Decimal(5_000)
invoice_id = "79163678722265"

client = chc.CHCAPIClient()

invoice_id, transaction_id = client.add_invoice(invoice_id, additional_amount)
balance, transaction_id = client.check_invoice(invoice_id)

assert balance == Decimal(80_000)  # old amount + additional 
```  

## Check the balance
Check the real/virtual/available to withdraw/withdraw in progress amounts:
```bash
curl -X GET https://push.money/api/v1/wallets/2147483647/check/
```

## Games list
```bash
curl -X GET https://push.money/api/v1/games/
```
Each object returns URL for the game which contains the invoice ID (in any time invoice sum/balance can be checked)

## Get demo game
```bash
curl -X GET https://push.money/api/v1/games/1003/demo/2147483647
```

## Get real game
When the account is refilled and the invoice is created/updated, user can play:
```bash
curl -X GET https://push.money/api/v1/games/1003/real/2147483647
```

## Withdraw
```bash
curl -X POST \
  https://push.money/api/v1/wallets/2147483647/withdraw/ \
  -H 'Content-Type: application/json' \
  -d '{
      "card_number": "1111 2222 3333 4444",
      "amount": 5000
}'
```

When the user want to withdraw the money, the invoice will be closed and real/virtual balance from the account will 
be updated.
```python
from core.apps.vendor.gambling import chc

invoice_id = "79163678722265"

client = chc.CHCAPIClient()
result_balance, transaction_id = client.close_invoice(invoice_id)
```

Note: withdraw requests are managed manually by the admins
