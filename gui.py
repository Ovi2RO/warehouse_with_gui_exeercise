import tkinter as tk
from tkinter import ttk
from user import User
from data import *
from tools import *
from datetime import datetime
import tkinter.messagebox

user = None
warehouse = []

def save_user():
    global user
    user_name = user_entry.get()
    first_name = first_name_entry.get()
    last_name = last_name_entry.get()
    delivery_address = address_entry.get()
    user = User(user_name=user_name, first_name=first_name, last_name=last_name, delivery_address=delivery_address)
    tkinter.messagebox.showinfo(title=f"Welcome {user_name}", message=f"Hello {first_name} {last_name}\nEnjoy the search")
    # print(user.user_name)
    # print(user.first_name)
    # print(user.last_name)
    # print(user.delivery_address)

def change_to_profile():
    profile_frame.pack(fill="both", expand=1)
    search_frame.forget()
    cart_frame.forget()
    

def change_to_search():
    search_frame.pack(fill="both", expand=1)
    profile_frame.forget()
    cart_frame.forget()

def change_to_cart():
    cart_frame.pack(fill="both", expand=1)
    search_frame.forget()
    profile_frame.forget()

def do_search():
    global warehouse
    warehouse = []
    output_text.delete(0, tk.END)
    warehouse_selected = warehouse_selector_combobox.get()
    order_by = order_selection_combobox.get()
    if warehouse_selected == "All":
        warehouse = stock
    elif warehouse_selected == "1":
        for item in stock:
            if item["warehouse"] == 1:
                warehouse.append(item)
    elif warehouse_selected == "2":
        for item in stock:
            if item["warehouse"] == 2:
                warehouse.append(item)

    for item in warehouse:
        item_date_obj = datetime.strptime(item["date_of_stock"], "%Y-%m-%d %H:%M:%S")
        item["days_in_stock"] = (datetime.today() - item_date_obj).days
    
    
    if order_by == "State":
        warehouse = sorted(warehouse, key=lambda d: d["state"])
    elif order_by == "Category":
        warehouse = sorted(warehouse, key=lambda d: d["category"])
    elif order_by == "Days in stock":
        warehouse = sorted(warehouse, key=lambda d: d["days_in_stock"])
        

    for i in warehouse:
        state = i["state"]
        category = i["category"]
        days_in_stock = i["days_in_stock"]
        out_str = f"{category}- state: {state}, days: {days_in_stock}"
        i["description"] = out_str
        output_text.insert(tk.END, i["description"])
    
def add_to_cart():
    selected_item = output_text.selection_get()
    
    for item in warehouse:
        if item["description"] == selected_item:
            user.add_to_cart(item)
            warehouse.remove(item)
    
    # print(val_list)
    # print(user.items_purchased)

def refresh_cart():
    cart_listbox.delete(0,tk.END)
    for item in user.items_purchased:
        cart_listbox.insert(tk.END, item["description"])

def remove_from_cart():
    removed_item = cart_listbox.selection_get()
    user.remove_from_cart(removed_item)
    refresh_cart()

def finalize_cart():
    tkinter.messagebox.showinfo(title="Order confirmed", message="Thank you for your purchase")
    user.clear_cart()
    refresh_cart()


# Creating the main window
window = tk.Tk()
window.title("Warehouse hide&seek")
window.geometry("650x450+50+50")

# Creating a frame for the window
main_frame = tk.Frame(window)
main_frame.pack()

# Creating a frame to contain the main menu
menu_frame = tk.LabelFrame(main_frame, text="Menu")
menu_frame.grid(row=0, columnspan=3, padx=10, pady=10)

# Adding to the menu frame the 4 buttons of the menu
btn_change_to_profile = tk.Button(menu_frame, text="Change to profile", command=change_to_profile, width=20)
btn_change_to_profile.grid(row=0, column=0, padx=5, pady=10)

btn_change_to_search = tk.Button(menu_frame, text="Change to search", command=change_to_search, width=20)
btn_change_to_search.grid(row=0, column=1, padx=5, pady=10)

btn_change_to_cart = tk.Button(menu_frame, text="Change to cart", command=change_to_cart, width=20)
btn_change_to_cart.grid(row=0, column=2, padx=5, pady=10)



# Creating a LabelFrame to expand the menu options
second_frame = tk.LabelFrame(main_frame)
second_frame.grid(row=1, column=0, sticky="W", padx=10, pady=10)


# Creating the LabelFrame for Profile menu option
profile_frame = tk.LabelFrame(second_frame)
profile_inner_frame = tk.LabelFrame(profile_frame, text="User profile")

# Adding the elements for Profile menu option
user_label = tk.Label(profile_inner_frame, text="Username: ")
user_label.grid(row=0, column=1)
user_entry = tk.Entry(profile_inner_frame)
user_entry.grid(row=1, column=1)

first_name_label = tk.Label(profile_inner_frame, text="First name: ")
first_name_label.grid(row=2, column=1)
first_name_entry = tk.Entry(profile_inner_frame)
first_name_entry.grid(row=3, column=1)

last_name_label = tk.Label(profile_inner_frame, text="Last name: ")
last_name_label.grid(row=4, column=1)
last_name_entry = tk.Entry(profile_inner_frame)
last_name_entry.grid(row=5, column=1)

address_label = tk.Label(profile_inner_frame, text="Address: ")
address_label.grid(row=6, column=1)
address_entry = tk.Entry(profile_inner_frame)
address_entry.grid(row=7, column=1)

empty_section_p1 = tk.Label(profile_inner_frame, text="")
empty_section_p1.grid(row=8, column=1)

empty_section_p2 = tk.Label(profile_inner_frame, text="")
empty_section_p2.grid(row=9, column=1)

save_btn = tk.Button(profile_inner_frame, text="Save", command=save_user)
save_btn.grid(row=10, column=1, padx= 10, pady= 10)

# Packing the Profile frame
profile_inner_frame.grid(row=0, column=0, sticky="news", padx=10, pady=5)
profile_frame.pack(pady=30, padx=10)


# Create a LabelFrame for Search menu option
search_frame = tk.LabelFrame(second_frame)
search_inner_frame = tk.LabelFrame(search_frame, text="Search")

# Adding elements for Search menu option
warehouse_selection_label = tk.Label(search_inner_frame, text="Select warehouse:")
warehouse_selection_label.grid(row=0, column=1)
warehouse_selector_combobox = ttk.Combobox(search_inner_frame, values=get_warehouses(stock))
warehouse_selector_combobox.grid(row=1, column=1)

order_selection_label = tk.Label(search_inner_frame, text="Order by: ")
order_selection_label.grid(row=2, column=1)
order_selection_combobox = ttk.Combobox(search_inner_frame, values=["None", "State", "Category", "Days in stock"])
order_selection_combobox.grid(row=3, column=1)

empty_section1 = tk.Label(search_inner_frame, text="")
empty_section1.grid(row=4, column=1)

empty_section2 = tk.Label(search_inner_frame, text="")
empty_section2.grid(row=5, column=1)

empty_section3 = tk.Label(search_inner_frame, text="")
empty_section3.grid(row=6, column=1)

empty_section4 = tk.Label(search_inner_frame, text="")
empty_section4.grid(row=7, column=1)

empty_section5 = tk.Label(search_inner_frame, text="")
empty_section5.grid(row=8, column=1)

empty_section6 = tk.Label(search_inner_frame, text="")
empty_section6.grid(row=9, column=1)

search_btn = tk.Button(search_inner_frame, text="Search", command=do_search)
search_btn.grid(row=10, column=1, padx= 10, pady= 10)

# Packing the Search menu frame
search_inner_frame.grid(row=0, column=0, sticky="news", padx=5, pady=10)

# Creating the search output frame
search_inner2_frame = tk.LabelFrame(search_frame, text="Result")

# Adding the output elements
output_text = tk.Listbox(search_inner2_frame, height=12, width=45)
output_text.grid(row=0, column=1, sticky="news")

add_button = tk.Button(search_inner2_frame, text="Add to cart", command=add_to_cart)
add_button.grid(row=8, column=1, padx= 10, pady= 10)

# Packing the search output frame
search_inner2_frame.grid(row=0, column=1, columnspan=2, sticky="news", padx=10, pady=10)

#Packing the Search frame
search_frame.pack(pady=30, padx=10)


#Creating the Cart Frame
cart_frame = tk.LabelFrame(second_frame)
cart_labelFrame = tk.LabelFrame(cart_frame, text="Cart")

cart_listbox = tk.Listbox(cart_labelFrame, width=73)
cart_listbox.grid(row=0, column=0, columnspan=3, sticky="news")

refresh_button = tk.Button(cart_labelFrame, text="Refresh", command=refresh_cart)
refresh_button.grid(row=1, column=0, padx=10, pady=10)

remove_button = tk.Button(cart_labelFrame, text="Remove", command=remove_from_cart)
remove_button.grid(row=1, column=1, padx=10, pady=10)

finalize_button = tk.Button(cart_labelFrame, text="Finalize", command=finalize_cart)
finalize_button.grid(row=1, column=2, padx=10, pady=10)

cart_labelFrame.pack(pady=10)





profile_frame.pack(fill="both", expand=1)





# third_frame = tk.LabelFrame(main_frame, text="result")
# third_frame.grid(row=1, columnspan=3)
# # any_label = tk.Label(third_frame, text="bla")
# # any_label.grid(row=0, column=0)















window.mainloop()