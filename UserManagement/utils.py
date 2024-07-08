from rest_framework_simplejwt.tokens import RefreshToken

def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)
    access_token = refresh.access_token

    return {
        'refresh_token': str(refresh),
        'access_token': str(refresh.access_token),
    }