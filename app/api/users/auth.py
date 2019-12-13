from mozilla_django_oidc import auth
from django.contrib.auth.models import Group
from django.db import transaction

CLAIMS_FIRST_NAME = 'FirstName'
CLAIMS_LAST_NAME = 'LastName'
PAYLOAD_NONCE = 'nonce'
CLAIMS_ROLES = 'roles'
ACCESS_INFO_REALM = 'realm_access'

class OIDCAuthenticationBackend(auth.OIDCAuthenticationBackend):

    def create_user(self, claims):
        user = super(OIDCAuthenticationBackend, self).create_user(claims)

        user.first_name = claims.get(CLAIMS_FIRST_NAME, '')
        user.last_name = claims.get(CLAIMS_LAST_NAME, '')
        user.save()

        self.update_groups(user, claims)

        return user

    def update_user(self, user, claims):
        user.first_name = claims.get(CLAIMS_FIRST_NAME, '')
        user.last_name = claims.get(CLAIMS_LAST_NAME, '')
        user.save()

        self.update_groups(user, claims)

        return user

    def update_groups(self, user, claims):
        """
        Transform roles obtained from keycloak into Django Groups and
        add them to the user. Note that any role not passed via keycloak
        will be removed from the user.
        """
        with transaction.atomic():
            user.groups.clear()
            for role in claims.get(CLAIMS_ROLES):
                group, _ = Group.objects.get_or_create(name=role)
                group.user_set.add(user)

    def get_userinfo(self, access_token, id_token, payload):
        """
        Get user details from the access_token and id_token and return
        them in a dict.
        """
        user_info = super().get_userinfo(access_token, id_token, payload)
        # NOTE: tempoerary disable the Nonce here, since it's not supported by KPN Grip yet
        access_info = self.verify_token(access_token, nonce=None)  # payload.get(PAYLOAD_NONCE))
        roles = access_info.get(ACCESS_INFO_REALM, {}).get(CLAIMS_ROLES, [])

        user_info[CLAIMS_ROLES] = roles

        '''
        NOTE: This is a temporary patch to support the capitalized user info email,
        instead of the lower capital email which is supposed to be retrieved using the (not yet supported) email scope.
        '''
        user_info['email'] = user_info.get('Email')

        return user_info
