# Banana Script for Banana by Carv Protocol

This repository contains a Python script designed to automate interactions with the Banana API provided by Carv. The script logs into multiple accounts, performs various actions like clicking, claiming lotteries, equipping bananas, selling them, and speeding up processes based on the configurations set in `config.json`.

[![Join our Telegram](https://img.shields.io/badge/Telegram-2CA5E0?style=for-the-badge&logo=telegram&logoColor=white)](https://t.me/cucumber_scripts)
[![GitHub](https://img.shields.io/badge/GitHub-181717?style=for-the-badge&logo=github&logoColor=white)](https://github.com/cucumber-pickle/Cucumber)

## Registrations
 - Open and start  [BANANA BOT](https://t.me/OfficialBananaBot/banana?startapp=referral=LBA5LL) 
 - Do tap And Claim lottery
 - Collect PEEL also USDT
 - Withdraw USDT Instant

### What's new in this update? 

16.10.2024

- fixed a lottery bug. Added a 10-second delay between lotteries
- added claim of rewards for invited friends
- fixed the equip error of the most profitable banana
- fixed the error of selling bananas if there are more than 1

17.10.2024
- can't Claim harvest now. If it can be fixed, I will add this. Fixed the bot stopping with this error. 


## Features

- **Multi-account Support:** Automate actions across multiple accounts.
- **Lottery Operations:** Automatically handle lottery claims and clicks.
- **Banana Management:** Equip, sell, and manage your banana inventory.
- **Auto Complete Task** Automatically perform available quest
- **Auto Claim Quest Reward** After completing quest bot claim banana reward
- **Speed Up:** Automatically perform speed-up operations if enabled.
- **Configurable Settings:** Control various aspects of the script via a `config.json` file.

## Installation

1. **Clone the repository:**

   ```bash
   git clone https://github.com/cucumber-pickle/BananaCum.git
   cd BananaCum
   
Create and activate a virtual environment:

   ```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```
Install the required dependencies:

   ```bash
pip install -r requirements.txt
   ```

## Configuration
Create a config.json file in the root directory with the following structure:
   ```json
{
    "use_proxy": false,
    "auto_sell": false,
    "auto_speedup": false,
    "auto_task": false,
    "delay_account": 5,
    "cycle_delay": 3800
}
   ```
`use_proxy`: Enable it with `true` to activate proxy usage 

`auto_sell`: Automatically sell bananas if set to true (if banana > 1)

`auto_speedup`: Enable the speed-up (BaBoost) operation if set to true.

`auto_task`: Enable the auto-task (auto-task) operation if set to true.

`delay_account`: Delay between processing different accounts (in seconds).

`cycle_delay`: Delay between different cycles of operations (in seconds).

### Proxy Setup (Optional):

If you enable proxy support in `config.json`, create a `proxies.txt` file in the root directory, containing a list of proxies, one per line.

Example (proxy format: username:password@host:port):

   ```graphql
user1:pass1@123.123.123.123:8080
user2:pass2@456.456.456.456:8080
   ```

## Fill query.txt
Add a query.txt file containing the login information (e.g., tokens or other necessary data). Each line should represent a separate account.
1. Use PC/Laptop or Use USB Debugging Phone
2. open the `Banana bot miniapp`
3. Inspect Element `(F12)` on the keyboard
4. at the top of the choose "`Application`" 
5. then select "`Session Storage`" 
6. Select the links "`Banana`" and "`tgWebAppData`"
7. Take the value part of "`tgWebAppData`"
8. take the part that looks like this: 

```txt 
query_id=xxxxxxxxx-Rxxxxuj&
```
9. add it to `query.txt` file or create it if you dont have one


You can add more and run the accounts in turn by entering a query id in new line like this:
```txt
query_id=xxxxxxxxx-Rxxxxujhash=cxxx
query_id=xxxxxxxxx-Rxxxxujhash=cxxxx
```

after that run the Banana bot by writing the command

## Usage
To run the script, simply execute:

   ```bash
python main.py
   ```
The script will start processing each account listed in query.txt, performing all configured operations.


## This bot helpfull?  Please support me by buying me a coffee: 
``` 0xc4bb02b8882c4c88891b4196a9d64a20ef8d7c36 ``` - BSC (BEP 20)

``` UQBiNbT2cqf5gLwjvfstTYvsScNj-nJZlN2NSmZ97rTcvKz0 ``` - TON

``` 0xc4bb02b8882c4c88891b4196a9d64a20ef8d7c36 ``` - Optimism

``` THaLf1cdEoaA73Kk5yiKmcRwUTuouXjM17 ``` - TRX (TRC 20)

## License
This project is licensed under the MIT License - see the LICENSE file for details.

## Contact
For questions or support, please contact [CUCUMBER TG CHAT](https://t.me/cucumber_scripts_chat)
