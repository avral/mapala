import json
import requests


class Api:
    """
    Api module for Graphene like blockchain api
    """
    def __init__(self, url):
        self.url = url

    def __call__(self, method, *params):
        params = {
            'id': 1,
            'method': method,
            'params': params
        }

        return requests.post(
            self.url,
            data=json.dumps(params),
            headers={'content-type': 'application/json'}
        ).json()

    def user_exists(self, username):
        # Cli wallt only
        return 'error' not in self('get_account', username)
