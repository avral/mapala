import swiftclient

from backend.settings import STORAGE


class Storage(swiftclient.Connection):
    def __init__(self):
        super().__init__(**STORAGE)

        # Аутентификация
        self.storage_url = self.get_auth()[0]

        # Если нет контейнера под посты - создаем
        self.put_container('posts', headers={'X-Container-Read': '.r:*'})
