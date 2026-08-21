# Importing nesesary modules
import tkinter as tk
from tkinter import ttk
from datetime import datetime

#...............................................................................................................

#Looks for certian values in database
def logg_curio(root, cursor, connection, date_now, category_data):

#...............................................................................................................

#Creates window
    print("logg_curio Button pressed")
    popup3 = tk.Toplevel(root)
    popup3.title("Logg Hobby")
    popup3.geometry("300x220")

#...............................................................................................................

    # Curio ID
    tk.Label(popup3, text="Curio ID").pack()
    id_entry = tk.Entry(popup3)
    id_entry.pack()  

#...............................................................................................................
    
    # New log update
    def save_logg():
        try:
            curio_id = int(id_entry.get())
            today = datetime.now().strftime("%Y-%m-%d") # Gets current date and user id entry
            cursor.execute(""" UPDATE curios 
                            SET last_logged = ?, status = ?
                            WHERE id = ?"""
                           ,(today, "Active", curio_id))
            connection.commit()

            # printing info to play area??? (idk what its called again)
            if cursor.rowcount == 0:
                print("No Curio found")
            else:
                print("Progress logged")
                popup3.destroy()

#...............................................................................................................

        except ValueError:
            print("Please enter a valid id")
    tk.Button(popup3,text="Log Progress",command=save_logg).pack(pady=10)