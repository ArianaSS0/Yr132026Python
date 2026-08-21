# V4, im up to splitting files and adding the simulation game elements
# My hopes are that this will be considered a finished product 

#===============================================================================================================
#Runns when user opens the program
print ("\033[1;36;40m Program running \033[0m") #Cyan text
print("")
#===============================================================================================================

#  Importing Necessary Modules  # 

#database tool
import sqlite3 
connection = sqlite3.connect("CURIO_STORAGE.db") #Creates/conects to a database file 
cursor = connection.cursor() #Controll that sents instructions into database

# GUI tool
import tkinter as tk 
from tkinter import ttk

# Folder location tool
import os

#Date and time
from datetime import datetime

#Import pip requests third party lyibrary from other code...
#Curently using for temp and weather
import requests #Notice everything taken from here makes startup take longer, I may need to add a loading screen...

#===============================================================================================================

# Getting real time values # 

#These are blank values that change later in code. 
#Here they just curently act as placeholders
weather = "Unknown"
tempurature = "Unknown"

#Time
#Gets the curent time from the users computer
time_now = datetime.now().strftime("%H:%M:%S") #String format time

#Date
#Gets the current data from the users computer
#date_now = "2026-06-25" #(Test)
date_now = datetime.now().strftime("%Y-%m-%d") #red text hoppfully just error finders mistake :l

def get_API_data():
#This def helps collect data from the API while also alowing the program to move on if there is no internet

    #Setting up Tempurature and weather
    city = "Auckland"

    try:
        api = requests.get(f"https://wttr.in/{city}?format=j1", timeout=5).json() 
        #calls from javascript, timeout affter 5 seconds alows program to move on with no internet

        #Get Tempurature
        tempurature = api["current_condition"][0]["temp_C"]
        #Gathers record of the curent tempurature in auckland from API server online

        #Get Weather
        weather = api["current_condition"][0]["weatherDesc"][0]["value"]
        #Gathers record of curent weather in auckland from API server online

        #Print results
        #print(tempurature,"°C", weather)
        print("Data recieved")
        return (weather), (tempurature)

    except requests.exceptions.ConnectionError:
        print("No internet")
        return ("Uknown"), ("Uknown") #Returns these values instead of temp and weather
    #If there is no internet, the program moves on
    
    except requests.exceptions.Timeout:
        print("Timed out")
        return ("Unknown"), ("Unknown") #Returns these values instead of temp and weather
    #If the 5 second timeout timmer gos off, the program moves on
    
    except requests.exceptions.RequestException:
        print("API error")
        return ("Uknown"), ("Uknown") #Returns these values instead of temp and weather
    #If there is another error regarding gathering information through the API key,
    #The program moves on

weather, tempurature = get_API_data()
#This collects the data that the get_API_data spits out
#it either prints weather and tempurature or "Unknown" X2

#===============================================================================================================

# Setting up lists #

#Category list
category_data = list(("Creative","Outdoor","Collection","Culinary","Digital","Entertainment","Fitness","Knowladge"))
#Used later in dropdown menues to help the user choose what category thier hobby resides in

#===============================================================================================================

# Setting-up-table  # 

#CREATE TABLE IF NOT EXISTS curios : 
#means a new database file will be created in the same folder if one isnt currently avalibel
cursor.execute("""
            CREATE TABLE IF NOT EXISTS curios (
                        id INTEGER PRIMARY KEY AUTOINCREMENT, 
                        name TEXT NOT NULL,
                        category TEXT NOT NULL,
                        description TEXT,
                        date_created TEXT NOT NULL,
                        last_logged TEXT NOT NULL,
                        status TEXT NOT NULL
                    ) 
            """) # Creates 7 tables to store curio data, NOT NULL means no empty input

print("Database and table successfully generated")
#Prints message if the database is sucsessfully found or generated

#===============================================================================================================
# GUI # 
#===============================================================================================================

# Startup #

#This creates the main database that everything will reside within
#(Exept for the tabs created from the buttons)
root = tk.Tk()
root.title("Curioverse - Hobby Tracker") #Name
root.geometry('500x300') #Width x Hight
root["bg"] = "#939071" #Bg colour

#===============================================================================================================

# Setting-up tkinter button animation  # 
#Footer buttons
def on_press(event):
    event.widget.config(relief="sunken")

def on_release(event):
    event.widget.config(relief="raised")
#This creates the satisfying animation of the button apearing to be pushed down when clicked

#===============================================================================================================

# Top Screen area #

frame_top = tk.Frame(root)
frame_top.pack(fill="x") 
#fills all space avalible within the width of the window

#all the text and values for the top lable

#Displays current data
tk.Label(frame_top, text=" Date:", font=("Arial", 10, "bold")).pack(side="left")
tk.Label(frame_top, text=date_now).pack(side="left")

#Displays current time
#time updates every minute
tk.Label(frame_top, text="  Time:", font=("Arial", 10, "bold")).pack(side="left") 
time_label = tk.Label(frame_top, text="", font=("Arial", 10))
time_label.pack(side="left")
def update_time():
    current_time = datetime.now().strftime("%H:%M")
    time_label.config(text=current_time)
    root.after(60000, update_time) #runs every 60,000ms (1 minute)
    print("Time Updated")
#This means whenever 60 seconds has past, the time in the main window updates to the curent time

#Displays curent weather
tk.Label(frame_top, text="  Weather:", font=("Arial", 10, "bold")).pack(side="left")
tk.Label(frame_top, text=weather).pack(side="left")

#Displays current tempurature
tk.Label(frame_top, text="  Tempurature:", font=("Arial", 10, "bold")).pack(side="left")
tk.Label(frame_top, text=f"{tempurature}°C").pack(side="left") 
#f string combines degrees symbol with stored value

#===============================================================================================================

#Reload curios treeview button
def reload_curios():
    for item in tree.get_children():
        tree.delete(item)

    #Runs code that updataes the treeview table
    cursor.execute("""SELECT "ID", "Name", "Category",Last_Logged, "Status" FROM curios""")
    rows = cursor.fetchall()
    for row in rows:
        tree.insert("","end", values=row)

#===============================================================================================================

# Middle play area #

#Creates the tree/table that resides in the middle of the window
middle_frame = tk.Frame(root)
middle_frame.pack(expand=True, fill="both") #Takes up all space between window and footer
tree = ttk.Treeview(middle_frame,
    columns=("ID", "Name", "Category","Logg", "Status"),
    show="headings",
    height=5)

#text displayed at top
tree.heading("ID", text="ID")
tree.heading("Name", text="Name")
tree.heading("Category", text="Category")
tree.heading("Logg", text="Last Logged")
tree.heading("Status", text="Status")

#where info is displayed
tree.column("ID", width=25)
tree.column("Name", width=120)
tree.column("Category", width=80)
tree.column("Logg", width=75)
tree.column("Status", width=50)

#scrolling function for displaying multiple curios
scrollbar = ttk.Scrollbar(middle_frame, orient="vertical", command=tree.yview)
tree.configure(yscrollcommand=scrollbar.set)
scrollbar.pack(side="right", fill="y")
tree.pack(expand=True, fill="both") #Takes up all avalible space in the middle area

#...............................................................................................................
#Reload treeview button
button_reload = tk.Button(middle_frame,text="Reload",command=reload_curios)
button_reload.pack(side="bottom", pady=5)

#Runs code
cursor.execute("""SELECT "ID", "Name", "Category",Last_Logged, "Status" FROM curios""")
rows = cursor.fetchall()
for row in rows:
    tree.insert("","end", values=row)

#===============================================================================================================

# Footer bar # 
# (And Buttons!)

#Shapes gives colour and sizes the footer containing the buttons
footer = tk.Frame(root, width=100, height=50, bg="light yellow") #frame
footer.pack_propagate(False) #prevents frame from shrinking?
footer.pack(side="bottom", fill="x") #locates at bottom of tab

#...............................................................................................................
#Button 1  
#Allows user to add a curio to the database
from add_curioV4 import add_curio

# leftover button operation formatting
button_add = tk.Button(footer, font = ("Arial",11), width = 9, height = 1, text = "Add Hobby", 
                       command=lambda: add_curio(root,cursor,connection,date_now,category_data))
button_add.pack(side="left", padx=5, pady=2) #button padding from boarder

#...............................................................................................................
# Button 2
#Allows user to edit a curio
from edit_curioV4 import edit_curio
button_edit = tk.Button(
    footer,
    font=("Arial", 11),
    width=9,
    height=1,
    text="Edit Hobby",
    command=lambda: edit_curio (root,cursor,connection,date_now,category_data))
    # lambada: the way to pass functions without explicitly defining them
button_edit.pack(side="left", padx=5, pady=2)

#...............................................................................................................
#Button 3
#Allows user to delete curios
from delete_curioV4 import delete_curio
button_delete = tk.Button(footer, font = ("Arial",11), width = 9, height = 1, text = "Delete Hobby", 
                          command=lambda: delete_curio (root,cursor,connection,date_now,category_data))
button_delete.pack(side="left", padx=5, pady=2)

#...............................................................................................................
#Button 4
#Allows user to view curios
from view_curioV4 import view_curio
button_view = tk.Button(footer, font = ("Arial",11), width = 9, height = 1, text = "View Hobby", 
                        command=lambda: view_curio(root,cursor,connection,date_now,category_data))
button_view.pack(side="left", padx=5, pady=2)

#...............................................................................................................
#Button 5
#Logg button, when clicked; changes last logged to present day.
from logg_curioV4 import logg_curio
button_logg = tk.Button(footer, font = ("Arial",11), width = 9, height = 1, text = "Log Hobby", 
                        command= lambda:logg_curio(root,cursor,connection,date_now,category_data))
button_logg.pack(side="left", padx=5, pady=2)

#===============================================================================================================

#End of footer bar 

#===============================================================================================================
#...............................................................................................................

# Updating last logged info 
# Checks activity of hobbys and marks as active or unactive

today = datetime.now() # Gets current date
rows = cursor.fetchall() # Looks through the rows within the table (feeds onto lower line of code)

#Gatheres the time last logged from each curio/hobby
for curio_id, last_logged in rows:
    last_logged_date = datetime.strptime(last_logged, "%Y-%m-%d")
    days = (today - last_logged_date).days

    if days > 30:
        status = "Inactive"
    else:
        status = "Active"
#Updates the current status of the curios/hobbys depending on how long its been since the user last checked on them

    cursor.execute("""
        UPDATE curios
        SET status = ?
        WHERE id = ?
    """, (status, curio_id))
#Updates the curio/hobbys status to Active or Inactive depending on in 30 days have passed

#...............................................................................................................

connection.commit()
#Creates the main widow for the user

# running loop and updating time
update_time()
root.mainloop() #while if statement for the GUI
#This isnt kept inside conection.commit() because otherwise it would freeze.
#Everything whithin conection.commit is frozen

#===============================================================================================================
#Runns if user quits the program
connection.close()
print("")
print ("\033[1;31;40m Program closing \033[0m") #Red text
#===============================================================================================================