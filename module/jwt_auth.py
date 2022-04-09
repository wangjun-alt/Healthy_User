import jwt
import datetime
from django.conf import settings

def create_token(payload, timeout=1440):
    salt = settings.SECRET_KEY
    # 构造header
    headers = {
        'typ': 'jwt',
        'alg': 'HS256'
    }

    # 构造payload
    payload['exp'] = datetime.datetime.utcnow() + datetime.timedelta(minutes=timeout)

    token = jwt.encode(payload=payload, key=salt, algorithm='HS256', headers=headers)

    return token