def filter_by_state(list: list(), states: str = "EXECUTED") -> list():
    new_list = []

    for item in list:
      if item.get("state") == states:
          new_list.append(item)

    return new_list


