from decimal import Decimal

from core.apps.vendor.gambling import chc


def main():
    client = chc.CHCAPIClient()

    print("Create invoice...")
    initial_amount = Decimal(500)
    invoice_id, transaction_id = client.create_invoice(initial_amount)
    print(f"Invoice ID: {invoice_id}\nTransaction ID {transaction_id}")

    print("\n\nCheck invoice...")
    initial_balance, transaction_id = client.check_invoice(invoice_id)
    print(f"Invoice sum: {initial_balance}\nTransaction ID {transaction_id}")

    print(f"\n\nAdd additional sum to invoice {invoice_id}...")
    additional_amount = Decimal(250.5)
    new_balance, transaction_id = client.add_invoice(invoice_id, additional_amount)
    assert new_balance == initial_amount + additional_amount
    print(f"Invoice sum: {new_balance}\nTransaction ID {transaction_id}")

    print(f"\n\nClose invoice {invoice_id}...")
    close_balance, transaction_id = client.close_invoice(invoice_id)
    assert close_balance == new_balance == initial_amount + additional_amount
    print(f"Close sum: {close_balance}\nTransaction ID {transaction_id}")

    game_url = chc.get_game_url(invoice_id, 1002)
    print(f"\n\nGame URL: {game_url}")


if __name__ == '__main__':
    main()
