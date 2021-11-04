# ...
# # Other imports
# from . import keys
# # Make sure to have the keys array in the __init__.py file
# # in the cognito folder
# # Standard Format:
# # keys = [{...},{...}]

# # In order to get the keys data, visit
# # https://cognito-idp.{region}.amazonaws.com/{userPoolId}/.well-known/jwks.json
# # Replace region and userPoolId with respective values
# ...

# def get_jwt_claims(token):
#     # get the kid from the headers prior to verification
#     headers = jwt.get_unverified_headers(token)
#     kid = headers["kid"]
#     # search for the kid in the downloaded public keys
#     key_index = -1
#     for i in range(len(keys)):
#         if kid == keys[i]["kid"]:
#             key_index = i
#             break
#     if key_index == -1:
#         print("Public key not found in jwks.json")
#         return []
#     # construct the public key
#     public_key = jwk.construct(keys[key_index])
#     # get the last two sections of the token,
#     # message and signature (encoded in base64)
#     message, encoded_signature = str(token).rsplit(".", 1)
#     # decode the signature
#     decoded_signature = base64url_decode(encoded_signature.encode("utf-8"))
#     # verify the signature
#     if not public_key.verify(message.encode("utf8"), decoded_signature):
#         print("Signature verification failed")
#         return []
#     # print("Signature successfully verified")
#     # since we passed the verification, we can now safely
#     # use the unverified claims
#     claims = jwt.get_unverified_claims(token)
#     ts = claims["exp"]
#     os.environ["TZ"] = "Asia/Kolkata"
#     time.tzset()
#     print(
#         "Current Expiry of Token : {}".format(
#             time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(ts))
#         )
#     )
#     # Checking token expiry
#     if time.time() > claims["exp"]:
#         print("Token is expired")
#         return []
#     if claims["aud"] != settings.COGNITO_CONFIG["app_client_id"]:
#         print("Token was not issued for this audience")
#         return []
#     return claims


# class CognitoAuthenticationMixin:
#     @staticmethod
#     def get_auth_token(request):
#         raise NotImplementedError()

#     def authenticate(self, request):
#         token = self.get_auth_token(request)
#         try:
#             claims = get_jwt_claims(token)
#             if len(claims) > 0:
#                 user = UserModel.objects.get(email=claims["email"])
#                 return user
#             raise NoSuchClaims()
#         except UserModel.DoesNotExist:
#             raise NoSuchUser()
#         except Exception:
#             raise InvalidAuthToken()


# class CognitoAuthentication(
#     CognitoAuthenticationMixin, authentication.BaseAuthentication
# ):
#     @staticmethod
#     def get_auth_token(request):
#         try:
#             return request.META["HTTP_AUTHORIZATION"]
#         except Exception:
#             raise NoAuthToken()

#     def authenticate(self, request):
#         user = super(CognitoAuthentication, self).authenticate(request)
#         return user, None