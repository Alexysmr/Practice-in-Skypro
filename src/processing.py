def filter_by_state(clients: list, state: str ='EXECUTED') -> list:
    """Функция фильтрации по статусу state"""
    filtered = []
    for client in clients:
        if client['state'] == state:
            filtered.append(client)
    return filtered


def sort_by_date(clients: list, sort_reverse: bool=True) ->list:
    """Функция сортировки по дате"""
    date_sorted = sorted(clients, key=lambda clients: clients['date'], reverse=sort_reverse)
    return date_sorted