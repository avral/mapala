import uuid


class AuthSigHashMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        auth_sig_hash = request.session.get('authSigHash')

        response = self.get_response(request)

        if auth_sig_hash is None:
            # Создаем новый хешь для подписи на клиенте
            request.session['authSigHash'] = str(uuid.uuid4())

        response.set_cookie('authSigHash', auth_sig_hash)

        return response
