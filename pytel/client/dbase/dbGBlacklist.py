# pytel < https://t.me/kastaid >
# Copyright (C) 2023-present kastaid
#
# This file is a part of < https://github.com/kastaid/pytel/ >
# Please read the GNU Affero General Public License in
# < https://github.com/kastaid/pytel/blob/main/LICENSE/ >

from asyncache import (
    cached,)
from cachetools import (
    LRUCache,
    func,)
from ._BaseClient import (
    pydb,)


@func.lru_cache
def get_blacklisted():
    return (
        pydb.get_key(
            "GBLACKLIST_CHATS"
        )
        or {}
    )


@func.lru_cache
def check_blacklisted(
    user, chat=None
):
    bl = (
        get_blacklisted()
    )
    if bl.get(int(user)):
        x = bl[
            int(user)
        ]["chat"]
        if chat in list(
            x
        ):
            return True
        return False
    return False


@func.lru_cache
def add_blacklisted(
    user, chat
):
    bl = (
        get_blacklisted()
    )
    if bl.get(int(user)):
        bl[int(user)][
            "chat"
        ].append(chat)
    else:
        bl.update(
            {
                int(
                    user
                ): {
                    "chat": [
                        chat
                    ]
                }
            }
        )
    pydb.set_key(
        "GBLACKLIST_CHATS",
        bl,
    )


@func.lru_cache
def rem_blacklisted(
    user, chat
):
    bl = (
        get_blacklisted()
    )
    if (
        bl.get(int(user))
        and bl[
            int(user)
        ]["chat"]
    ):
        bl[int(user)][
            "chat"
        ].remove(chat)
        return pydb.set_key(
            "GBLACKLIST_CHATS",
            bl,
        )


@func.lru_cache
def rem_all_blacklisted(
    user,
):
    bl = (
        get_blacklisted()
    )
    if bl.get(int(user)):
        bl.pop(int(user))
        return pydb.set_key(
            "GBLACKLIST_CHATS",
            bl,
        )


@cached(
    LRUCache(
        maxsize=1024,
    )
)
async def list_blacklisted(
    user,
):
    bl = (
        get_blacklisted()
    )
    if bl.get(int(user)):
        return bl[
            int(user)
        ]["chat"]
