from src.agent import generate_random_user_agent


def headers():
    return {
        'Accept': 'application/json, text/plain, */*',
        'Connection': 'keep-alive',
        'Content-Type': 'application/json',
        'Origin': 'https://banana.carv.io',
        'Referer': 'https://banana.carv.io/',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'priority': 'u=1, i',
        'sec-fetch-site': 'same-site',
        'User-Agent': generate_random_user_agent(),
        'x-app-id': 'carv'
    }

# def headers():
#     return {
#          "Accept": "application/json, text/plain, */*",
#         "Origin": "https://banana.carv.io",
#         "Referer": "https://banana.carv.io/",
#         'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36"
#     }