import sys
import json
import threading
import time
from colorama import *
from src.core import Banana, config
from requests.exceptions import RequestException
from src.deeplchain import log, log_error, countdown_timer, mrh, htm, bru, kng, pth, hju, _banner, _clear, load_config

init(autoreset=True)
config = load_config()

# Global Lock for logging (used in multithreading to avoid log overlap)
log_lock = threading.Lock()

def log_safe(message):
    """Thread-safe logging to avoid overlapping logs."""
    with log_lock:
        log(message)

def process_token(banana, token, current_index, total_accounts):
    try:
        use_proxy = config.get('use_proxy', False)
        user_info = banana.get_user_info(token)
        data = user_info['data']
        if isinstance(data, str): 
            data = json.loads(data)

        host_port = handle_proxy(banana) if use_proxy else 'No proxy'
        
        # Extract user data
        username = data.get('username', 'Unknown')
        total_usdt = data.get('usdt', 0)
        total_peel = data.get('peel', 0)
        click_count = data.get('max_click_count', 0)
        speedup_count = data.get('speedup_count', 0)
        total_banana = data.get('banana_count', 0)

        # Thread-safe logging
        log_safe(hju + f"Account: {pth}{current_index}/{total_accounts}")
        log_safe(hju + f"Using proxy: {pth}{host_port}")
        log_safe(htm + "~" * 38)

        log_safe(bru + f"Logged in as {pth}{username}")
        log_safe(hju + f"Balance: {pth}{total_peel} {kng}PEEL {hju}| {pth}{total_usdt} {hju}USDT")
        log_safe(hju + f"Click limit: {pth}{click_count} {hju}| BaBoost: {pth}{speedup_count}")

        # Perform actions
        banana.get_lottery(token)
        banana.banana_list(token)
        banana.do_speedup(token)

        log_safe(f"{hju}You have a total {pth}{total_banana} {kng}Banana")
        log_safe(htm + "~" * 38)

        # Delay between processing each account
        countdown_timer(config["delay_account"])

    except RequestException as e:
        log_safe(mrh + f"Something wrong, please check {hju}last.log {mrh}file!")
        log_error(f"{str(e)}")

def handle_proxy(banana):
    """Handle proxy rotation and logging."""
    proxy = banana.get_current_proxy()
    if proxy:
        proxy_url = proxy.get('http', '')
        host_port = proxy_url.split('@')[-1] if '@' in proxy_url else proxy_url.split('//')[-1]
    else:
        host_port = 'No proxy'
    
    # Rotate proxy for the next request
    banana.proxy_index = (banana.proxy_index + 1) % len(banana.proxies)
    return host_port

def load_tokens():
    try:
        with open('tokens.json', 'r') as file:
            return json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        return {}

def save_tokens(tokens):
    with open('tokens.json', 'w') as file:
        json.dump(tokens, file, indent=4)

def process_account(banana, query, tokens, current_index, total_accounts):
    """Process each account in a separate thread."""
    user_id = banana.extract_user_id(query)
    existing_token = tokens.get(user_id, [])

    if existing_token:
        token_to_use = existing_token[0]
    else:
        new_token = banana.login(query)
        if new_token:
            tokens.setdefault(user_id, []).append(new_token)
            save_tokens(tokens)
            token_to_use = new_token
        else:
            log_safe(f"Failed to get token for user ID {user_id}")
            return

    process_token(banana, token_to_use, current_index + 1, total_accounts)

def main():
    _clear()
    _banner()
    banana = Banana()

    # Load queries and tokens
    try:
        with open('query.txt', 'r') as file:
            queries = [line.strip() for line in file.readlines()]
    except FileNotFoundError:
        log_safe(mrh + "No query.txt file found.")
        return

    total_accounts = len(queries)
    tokens = load_tokens()

    # Start processing accounts using multithreading
    threads = []
    for current_index, query in enumerate(queries):
        thread = threading.Thread(target=process_account, args=(banana, query, tokens, current_index, total_accounts))
        threads.append(thread)
        thread.start()
        time.sleep(0.5)  # Small delay to avoid overwhelming the server

    # Wait for all threads to finish
    for thread in threads:
        thread.join()

    countdown_timer(config["cycle_delay"])

if __name__ == '__main__':
    while True:
        try:
            main()
        except Exception as e:
            log_safe(mrh + f"Something went wrong, please check {hju}last.log {mrh}file!")
            log_error(f"{str(e)}")
            log_safe(f"{pth}~" * 38)
            countdown_timer(5)
        except KeyboardInterrupt:
            log_safe(mrh + "Progress terminated by user")
            sys.exit(0)
