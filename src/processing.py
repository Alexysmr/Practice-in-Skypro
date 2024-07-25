def filter_by_state(clients: list, state: str = "EXECUTED") -> list:
    """Функция фильтрации по статусу state"""
    filtered = []
    for client in clients:
        if client != {}:
            if client["state"] == state:
                filtered.append(client)
    return filtered


def sort_by_date(clients: list, sort_reverse: bool = True) -> any:
    """Функция сортировки по дате"""
    if clients != []:
        symbols = (".", "/", "*", ":", ",", " ")
        for cell in clients:
            repair_date = ""
            counter = 0
            if cell != {}:
                for element in cell["date"]:
                    if counter != 10:
                        if element in symbols:
                            element = "-"
                        counter += 1
                    repair_date += element
            else:
                repair_date = "Ошибка введённых данных"
            cell["date"] = repair_date
    else:
        return "Ошибка введённых данных"

    date_sorted = sorted(clients, key=lambda clients: clients["date"], reverse=sort_reverse)
    return date_sorted
