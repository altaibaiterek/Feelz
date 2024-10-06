from django.middleware.csrf import CsrfViewMiddleware


class AllowAllCsrf(CsrfViewMiddleware):
    def _reject(self, request):
        return False
