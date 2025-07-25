import httpx
response = httpx.get("https://generativelanguage.googleapis.com")
print(response.status_code)