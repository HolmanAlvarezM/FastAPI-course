from jwt import encode, decode

secret_key = "my_super_secret_key"
def create_token(data: dict) -> str:
    token: str = encode(payload=data, key="my_super_secret_key", algorithm="HS256")
    return token

def validate_token(token: str) -> dict:
    data: dict = decode(token, key="my_super_secret_key", algorithms=["HS256"])
    return data