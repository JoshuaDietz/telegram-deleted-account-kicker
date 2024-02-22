# Telegram userbot to kick deleted accounts from groups

Python userbot which automatically kicks deleted accounts from specified Telegram groups.

## Installation

Python 3 and pip need to be installed on your computer

Run `pip3 install -U pyrogram`

## Configuration

Download the source and jump into the directory where you downloaded it. Take the `config-template.yml`, fill in
all your details and save it. Then rename it to `config.yml`. You can obtain your Telegram api id and hash from
https://my.telegram.org/apps Keep a special look on `sleep_per_chat` and `sleep_after_kick` as you can get
FloodWait exceptions from Telegram if you're running too fast.

## Usage

1. `python3 -m venv .venv`
1. `./.venv/bin/pip3 install -U pyrogram`
1. `./.venv/bin/pip3 install -U pyyaml`
1. `cp config-template.yml config.yml`
1. Run it: `./.venv/bin/python3 main.py`

On the first start you will be asked for your phone number, the verification code and if you have twofactor auth
enabled for the password as well. Enter all and the programm should start running. You don't need to log in again.
If you want to log out simply end the session from another device AND delete the my_account.session file.

## Troubleshooting

#### ModuleNotFoundError: No module named 'yaml'

Just install it with `pip3 install pyyaml`

### pyrogram.errors.exceptions.bad_request_400.MessageTooLong: [400 MESSAGE_TOO_LONG]: The message text is over 4096 characters (caused by "messages.SendMessage")

Use branch 4096Fix
