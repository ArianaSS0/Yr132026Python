import tkinter as tk

root = tk.Tk()
root.title("My 2nd GUI app")
root.geometry('900x500')
#structuring app size and base name 
#root means the backgound

#------------------------------------------------------

page1 = tk.Frame(root)
page2 = tk.Frame(root)

#top text
label = tk.Label(root, text = "Hello!", font=('Arial',16))
label.pack()  # This makes it visible

#colouring
label.config(fg='lightgrey', bg='black') #colours top text
root.config(bg='black')
#fg= foreground, bg= background


root.mainloop()
#loops display