import tkinter as tk
from tkinter import messagebox
from dashboard_Gui import gui as dashboard
def gui():
    global gebruikersnaam_entry
    global wachtwoord_entry
    global inlog

    inlog = tk.Tk()
    inlog.title("Inlog Systeem")
    inlog.geometry("300x250+600+250")

    icon = tk.PhotoImage(file="proRail_Logo.png")
    inlog.iconphoto(False, icon)

    inlog.overrideredirect(True)

    gebruikersnaam_label = tk.Label(inlog, text="Gebruikersnaam")
    gebruikersnaam_label.pack(pady=5)
    gebruikersnaam_entry = tk.Entry(inlog)
    gebruikersnaam_entry.pack(pady=5)

    wachtwoord_label = tk.Label(inlog, text="Wachtwoord")
    wachtwoord_label.pack(pady=5)
    wachtwoord_entry = tk.Entry(inlog, show="*")
    wachtwoord_entry.pack(pady=5)

    inlog_knop = tk.Button(inlog, text="Inloggen", command=inloggen)
    inlog_knop.pack(pady=10)
    inlog.bind('<Return>', lambda event: inloggen())

    nieuwe_gebruiker_knop = tk.Button(inlog, text="Nieuwe gebruiker", command=nieuwe_gebruiker)
    nieuwe_gebruiker_knop.pack(pady=10)

    inlog.mainloop()

def nieuwe_gebruiker():
    gebruikersnaam = gebruikersnaam_entry.get()
    wachtwoord = wachtwoord_entry.get()

    if not gebruikersnaam or not wachtwoord:
        messagebox.showwarning("Fout", "Vul zowel gebruikersnaam als wachtwoord in!")
        return


    with open("inlog_Gegevens.txt", "r") as bestand:
        lijnen = bestand.readlines()
        for lijn in lijnen:
            opgeslagen_gebruiker, opgeslagen_wachtwoord = lijn.strip().split(',')
            if opgeslagen_gebruiker == gebruikersnaam:
                messagebox.showwarning("Fout", "Gebruiker bestaat al!")
                return

    with open("inlog_Gegevens.txt", "a") as file:
        file.write(f"{gebruikersnaam},{wachtwoord}\n")
    messagebox.showinfo("Succes", "Gebruiker aangemaakt!")
    gebruikersnaam_entry.delete(0, tk.END)
    wachtwoord_entry.delete(0, tk.END)

def inloggen():
    gebruikersnaam = gebruikersnaam_entry.get()
    wachtwoord = wachtwoord_entry.get()

    with open("inlog_Gegevens.txt", "r") as file:
        lijnen = file.readlines()
        for lijn in lijnen:
            opgeslagen_gebruiker, opgeslagen_wachtwoord = lijn.strip().split(',')
            if opgeslagen_gebruiker == gebruikersnaam and opgeslagen_wachtwoord == wachtwoord:
                messagebox.showinfo("Welkom", f"Inloggen geslaagd, Welkom {opgeslagen_gebruiker}")
                inlog.destroy()
                dashboard()
                return
    messagebox.showwarning("Fout", "Onjuiste gebruikersnaam of wachtwoord!")

if __name__ == "__main__":
    gui()