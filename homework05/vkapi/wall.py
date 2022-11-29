import math
import textwrap
import time
import typing as tp
from string import Template

import pandas as pd  # type: ignore
from pandas import json_normalize

from vkapi import config, session
from vkapi.exceptions import APIError


def get_posts_2500(count: int = 2500, **params: tp.Any) -> tp.List[tp.Dict[str, tp.Any]]:
    params["count"] = str(count)
    code = (
        """
        var params = %s;
        var i = 0;
        var posts = [];
        while (i < 25 && params.count > 0) {
            var res = API.wall.get(params).items;
            posts.push(res);
            i = i + 1;
            params.count = params.count - 100;
            params.offset = params.offset + res.length;
        }
        return posts;
    """
        % params
    )

    response = session.post(
        "execute",
        code=code,
        access_token=config.VK_CONFIG["access_token"],
        v=config.VK_CONFIG["version"],
    )
    try:
        return response.json()["response"]["items"]
    except Exception as e:
        raise APIError.bad_request(message=str(e))


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
    params = {
        "owner_id": owner_id,
        "domain": domain,
        "offset": offset,
        "filter": filter,
        "extended": extended,
        "fields": fields,
        "v": config.VK_CONFIG["version"],
    }

    data = []
    start_time = time.time()
    for post_bundle in range(math.ceil(count / max_count)):
        if count > 0 and count >= max_count:
            posts_list = get_posts_2500(count=2500, **params)
            data += posts_list
            count -= 2500
            params["offset"] += 2500  # type: ignore
        else:
            posts_list = get_posts_2500(count=count, params=params)
            data += posts_list
            break

        time_passed = time.time() - start_time
        if time_passed < 1:
            time.sleep(1 - time_passed)
            start_time = time.time()

    return pd.json_normalize(data)
