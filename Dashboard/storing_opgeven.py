import tkinter as tk
from tkinter import messagebox
import datetime
import pandas as pd
import numpy as np


def storing_opgeven():
    global opgeven_storing
    opgeven_storing = tk.Toplevel()

    opgeven_storing.title("Nieuwe storing of oude storing aanvullen")
    icon = tk.PhotoImage(file="proRail_Logo.png")
    opgeven_storing.iconphoto(False, icon)

    storing_opgeven_label = tk.Label(opgeven_storing,
                                     text="Wilt u een nieuwe storing aanmaken of een oude storing aanvullen?")
    storing_opgeven_label.pack(pady=5)

    nieuwe_storing_knop = tk.Button(opgeven_storing, text="Nieuwe storing aanmaken", command=nieuwe_storing)
    nieuwe_storing_knop.pack(pady=10)

    oude_storing_aanvullen = tk.Button(opgeven_storing, text="Oude storing aanvullen", command=storing_aanvullen)
    oude_storing_aanvullen.pack(pady=10)
    opgeven_storing.mainloop()


def nieuwe_storing():
    opgeven_storing.destroy()
    global nieuwe_storing_window

    nieuwe_storing_window = tk.Toplevel()
    nieuwe_storing_window.title("Nieuwe Storing invoeren")
    icon = tk.PhotoImage(file="proRail_Logo.png")
    nieuwe_storing_window.iconphoto(False, icon)

    prioriteit_label = tk.Label(nieuwe_storing_window, text="Prioriteit:")
    prioriteit_label.pack(pady=5)

    prioriteit_entry = tk.Entry(nieuwe_storing_window)
    prioriteit_entry.pack(pady=5)

    orzaak_label = tk.Label(nieuwe_storing_window, text="Oorzaak Code:")
    orzaak_label.pack(pady=5)

    oorzaak_entry = tk.Entry(nieuwe_storing_window)
    oorzaak_entry.pack(pady=5)

    save_button = tk.Button(nieuwe_storing_window, text="Opslaan",
                            command=lambda: nieuwe_storing_opslaan([prioriteit_entry.get(), oorzaak_entry.get()]))
    save_button.pack(pady=20)
    nieuwe_storing_window.bind('<Return>',
                               lambda event: nieuwe_storing_opslaan([prioriteit_entry.get(), oorzaak_entry.get()]))
    nieuwe_storing_window.mainloop()


def storing_aanvullen():
    opgeven_storing.destroy()
    global storing_aanvullen_window
    storing_aanvullen_window = tk.Toplevel()

    storing_aanvullen_window.title("Vul een storing aan")
    icon = tk.PhotoImage(file="proRail_Logo.png")
    storing_aanvullen_window.iconphoto(False, icon)

    storing_label = tk.Label(storing_aanvullen_window, text="Storing:")
    storing_label.pack(pady=5)

    storing_entry = tk.Entry(storing_aanvullen_window)
    storing_entry.pack(pady=5)

    save_button = tk.Button(storing_aanvullen_window, text="Opslaan",
                            command=lambda: storing_aanvullen_opslaan(storing_entry.get()))
    save_button.pack(pady=20)
    storing_aanvullen_window.bind('<Return>', lambda event: storing_aanvullen_opslaan(storing_entry.get()))
    storing_aanvullen_window.mainloop()


def nieuwe_storing_opslaan(storing_informatie):
    storing_informatie.append(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    storing_informatie.append("in proces")
    storing_informatie.append(np.NaN)
    nieuwe_storing = {"stm_prioriteit": storing_informatie[0], "stm_oorz_code": storing_informatie[1],
                      "stm_sap_meldtijd": storing_informatie[2], "status_storing": storing_informatie[3],
                      "status_storing_aanvulling": storing_informatie[4]}
    df = pd.read_csv("storing_Gegevens_3_features.csv", sep=";")
    df = df._append(nieuwe_storing, ignore_index=True)
    df.to_csv("storing_Gegevens_3_features.csv", sep=";", index=False)
    messagebox.showinfo("Succes", "Storing aangemaakt!")
    nieuwe_storing_window.destroy()


def storing_aanvullen_opslaan(storing_informatie):
    # with open("storing_Gegevens.txt", "r") as file:
    #     lijnen = file.readlines()
    #     for lijn in lijnen:
    #         telling = 0
    #         for i in range(8):
    #             if lijn[i] == storing_informatie[i] or lijn[i] == "x" :
    #                 zorgen dat hier code staat dat de regel uit de text file haalt, en alle informatie die er van de een staat en ander niet in een nieuwe regel komt, vice versa
    #
    #             else:
    #                 break

    with open("storing_Gegevens.txt", "a") as file:
        datum = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        file.write(f"{storing_informatie}|{datum}\n")
    messagebox.showinfo("Succes", "Storing aangevuld!")
    storing_aanvullen_window.destroy()
    # nog functie aanmaken dat zorgt dat de storing bijgevuld word ipv dat er een nieuwe storing word aangemaakt