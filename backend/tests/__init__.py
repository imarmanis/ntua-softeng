def url_for(path):
    return '/observatory/api' + path


def auth_header(token):
    return {
        'X-OBSERVATORY-AUTH': token
    }
