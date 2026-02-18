import requests
from config import Config

headers = {
    'x-cg-demo-api-key': Config.COINGECKO_API_KEY
}


class CoinGeckoClient:
    BASE_URL = Config.COINGECKO_API_URL

    @staticmethod
    def get_cryptocurrency_list():
        try:
            response = requests.get(
                url=f'{CoinGeckoClient.BASE_URL}/coins/list', timeout=10, headers=headers)
            response.raise_for_status()
            coins = response.json()
            return coins

        except requests.exceptions.RequestException as e:
            print(f'Error: {e}')
            return None

    @staticmethod
    def get_current_price(coingecko_id):
        try:
            response = requests.get(url=f'{CoinGeckoClient.BASE_URL}/simple/price', timeout=10, headers=headers, params={
                'ids': coingecko_id,
                'vs_currencies': 'usd',
                'include_market_cap': 'true',
                'include_24h_vol': 'true'
            })
            response.raise_for_status()
            data = response.json()
            return data.get(coingecko_id)

        except requests.exceptions.RequestException as e:
            print(f'Error {e}')
            return None

    @staticmethod
    def get_historical_prices(coingecko_id, days=7):
        try:
            response = requests.get(f'{CoinGeckoClient.BASE_URL}/coins/{coingecko_id}/market_chart',
                                    timeout=10,
                                    headers=headers,
                                    params={
                                        'vs_currency': 'usd',
                                        'days': days,
                                        'interval': 'daily'
            })
            response.raise_for_status()
            data = response.json()
            return data.get('prices', [])

        except requests.exceptions.RequestException as e:
            print(f'Error {e}')
            return None

    @staticmethod
    def get_full_market_data(coingecko_id, days=7):
        try:
            response = requests.get(f'{CoinGeckoClient.BASE_URL}/coins/{coingecko_id}/market_chart',
                                    timeout=10,
                                    headers=headers,
                                    params={
                                    'vs_currency': 'usd',
                                    'days': days,
                                    'interval': 'daily'
                                    })
            response.raise_for_status()
            data = response.json()
            return {
                'prices': data.get('prices', []),
                'volumes': data.get('volumes', []),
                'market_caps': data.get('market_caps', [])
            }

        except requests.exceptions.RequestException as e:
            print(f'Error {e}')
            return None
