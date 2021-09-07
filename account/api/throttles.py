from rest_framework.throttling import SimpleRateThrottle,AnonRateThrottle,UserRateThrottle

class RegisterThrottle(SimpleRateThrottle):
    scope = 'registerthrottle'

    def get_cache_key(self, request, view):
        if request.user.is_authenticated and request.method == 'GET':
            return None  # Only throttle unauthenticated requests.

        return self.cache_format % {
            'scope': self.scope,
            'ident': self.get_ident(request)
        }


# class RegisterThrottle(AnonRateThrottle):
#     scope = 'registerthrottle'


'''if login use user id else ip address'''
# class RegisterThrottle(UserRateThrottle):
#     scope = 'registerthrottle'