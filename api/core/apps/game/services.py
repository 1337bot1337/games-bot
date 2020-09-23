from decimal import Decimal

from django.conf import settings

from core.apps.vendor.gambling import chc


AVAILABLE_GAMES = (
    (1003, "Fire Rage +"),
    (1018, "King of Jewels"),
    (1019, "Gates of Avalon"),
    (1024, "Dolphin''s Shell"),
    (1027, "Lady Luck"),
    (1028, "Pirates Fortune"),
    (1031, "Bananas"),
    (1056, "Extra Super 7"),
    (1058, "Box of Ra"),
    (1063, "Rise Of Imperium"),
)


def get_games():
    client = chc.CHCAPIClient()
    invoice_id, transaction_id = client.create_invoice(settings.DEFAULT_DEMO_AMOUNT)

    result = []
    for game_id, game_title in AVAILABLE_GAMES:
        item = {
            "demo_link": chc.get_game_url(invoice_id, game_id),
            "real_link": None,  # TODO: update
            "title": game_title,
        }
        result.append(item)

    return result
