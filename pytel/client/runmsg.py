# pytel < https://t.me/kastaid >
# Copyright (C) 2023-present kastaid
#
# This file is a part of < https://github.com/kastaid/pytel/ >
# PLease read the GNU Affero General Public License in
# < https://github.com/kastaid/pytel/blob/main/LICENSE/ >

from asyncio import Lock
from contextlib import suppress
from os import getpid
from pyrogram import __version__
from pyrogram.enums import ParseMode
from pyrogram.errors.exceptions.bad_request_400 import (
    MessageIdInvalid,)
from pyrogram.raw.all import layer
from version import __version__ as versi
from ..config import PREFIX, LOGCHAT_ID
from .dbase.dbLogger import (
    already_logger,
    check_logger,)
from .utils import random_prefixies

_SEND_LOCK = Lock()

_TEXT = """
<b><u>PYTEL-Premium</b></u> is up and running!
├ <b>PID :</b>  <i>{}</i>
├ <b>PYTEL :</b>  <i>{}</i>
├ <b>Layer :</b>  <i>{}</i>
├ <b>Pyrogram :</b>  <i>{}</i>
└ <b>Prefix :</b> <code>{}</code>

<b><u>How to check expired</u> ?</b>
└ <code>{}status</code> <b>:</b> <i>To check ur expired</i>.

(c) @kastaid #pytel
"""


async def running_message(self) -> None:
    async with _SEND_LOCK:
        try:
            if self:
                user_id = self.me.id
            if (
                already_logger(
                    user_id=user_id
                )
                and not LOGCHAT_ID
            ):
                log_data = (
                    check_logger().get(
                        user_id
                    )
                )
                log_id = log_data[0]
                await self.send_message(
                    int(int(log_id)),
                    text=_TEXT.format(
                        getpid(),
                        versi,
                        layer,
                        __version__,
                        "".join(PREFIX),
                        random_prefixies(
                            PREFIX
                        ),
                    ),
                    parse_mode=ParseMode.HTML,
                    disable_notification=False,
                )
        except OSError:
            with suppress(
                BaseException
            ):
                await self.connect()
        except MessageIdInvalid as excp:
            self.send_log.exception(
                excp
            )
        except KeyError:
            pass
        except Exception as excp:
            self.send_log.exception(
                excp
            )
