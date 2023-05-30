class User:
    def __init__(self, user_name, first_name, last_name, delivery_address) -> None:
        self.user_name = user_name
        self.first_name = first_name
        self.last_name = last_name
        self.delivery_address = delivery_address
        self.items_purchased = []
    
    def add_to_cart(self, item):
        self.items_purchased.append(item)

    def remove_from_cart(self, i_item):
        for item in self.items_purchased:
            if item["description"] == i_item:
                self.items_purchased.remove(item)

    def clear_cart(self):
        self.items_purchased = []

def add_user():
    user_name = input("Choose a Username: ")
    first_name = input("Insert first name: ")
    last_name = input("Insert last name: ")
    delivery_address = input("Insert delivery address: ")
    user = User(user_name=user_name, first_name=first_name, last_name=last_name, delivery_address=delivery_address)
    print(f"Hello {user.user_name}!\nWelcome to the Best Nothing HERE")
    return user

# user1 = add_user()
# user1.add_to_cart({"shaw": 35})
# print(user1.items_purchased)