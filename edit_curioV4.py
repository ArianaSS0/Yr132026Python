import tkinter as tk

#Imports data from database?
def edit_curio(root, cursor, connection, date_now, category_data):
    print("edit_curio Button pressed")

    #Creates the tab everything is displayed within
    popup2 = tk.Toplevel(root)
    popup2.title("Edit Hobby") #Tab name
    popup2.geometry("300x220")

#...............................................................................................................

    # Curio ID
    tk.Label(popup2, text="Curio ID").pack()
    id_entry = tk.Entry(popup2)
    id_entry.pack()
    #Here the user enters the id of the curio they wish to edit

#...............................................................................................................

# Curio Name
    tk.Label(popup2, text="Name").pack()
    name_entry = tk.Entry(popup2)
    name_entry.pack()
    #Here the user enters the new name of the curio

#...............................................................................................................

# Curio Description
    tk.Label(popup2, text="Description").pack()
    description_entry = tk.Entry(popup2)
    description_entry.pack()
    #Here the user enters the new description of the curio

#...............................................................................................................

    #category dropdown menue
    tk.Label(popup2, text="Category").pack()
    category_choice = tk.StringVar()
    category_choice.set(category_data[0])  # Default selection
    category_menu = tk.OptionMenu(
        popup2,
        category_choice,
        *category_data)
    category_menu.pack()
    #takes list from main python and uses it as a dropdown within the tab

#...............................................................................................................

    def save_edit():
        try:
            curio_id = int(id_entry.get())
            new_value = value_entry.get()
            if edit_option.get() == "Name":
                cursor.execute(
                    "UPDATE curios SET name = ? WHERE id = ?",
                    (new_value, curio_id)
                )
            elif edit_option.get() == "Category": 
                new_value = category_choice.get()
                cursor.execute(
                    "UPDATE curios SET category = ? WHERE id = ?",
                    (new_value, curio_id)
                )
            elif edit_option.get() == "Description":
                cursor.execute(
                    "UPDATE curios SET description = ? WHERE id = ?",
                    (new_value, curio_id)
                )
            connection.commit()
            if cursor.rowcount == 0:
                print("No Curio with that ID found.")
            else:
                print("Curio successfully edited.")
                popup2.destroy()
        except ValueError:
            print("Please enter a valid ID.")
    tk.Button(
        popup2,
        text="Update",
        command=save_edit
    ).pack(pady=10)