import tkinter as tk
from tkinter import messagebox
import datetime
import pandas as pd
import numpy as np


def nieuwe_storing():
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

    save_button = tk.Button(nieuwe_storing_window, text="Opslaan", command=lambda:nieuwe_storing_opslaan([prioriteit_entry.get(), oorzaak_entry.get()]))
    save_button.pack(pady=20)
    nieuwe_storing_window.bind('<Return>', lambda event: nieuwe_storing_opslaan([prioriteit_entry.get(), oorzaak_entry.get()]))
    nieuwe_storing_window.mainloop()

def nieuwe_storing_opslaan(storing_informatie):
    storing_informatie.append(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    storing_informatie.append("in proces")
    storing_informatie.append(np.NaN)
    nieuwe_storing = {"stm_prioriteit":storing_informatie[0] , "stm_oorz_code": storing_informatie[1] , "stm_sap_meldtijd": storing_informatie[2], "status_storing": storing_informatie[3], "status_storing_aanvulling": storing_informatie[4]}
    df = pd.read_csv("storing_Gegevens_3_features.csv", sep=";")
    df = df._append(nieuwe_storing, ignore_index=True)
    df.to_csv("storing_Gegevens_3_features.csv", sep=";", index=False)
    messagebox.showinfo("Succes", "Storing aangemaakt!")
    nieuwe_storing_window.destroy()
