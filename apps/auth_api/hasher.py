import bcrypt

from django.contrib.auth.hashers import BCryptSHA256PasswordHasher


class MyCryptoHash(BCryptSHA256PasswordHasher):
    rounds = 13

    def verify(self, password, encoded):
        if encoded.startswith('bcrypt_sha256$'):
            encoded = encoded[14:]

        return bcrypt.checkpw(password.encode('utf-8'), encoded.encode('utf-8'))
