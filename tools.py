from data import stock

def dict_sorter(warehouse_sort:list, sort_by:int):
    for item in warehouse_sort:
        item_date_obj = datetime.strptime(item["date_of_stock"], "%Y-%m-%d %H:%M:%S")
        item["days_in_stock"] = (datetime.today() - item_date_obj).days
    
    if sort_by == 1:
        result = sorted(warehouse_sort, key=lambda d: d["state"])
    elif sort_by == 2:
        result = sorted(warehouse_sort, key=lambda d: d["category"])
    elif sort_by == 3:
        result = sorted(warehouse_sort, key=lambda d: d["days_in_stock"])
    return result


def get_warehouses(db:list):
    warehouse_numbers = set()
    for item in db:
        for key, value in item.items():
            if key == "warehouse":
                warehouse_numbers.add(value)
    warehouses = ["All"]
    for i in warehouse_numbers:
        warehouses.append(i)
    return warehouses

#print(get_warehouses(stock))
