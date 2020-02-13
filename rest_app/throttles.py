from rest_framework.throttling import SimpleRateThrottle


# 自定义的节流类
class AnonymousThrottle(SimpleRateThrottle):
    # 如果有配置了多个缓存，默认使用'default'，可以通过 cache 属性指定
    # cache = caches['alternate']
    scope = 'anonymous'
    # 获取用户的IP
    def get_cache_key(self, request, view):
        return self.get_ident(request)


class UserThrottle(SimpleRateThrottle):

    scope = 'User'
    # 获取用户的用户名
    def get_cache_key(self, request, view):
        return request.user.username