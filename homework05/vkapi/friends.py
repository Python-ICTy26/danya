import dataclasses
import math
import time
import typing as tp

from vkapi import config, session
from vkapi.exceptions import APIError

QueryParams = tp.Optional[tp.Dict[str, tp.Union[str, int]]]


@dataclasses.dataclass(frozen=True)
class FriendsResponse:
    count: int
    items: tp.Union[tp.List[int], tp.List[tp.Dict[str, tp.Any]]]


def get_friends(
    user_id: int, count: int = 5000, offset: int = 0, fields: tp.Optional[tp.List[str]] = None
) -> FriendsResponse:
    """
    Получить список идентификаторов друзей пользователя или расширенную информацию
    о друзьях пользователя (при использовании параметра fields).

    :param user_id: Идентификатор пользователя, список друзей для которого нужно получить.
    :param count: Количество друзей, которое нужно вернуть.
    :param offset: Смещение, необходимое для выборки определенного подмножества друзей.
    :param fields: Список полей, которые нужно получить для каждого пользователя.
    :return: Список идентификаторов друзей пользователя или список пользователей.
    """

    try:
        response = session.get(
            "friends.get",
            user_id=user_id,
            count=count,
            offset=offset,
            fields=fields,
            access_token=config.VK_CONFIG["access_token"],
            v=config.VK_CONFIG["version"],
        )
        response_data = response.json()["response"]
        return FriendsResponse(**response_data)
    except Exception as e:
        raise APIError.bad_request(message=str(e))


class MutualFriends(tp.TypedDict):
    id: int
    common_friends: tp.List[int]
    common_count: int


def get_mutual(
    source_uid: tp.Optional[int] = None,
    target_uid: tp.Optional[int] = None,
    target_uids: tp.Optional[tp.List[int]] = None,
    order: str = "",
    count: tp.Optional[int] = None,
    offset: int = 0,
    progress=None,
) -> tp.Union[tp.List[int], tp.List[MutualFriends]]:

    request_bundles = math.ceil(len(target_uids) / 100) if target_uids else 1

    time_start = time.time()
    count_request_bundles = 0
    mutual_list = []

    for request_bundle in range(request_bundles):
        response = session.get(
            "friends.getMutual",
            source_uid=source_uid,
            target_uid=target_uid,
            target_uids=target_uids,
            order=order,
            count=count,
            offset=request_bundle * 100 + offset,
            progress=progress,
        )
        if response.status_code == 200:
            response_data = response.json()["response"]
            for mutual in response_data:
                mutual_list.append(mutual)

        count_request_bundles += 1

        time_passed = time.time() - time_start
        if time_passed < 1 and count_request_bundles >= 3:
            count_request_bundles = 0
            start = time.time()
            time.sleep(1 - time_passed)

    try:
        mutual_list_formatted = [MutualFriends(**mutual) for mutual in mutual_list]  # type: ignore
    except TypeError:
        return mutual_list

    return mutual_list_formatted
