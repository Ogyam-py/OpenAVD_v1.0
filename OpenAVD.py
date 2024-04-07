import tkinter as tk
import customtkinter as cus
from CTkMessagebox import CTkMessagebox
from AVD_aeroplane import aeroplane
from tkinter import PhotoImage

cus.set_appearance_mode("light")
cus.set_default_color_theme("dark-blue")


root = cus.CTk()
root.title("OpenAVD")
root.geometry("900x650+250+20")
root.resizable(width=0,height=0)

# Picture will be embeded into the frame.
bframe = cus.CTkFrame(root,width=600,height=410)
bframe.place(relx=0.02,rely=0.02)

sframe = cus.CTkFrame(root,width=250,height=600)
sframe.place(relx=0.704,rely=0.051)

dframe = cus.CTkFrame(root,width=600,height=200)
dframe.place(relx=0.02,rely=0.67)

img = PhotoImage(file="aircraft design.png")
#img = img.subsample(2,2)
cus.CTkLabel(bframe,image=img).place(x=0,y=0)

#stframe = cus.CTkFrame(sframe,width=225,height=380)
#stframe.place(relx=0.05,rely=0.05)
sons = ["Crude Method", "Refined Method"]
sonic = cus.CTkComboBox(sframe,width=200,values=sons)
sonic.set("Select Method")
sonic.place(relx=0.1,rely=0.35)

pay_frame = cus.CTkFrame(sframe,width=225,height=130)
pay_frame.place(relx=0.05,rely=0.68)
cus.CTkLabel(sframe,text="Range").place(relx=0.1,rely=0.43)
Range_ = cus.CTkEntry(sframe,placeholder_text="in km",width=120)
Range_.place(relx=0.1,rely=0.48)
cus.CTkLabel(sframe,text="Endurance").place(relx=0.1,rely=0.54)
Endure_ = cus.CTkEntry(sframe,placeholder_text="in seconds",width=120)
Endure_.place(relx=0.1,rely=0.59)
cus.CTkLabel(pay_frame,text="Payload",font=("arial",14, "bold")).place(relx=0.02,rely=0.01)
Pay_1 = cus.CTkEntry(pay_frame,placeholder_text="in quantity",width=120)
Pay_1.place(relx=0.4,rely=0.2)
cus.CTkLabel(pay_frame,text="Crew").place(relx=0.1,rely=0.2)
Pay_2 = cus.CTkEntry(pay_frame,placeholder_text="in kg",width=120)
Pay_2.place(relx=0.4,rely=0.45)
cus.CTkLabel(pay_frame,text="Cargo").place(relx=0.1,rely=0.45)
Pay_3 = cus.CTkEntry(pay_frame,placeholder_text="in kg",width=120)
Pay_3.place(relx=0.4,rely=0.7)
cus.CTkLabel(pay_frame,text="Dropable").place(relx=0.1,rely=0.7)

radio_frame = cus.CTkFrame(sframe,width=225,height=175)
radio_frame.place(relx=0.05,rely=0.02)

cus.CTkLabel(radio_frame,text="Aircraft Type",font=("arial",14,"bold")).place(relx=0.1,rely=0.05)


# Define a variable to store the selected option
def radiobutton_event():
    plane = str(choice.get())
   
choice = cus.StringVar(root, value="")
plane = str(choice.get())

# Create the radio buttons with different options and variable
option1_button = cus.CTkRadioButton(master=radio_frame, text="Transport", variable=choice, value="jt",command=radiobutton_event)
option1_button.place(relx=0.05,rely=0.3)

option2_button = cus.CTkRadioButton(master=radio_frame, text="Fighter", variable=choice, value="fj",command=radiobutton_event)
option2_button.place(relx=0.05,rely=0.5)

option3_button = cus.CTkRadioButton(master=radio_frame, text="Seaplane", variable=choice, value="sp",command=radiobutton_event)
option3_button.place(relx=0.05,rely=0.7)



# Function to update label based on selected option (Optional)
def update_label():
  #selected_label.configure(text=f"Selected Option: {choice.get()}")
    None

# Bind the update function to radio button selection (Optional)
option1_button.configure(command=update_label)
option2_button.configure(command=update_label)
option3_button.configure(command=update_label)


def change():
    val = switch.get()
    if val:
        cus.set_appearance_mode("dark")
        Fuselage_out.configure(text_color="black")
        Take_weight_out.configure(text_color="black")
        Wing_size_out.configure(text_color="black")
        Engine_size_out.configure(text_color="black")
        Max_v_out.configure(text_color="black")
        RTD_out.configure(text_color="black")

    
        
    else:
        cus.set_appearance_mode("light")
    
switch = cus.CTkSwitch(root,text="Dark Mode",
                       onvalue=1,
                       offvalue=0,
                       command=change)
switch.place(relx=0.86,rely=0.01)
#cus.CTkButton(root,text="theme",command=change,width=15).place(relx=0.9,rely=0.9)


cus.CTkLabel(dframe,text="Specifications",font=("arial",14,"bold")).place(relx=0.05,rely=0.05)
cus.CTkLabel(dframe,text="Fuselage",font=("arial",13)).place(relx=0.05,rely=0.3)
cus.CTkLabel(dframe,text="Takeoff Weight",font=("arial",13)).place(relx=0.05,rely=0.5)
cus.CTkLabel(dframe,text="Wing size",font=("arial",13)).place(relx=0.05,rely=0.7)
cus.CTkLabel(dframe,text="Engine Size",font=("arial",13)).place(relx=0.55,rely=0.3)
cus.CTkLabel(dframe,text="Max Velocity",font=("arial",13)).place(relx=0.55,rely=0.5)
cus.CTkLabel(dframe,text="RDT&E + F",font=("arial",13)).place(relx=0.55,rely=0.7)

#cus.CTkLabel(dframe,text="",font=("arial",14,"bold")).place(relx=0.05,rely=0.05)
global Fuselage_out
Fuselage_out = cus.CTkLabel(dframe,text="",font=("arial",13,"bold"),fg_color="white",width=150)
Fuselage_out.place(relx=0.2,rely=0.3)
Take_weight_out = cus.CTkLabel(dframe,text="",font=("arial",13,"bold"),fg_color="white",width=150)
Take_weight_out.place(relx=0.2,rely=0.5)
Wing_size_out = cus.CTkLabel(dframe,text="",font=("arial",13,"bold"),fg_color="white",width=150)
Wing_size_out.place(relx=0.2,rely=0.7)
Engine_size_out = cus.CTkLabel(dframe,text="",font=("arial",13,"bold"),fg_color="white",width=150)
Engine_size_out.place(relx=0.7,rely=0.3)
Max_v_out = cus.CTkLabel(dframe,text="",font=("arial",13,"bold"),fg_color="white",width=150)
Max_v_out.place(relx=0.7,rely=0.5)
RTD_out = cus.CTkLabel(dframe,text="",font=("arial",13,"bold"),fg_color="white",width=150)
RTD_out.place(relx=0.7,rely=0.7)
#Fuselage_out.configure(text=str(45))

def calculate():
    # Inputs from the App
    crew = eval(Pay_1.get())
    cargo = eval(Pay_2.get())
    dropable = eval(Pay_3.get())
    range_val = eval(Range_.get()) 
    Endurance_val = eval(Endure_.get())
    Refined_status = sonic.get()

    if Refined_status == "Crude Method":
        refined = False
    else:
        refined = True

    plane = str(choice.get())
    # print(plane)

    aero_design = aeroplane(plane, range_val, Endurance_val, crew, cargo, dropable)
    parameters = aero_design.main(refined)
    # print(parameters)

    # Output from the App
    fuselage = parameters["fuselage"]
    weight = str(parameters["weight"]) + " Kg"
    wing_size = parameters["wing_size"]
    Engine_size = str(parameters["engine_size"]) + " N"
    max_v = str(parameters["V_max"]) + " m/s"
    RTD_ = str(round(parameters["RTD&E"]/1000000, 3)) + " M USD"

    Fuselage_out.configure(text=str(fuselage))
    Take_weight_out.configure(text=str(weight))
    Wing_size_out.configure(text=str(wing_size))
    Engine_size_out.configure(text=str(Engine_size))
    Max_v_out.configure(text=str(max_v))
    RTD_out.configure(text=str(RTD_))


cus.CTkButton(sframe,text="ESTIMATE",font=("courier",15,"bold"), command=calculate).place(relx=0.2,rely=0.94)

root.mainloop()