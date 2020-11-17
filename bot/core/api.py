import requests
import pyrogram


class GameAPI:
    base_url = 'https://smarted.store/api/v1/'
    #base_url = 'http://api:8080/api/v1/'
    @classmethod
    def get_games(cls):
        response = requests.get(cls.base_url+'games')
        if response.status_code == 200:
            return response.json()

    @classmethod
    def get_game_url(cls, game_id, type_game, tg_id):
        response = requests.get(cls.base_url+f'games/{game_id}/{type_game}/{tg_id}/')
        if response.status_code == 200:
            return response.json()

    @classmethod
    def registration_user(cls, tg_user: pyrogram.User, source: str):
        request_url = 'accounts/user/'

        username = tg_user.username
        first_name = tg_user.first_name
        last_name = tg_user.last_name

        if not username:
            username = '[отсутствует]'
        if not first_name:
            first_name = '[отсутствует]'
        if not last_name:
            last_name = '[отсутствует]'

        response = requests.post(cls.base_url+request_url, data={
            'tg_id': tg_user.id,
            'username': username,
            'first_name': first_name,
            'last_name': last_name,
            'source': source})

        if response.status_code == 201:
            return 'is_created'

    @classmethod
    def check_user(cls, tg_id):
        request_url = f'accounts/{tg_id}/'
        response = requests.get(cls.base_url+request_url)
        return response

    @classmethod
    def get_balance(cls, tg_id):
        response = requests.get(cls.base_url+f'wallets/{tg_id}/check/')

        if response.status_code == 200:
            return response.json()

    @classmethod
    def withdrawal_request(cls, tg_id, card, amount):
        request_url = f'wallets/{tg_id}/withdraw/'
        response = requests.post(cls.base_url + request_url, data={'card_number': card, 'amount': amount})

        if response.status_code == 200:
            return response.status_code

    @classmethod
    def deposit_user(cls, tg_id, amount):

        return cls.base_url+f'payment/generate/{tg_id}/{amount}/'

    @classmethod
    def send_statistic(cls, tg_id, type_action, data):
        request_url = 'http://api:8080/api/v1/statistic/register/'
        r=requests.post(request_url, json={"tg_id": tg_id, "type_action": type_action, "data": data})



