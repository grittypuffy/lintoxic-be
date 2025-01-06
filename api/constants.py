FACT_CHECKER_API_ENDPOINT = 'https://api.detecting-ai.com/fact-checker/check/'

FACT_CHECKER_API_HEADERS = {
    'accept': 'application/json, text/plain, */*',
    'accept-language': 'en-GB,en-US;q=0.9,en;q=0.8',
    'content-type': 'application/json',
    'origin': 'https://detecting-ai.com',
    'priority': 'u=1, i',
    'referer': 'https://detecting-ai.com/',
    'sec-ch-ua': '"Chromium";v="131", "Not_A Brand";v="24"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Linux"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-site',
    'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36'
}

cors_allowed_headers = [
    "Access-Control-Allow-Origin",
    "Referer",
    "Set-Cookie",
    "Cookie",
    "Content-Length",
    "Content-Type",
    "Access-Control-Allow-Credentials",
    "Access-Control-Allow-Headers",
    "Access-Control-Allow-Methods"
]

cors_allowed_methods = ["GET", "POST", "OPTIONS"]
