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
                        date_created TEXT NOT NULL,
                        last_logged TEXT NOT NULL,
                        status TEXT NOT NULL
                    ) 
            """) # Creates 6 tables, NOT NULL means no empty input

print("Database and table successfully generated")

#===============================================================================================================
# GUI # 
#===============================================================================================================

# Startup #

root = tk.Tk()
root.title("Curioverse (V4)") #Name
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
tk.Label(frame_top, text="   Date:", font=("Arial", 10, "bold")).pack(side="left")
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
#Allows user to edit a curio
from edit_curioV4 import edit_curio
button_edit = tk.Button(
    footer,
    font=("Arial", 12),
    width=10,
    height=1,
    text="Edit Curio",
    command=lambda: edit_curio (root,cursor,connection,date_now,category_data))
button_edit.pack(side="left", padx=12, pady=5)

#...............................................................................................................
#Button 3
#Allows user to delete curios
from delete_curioV4 import delete_curio
button_delete = tk.Button(footer, font = ("Arial",12), width = 10, height = 1, text = "Delete Curio", command=lambda: delete_curio (root,cursor,connection,date_now,category_data))
button_delete.pack(side="left", padx=12, pady=5)

#...............................................................................................................
#Button 4
#Allows user to view curios
from view_curioV4 import view_curio
button_view = tk.Button(footer, font = ("Arial",12), width = 11, height = 1, text = "View Curios", command=lambda: view_curio(root,cursor,connection,date_now,category_data))
button_view.pack(side="left", padx=12, pady=5)

#Button 5
#Logg button, when clicked; changes last logged to present day.
def logg_curio():
    print("logg_curio Button pressed")

button_logg = tk.Button(footer, font = ("Arial",12), width = 11, height = 1, text = "Logg Curio", command=logg_curio)
button_logg.pack(side="left", padx=12, pady=5)

#End of footer bar 
update_time()
root.mainloop() #while if statement for the GUI

#===============================================================================================================
connection.close()
print("")
print ("\033[1;31;40m Program closing \033[0m") #Red text
#===============================================================================================================