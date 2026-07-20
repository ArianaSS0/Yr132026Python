import tkinter as tk

def delete_curio(root, cursor, connection, date_now, category_data):
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