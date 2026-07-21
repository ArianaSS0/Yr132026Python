import tkinter as tk
from tkinter import ttk

def view_curio(root, cursor, connection, date_now, category_data):
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