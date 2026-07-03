# I realised I was starting with the wrong things, so for this version I will work with sorting out 
# creating new curios veiwing them, editing them and other before I add the simulation part.
#===============================================================================================================
print ("\033[1;36;40m Program running \033[0m") #Cyan text
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

#===============================================================================================================
# Play-Field # 

print("")

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

print("Database and table successfully generated!")
print("")

while True :

    print("")
    print("Your current actions are: ")
    print("""
          - New Curio
          - View Curios
          - Edit Curio
          - Delete Curio
          - Close
          """)

    user_input = input("What action would you like to take?: ")
    print("")

#===============================================================================================================
    # Database Create New Curio
    if user_input == "New Curio":

        #user input to make new curio
        name2 = input("Name: ")
        category2 = input("Category: ")
        description2 = input("Description: ")
        state2 = ("Active")

        cursor.execute("""
            INSERT INTO curios (
                        name, 
                        category, 
                        description, 
                        date_created,
                        status
                    )
            VALUES ( 
                        ?, 
                        ?, 
                        ?,
                        ?,
                        ?
                    )
                        """, (name2, category2, description2, date_now, state2)) # Puts Values inside the database
        print("Curio sucsessfully created")
        print("")


        connection.commit() #sends info to table

#===============================================================================================================
    #Edit Curio
    elif user_input == "Edit Curio":
        #printing database/curio info
        print("Printing Curios:")
        print("")
        cursor.execute("SELECT * FROM curios") #Select data from table
        rows = cursor.fetchall()#Select ALL data
        for row in rows:
            print(row)
        print("")

        # Editing code
        curio_id = int(input("Enter the ID of the Curio to edit: "))#int input is for intagers only
        user_input = input("""
                           What would you like to edit?" 
                            - Name 
                            - Category
                            - Description
                            """)
        if user_input == "Name":
            new_name = input("Enter new name: ")
            cursor.execute("""
                UPDATE curios
                SET name = ?
                WHERE id = ?
                """, (new_name,curio_id)) #execute is to update info
            connection.commit()
            print("Curio sucsessfully editid.")
            print("")
        elif user_input == "Category":
            new_category = input("Enter new category: ")
            cursor.execute("""
                UPDATE curios
                SET category = ?
                WHERE id = ?
                """, (new_category,curio_id))
            connection.commit()
            print("Curio sucsessfully editid.")
            print("")
        elif user_input == "Description":
            new_description = input("Enter new description: ")
            cursor.execute("""
                UPDATE curios
                SET description = ?
                WHERE id = ?
                """, (new_description,curio_id))
            connection.commit()
            print("Curio sucsessfully editid.")
            print("")
        else:
            print ("Error")

#===============================================================================================================
    #Delete Curio
    elif user_input == "Delete Curio":
        #printing database/curio info
        print("Printing Curios:")
        print("")
        cursor.execute("SELECT * FROM curios")
        rows = cursor.fetchall()
        #Printing database
        for row in rows:
            print(row)
        print("")
        curio_id = int(input("Enter the ID of the Curio to delete: "))
        cursor.execute("""
                       DELETE FROM curios
                       WHERE id = ?
                    """, (curio_id,))
        connection.commit()
        if cursor.rowcount == 0: #If there are no curios print error basically
            print("Error. No curio with that ID was found")
            print("")
        else:
            print("Curio sucsessfully deleted.")
            print("")

#===============================================================================================================
    # See Curios
    elif user_input == "View Curios":

        #printing database/curio info
        print("Printing Curios:")
        print("")
        cursor.execute("SELECT * FROM curios")
        rows = cursor.fetchall()
        #Printing database
        for row in rows:
            print(row)
        print("")

#===============================================================================================================
    # Close program
    elif user_input == "Close":
        break
    
#===============================================================================================================
    #Error message
    else:
        print("Error, try again.")
        print("")

#===============================================================================================================
connection.close()
print ("\033[1;31;40m Program closing \033[0m") #Red text
#===============================================================================================================