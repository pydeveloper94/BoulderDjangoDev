from .models import DjangoDev, OAuthAccount

class OAuthAccountAuthentication(object):
    """
    Custom user authentication for creating sessions after a users oauth
    account is created.
    """
    def authenticate(self, account=None):
        """
        Returns an attached user from an account
        """
        if account:
            return account.user
        return None
    
    def get_user(self, user_id):
        try:
            return DjangoDev.objects.get(pk=user_id)
        except DjangoDev.DoesNotExist:
            return None
