from src.agent import generate_random_user_agent

headers = {
            'Accept': 'application/json, text/plain, */*',
            'Connection': 'keep-alive',
            'Content-Type': 'application/json',
            'Origin': 'https://banana.carv.io',
            'Referer': 'https://banana.carv.io/',
            'User-Agent': generate_random_user_agent(),
        }
    