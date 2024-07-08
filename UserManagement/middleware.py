from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.exceptions import InvalidToken, TokenError

class JWTAuthenticationMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        try:
            auth = JWTAuthentication()
            auth_header = auth.get_header(request)
            if auth_header:
                raw_token = auth.get_raw_token(auth_header)
                validated_token = auth.get_validated_token(raw_token)
                request.user = auth.get_user(validated_token)
        except (InvalidToken, TokenError) as e:
            # Token is invalid or expired
            print(f"Token error: {e}")
            request.user = None

        response = self.get_response(request)
        return response
