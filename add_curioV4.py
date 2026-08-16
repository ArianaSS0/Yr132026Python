#Add curio code

import tkinter as tk

#...............................................................................................................


def add_curio(root, cursor, connection, date_now, category_data):
    print("add_curio Button pressed")
    # Creates popup
    popup1 = tk.Toplevel(root)
    popup1.title("Add Hobby")
    popup1.geometry("250x200") #Y,X
    #makes curio state automatically active
    state2 = ("Active")

#...............................................................................................................

    #user input to make new curio
    #lable 1
    tk.Label(popup1, text="Name").pack()
    name2 = tk.Entry(popup1)
    name2.pack()

#...............................................................................................................

    #lable 2
    tk.Label(popup1, text="Category").pack()
    category2 = tk.StringVar()
    category2.set(category_data[0])
    tk.OptionMenu(popup1, category2, *category_data).pack()

#...............................................................................................................

    #lable 3
    tk.Label(popup1, text="Description").pack()
    description2 = tk.Entry(popup1)
    description2.pack()

#...............................................................................................................

    def save_curio():
        name = name2.get().strip()

        if not name:
            print("Error, hoby must have name")
            return
            #prints name error mesage

#...............................................................................................................

        category = category2.get()
        description = description2.get()
        cursor.execute("""
                INSERT INTO curios (
                            name, 
                            category, 
                            description, 
                            date_created,
                            last_logged,
                            status
                        )
                VALUES ( 
                            ?, 
                            ?, 
                            ?,
                            ?,
                            ?,
                            ?
                        )
                            """, (name, category, description, date_now, date_now, state2)) # Puts Values inside the database

#...............................................................................................................
        
        connection.commit() #saves new information
        print("Curio sucsessfully created")
        popup1.destroy()

#...............................................................................................................


    #save button
    tk.Button(popup1,text="save", command=save_curio).pack(pady=10)