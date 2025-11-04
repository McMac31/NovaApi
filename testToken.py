import jwt, os
token = "eyJ...."   # pega aquí tu token
secret = os.environ.get("JWT_SECRET")  # o pon directamente tu secret para probar
print("secret:", secret)
try:
    payload = jwt.decode(token, secret, algorithms=["HS256"])
    print("OK: payload:", payload)
except Exception as e:
    print("FALLA:", type(e), e)
