from backend import settings


class LocaleMiddleware(object):
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Сохраняем локаль клиента
        if '/api/' in request.path:
            settings.LOCALE = request.META.get('HTTP_LOCALE') or 'ru'

        return self.get_response(request)
