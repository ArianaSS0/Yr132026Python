# V4, im up to splitting files and adding the simulation game elements
# My hopes are that this will be considered a finished product 
#===============================================================================================================
print ("\033[1;36;40m Program running \033[0m") #Cyan text
print("")
#===============================================================================================================

#  Importing Necessary Modules  # 

#database tool
import sqlite3 
connection = sqlite3.connect("CURIO_STORAGE.db") #Creates/conects to a database file named company.db
cursor = connection.cursor() #Controll that sents instructions into database
# GUI tool
import tkinter as tk 
from tkinter import ttk
# Folder location tool
import os
#Date and time
from datetime import datetime
#Import pip requests thierd party lybrary from other code...
#Curently using for temp and weather
import requests #Notice everything taken from here makes startup take longer, I may need to add a loading screen...

#===============================================================================================================

# Getting real time values # 

#Time
time_now = datetime.now().strftime("%H:%M:%S") #String format time
#Date
#date_now = "2026-06-25" #(Test)
date_now = datetime.now().strftime("%Y-%m-%d") #red text hoppfully just error finder mistake :l
#Setting up Tempurature and weather
city = "Auckland"
data1 = requests.get(f"https://wttr.in/{city}?format=j1").json() #calls from javascript
#Get Tempurature
tempurature = data1["current_condition"][0]["temp_C"]
#Get Weather
weather = data1["current_condition"][0]["weatherDesc"][0]["value"]
#Print results
#print(tempurature,"°C", weather)
print("Data recieved")

#===============================================================================================================

# Setting up lists #

#Category list
category_data = list(("Creative","Outdoor","Collection","Culinary","Digital","Entertainment","Fitness","Knowladge"))

#===============================================================================================================

# Setting-up-table  # 

cursor.execute("""
            CREATE TABLE IF NOT EXISTS curios (
                        id INTEGER PRIMARY KEY AUTOINCREMENT, 
                        name TEXT NOT NULL,
                        category TEXT NOT NULL,
                        description TEXT,
                        date_created TEXT,
                        status TEXT NOT NULL
                    ) 
            """) # Creates 6 tables, NOT NULL means no empty input

print("Database and table successfully generated")

#===============================================================================================================
# GUI # 
#===============================================================================================================

# Startup #

root = tk.Tk()
root.title("Curioverse (V3)") #Name
root.geometry('500x300') #Width x Hight
root["bg"] = "#939071" #Bg colour

#===============================================================================================================

# Setting-up tkinter button animation  # 
#Footer buttons
def on_press(event):
    event.widget.config(relief="sunken")

def on_release(event):
    event.widget.config(relief="raised")

#===============================================================================================================

# Top Screen area #

frame_top = tk.Frame(root)
frame_top.pack(fill="x")

#all the text and values for the top lable
tk.Label(frame_top, text="      Date:", font=("Arial", 10, "bold")).pack(side="left")
tk.Label(frame_top, text=date_now).pack(side="left")

#time updates every minute
tk.Label(frame_top, text="    Time:", font=("Arial", 10, "bold")).pack(side="left") 
time_label = tk.Label(frame_top, text="", font=("Arial", 10))
time_label.pack(side="left")
def update_time():
    current_time = datetime.now().strftime("%H:%M")
    time_label.config(text=current_time)
    root.after(60000, update_time) #run again in 60,000ms (1 minute)
    print("Time Updated")

tk.Label(frame_top, text="    Weather:", font=("Arial", 10, "bold")).pack(side="left")
tk.Label(frame_top, text=weather).pack(side="left")
tk.Label(frame_top, text="    Tempurature:", font=("Arial", 10, "bold")).pack(side="left")
tk.Label(frame_top, text=f"{tempurature}°C").pack(side="left") 
#f string combines degrees symbol with stored value

#===============================================================================================================

# Middle play area #

#===============================================================================================================

# Footer bar # 
# (And Buttons!)

footer = tk.Frame(root, width=100, height=80, bg="light yellow") #frame
footer.pack_propagate(False) #prevents frame from shrinking?
footer.pack(side="bottom", fill="x") #locates at bottom of tab

#...............................................................................................................
#Button 1  
#Allows user to add a curio to the database
from add_curioV4 import add_curio

# leftover button operation formatting
button_add = tk.Button(footer, font = ("Arial",12), width = 10, height = 1, text = "Add Curio", command=lambda: add_curio(root,cursor,connection,date_now,category_data))
button_add.pack(side="left", padx=12, pady=5) #button padding from boarder

#...............................................................................................................
# Button 2
def edit_curio():
    print("edit_curio Button pressed")
    popup2 = tk.Toplevel(root)
    popup2.title("Edit Curio")
    popup2.geometry("300x220")

    # Curio ID
    tk.Label(popup2, text="Curio ID").pack()
    id_entry = tk.Entry(popup2)
    id_entry.pack()
    # Field to edit
    tk.Label(popup2, text="Edit").pack()
    edit_option = tk.StringVar()
    edit_option.set("Name")  # Default option
    tk.OptionMenu(
        popup2,
        edit_option,
        "Name",
        "Category",
        "Description"
    ).pack()

    # New value
    tk.Label(popup2, text="New Value").pack()
    value_entry = tk.Entry(popup2)
    value_entry.pack()

    #category dropdown menue
    tk.Label(popup2, text="Category").pack()
    category_choice = tk.StringVar()
    category_choice.set(category_data[0])  # Default selection
    category_menu = tk.OptionMenu(
        popup2,
        category_choice,
        *category_data)
    category_menu.pack()

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
button_edit = tk.Button(
    footer,
    font=("Arial", 12),
    width=10,
    height=1,
    text="Edit Curio",
    command=edit_curio
)
button_edit.pack(side="left", padx=12, pady=5)

#...............................................................................................................
#Button 3
def delete_curio():
    print("delete_curio Button pressed")
     # Create popup to delete curio
    popup3 = tk.Toplevel(root)
    popup3.title("Delete Curio")
    popup3.geometry("250x200") #Y,X
    # Deleting curio code
    tk.Label(popup3, text="Enter Curio ID:").pack(pady=5)
    id_entry = tk.Entry(popup3)
    id_entry.pack()
    def confirm_delete():
        try:
            curio_id = int(id_entry.get())
            cursor.execute("""
                        DELETE FROM curios
                        WHERE id = ?
                        """, (curio_id,))
            connection.commit()
            if cursor.rowcount == 0: #If there are no curios print error basically
                print("Error. No curio with that ID was found")
            else:
                print("Curio sucsessfully deleted.")
        except ValueError:
            print("Please enter a valid ID.")
    #Delete button
    tk.Button(popup3, text="Delete", command=confirm_delete).pack(pady=10)

    button_delete = tk.Button(
        footer,
        font=("Arial", 12),
        width=10,
        height=1,
        text="Delete Curio",
        command=delete_curio
    )
    button_delete.pack(side="left", padx=12, pady=5)


button_delete = tk.Button(footer, font = ("Arial",12), width = 10, height = 1, text = "Delete Curio", command=delete_curio)
button_delete.pack(side="left", padx=12, pady=5)

#...............................................................................................................
#Button 4
def view_curios():
    print("view_curios Button pressed")
    # Create popup and grabs curio info
    popup4 = tk.Toplevel(root)
    popup4.title("Curios")
    popup4.geometry("650x200")
    cursor.execute("SELECT * FROM curios")
    rows = cursor.fetchall()

    #Displaying results
    tree = ttk.Treeview(popup4,
    columns=("ID", "Name", "Category", "Description", "Date", "Status"),
    show="headings")
    tree.heading("ID", text="ID")
    tree.heading("Name", text="Name")
    tree.heading("Category", text="Category")
    tree.heading("Description", text="Description")
    tree.heading("Date", text="Date Created")
    tree.heading("Status", text="Status")
    tree.column("ID", width=50)
    tree.column("Name", width=120)
    tree.column("Category", width=100)
    tree.column("Description", width=180)
    tree.column("Date", width=90)
    tree.column("Status", width=80)
    scrollbar = ttk.Scrollbar(
    popup4,
    orient="vertical",
    command=tree.yview)
    tree.configure(yscrollcommand=scrollbar.set)
    scrollbar.pack(side="right", fill="y")
    tree.pack(expand=True, fill="both")
    cursor.execute("SELECT * FROM curios")

    rows = cursor.fetchall()
    for row in rows:
        tree.insert("", "end", values=row)

    tk.Label(popup4, text="Search Name").pack()
    search_entry = tk.Entry(popup4)
    search_entry.pack()
    def search_curios():

        search = search_entry.get()

        cursor.execute("""
            SELECT *
            FROM curios
            WHERE name LIKE ?
        """, ('%' + search + '%',))

        rows = cursor.fetchall()
    for item in tree.get_children():
        tree.delete(item)
        for row in rows:
         tree.insert("", "end", values=row)
    tk.Button(
    popup4,
    text="Search", command=search_curios).pack()

    tk.Button(
    popup4,
    text="Show All",
    command=load_all_curios).pack()

    print("Displayed Curios")

button_view = tk.Button(footer, font = ("Arial",12), width = 11, height = 1, text = "View Curios", command=view_curios)
button_view.pack(side="left", padx=12, pady=5)


#End of footer bar 
update_time()
root.mainloop() #while if statement for the GUI

#===============================================================================================================
connection.close()
print("")
print ("\033[1;31;40m Program closing \033[0m") #Red text
#===============================================================================================================