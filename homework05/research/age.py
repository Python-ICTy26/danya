import datetime as dt
import statistics
import typing as tp

from vkapi.friends import get_friends


def age_predict(user_id: int) -> tp.Optional[float]:
    friends = get_friends(user_id, fields=["bdate"]).items
    age_list = [friend.get("bdate") for friend in friends]  # type: ignore
    count_has_age_friends = 0
    sum_age = 0
    for age in age_list:
        try:
            age_formatted = dt.datetime.strptime(age.replace(".", ""), r"%d%m%Y").date()  # type: ignore
        except (ValueError, AttributeError):
            continue
        count_has_age_friends += 1
        sum_age += (dt.datetime.now().date() - age_formatted).days // 365

    if count_has_age_friends:
        return sum_age / count_has_age_friends
    return None
