import tkinter as tk


# Function to handle listbox item selection
def on_select(event):
    selected_item = listbox.get(listbox.curselection())
    print("Selected item:", selected_item)


# Function to add item to the list
def add_item():
    new_item = entry.get()
    if new_item.strip():  # Check if the entry is not empty
        my_list.append(new_item)  # Add the item to the underlying list
        update_listbox()  # Update the listbox with the latest items
        entry.delete(0, tk.END)  # Clear the entry after adding the item


# Function to delete selected item from the list
def delete_item():
    try:
        selected_index = listbox.curselection()[0]
        deleted_item = listbox.get(selected_index)
        my_list.remove(deleted_item)  # Remove the item from the underlying list
        update_listbox()  # Update the listbox with the latest items
    except IndexError:  # Catch error if no item is selected
        pass


# Function to update listbox with the latest items
def update_listbox():
    listbox.delete(0, tk.END)  # Clear the existing items in the listbox
    for item in my_list:
        listbox.insert(tk.END, item)  # Insert each item from the updated list


# Function to print the selected item and return it from the list
def print_and_return_item():
    try:
        selected_index = listbox.curselection()[0]
        selected_item = listbox.get(selected_index)
        print("Selected item:", selected_item)
        return selected_item
    except IndexError:  # Catch error if no item is selected
        return None  # Return None when no item is selected


# Create main window
root = tk.Tk()
root.title("List Operations")

# Initial list
my_list = ["Apple", "Banana", "Orange"]

# Create a listbox to display the list
listbox = tk.Listbox(root, font=("Arial", 12), selectmode=tk.SINGLE)
listbox.pack(pady=10, padx=10, expand=True, fill=tk.BOTH)

# Populate the listbox with initial items
update_listbox()

# Bind the listbox item selection event
listbox.bind("<<ListboxSelect>>", on_select)

# Entry widget to enter new items
entry = tk.Entry(root, font=("Arial", 12))
entry.pack(pady=5, padx=10, fill=tk.BOTH)

# Button to add new item
add_button = tk.Button(root, text="Add Item", command=add_item)
add_button.pack(pady=5, padx=10, fill=tk.BOTH)

# Button to delete selected item
delete_button = tk.Button(root, text="Delete Item", command=delete_item)
delete_button.pack(pady=5, padx=10, fill=tk.BOTH)

# Button to print selected item and return it from the list
print_return_button = tk.Button(root, text="Print and Return Item", command=print_and_return_item)
print_return_button.pack(pady=5, padx=10, fill=tk.BOTH)

# Run the Tkinter event loop
root.mainloop()
