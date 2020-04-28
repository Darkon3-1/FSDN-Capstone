import json
from flask import request, _request_ctx_stack
from functools import wraps
from jose import jwt
from urllib.request import urlopen


AUTH0_DOMAIN = 'srtkoolice.auth0.com'
ALGORITHMS = ['RS256']
API_AUDIENCE = 'udacity-capstone'

# AuthError Exception
'''
AuthError Exception
A standardized way to communicate auth failure modes
'''


class AuthError(Exception):
    def __init__(self, error, status_code):
        self.error = error
        self.status_code = status_code

# Auth Header


def get_token_auth_header():
    try:
        auth = request.headers['Authorization']
    except KeyError:
        raise AuthError('Missing Authorization header.', 401)
    else:
        split_header = auth.split()
        if split_header[0].lower() != 'bearer':
            raise AuthError('"Bearer" must be first part of Auth header.', 401)

        if len(split_header) != 2:
            raise AuthError('Invalid token format.', 401)

        return split_header[1]


def check_permissions(permission, payload):
    valid = 'permissions' in payload and permission in payload['permissions']
    return True if valid else False


def verify_decode_jwt(token):
    jsonurl = urlopen(f'https://{AUTH0_DOMAIN}/.well-known/jwks.json')
    jwks = json.loads(jsonurl.read())

    unverified_header = jwt.get_unverified_header(token)

    rsa_key = {}
    if 'kid' not in unverified_header:
        raise AuthError('Authorization malformed.', 401)

    for key in jwks['keys']:
        if key['kid'] == unverified_header['kid']:
            rsa_key = {
                'kty': key['kty'],
                'kid': key['kid'],
                'use': key['use'],
                'n': key['n'],
                'e': key['e']
            }

    if rsa_key:
        try:
            payload = jwt.decode(
                token,
                rsa_key,
                algorithms=ALGORITHMS,
                audience=API_AUDIENCE,
                issuer='https://' + AUTH0_DOMAIN + '/'
            )

            return payload

        except jwt.ExpiredSignatureError:
            raise AuthError('Token expired.', 401)

        except jwt.JWTClaimsError:
            raise AuthError('Please, check the audience and issuer.', 401)
        except Exception:
            raise AuthError('Unable to parse authentication token.', 400)
    raise AuthError('Unable to find the appropriate key.', 400)


def requires_auth(permission=''):
    def requires_auth_decorator(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            token = get_token_auth_header()
            payload = verify_decode_jwt(token)
            if not check_permissions(permission, payload):
                raise AuthError('Permissions not in JWT.', 401)
            return f(payload, *args, **kwargs)

        return wrapper
    return requires_auth_decorator
