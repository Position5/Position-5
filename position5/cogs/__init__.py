"""
This file contains all constants to be used by cogs
"""
import logging
import functools
from discord.ext.commands import Context


log = logging.getLogger("position5.cogs")

COGS = [
    "cogs.activity",
    "cogs.basic",
    "cogs.core",
    "cogs.cricket",
    "cogs.db",
    "cogs.embed",
    "cogs.emotes",
    "cogs.error_handler",
    "cogs.fun",
    "cogs.pic",
    "cogs.poll",
    "cogs.react",
    "cogs.reddit",
    "cogs.stock",
]


EMOTES_PATH = "assets/emotes/"
FONT_PATH = "assets/font/"
MEME_PATH = "assets/meme/"
PIC_PATH = "assets/pic/"
TEMP_PATH = "assets/tmp/"

DISCLAIMER = """
I am NOT a SEBI registered advisor or a financial adviser.

Any post associated with this IP is satire and should be treated as such. At no point has anyone associated with this IP ever condoned, encouraged, committed or abated acts of violence or threats of violence against any persons, regardless of racial, ethnic, religious or cultural background.

In case of an investigation by any federal entity or similar, I do not have any involvement with this group or with the people in it, I do not know how I am here, probably added by a third party, I do not support any actions by the member of this group.

Any of my investment or trades I share here are provided for educational purposes only and do not constitute specific financial, trading or investment advice. The statements are intended to provide educational information only and do not attempt to give you advice that relates to your specific circumstances. You should discuss your specific requirements and situation with a qualified financial adviser. I do share details and numbers available in the public domain for any company or on the websites of NSE, BSE, YahooFinance and TradingView.
"""

WHY_NIFTY = """
1. It is diversified
2. Hard to manipulate
3. Highly liquid
4. Lesser margins
5. Broader economic call
6. Application of technical analysis
7. Less volatile
"""

EMOJIS_DICT = {
    "a": ["\U0001f1e6", "🅰️"],  # jeans
    "b": ["🅱️", "\U0001f1e7"],
    "c": ["\U0001f1e8", "©️", "\U0001f318"],
    "d": ["\U0001f1e9"],  # leftwards_arrow_with_hook
    "e": ["\U0001f1ea", "\U0001f4e7"],
    "f": ["\U0001f1eb"],
    "g": ["\U0001f1ec"],  # compression
    "h": ["\U0001f1ed", "♓"],
    "i": ["\U0001f1ee", "ℹ️"],
    "j": ["\U0001f1ef"],
    "k": ["\U0001f1f0"],
    "l": ["\U0001f1f1"],
    "m": ["\U0001f1f2", "Ⓜ️", "♏", "♍"],
    "n": ["\U0001f1f3", "♑"],
    # '⚪️',record_button, doughnut, nazar_amulet
    "o": ["\U0001f1f4", "🅾️", "⭕"],
    "p": ["\U0001f1f5", "🅿"],
    "q": ["\U0001f1f6"],
    "r": ["\U0001f1f7", "®"],
    "s": ["\U0001f1f8", "\U0001f4b2"],
    "t": ["\U0001f1f9", "✝️"],
    "u": ["\U0001f1fa", "⛎"],
    "v": ["\U0001f1fb"],  # v, vs
    "w": ["\U0001f1fc"],  # wc
    "x": ["\U0001f1fd", "❌", "❎", "✖️"],
    "y": ["\U0001f1fe"],
    "z": ["\U0001f1ff"],
    "0": ["0️⃣"],
    "1": ["1️⃣", "\U0001f947"],
    "2": ["2️⃣", "\U0001f948"],
    "3": ["3️⃣", "\U0001f949"],
    "4": ["4️⃣"],
    "5": ["5️⃣"],
    "6": ["6️⃣"],
    "7": ["7️⃣"],
    "8": ["8️⃣", "\U0001f3b1"],
    "9": ["9️⃣"],
    "!": ["❗", "❕"],
    "?": ["❓", "❔"],
    "*": ["*️⃣"],
    "#": ["#️⃣"],
    "+": ["➕"],
    "-": ["➖"],
    "$": ["\U0001f4b2"],
    # added for possible future use
    "10": ["🔟"],
    "100": ["💯"],
    "ab": ["🆎"],
    "abc": ["🔤"],
    "abcd": ["🔠", "🔡"],
    "cl": ["🆑"],
    "id": ["🆔"],
    "vs": ["🆚"],
    "ng": ["🆖"],
    "ok": ["🆗"],
    "up!": ["🆙"],
    "cool": ["🆒"],
    "new": ["🆕"],
    "free": ["🆓"],
    "wc": ["🚾"],
    "<3": ["❤️"],
    "!!": ["‼"],
    "!?": ["⁉"],
}

# List of urls
AGIFY = "https://api.agify.io"
GENDERIFY = "https://api.genderize.io"
NSE_FII_DII = "https://www.nseindia.com/reports/fii-dii"
NSE_FII_DII_TRADE_REACT = "https://www.nseindia.com/api/fiidiiTradeReact"


def delete_message():
    def wrapper(func):
        @functools.wraps(func)
        async def wrapped(*args, **kwargs):
            assert isinstance(ctx := args[1], Context)
            await ctx.message.delete()
            return await func(*args, **kwargs)

        return wrapped

    return wrapper


def log_params():
    def wrapper(func):
        @functools.wraps(func)
        async def wrapped(*args, **kwargs):
            assert isinstance(ctx := args[1], Context)
            log.info(
                "Author: %s | Message: %s | Method: %s | Params: %s",
                ctx.author.name,
                ctx.message.content,
                func.__name__,
                kwargs,
            )
            return await func(*args, **kwargs)

        return wrapped

    return wrapper
