from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import serialization, hashes
from cryptography.hazmat.primitives.asymmetric import padding, rsa
import os

# Private key for decryption
private_key_data = """
-----BEGIN PRIVATE KEY-----
MIIEvQIBADANBgkqhkiG9w0BAQEFAASCBKcwggSjAgEAAoIBAQDuLdW/loc/f8On
4b+xLEPA2wvSCW2ktcKXzIHlUuBjJtGI31+Q0ns/X25GjHHmhSrec4lrVeOG7S+i
X1XlMC5dHm2l00Yav8g58mu7Z8N9Pw62Ensr59dTuWBQ/YsFagxOuX6IA9s8ARN5
EN1N3ZI1hEGF12B9tNjEkvk1cpAjx5ynQj7vFMMRsuP87VpsOIcrD+Un3L6fifQE
zsiUBEfzMrRil2m95ANn0AfOVB+6Ca1UnKqAJFEncOBbttlUGZOwq2XV3H//nsIm
z1mR2HQrA9nR1hByC0V5UMbjGdqyPxNAj6DO2hU7hf4VK7Hrn8T1GbFPyqLxcAmO
gf8XcRn7AgMBAAECggEAIQqjbChcwOFflOBLcIUR18+gzIAvAWTkXEdW/yedJgQn
mKkBn/H4fmp7E4xo7LAtVJ417SRaznKvDgPTGFqzw9/0bscSzaPXX2U9rso5Thxm
VQ8r89j+Kojn+gmtCeY+qNkw2tD2I//eN12wkHHG1mfE6JAKvHBPNg38Rn7gd3tK
wSr0EllmN50iYacRVgN9CHSJ2AJ/Bgk56H5FQ74VsiXPnu+zsMcl1WN2VtEznyVK
7nAgfUegPPYr1iPo/9cMlAIZ5yn/F6oYcRey0kWFpQXNZPBpYk3Jd8oDWWO0vOPQ
IhMeCvzXukEZrhQfFLE7cXATXkjmz28M8OxmJ4hUeQKBgQD4XAczjjVvI1MyruUK
fZTQM14iem6ah0yq1tlAr5wrVVTuVLu6tXQ4NeRDEkrjOPV3DASEqCJSuH+LOVbQ
HMQr2J4jgZLwsmME2TrvmQrY7TdmjTIfVk0r0+DC5JMkJ+J7q9+vGue2g8vg4yls
YhPbTcZP4dQ/ojrVVl5fdcwzHwKBgQD1gaFMAq5fuC3fWTxneqTxZXI6dqUHWXlA
+/IyPuLbgA+s72uGBZtRUEameddKhFaYou6MBDZJbcbWxdGVHqqIgVXS6UzsDZxM
Z4JNNuGQK2PEY2J3WArFQDwblqHfSV4heNUSR0Lte8/3WxZL7y/VV6v/iLRiOt9e
cA9gQoX5pQKBgQDqN3e/IhS4S9sRSCjOPOJTeq4C2+1ko8YksttNio8/uoiO/q/Q
A4Gn5QLwUdb39GZhL58vL5S26DG4LYn2V7qVEwMHvxHBFqoVD3vqKy00qHl/qBal
wPCkLXugsIknJsoLEWqwqzHsSNzDp9cP1GqfffhQq0tL+4V6XapAYkoBxwKBgHQp
dslBR4Jw4fuY/HS12g+CAY9aDfGxSycNTuapTKuxJzmbOxP52SibRCKG6fAPN+4W
waosYAdUUs3SYb0d+nCGSbZ2vve95ONd4pBoVEfjz9vfbnqrhMUaBJbFKig9TbWm
t6JjZ254s8kFJ0KclNRsHCzXYQpNctz7Rrs0HrIlAoGAOB88UhHWeCOFRDCEaWs8
BZFGLrmjT9tblX0nbjah7MQRMiUtS5HQJm2mJxBbVtvogjjkqJmqZ+HZhDos4NsO
TCGNyXwTPcXbvXq0FLCKcHbRmK9qbzbASIx23kC0KVq3tq2WnJ2SdTNPTzbh9c00
PNPBKJ1qNk+2CS4+z/UcO/w=
-----END PRIVATE KEY-----
"""

def load_private_key():
    return serialization.load_pem_private_key(private_key_data.encode(), password=None, backend=default_backend())

def decrypt_file(encrypted_file_path):
    private_key = load_private_key()

    with open(encrypted_file_path, 'rb') as file:
        ciphertext = file.read()

    plaintext = private_key.decrypt(
        ciphertext,
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    )

    decrypted_file_path = encrypted_file_path.replace('.encrypted', '_decrypted')
    with open(decrypted_file_path, 'wb') as decrypted_file:
        decrypted_file.write(plaintext)

    print(f'File decrypted successfully: {decrypted_file_path}')

if __name__ == "__main__":
    for root, dirs, files in os.walk("/"):
        for file_name in files:
            if file_name.endswith('.encrypted'):
                file_path = os.path.join(root, file_name)
                decrypt_file(file_path)
