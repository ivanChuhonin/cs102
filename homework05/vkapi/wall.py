import time
import typing as tp
from string import Template

import pandas as pd
from pandas import json_normalize

from vkapi import Session, config


def get_posts_2500(
    owner_id: str = "",
    domain: str = "",
    offset: int = 0,
    count: int = 10,
    max_count: int = 2500,
    filter: str = "owner",
    extended: int = 0,
    fields: tp.Optional[tp.List[str]] = None,
) -> tp.Dict[str, tp.Any]:
    pass


def get_wall_execute(
    owner_id: str = "",
    domain: str = "",
    offset: int = 0,
    count: int = 10,
    max_count: int = 2500,
    filter: str = "owner",
    extended: int = 0,
    fields: tp.Optional[tp.List[str]] = None,
    progress=None,
) -> pd.DataFrame:
    """
    Возвращает список записей со стены пользователя или сообщества.

    @see: https://vk.com/dev/wall.get

    :param owner_id: Идентификатор пользователя или сообщества, со стены которого необходимо получить записи.
    :param domain: Короткий адрес пользователя или сообщества.
    :param offset: Смещение, необходимое для выборки определенного подмножества записей.
    :param count: Количество записей, которое необходимо получить (0 - все записи).
    :param max_count: Максимальное число записей, которое может быть получено за один запрос.
    :param filter: Определяет, какие типы записей на стене необходимо получить.
    :param extended: 1 — в ответе будут возвращены дополнительные поля profiles и groups, содержащие информацию о пользователях и сообществах.
    :param fields: Список дополнительных полей для профилей и сообществ, которые необходимо вернуть.
    :param progress: Callback для отображения прогресса.
    """

    access_token = config.VK_CONFIG["access_token"]
    version = config.VK_CONFIG["version"]
    domain = config.VK_CONFIG["domain"]
    session = Session(domain)
    call_count = 1 + ((count - 1) // max_count)
    posts_list = []

    for i in range(call_count):
        try:

            code = Template(
                """return API.wall.get({
                "owner_id": "$owner_id",
                "domain": "$domain",
                "offset": $offset,
                "count": "$count",
                "filter": "$filter",
                "extended": $extended,
                "fields": "$fields",
                "v": $version
                });"""
            ).substitute(
                owner_id=owner_id,
                domain=domain,
                offset=offset + max_count * i,
                count=count - max_count * i if count - max_count * i < 101 else 100,
                filter=filter,
                extended=extended,
                fields=fields,
                version=str(version))

            taken_posts = session.post("execute",
                data={
                    "code": code,
                    "access_token": access_token,
                    "v": version})

            time.sleep(1)

            for post in taken_posts.json()["response"]["items"]:
                posts_list.append(post)

        except:
            pass
    return json_normalize(posts_list)
