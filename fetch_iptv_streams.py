import requests
import json
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
import gzip

# Define URL and keys
url = "http://cms.testipmedia.xyz/newtv/itv/index2.php"
special_key = "p2p20210118"
key = special_key.encode()[:16]
iv = special_key.encode()[16:32]

# Generate random device ID
import secrets
device_id = secrets.token_hex(16).upper()

# Get IP address
ip = requests.get("http://g3.le.com/r?format=1")。json()['host']

# Get IP address from server
get_ip = requests.post(url, data={"getIP": device_id}).text

# Construct body data
body = {
    "mac": "5b8a4c0c",
    "model": "HD1910",
    "androidid": "775D2672A66CC2BF37676E9999510BA7",
    "deviceid": device_id,
    "ip": ip,
    "app_name": "Focus TV",
    "package_name": "com.newtvbaichuan.iptv",
    "token": "ADA8bC27b3E03AB57E2E15DA9eb8C9",
    "province": ""
}
compressed_body = gzip.compress(json.dumps(body).encode())

# Encrypt data
cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=default_backend())
encryptor = cipher.encryptor()
enc2 = encryptor.update(compressed_body) + encryptor.finalize()

# Post encrypted data and get response
res = requests.post(url, data={"login": enc2}).text

# Decrypt response
cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=default_backend())
decryptor = cipher.decryptor()
str_decrypted = decryptor.update(res) + decryptor.finalize()

# Uncompress and save to file
json_data = json.loads(gzip.decompress(str_decrypted).decode())
with open("orginal.txt", "w") as f:
    json.dump(json_data, f, ensure_ascii=False)

# Process data and save to iptv.txt
categories = json_data['data']
with open("iptv.txt", "w") as f:
    for category, channels in categories.items():
        if category != '收藏':
            f.write(f"{category},#genre#\n")
            for channel in channels['channels']:
                name = channel['channelName']。replace(".", "")
                url = channel['channelUrl'][0]
                f.write(f"{name},{url}\n")

print(open("iptv.txt", "r")。read())
