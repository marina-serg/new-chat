from django.contrib.auth import get_user_model
from django.core.cache import cache
from django.utils import timezone
from django.utils.deprecation import MiddlewareMixin

User = get_user_model()


class ActiveUserMiddleware(MiddlewareMixin):
    def process_request(self, request):
        if request.user.is_authenticated and request.session.session_key:
            cache_key = f'last-seen-{request.user.id}'
            last_seen = cache.get(cache_key)

            if last_seen is None:
                User.objects.filter(id=request.user.id).update(last_login=timezone.now())

                cache.set(cache_key, timezone.now(), 100)
