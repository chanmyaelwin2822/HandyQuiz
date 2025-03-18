import tkinter
import customtkinter
from PIL import ImageTk,Image
import sys
import os

customtkinter.set_appearance_mode("System")  # Modes: system (default), light, dark
customtkinter.set_default_color_theme("green")  # Themes: blue (default), dark-blue, green

app = customtkinter.CTk()  #creating cutstom tkinter window
# Get the screen resolution
screen_width = app.winfo_screenwidth()
screen_height = app.winfo_screenheight()
# print(screen_width,screen_height)
#app.geometry("600x440")
app.geometry(f"{screen_width}x{screen_height}+0+0")
app.title('Welcome')

def start_button():
    app.destroy()
    os.system("python main.py")
    # app.destroy()            # destroy current window and creating new one
    # w = customtkinter.CTk()
    # w.geometry("1280x720")
    # w.title('Menu')
    # l1=customtkinter.CTkLabel(master=w, text="Home Page",font=('Century Gothic',60))
    # l1.place(relx=0.5, rely=0.5,  anchor=tkinter.CENTER)
    # w.mainloop()
    
img1=ImageTk.PhotoImage(Image.open("./resources/aa.png"))
l1=customtkinter.CTkLabel(master=app,image=img1)
l1.pack()

#creating custom frame
frame=customtkinter.CTkFrame(master=l1, width=320, height=200, corner_radius=15)

# Make the frame transparent by using a transparent image as a background
transparent_image = tkinter.PhotoImage(width=1, height=1)
# Set background color to system transparent
frame["bg"] = "systemTransparent"
# Set highlight background color to system transparent
frame["highlightbackground"] = "systemTransparent"

frame.place(relx=0.5, rely=0.5, anchor=tkinter.CENTER)

#
# l2=customtkinter.CTkLabel(master=frame, text="Log into your Account",font=('Century Gothic',20))
# l2.place(x=50, y=45)
#
# entry1=customtkinter.CTkEntry(master=frame, width=220, placeholder_text='Username')
# entry1.place(x=50, y=110)
#
# entry2=customtkinter.CTkEntry(master=frame, width=220, placeholder_text='Password', show="*")
# entry2.place(x=50, y=165)
#
l3=customtkinter.CTkLabel(master=frame, text="Welcome to Our Quiz",font=('Century Gothic',20))
l3.place(x=50,y=50)

#Create custom button
button1 = customtkinter.CTkButton(master=frame, width=220, height= 30, text="Start", command=start_button, corner_radius=6)
button1.place(x=50, y=120)
# button2 = customtkinter.CTkButton(master=frame, width=220, text="Stop", command=stop_button, corner_radius=6)
# button2.place(x=50, y=160)

# img2=customtkinter.CTkImage(Image.open("./assets/Google__G__Logo.svg.webp").resize((20,20), Image.ANTIALIAS))
# img3=customtkinter.CTkImage(Image.open("./assets/124010.png").resize((20,20), Image.ANTIALIAS))
# button2= customtkinter.CTkButton(master=frame, image=img2, text="Google", width=100, height=20, compound="left", fg_color='white', text_color='black', hover_color='#AFAFAF')
# button2.place(x=50, y=290)
#
# button3= customtkinter.CTkButton(master=frame, image=img3, text="Facebook", width=100, height=20, compound="left", fg_color='white', text_color='black', hover_color='#AFAFAF')
# button3.place(x=170, y=290)




# You can easily integrate authentication system 

app.mainloop()
