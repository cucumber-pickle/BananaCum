import time
import json
import textwrap
import cloudscraper
from colorama import *
from src.headers import headers
from urllib.parse import parse_qs
from src.agent import generate_random_user_agent
from datetime import datetime, timedelta
from requests.exceptions import RequestException
from src.agent import generate_random_user_agent
from src.deeplchain import log, log_error, mrh, pth, kng, hju, bru, load_config, countdown_timer

init(autoreset=True)
config = load_config()
class TokenManager:
    def __init__(self, tokens_file='tokens.json'):
        self.tokens_file = tokens_file
        self.tokens = self.load_tokens()

    def load_tokens(self):
        try:
            with open(self.tokens_file, 'r') as file:
                return json.load(file)
        except (FileNotFoundError, json.JSONDecodeError):
            return {}


    def save_token(self, user_id, token):
        if user_id in self.tokens:
            if token not in self.tokens[user_id]: 
                self.tokens[user_id].append(token)
        else:
            self.tokens[user_id] = token

        with open(self.tokens_file, 'w') as file:
            json.dump(self.tokens, file, indent=4)

    def get_tokens(self, user_id):
        return self.tokens.get(user_id, [])
class Banana:
    def __init__(self):
        self.base_url = "https://interface.carv.io/banana"
        self.scraper = cloudscraper.create_scraper() 
        self.headers = headers
        self.proxy_index = 0
        self.proxies = [] 
        self.token_manager = TokenManager()

        if config["use_proxy"]:
            self.proxies = self.load_proxies()
            self.proxy_index = 0

    def load_query(self):
        with open('query.txt', 'r') as file:
            return file.read().strip()

    def extract_user_id(self, query):
        query_params = parse_qs(query)
        user_info = json.loads(query_params['user'][0])
        return str(user_info['id'])

    def load_proxies(self):
        proxies = []
        try:
            with open('proxies.txt', 'r') as file:
                lines = file.readlines()
                for line in lines:
                    proxy = line.strip()
                    proxies.append({
                        'http': f'http://{proxy}', 
                        'https': f'http://{proxy}',
                    })
            return proxies
        except Exception as e:
            log(mrh + f"Something wrong check last.log file!")
            log_error(f"{str(e)}")
            return proxies

    def login(self, query):
        user_id = self.extract_user_id(query)
        payload = {'tgInfo': query, 'InviteCode': ""}
        response = self._post('login', payload)
        token = response.get('data', {}).get('token', '').strip()
        
        if token:
            self.token_manager.save_token(user_id, token)
        return token 

    def get_current_proxy(self):
        if self.proxies:
            proxy = self.proxies[self.proxy_index]
            return proxy
        return None

    def set_random_user_agent(self):
        self.headers['User-Agent'] = generate_random_user_agent()

    def _post(self, endpoint, payload):
        try:
            self.set_random_user_agent()
            response = self.scraper.post(
                url=f"{self.base_url}/{endpoint}",
                headers=self.headers,
                json=payload,
                proxies=self.get_current_proxy(),
                timeout=10
            )
            response.raise_for_status()
            return response.json()
        except RequestException as e:
            # log(mrh + f"Something wrong please check {hju}last.log {mrh}file!")
            log_error(f"{str(e)}")
            if self.proxies:
                self.proxy_index = (self.proxy_index + 1) % len(self.proxies)


    def _get(self, endpoint):
        while True:
            try:
                self.set_random_user_agent()
                response = self.scraper.get(
                    url=f"{self.base_url}/{endpoint}",
                    headers=self.headers,
                    proxies=self.get_current_proxy(),
                    timeout=10
                )
                response.raise_for_status()
                return response.json()
            except RequestException as e:
                log(mrh + f"Something wrong please check {hju}last.log {mrh}file!")
                log_error(f"{str(e)}")
                if self.proxies:
                    self.proxy_index = (self.proxy_index + 1) % len(self.proxies)
                time.sleep(2) 
    def get_request_time(self):
        return int(time.time() * 1000)

    def set_auth_header(self, token: str):
        self.headers.update({
            'Authorization': token,
            'Content-Type': 'application/json',

        })


    def get_user_info(self, token: str):
        self.set_auth_header(token)
        return self._get('get_user_info')

    def get_lottery(self, token: str):
        self.set_auth_header(token)
        get_user = self.get_user_info(token)
        response = self._get('get_lottery_info')
        try:
            data = response.get('data', {})
            max_click = get_user['data']['max_click_count']
            today_click = get_user['data']['today_click_count']

            if max_click > today_click:
                click = self.do_click(token, max_click - today_click)
                clicked = click['data'].get('peel', 0)
                if click['msg'] == "Success":
                    log(f"{hju}Success Clicked {pth}{clicked}")
                else:
                    log(f"{mrh}{click['msg']}")
            else:
                log(f"{kng}Out of clicks, banana break")

            now = datetime.now()
            last_start = data['last_countdown_start_time']
            countdown_interval = data['countdown_interval']
            countdown_end = data['countdown_end']
            last_start_time = datetime.fromtimestamp(last_start / 1000)
            remaining_time = last_start_time + timedelta(minutes=countdown_interval) - now

            response_invite = self._get('get_invite_list?inviteType=1&pageNum=1&pageSize=15')
            if response_invite.get('data'):
                claim_lottery_count = response_invite.get('data').get('claim_lottery_count')

                if claim_lottery_count > 0:
                    claim_lottery = self.claim_lottery(token, lottery_type=2)
                    if claim_lottery['msg'] == "Success":
                        log(f"{bru}Lottery {hju}claimed invite bonus successfully")
                    else:
                        log(f"{mrh}{claim_lottery['msg']}")

            if remaining_time.total_seconds() > 0 and not countdown_end:
                hours, remainder = divmod(remaining_time.total_seconds(), 3600)
                minutes, seconds = divmod(remainder, 60)
                log(f"{hju}Claim available in : {pth}{int(hours)}h {int(minutes)}m {int(seconds)}s")
            else:
                claim_lottery = self.claim_lottery(token, lottery_type=1)
                if claim_lottery['msg'] == "Success":
                    log(f"{bru}Lottery {hju}claimed successfully")
                else:
                    log(f"{mrh}{claim_lottery['msg']}")

            get_lottery = self.get_user_info(token)
            harvest = get_lottery['data']['lottery_info']['remain_lottery_count']
            log(bru + f"You have {pth}{harvest} remain_lottery_count")

            while harvest > 0:
                user_ads_info = self.user_ads_info(token)
                if user_ads_info and user_ads_info.get('data').get('show_for_peels'):
                    countdown_timer(10)
                    harvest = self.do_lottery(token)
                    self.claim_ads_income(token)
                else:
                    countdown_timer(1)
                    harvest = self.do_lottery(token)
        except Exception as e:
            log(e)
            log(mrh + f"Сlaim harvest failed!")


    def get_share_info(self, token: str):
        self.set_auth_header(token)
        return self._get('get_share_info')

    def user_ads_info(self, token: str):
        self.set_auth_header(token)
        return self._get('user_ads_info')

    def do_click(self, token: str, click_count: int):
        self.set_auth_header(token)
        payload = {'clickCount': click_count}
        return self._post('do_click', payload)

    def claim_lottery(self, token: str, lottery_type: int):
        self.set_auth_header(token)
        payload = {'claimLotteryType': lottery_type}
        return self._post('claim_lottery', payload)

    def do_lottery(self, token: str):

        self.headers.update({
            'Authorization': token,
            'Content-Type': 'application/json',
            'x-interceptor-id': '28071317665964c4506c26c6479f686aa1a2688f5a8d5ef89af219680208bfe66306a3ab8b6d56c2027bfb158ac4f098'
        })
        response = self._post('do_lottery', {})
        data = response.get('data', {})
        banana_info = data.get('banana_info', {})

        if response.get('msg') == "Success":
            log(f"{bru}Banana name: {pth}{banana_info.get('name', '')}")
            log(f"{bru}Banana ripeness: {pth}{banana_info.get('ripeness', '')}")
            log(f"{bru}Banana limit: {pth}{banana_info.get('daily_peel_limit', '')} {kng}Peel")
            log(f"{bru}Banana price: {pth}{banana_info.get('sell_exchange_peel', '')} {kng}Peel "
                f"{bru} | "
                f"{pth}{banana_info.get('sell_exchange_usdt', '')} {hju}USDT"
            )

            banana_id = banana_info.get('banana_id', 0)
            self.do_share(token, banana_id)

            remain_lottery_count = data.get('remain_lottery_count', 0)
            log(f"{hju}Remaining lottery count: {pth}{remain_lottery_count}")

            return remain_lottery_count
        else:
            log(f"{mrh}{response.get('msg', '')}")
            return 0

    def do_share(self, token: str, banana_id):
        self.set_auth_header(token)
        payload = {"banana_id": banana_id}
        response = self._post('do_share', payload)

        if response.get('msg') == "Success":
            peel = response['data'].get('peel', 0)
            peel_total = response['data'].get('peel_total', 0)

            log(f"{hju}Success share!")
            log(f"{bru}Claimed peels: {pth}{peel}")
            log(f"{bru}Peel total: {pth}{peel_total} ")
        else:
            log(f"{mrh}{response.get('msg', '')}")

    def claim_ads_income(self, token: str):
        self.set_auth_header(token)
        response = self._post('claim_ads_income', {})

        if response.get('msg') == "Success":
            income = response['data'].get('income', 0)
            peels = response['data'].get('peels', 0)
            speedup = response['data'].get('speedup', 0)

            log(f"{bru}Claimed income: {pth}{income} USDT")
            log(f"{bru}Claimed peels: {pth}{peels}")
            log(f"{bru}Speedup: {pth}{speedup}")
        else:
            log(f"{mrh}{response.get('msg', '')}")

    def banana_list(self, token: str):
        self.set_auth_header(token)
        get_user = self.get_user_info(token)
        page_number = 1
        banana_bag = []
        try:
            for page_number in range(1, 20):
                response = self._get(f'get_banana_list/v2?page_num={page_number}&page_size=10')
                if response.get('msg') != "Success":
                    break

                banana_list = response.get('data', {}).get('list', [])
                banana_bag.extend(banana for banana in banana_list if banana['count'] >= 1)

                if page_number * 10 >= response.get('data', {}).get('total', 0):
                    break

            if not banana_bag:
                log(mrh + "No bananas available to equip.")
                return
            highest = max(banana_bag, key=lambda x: x['daily_peel_limit'])
            current_equip_id = get_user['data']['equip_banana']['banana_id']

            if highest['daily_peel_limit'] > get_user['data']['equip_banana']['daily_peel_limit']:
                equip_banana = self.do_equip(token, highest['banana_id'])
                if equip_banana['msg'] == "Success":
                    log(bru + f"Got a new, higher banana")
                    log(hju + f"Banana name: {pth}{highest['name']}")
                    log(hju + f"Banana ripeness: {pth}{highest['ripeness']}")
                    log(hju + f"Banana limit: {pth}{highest['daily_peel_limit']} {hju} peel / day")
                else:
                    log(f"{mrh}{equip_banana['msg']}")
            else:
                log(kng + f"Already using the highest banana")
                log(hju + f"Banana name: {pth}{highest['name']}")
                log(hju + f"Banana ripeness: {pth}{highest['ripeness']}")
                log(hju + f"Banana limit: {pth}{highest['daily_peel_limit']} {hju} peel / day")

            if config["auto_sell"]:
                count_banana = [banana for banana in banana_bag if banana['count'] > 1]
                for sell in count_banana:
                    sell_banana = self.do_sell(token, sell['banana_id'], 1)
                    get_peel = sell_banana['data']['sell_got_peel']
                    get_usdt = sell_banana['data']['sell_got_usdt']

                    if sell_banana['msg'] == "Success":
                        log(hju + f"Successfully Sold : {pth}{sell['name']}")
                        log(hju + f"You got {pth}{get_peel} {kng}peel | {pth}{get_usdt} {hju}USDT")
                    else:
                        log(f"{mrh}{sell_banana['msg']}")
        except Exception as e:
            log(mrh + f'Failed banana_list')

        def fame(task_name, max_length=25):
            if len(task_name) > max_length:
                return textwrap.shorten(task_name, width=max_length, placeholder="...")
            return task_name
        
        if config.get("auto_task", False):
            while True:
                claim_lottery_response = self.claim_quest_lottery(token)
                try:
                    if claim_lottery_response.get('msg') == "Success":
                        log(hju + "Successfully claimed quest lottery!")
                    else:
                        log(mrh + "Not available quest lottery to claim.")
                        break
                except Exception as e:
                    log(mrh + f"Failed quest lottery to claim")

            all_quests = self.quest_list(token)
            for quest in all_quests:
                quest_id = quest["quest_id"]
                quest_name = fame(quest["quest_name"])
                achieve_status = quest["is_achieved"]
                claim_status = quest["is_claimed"]
                try:
                    if not achieve_status and not claim_status:
                        self.achieve_quest(token, quest_id=quest_id)
                        claim_quest = self.claim_quest(token, quest_id=quest_id)
                        quest_status = claim_quest.get("msg", "Failed")

                        if quest_status == "Success":
                            log(hju + f"Quest {pth}{quest_name} claimed successfully.")
                        else:
                            log(mrh + f"Verification needed for {pth}{quest_name}.")

                    elif achieve_status and not claim_status:
                        claim_quest = self.claim_quest(token, quest_id=quest_id)
                        try:
                            quest_status = claim_quest.get("msg", "Failed")
                        except:
                            log(mrh + f"Failed quest")
                        if quest_status == "Success":
                            log(hju + f"Quest {pth}{quest_name} claimed successfully.")
                            countdown_timer(3)
                        else:
                            log(mrh + f"Real verification needed for {pth}{quest_name}.")

                    progress = claim_quest.get('data', {}).get('progress', "0/3")
                    if progress == "3/3":
                        log(hju + f"Quest progress complete ({progress}). Attempting to claim lottery again...")
                        claim_lottery_response = self.claim_quest_lottery(token)

                        if claim_lottery_response.get('msg') == "Success":
                            log(hju + "Successfully claimed quest lottery!")
                            countdown_timer(3)
                        else:
                            log(mrh + "Failed to claim quest lottery.")
                except Exception as e:
                    log(mrh + f"Failed claim quest")
            
            log(hju + f"Current progress: {progress}, more quests needed.")
        
    def quest_list(self, token: str):
        self.set_auth_header(token)
        page_number = 1
        all_quests = []
        
        while True:
            try:
                response = self._get(f'get_quest_list/v2?page_num={page_number}&page_size=10')
                quest_list = response.get('data', {}).get('list', [])
                all_quests.extend(quest_list)
                total_quests = response.get('data', {}).get('total', 0)
                if page_number * 10 >= total_quests:
                    break

                page_number += 1
            except:
                log(mrh + f"Failed quest list")
        return all_quests

    def achieve_quest(self, token: str, quest_id: int):
        self.headers.update({
            'Authorization': token,
            'x-interceptor-id': 'a572954edccd61bbbb45e80814a42b39ae21468413f897afb60a19ca5d8374f46b2689a33747b192ae770f7b4d91fbe4'
        })
        payload = {"quest_id": quest_id}
        return self._post('achieve_quest', payload)

    def claim_quest(self, token: str, quest_id: int):
        self.set_auth_header(token)
        payload = {"quest_id": quest_id}
        return self._post('claim_quest', payload)

    def claim_quest_lottery(self, token: str):
        self.set_auth_header(token)
        payload = {}
        return self._post('claim_quest_lottery', payload)
    
    def do_equip(self, token: str, banana_id: int):
        self.set_auth_header(token)
        payload = {'bananaId': banana_id}
        return self._post('do_equip', payload)

    def do_sell(self, token: str, banana_id: int, sell_count: int):
        self.set_auth_header(token)
        payload = {'bananaId': banana_id, 'sellCount': sell_count}
        return self._post('do_sell', payload)

    def do_speedup(self, token: str):
        if not config["auto_speedup"]:
            return

        self.set_auth_header(token)
        payload = {}
        while True:
            try:
                response = self._post('do_speedup', payload)
                try:
                    data = response.get('data', {})
                except Exception as e:
                    log(mrh + "Failed speed up!")
                if not data:
                    return

                speedup_count = data.get('speedup_count', 0)
                log(hju + f"Baboost left: {pth}{speedup_count}")
                if speedup_count == 0:
                    break

                now = datetime.now()
                last_start = data['lottery_info']['last_countdown_start_time']
                countdown_interval = data['lottery_info']['countdown_interval']
                countdown_end = data['lottery_info']['remain_lottery_count']
                last_start_time = datetime.fromtimestamp(last_start / 1000)
                remaining_time = last_start_time + timedelta(minutes=countdown_interval) - now

                if remaining_time.total_seconds() > 0 and not countdown_end:
                    hours, remainder = divmod(remaining_time.total_seconds(), 3600)
                    minutes, seconds = divmod(remainder, 60)
                    log(hju + f"Countdown after baboost: {pth}{int(hours)}h {int(minutes)}m {int(seconds)}s")
                    countdown_timer(3)
                else:
                    break
                
            except RequestException as e:
                log(mrh + f"Something wrong please check {hju}last.log {mrh}file!")
                log_error(f"{str(e)}")