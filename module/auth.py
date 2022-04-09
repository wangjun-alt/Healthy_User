from django.conf import settings
from rest_framework.exceptions import AuthenticationFailed
from jwt import exceptions
import jwt

def GetOpenid(token):
    salt = settings.SECRET_KEY
    try:
        payload = jwt.decode(token, salt, algorithms=['HS256'])
    except exceptions.ExpiredSignatureError:
        raise AuthenticationFailed({'code': 400, 'error': "token已失效,请重新登录"})
    except jwt.DecodeError:
        raise AuthenticationFailed({'code': 400, 'error': "token认证失败"})
    except jwt.InvalidTokenError:
        raise AuthenticationFailed({'code': 400, 'error': "非法的token"})
    openid = payload.get('username')
    return openid
