from django.http import HttpResponseBadRequest
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.authtoken.models import Token
from api.users.auth import OIDCAuthenticationBackend
from utils.safety_lock import safety_lock

class IsAuthenticatedView(APIView):
    permission_classes = ()

    @safety_lock
    def get(self, request):
        permission_class = IsAuthenticated()
        is_authenticated = permission_class.has_permission(request, self)
        return Response({'is_authenticated': is_authenticated})


class ObtainAuthTokenOIDC(APIView):
    permission_classes = ()

    @safety_lock
    def post(self, request, *args, **kwargs):
        code = request.data.get('code', None)

        if not code:
            return HttpResponseBadRequest('No authentication code found')

        authentication_backend = OIDCAuthenticationBackend()

        try:
            user = authentication_backend.authenticate(request, **kwargs)
        except Exception as e:
            print(e)
            return HttpResponseBadRequest('Could not authenticate')

        token, created = Token.objects.get_or_create(user=user)

        return Response({'token': token.key})


obtain_auth_token = ObtainAuthTokenOIDC.as_view()
