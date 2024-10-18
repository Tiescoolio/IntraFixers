import tkinter as tk
from tkinter import messagebox
import datetime

def storing_opgeven():
    global opgeven_storing
    opgeven_storing = tk.Toplevel()

    opgeven_storing.title("Nieuwe storing of oude storing aanvullen")
    icon = tk.PhotoImage(file="proRail_Logo.png")
    opgeven_storing.iconphoto(False, icon)

    storing_opgeven_label = tk.Label(opgeven_storing, text="Wilt u een nieuwe storing aanmaken of een oude storing aanvullen?")
    storing_opgeven_label.pack(pady=5)

    nieuwe_storing_knop = tk.Button(opgeven_storing, text="Nieuwe storing aanmaken", command=nieuwe_storing)
    nieuwe_storing_knop.pack(pady=10)

    oude_storing_aanvullen = tk.Button(opgeven_storing, text="Oude storing aanvullen", command=storing_aanvullen)
    oude_storing_aanvullen.pack(pady=10)
    opgeven_storing.mainloop()

def nieuwe_storing():
    opgeven_storing.destroy()
    global nieuwe_storing

    nieuwe_storing = tk.Toplevel()
    nieuwe_storing.title("Nieuwe Storing invoeren")
    icon = tk.PhotoImage(file="proRail_Logo.png")
    nieuwe_storing.iconphoto(False, icon)

    storing_label = tk.Label(nieuwe_storing, text="Storing:")
    storing_label.pack(pady=5)

    storing_entry = tk.Entry(nieuwe_storing)
    storing_entry.pack(pady=5)

    save_button = tk.Button(nieuwe_storing, text="Opslaan", command=lambda:nieuwe_storing_opslaan(storing_entry.get()))
    save_button.pack(pady=20)
    nieuwe_storing.bind('<Return>', lambda event: nieuwe_storing_opslaan(storing_entry.get()))
    nieuwe_storing.mainloop()

def storing_aanvullen():
    opgeven_storing.destroy()
    storing_aanvullen = tk.Toplevel()

    storing_aanvullen.title("Vul een storing aan")
    icon = tk.PhotoImage(file="proRail_Logo.png")
    storing_aanvullen.iconphoto(False, icon)

    storing_label = tk.Label(storing_aanvullen, text="Storing:")
    storing_label.pack(pady=5)

    storing_entry = tk.Entry(storing_aanvullen)
    storing_entry.pack(pady=5)

    save_button = tk.Button(storing_aanvullen, text="Opslaan", command=lambda:storing_aanvullen_opslaan(storing_entry.get()))
    save_button.pack(pady=20)
    storing_aanvullen.bind('<Return>', lambda event: storing_aanvullen_opslaan(storing_entry.get()))
    storing_aanvullen.mainloop()

def nieuwe_storing_opslaan(storing_informatie):
    with open("storing_Gegevens.txt", "a") as file:
        datum =datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        file.write(f"{storing_informatie}|{datum}\n")
    messagebox.showinfo("Succes", "Storing aangemaakt!")
    nieuwe_storing.destroy()
    # nog aanmaken dat er een entry is voor elke kolom die we gebruiken

def storing_aanvullen_opslaan(storing_informatie):
    with open("storing_Gegevens.txt", "a") as file:
        datum =datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        file.write(f"{storing_informatie}|{datum}\n")
    messagebox.showinfo("Succes", "Storing aangevuld!")
    storing_aanvullen.destroy()
    # nog functie aanmaken dat zorgt dat de storing bijgevuld word ipv dat er een nieuwe storing word aangemaakt