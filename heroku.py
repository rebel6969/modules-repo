# Copyright (C) 2020 Adek Maulana.
# All rights reserved.
"""
   Heroku manager for your userbot
"""

import heroku3
import asyncio
import os
import requests
import math
import io
import os
import requests
from userbot.events import register
from telethon.tl.types import MessageMediaPhoto

import glob

class Var:
    HEROKU_API_KEY="f1072845-0058-4b28-9f01-928b3f651110"

Heroku = heroku3.from_key(Var.HEROKU_API_KEY)
heroku_api = "https://api.heroku.com"


@register(outgoing=True, pattern="^.usage(?: |$)(.*)")

async def dyno_usage(dyno):
    """
        Get your account Dyno Usage
    """
    await dyno.edit("`Processing...`")
    useragent = ('Mozilla/5.0 (Linux; Android 10; SM-G975F) '
                 'AppleWebKit/537.36 (KHTML, like Gecko) '
                 'Chrome/80.0.3987.149 Mobile Safari/537.36'
                 )
    user_id = Heroku.account().id
    headers = {
     'User-Agent': useragent,
     'Authorization': f'Bearer {Var.HEROKU_API_KEY}',
     'Accept': 'application/vnd.heroku+json; version=3.account-quotas',
    }
    path = "/accounts/" + user_id + "/actions/get-quota"
    r = requests.get(heroku_api + path, headers=headers)
    if r.status_code != 200:
        return await dyno.edit("`Error: something bad happened`\n\n"
                               f">.`{r.reason}`\n")
    result = r.json()
    quota = result['account_quota']
    quota_used = result['quota_used']

    """ - Used - """
    remaining_quota = quota - quota_used
    percentage = math.floor(remaining_quota / quota * 100)
    minutes_remaining = remaining_quota / 60
    hours = math.floor(minutes_remaining / 60)
    minutes = math.floor(minutes_remaining % 60)

    """ - Current - """
    App = result['apps']
    try:
        App[0]['quota_used']
    except IndexError:
        AppQuotaUsed = 0
        AppPercentage = 0
    else:
        AppQuotaUsed = App[0]['quota_used'] / 60
        AppPercentage = math.floor(App[0]['quota_used'] * 100 / quota)
    AppHours = math.floor(AppQuotaUsed / 60)
    AppMinutes = math.floor(AppQuotaUsed % 60)

    await asyncio.sleep(1.5)

    return await dyno.edit("**Dyno Usage**:\n\n"
                           f" -> `Dyno usage for`  **{Var.HEROKU_APP_NAME}**:\n"
                           f"     •  `{AppHours}`**h**  `{AppMinutes}`**m**  "
                           f"**|**  [`{AppPercentage}`**%**]"
                           "\n\n"
                           " -> `Dyno hours quota remaining this month`:\n"
                           f"     •  `{hours}`**h**  `{minutes}`**m**  "
                           f"**|**  [`{percentage}`**%**]"
                           )


