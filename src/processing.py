def filter_by_state(list: list(), states: str = "EXECUTED") -> list():
    new_list = []

    for item in list:
      if item.get("state") == states:
          new_list.append(item)

    return new_list

def sort_by_date(list: list(), reverse: bool = True) -> list():
    return sorted(list, key=lambda x:x["date"], reverse=reverse)

