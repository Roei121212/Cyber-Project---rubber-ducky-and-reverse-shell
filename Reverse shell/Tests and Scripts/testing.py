import tkinter as tk


my_list = ["Apple", "Banana", "Orange"]
# Function to handle listbox item selection
def on_select(event):
    selected_item = listbox.get(listbox.curselection())
    print("Selected item:", selected_item)

# Function to add item to the list
def add_item():
    new_item = entry.get()
    if new_item.strip():  # Check if the entry is not empty
        my_list.append(new_item)  # Add the item to the underlying list
        entry.delete(0, tk.END)  # Clear the entry after adding the item

# Function to delete selected item from the list
def delete_item():
    try:
        selected_index = listbox.curselection()[0]
        deleted_item = listbox.get(selected_index)
        my_list.remove(deleted_item)  # Remove the item from the underlying list
    except IndexError:  # Catch error if no item is selected
        pass

# Function to update listbox with the latest items
def update_listbox():
    listbox.delete(0, tk.END)  # Clear the existing items in the listbox
    for item in my_list:
        listbox.insert(tk.END, item)  # Insert each item from the updated list

# Function to update the list and listbox automatically at regular intervals
def auto_update():
    update_listbox()  # Update the listbox with the latest items
    root.after(500, auto_update)  # Call this function again after 500ms

# Create main window
root = tk.Tk()
root.title("List Operations")

# Initial list


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

# Start auto-updating the listbox
auto_update()

# Run the Tkinter event loop
root.mainloop()
