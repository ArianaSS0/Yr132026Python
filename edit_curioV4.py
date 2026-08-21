# Importing nesesary modules
import tkinter as tk

#Imports data from database
def edit_curio(root, cursor, connection, date_now, category_data):
    print("edit_curio Button pressed")

    #Creates the tab/window everything is displayed within
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
            #Transfuring user input from the values to something SQLite can read
            #!!! With the .get() !!!
            #also .get without .strip - if not... means blank infor can be entered
            curio_id = int(id_entry.get())
            new_name = name_entry.get().strip()
            if not new_name:
                print("Error, hobby must have name")
                return
                 #prints name error mesage
                        
            new_description = description_entry.get()
            new_category = category_choice.get()

            cursor.execute ("""
                UPDATE curios
                SET name = ?, description = ?, category = ?
                WHERE id = ?
                """,
                #sets up new name description and category
                #WHERE id = ?   gathers id to save entrys to
                (
                    new_name,
                    new_description,
                    new_category,
                    curio_id
                )
                #Gathers user entrys and prpeps them to save
            )

            connection.commit()
            #saves new information to database

            if cursor.rowcount == 0:
                print("No Curio with that ID found.")
                #Error message for incorect id input

            else:
                print("Curio successfully edited.")
                popup2.destroy()
                #Prints sucsess message and closes tab

        except ValueError:
            print("Please enter a valid ID.")
            #Another error mesage

#...............................................................................................................

    tk.Button(
        popup2,
        text="Update",
        command=save_edit
    ).pack(pady=10)
    #tab formatting