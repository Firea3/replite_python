import requests
with open("cookie.txt", "r", encoding="utf-8") as f:
    cookie_text = f.read().strip()
headers = {
        'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/150.0.0.0 Safari/537.36','Cookie':cookie_text
}
res = requests.get('https://godamh.com/',headers=headers)
print(res)
print(res.text)
