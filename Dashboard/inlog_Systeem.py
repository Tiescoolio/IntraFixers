import tkinter as tk
from tkinter import messagebox
from dashboard_Gui import gui as dashboard
def gui():
    global username_entry
    global password_entry
    global login_window

    # Gegevens van de window opgeven
    login_window = tk.Tk()
    login_window.title("Inlog Systeem")
    login_window.configure(background="#f7d417")
    login_window.geometry("300x250+600+250")

    # Icoon aanmaken voor de window
    icon = tk.PhotoImage(file="proRail_Logo.png")
    login_window.iconphoto(False, icon)

    # Override de toolbar bovenin een window
    login_window.overrideredirect(True)

    # Label en entry aanmaken waar de gebruikersnaam ingevoerd kan worden
    username_label = tk.Label(login_window, text="Gebruikersnaam", background="#f7d417", foreground="#003373",
                              font=("Helvetica", 16, "bold italic"))
    username_label.pack(pady=5)
    username_entry = tk.Entry(login_window)
    username_entry.pack(pady=5)

    # Label en entry aanmaken waar het wachtwoord ingevoerd kan worden
    password_label = tk.Label(login_window, text="Wachtwoord", background="#f7d417", foreground="#003373",
                              font=("Helvetica", 16, "bold italic"))
    password_label.pack(pady=5)
    password_entry = tk.Entry(login_window, show="*")
    password_entry.pack(pady=5)

    # Knop aanmaken voor het inloggen, en deze command ook verbinden met de "enter" toets
    login_button = tk.Button(login_window, text="Inloggen", command=login)
    login_button.pack(pady=10)
    login_window.bind('<Return>', lambda event: login())

    # Knop aanmaken voor het aanmaken van een nieuwe gebruiker
    new_user_button = tk.Button(login_window, text="Nieuwe gebruiker", command=new_user)
    new_user_button.pack(pady=10)

    login_window.mainloop()

def new_user():
    # Pak de inputs van de entries en zet ze in variabelen
    username = username_entry.get()
    password = password_entry.get()

    if not username or not password:
        messagebox.showwarning("Fout", "Vul zowel gebruikersnaam als wachtwoord in!")
        return

    # Zorg dat er niet meerdere gebruikers met dezelfde gebruikersnaam kunnen zijn
    with open("inlog_Gegevens.txt", "r") as file:
        lines = file.readlines()
        for line in lines:
            saved_user, saved_password = line.strip().split(',')
            if saved_user == username:
                messagebox.showwarning("Fout", "Gebruiker bestaat al!")
                return

    # Slaat de nieuwe gebruiker op in de text file
    with open("inlog_Gegevens.txt", "a") as file:
        file.write(f"{username},{password}\n")
    messagebox.showinfo("Succes", "Gebruiker aangemaakt!")
    username_entry.delete(0, tk.END)
    password_entry.delete(0, tk.END)

def login():
    # Pak de inputs van de entries en zet ze in variabelen
    username = username_entry.get()
    password = password_entry.get()

    # Kijkt of het wachtwoord past bij de gebruikersnaam, zo ja word de persoon ingelogd
    with open("inlog_Gegevens.txt", "r") as file:
        lines = file.readlines()
        for line in lines:
            saved_user, saved_password = line.strip().split(',')
            if saved_user == username and saved_password == password:
                messagebox.showinfo("Welkom", f"Inloggen geslaagd, Welkom {saved_user}")
                login_window.destroy()
                dashboard()
                return
    messagebox.showwarning("Fout", "Onjuiste gebruikersnaam of wachtwoord!")

if __name__ == "__main__":
    gui()