# Copyright (C) 2019 The Raphielscape Company LLC.
#
# Licensed under the Raphielscape Public License, Version 1.c (the "License");
# you may not use this file except in compliance with the License.
#
#

import asyncio
import random
import re
import time
import functools
from telethon import events
from cowpy import cow

from userbot import CMD_HELP, ZALG_LIST
from .. import loader, utils


# ================= CONSTANT =================
METOOSTR = [
    "Me too thanks",
    "Haha yes, me too",
    "Same lol",
    "Me irl",
    "Same here",
    "Haha yes",
    "Me rn",
]
EMOJIS = [
    "😂",
    "😂",
    "👌",
    "✌",
    "💞",
    "👍",
    "👌",
    "💯",
    "🎶",
    "👀",
    "😂",
    "👓",
    "👏",
    "👐",
    "🍕",
    "💥",
    "🍴",
    "💦",
    "💦",
    "🍑",
    "🍆",
    "😩",
    "😏",
    "👉👌",
    "👀",
    "👅",
    "😩",
    "🚰",
]
UWUS = [
    "(・`ω´・)",
    ";;w;;",
    "owo",
    "UwU",
    ">w<",
    "^w^",
    r"\(^o\) (/o^)/",
    "( ^ _ ^)∠☆",
    "(ô_ô)",
    "~:o",
    ";-;",
    "(*^*)",
    "(>_",
    "(♥_♥)",
    "*(^O^)*",
    "((+_+))",
]
FACEREACTS = [
    "ʘ‿ʘ",
    "ヾ(-_- )ゞ",
    "(っ˘ڡ˘ς)",
    "(´ж｀ς)",
    "( ಠ ʖ̯ ಠ)",
    "(° ͜ʖ͡°)╭∩╮",
    "(ᵟຶ︵ ᵟຶ)",
    "(งツ)ว",
    "ʚ(•｀",
    "(っ▀¯▀)つ",
    "(◠﹏◠)",
    "( ͡ಠ ʖ̯ ͡ಠ)",
    "( ఠ ͟ʖ ఠ)",
    "(∩｀-´)⊃━☆ﾟ.*･｡ﾟ",
    "(⊃｡•́‿•̀｡)⊃",
    "(._.)",
    "{•̃_•̃}",
    "(ᵔᴥᵔ)",
    "♨_♨",
    "⥀.⥀",
    "ح˚௰˚づ ",
    "(҂◡_◡)",
    "ƪ(ړײ)‎ƪ​​",
    "(っ•́｡•́)♪♬",
    "◖ᵔᴥᵔ◗ ♪ ♫ ",
    "(☞ﾟヮﾟ)☞",
    "[¬º-°]¬",
    "(Ծ‸ Ծ)",
    "(•̀ᴗ•́)و ̑̑",
    "ヾ(´〇`)ﾉ♪♪♪",
    "(ง'̀-'́)ง",
    "ლ(•́•́ლ)",
    "ʕ •́؈•̀ ₎",
    "♪♪ ヽ(ˇ∀ˇ )ゞ",
    "щ（ﾟДﾟщ）",
    "( ˇ෴ˇ )",
    "눈_눈",
    "(๑•́ ₃ •̀๑) ",
    "( ˘ ³˘)♥ ",
    "ԅ(≖‿≖ԅ)",
    "♥‿♥",
    "◔_◔",
    "⁽⁽ଘ( ˊᵕˋ )ଓ⁾⁾",
    "乁( ◔ ౪◔)「      ┑(￣Д ￣)┍",
    "( ఠൠఠ )ﾉ",
    "٩(๏_๏)۶",
    "┌(ㆆ㉨ㆆ)ʃ",
    "ఠ_ఠ",
    "(づ｡◕‿‿◕｡)づ",
    "(ノಠ ∩ಠ)ノ彡( \\o°o)\\",
    "“ヽ(´▽｀)ノ”",
    "༼ ༎ຶ ෴ ༎ຶ༽",
    "｡ﾟ( ﾟஇ‸இﾟ)ﾟ｡",
    "(づ￣ ³￣)づ",
    "(⊙.☉)7",
    "ᕕ( ᐛ )ᕗ",
    "t(-_-t)",
    "(ಥ⌣ಥ)",
    "ヽ༼ ಠ益ಠ ༽ﾉ",
    "༼∵༽ ༼⍨༽ ༼⍢༽ ༼⍤༽",
    "ミ●﹏☉ミ",
    "(⊙_◎)",
    "¿ⓧ_ⓧﮌ",
    "ಠ_ಠ",
    "(´･_･`)",
    "ᕦ(ò_óˇ)ᕤ",
    "⊙﹏⊙",
    "(╯°□°）╯︵ ┻━┻",
    r"¯\_(⊙︿⊙)_/¯",
    "٩◔̯◔۶",
    "°‿‿°",
    "ᕙ(⇀‸↼‶)ᕗ",
    "⊂(◉‿◉)つ",
    "V•ᴥ•V",
    "q(❂‿❂)p",
    "ಥ_ಥ",
    "ฅ^•ﻌ•^ฅ",
    "ಥ﹏ಥ",
    "（ ^_^）o自自o（^_^ ）",
    "ಠ‿ಠ",
    "ヽ(´▽`)/",
    "ᵒᴥᵒ#",
    "( ͡° ͜ʖ ͡°)",
    "┬─┬﻿ ノ( ゜-゜ノ)",
    "ヽ(´ー｀)ノ",
    "☜(⌒▽⌒)☞",
    "ε=ε=ε=┌(;*´Д`)ﾉ",
    "(╬ ಠ益ಠ)",
    "┬─┬⃰͡ (ᵔᵕᵔ͜ )",
    "┻━┻ ︵ヽ(`Д´)ﾉ︵﻿ ┻━┻",
    r"¯\_(ツ)_/¯",
    "ʕᵔᴥᵔʔ",
    "(`･ω･´)",
    "ʕ•ᴥ•ʔ",
    "ლ(｀ー´ლ)",
    "ʕʘ̅͜ʘ̅ʔ",
    "（　ﾟДﾟ）",
    r"¯\(°_o)/¯",
    "(｡◕‿◕｡)",
]
RUNSREACTS = [
    "Runs to Thanos",
    "Runs far, far away from earth",
    "Running faster than usian bolt coz I'mma Bot",
    "Runs to Marie",
    "This Group is too cancerous to deal with.",
    "Cya bois",
    "Kys",
    "I am a mad person. Plox Ban me.",
    "I go away",
    "I am just walking off, coz me is too fat.",
    "I Fugged off!",
]
DISABLE_RUN = False

# ===========================================

def register(cb): 
    cb(Meme())


class Meme(loader.Module):
    """ Userbot module for having some fun. """

    def __init__(self):
        self.name = _("Meme")
        self._me = None
        self._ratelimit = []

    async def client_ready(self, client, db):
        self._db = db
        self._client = client
        self._me = await client.get_me()
        if "Meme.watchout" not in str(client.list_event_handlers()):
            client.add_event_handler(
                functools.partial(self.watchout),
                events.NewMessage(outgoing=True, incoming=False, forwards=False))


    async def cpcmd(self, cp_e):
        """ Copypasta the famous meme """
        textx = await cp_e.get_reply_message()
        message = utils.get_args_raw(cp_e)

        if message:
            pass
        elif textx:
            message = textx.text
        else:
            await cp_e.edit("`😂🅱️IvE👐sOME👅text👅 for✌️Me👌tO👐MAkE👀iT💞funNy!💦`")
            return

        reply_text = random.choice(EMOJIS)
        # choose a random character in the message to be substituted with 🅱️
        b_char = random.choice(message).lower()
        for owo in message:
            if owo == " ":
                reply_text += random.choice(EMOJIS)
            elif owo in EMOJIS:
                reply_text += owo
                reply_text += random.choice(EMOJIS)
            elif owo.lower() == b_char:
                reply_text += "🅱️"
            else:
                if bool(random.getrandbits(1)):
                    reply_text += owo.upper()
                else:
                    reply_text += owo.lower()
        reply_text += random.choice(EMOJIS)
        await cp_e.edit(reply_text)

    async def cowsaycmd(self, cowmsg):
        """ For .cowsay module, userbot wrapper for cow which says things. """
        text = utils.get_args_raw(cowmsg)
        arg = "default"
        cheese = cow.get_cow(arg)
        cheese = cheese()

        await cowmsg.edit(f"<code>{cheese.milk(text).replace('`', '´')}</code>")

    async def vaporcmd(self, vpr):
        """ Vaporize everything! """
        reply_text = list()
        textx = await vpr.get_reply_message()
        message = utils.get_args_raw(vpr)
        if message:
            pass
        elif textx:
            message = textx.text
        else:
            await vpr.edit("`Ｇｉｖｅ ｓｏｍｅ ｔｅｘｔ ｆｏｒ ｖａｐｏｒ！`")
            return

        for charac in message:
            if 0x21 <= ord(charac) <= 0x7F:
                reply_text.append(chr(ord(charac) + 0xFEE0))
            elif ord(charac) == 0x20:
                reply_text.append(chr(0x3000))
            else:
                reply_text.append(charac)

        await vpr.edit("".join(reply_text))


    async def strcmd(self, stret):
        """ Stretch it."""
        textx = await stret.get_reply_message()
        message = stret.text
        message = utils.get_args_raw(stret)
        if message:
            pass
        elif textx:
            message = textx.text
        else:
            await stret.edit("<b>GiiiiiiiB sooooooomeeeeeee teeeeeeext!</b>")
            return

        count = random.randint(3, 10)
        reply_text = re.sub(r"([aeiouAEIOUａｅｉｏｕＡＥＩＯＵаеиоуюяыэё])", (r"\1" * count),
                            message)
        await stret.edit(reply_text)

    async def zalcmd(self, zgfy):
        """ Invoke the feeling of chaos. """
        reply_text = list()
        textx = await zgfy.get_reply_message()
        message = utils.get_args_raw(zgfy)
        if message:
            pass
        elif textx:
            message = textx.text
        else:
            await zgfy.edit(
                "`gͫ ̆ i̛ ̺ v͇̆ ȅͅ   a̢ͦ   s̴̪ c̸̢ ä̸ rͩͣ y͖͞   t̨͚ é̠ x̢͖  t͔͛`"
            )
            return

        for charac in message:
            if not charac.isalpha():
                reply_text.append(charac)
                continue

            for _ in range(0, 3):
                randint = random.randint(0, 2)

                if randint == 0:
                    charac = charac.strip() + \
                        random.choice(ZALG_LIST[0]).strip()
                elif randint == 1:
                    charac = charac.strip() + \
                        random.choice(ZALG_LIST[1]).strip()
                else:
                    charac = charac.strip() + \
                        random.choice(ZALG_LIST[2]).strip()

            reply_text.append(charac)

        await zgfy.edit("".join(reply_text))


    async def hicmd(self, hello):
        """ Greet everyone! """
        await hello.edit("Hoi!😄")


    async def owocmd(self, owo):
        """ UwU """
        textx = await owo.get_reply_message()
        message = utils.get_args_raw(owo)
        if message:
            pass
        elif textx:
            message = textx.text
        else:
            await owo.edit("` UwU no text given! `")
            return

        reply_text = re.sub(r"(r|l)", "w", message)
        reply_text = re.sub(r"(R|L)", "W", reply_text)
        reply_text = re.sub(r"n([aeiou])", r"ny\1", reply_text)
        reply_text = re.sub(r"N([aeiouAEIOU])", r"Ny\1", reply_text)
        reply_text = re.sub(r"\!+", " " + random.choice(UWUS), reply_text)
        reply_text = reply_text.replace("ove", "uv")
        reply_text += " " + random.choice(UWUS)
        await owo.edit(reply_text)


    async def reactcmd(self, react):
        """ Make your userbot react to everything. """
        index = random.randint(0, len(FACEREACTS))
        reply_text = FACEREACTS[index]
        await react.edit(reply_text)


    async def shgcmd(self, shg):
        r""" ¯\_(ツ)_/¯ """
        await shg.edit(r"¯\_(ツ)_/¯")


    async def runcmd(self, run):
        """ Run, run, RUNNN! """
        if not DISABLE_RUN:
            index = random.randint(0, len(RUNSREACTS) - 1)
            reply_text = RUNSREACTS[index]
            await run.edit(reply_text)


    async def disruncmd(srlf, norun):
        """ Some people don't like running... """
        global DISABLE_RUN
        DISABLE_RUN = True
        await norun.edit("```Done!```")


    async def enruncmd(self, run):
        """ But some do! """
        global DISABLE_RUN
        DISABLE_RUN = False
        await run.edit("```Done!```")


    async def metoocmd(self, hahayes):
        """ Haha yes """
        reply_text = random.choice(METOOSTR)
        await hahayes.edit(reply_text)


    async def mockcmd(self, mock):
        """ Do it and find the real fun. """
        reply_text = list()
        textx = await mock.get_reply_message()
        message = utils.get_args_raw(mock)
        if message:
            pass
        elif textx:
            message = textx.text
        else:
            await mock.edit("`gIvE sOMEtHInG tO MoCk!`")
            return

        for charac in message:
            if charac.isalpha() and random.randint(0, 1):
                to_app = charac.upper() if charac.islower() else charac.lower()
                reply_text.append(to_app)
            else:
                reply_text.append(charac)

        await mock.edit("".join(reply_text))


    async def clapcmd(self, memereview):
        """ Praise people! """
        textx = await memereview.get_reply_message()
        message = utils.get_args_raw(memereview)
        if message:
            pass
        elif textx:
            message = textx.text
        else:
            await memereview.edit("`Hah, I don't clap pointlessly!`")
            return
        reply_text = "👏 "
        reply_text += message.replace(" ", " 👏 ")
        reply_text += " 👏"
        await memereview.edit(reply_text)


    async def typecmd(self, typew):
        """ Just a small command to make your keyboard become a typewriter! """
        textx = await typew.get_reply_message()
        message = utils.get_args_raw(typew)
        if message:
            pass
        elif textx:
            message = textx.text
        else:
            await typew.edit("`Give a text to type!`")
            return
        sleep_time = 0.03
        typing_symbol = "|"
        old_text = ''
        await typew.edit(typing_symbol)
        await asyncio.sleep(sleep_time)
        for character in message:
            old_text = old_text + "" + character
            typing_text = old_text + "" + typing_symbol
            await typew.edit(typing_text)
            await asyncio.sleep(sleep_time)
            await typew.edit(old_text)
            await asyncio.sleep(sleep_time)


    async def scamcmd(self, event):
        """ Just a small command to fake chat actions for fun !! """
        if not event.text[0].isalpha() and event.text[0] not in ("/", "#", "@",
                                                                             "!"):
            options = [
                'typing', 'contact', 'game', 'location', 'voice', 'round', 'video',
                'photo', 'document', 'cancel'
            ]
            input_str = utils.get_args_raw(event)
            args = input_str.split()
            if len(args) is 0:  # Let bot decide action and time
                scam_action = random.choice(options)
                scam_time = random.randint(30, 60)
            elif len(args) is 1:  # User decides time/action
                try:
                    scam_action = str(args[0]).lower()
                    scam_time = random.randint(30, 60)
                except ValueError:
                    scam_action = random.choice(options)
                    scam_time = int(args[0])
            elif len(args) is 2:  # User decides both action and time
                scam_action = str(args[0]).lower()
                scam_time = int(args[1])
            else:
                await event.edit("`Invalid Syntax !!`")
                return
            try:
                if (scam_time > 0):
                    await event.delete()
                    async with event.client.action(event.chat_id, scam_action):
                        await asyncio.sleep(scam_time)
            except BaseException:
                return

    async def watchout(self, message):
        if message.text.lower() == "oof":
            t = "Oof"
            for j in range(15):
                t = t[:-1] + "of"
                await message.edit(t)

        if message.text.lower() == ":/":
            uio = ["/", "\\"]
            for i in range(1, 15):
                time.sleep(0.3)
                await message.edit(":" + uio[i % 2])

        if message.text.lower() == "-_-":
            okay = "-_-"
            for _ in range(10):
                okay = okay[:-1] + "_-"
                await message.edit(okay)