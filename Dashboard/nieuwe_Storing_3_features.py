import pickle
import tkinter as tk
from tkinter import messagebox
import datetime
import pandas as pd
import numpy as np
from threading import Thread


def nieuwe_storing():
    global nieuwe_storing_window
    nieuwe_storing_window = tk.Toplevel()
    nieuwe_storing_window.title("Nieuwe Storing invoeren")
    icon = tk.PhotoImage(file="proRail_Logo.png")
    nieuwe_storing_window.iconphoto(False, icon)

    beschrijving_label = tk.Label(nieuwe_storing_window, text="Beschrijving van de storing:")
    beschrijving_label.pack(pady=5)

    beschrijving_entry = tk.Entry(nieuwe_storing_window)
    beschrijving_entry.pack(pady=5)

    prioriteit_label = tk.Label(nieuwe_storing_window, text="Prioriteit:")
    prioriteit_label.pack(pady=5)

    prioriteit_entry = tk.Entry(nieuwe_storing_window)
    prioriteit_entry.pack(pady=5)

    orzaak_label = tk.Label(nieuwe_storing_window, text="Oorzaak Code:")
    orzaak_label.pack(pady=5)

    oorzaak_entry = tk.Entry(nieuwe_storing_window)
    oorzaak_entry.pack(pady=5)

    save_button = tk.Button(nieuwe_storing_window, text="Opslaan", command=lambda: nieuwe_storing_opslaan([prioriteit_entry.get(), oorzaak_entry.get()]))
    save_button.pack(pady=20)
    nieuwe_storing_window.bind('<Return>', lambda event: nieuwe_storing_opslaan([prioriteit_entry.get(), oorzaak_entry.get(), beschrijving_entry.get()]))
    nieuwe_storing_window.mainloop()


def nieuwe_storing_opslaan(storing_informatie):
    storing_informatie.append(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    storing_informatie.append("in proces")
    storing_informatie.append(np.NaN)
    nieuwe_storing_informatie = {
        "stm_prioriteit": float(storing_informatie[0]),
        "stm_oorz_code": float(storing_informatie[1]),
        "stm_sap_meldtijd": storing_informatie[3],
        "status_storing": storing_informatie[4],
        "status_storing_aanvulling": storing_informatie[5],
        "storing_beschrijving": storing_informatie[2]
    }

    df = pd.read_csv("storing_Gegevens_3_features.csv", sep=";")
    df = df._append(nieuwe_storing_informatie, ignore_index=True)
    df.to_csv("storing_Gegevens_3_features.csv", sep=";", index=False)
    messagebox.showinfo("Succes", "Storing aangemaakt!")
    nieuwe_storing_window.destroy()


    tijd = storing_informatie[3].split(" ")[1]
    tijd_split = tijd.split(":")
    totaal_minuten = (int(tijd_split[0]) * 60) + int(tijd_split[1]) + (int(tijd_split[2]) / 60)
    model_invoer = [float(storing_informatie[0]), float(storing_informatie[1]), totaal_minuten]
    run_model_thread = Thread(target=run_base_model, args=model_invoer)
    run_model_thread.start()


def update_csv_with_prediction(storing_input, prediction_result):
    df = pd.read_csv("storing_Gegevens_3_features.csv", sep=";")
    criteria_storing = (df["stm_sap_meldtijd"] == storing_input[3])
    gezochte_storing = df[criteria_storing]
    if not gezochte_storing.empty:
        df.loc[gezochte_storing.index[0], "status_storing"] = prediction_result
        with open("storing_Gegevens_3_features.csv", mode="w", newline="", encoding="utf-8") as file:
            df.to_csv(file, sep=";", index=False)


def run_base_model(storing_input):
    with open("base_model.pkl", "rb") as file:
        base_model = pickle.load(file)
    prediction_result = base_model.predict(storing_input)
    update_csv_with_prediction(storing_input, prediction_result)
