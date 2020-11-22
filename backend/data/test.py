from jose import jwk, jwt
from jose.utils import base64url_decode
import boto3
import hashlib
import hmac
import base64
import jose

# token = "eyJraWQiOiJJQ2tTdFVtVjQ4OUNhOXZQRTkxcDhQSWhpejNLMXRMK3J3YXdUdCtkSWNVPSIsImFsZyI6IlJTMjU2In0.eyJzdWIiOiIxMjA3ZDM5Zi1jZjBkLTQ5NDctODQ2MC03NzQ2NzdhZmRiNjQiLCJ0b2tlbl91c2UiOiJhY2Nlc3MiLCJzY29wZSI6ImF3cy5jb2duaXRvLnNpZ25pbi51c2VyLmFkbWluIiwiYXV0aF90aW1lIjoxNjA1MDA0MDgxLCJpc3MiOiJodHRwczpcL1wvY29nbml0by1pZHAudXMtZWFzdC0yLmFtYXpvbmF3cy5jb21cL3VzLWVhc3QtMl9BalBZVHozVjEiLCJleHAiOjE2MDUwMDQzODEsImlhdCI6MTYwNTAwNDA4MSwidmVyc2lvbiI6MiwianRpIjoiNWRiMmZmMWYtYzFhNy00MDJiLTkwMmItZWUyZWNjYzQ1ZDAwIiwiY2xpZW50X2lkIjoiajF2azFlbGU5b25vbDNicWhkMTJ1N2thaCIsInVzZXJuYW1lIjoibmlraGlsYWtraSJ9.FefF7pplTbCB3UmZBkl0i8H8RPjBZG5Nj79ETg0-2TDX05XPd2hI7mT0GB2JF2BckWr60yay-M1dnmr04CG4T1IZKACzhsjGUagaYqgMonswiN7mpciJ8lrcsQEmj2qWuBX1sqAGSoPeucVO4klMpNtOBB7wdYI6cItp9EeHKnAp8ik9-Ae78uxpqn3eWJac1XeaC62_5qvY0N8K_GRmYlpJfst9bl3kvUAJg5KGmzL7rFJbOHZEHsNukzG_q5wgKo5p_ug7mk8atqxBgvzNls-QXg_PQZb91zdNXdeXuigTFcc8MwUBx_fI9VVDqUMtxTHrvFx8RtyIRyDiuY5rLQ"
token = "eyJraWQiOiJJQ2tTdFVtVjQ4OUNhOXZQRTkxcDhQSWhpejNLMXRMK3J3YXdUdCtkSWNVPSIsImFsZyI6IlJTMjU2In0.eyJzdWIiOiIxMjA3ZDM5Zi1jZjBkLTQ5NDctODQ2MC03NzQ2NzdhZmRiNjQiLCJ0b2tlbl91c2UiOiJhY2Nlc3MiLCJzY29wZSI6ImF3cy5jb2duaXRvLnNpZ25pbi51c2VyLmFkbWluIiwiYXV0aF90aW1lIjoxNjA1MDA0NzAxLCJpc3MiOiJodHRwczpcL1wvY29nbml0by1pZHAudXMtZWFzdC0yLmFtYXpvbmF3cy5jb21cL3VzLWVhc3QtMl9BalBZVHozVjEiLCJleHAiOjE2MDUwMDUwMDEsImlhdCI6MTYwNTAwNDcwMSwidmVyc2lvbiI6MiwianRpIjoiZGU4ZDJiOTEtZjg0YS00NTM2LTkxNmYtNzRiZTQ5OWQ3NDdjIiwiY2xpZW50X2lkIjoiajF2azFlbGU5b25vbDNicWhkMTJ1N2thaCIsInVzZXJuYW1lIjoibmlraGlsYWtraSJ9.lgrtxIq5we8wk2JxFkiABTLUG0pCRTu_WQmEAw0BxelLZtVKTc7SQpJeZIbGoFHzSYc-ew_NoZOVoE3KxpVJVjYf0tnUxepe42AJHeOTDomRkzjLejJ9RqnX1O0elKNBtzpvN6ap1vwKVy7t_daLOlDzxFW4M10zwyh7NVBdrf1jhpYiluJzTiwIprgUKUI5r_k-BBmgI5invO5-_OtvTUzdFro4Kz2Ju3enjNbu3idPCsHmDMrKRgm6ZRkBLJSrr1AUGl8OtdVf30hfda1pZQc0TveYXTAVj-zUWpHLXNc9JIkEsM6h3bmCvAA_RhSEQCMt_RynxQGoxyjg1DoI1A"
# headers = jwt.get_unverified_headers(token)
# print(headers)
# key = {
#     "alg": "RS256",
#     "e": "AQAB",
#     "kid": "ICkStUmV489Ca9vPE91p8PIhiz3K1tL+rwawTt+dIcU=",
#     "kty": "RSA",
#     "n": "x2900IOephHQtLSCYyCpOSJf7JJNeVDyPt7-0V8I4IdZLZe6fZJVMATl7fTZTGO9FVveuEb5kdXNuwNMJVxlfOEebcJlRVCM24zKJgWU5-Q3nhlAENtTLE1NRqvI1aJT84p0LKpNFaubORGE9eKhbb2kigwQKKujcEcR2ReySpNstDL-LbtAc36drQKr36eUzMYmGqeA1gC_TGAE2s7eWE8f6m-74Q4bEMNotF3l4ZnC1DgO055_SCyWaXdoc3dzSkkd3QV_oznaQbMFop10ad4XIsL5FTJSw0NTG7Ws8cZFV5OAaB1OO7HeEz9O_lfL4zDf4kQVyG9enTJPDmaenw",
#     "use": "sig",
# }
# # public_key = jwk.construct(key)
# # print(public_key)
# # jwt.decode(token, public_key, algorithms=["RS256"])

# claims = jwt.get_unverified_claims(token)
# print(claims)
client = boto3.client("cognito-idp")
app_client_secret = "15l17d85gkbr54pb1s8vpq6f6llbne7dnmudg7hu9pfpt09mirtn"
app_client_id = "j1vk1ele9onol3bqhd12u7kah"
user_pool_id = "us-east-2_AjPYTz3V1"
username = "arpitjain"
key = bytes(app_client_secret, "latin-1")
msg = bytes(username + app_client_id, "latin-1")
new_digest = hmac.new(key, msg, hashlib.sha256).digest()
secret_code = base64.b64encode(new_digest).decode()
# response = client.admin_initiate_auth(
#     UserPoolId=user_pool_id,
#     ClientId=app_client_id,
#     AuthFlow="USER_SRP_AUTH",
#     AuthParameters={
#         "USERNAME": username,
#         "SECRET_HASH": secret_code,
#         "SRP_A": "23423423"
#         # "PASSWORD": "P@ssw0rd",
#     },
# )
# response = client.global_sign_out(AccessToken=token)
response = client.get_user(AccessToken=token)
print(response.get("Username"))
username = response.get("Username")
group_name = client.admin_list_groups_for_user(
    Username=username, UserPoolId=user_pool_id, Limit=1
)
print(group_name.get("Groups")[0].get("GroupName"))
