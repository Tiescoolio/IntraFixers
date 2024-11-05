import pickle
import tkinter as tk
from tkinter import messagebox
import datetime
import pandas as pd
import numpy as np
from threading import Thread


def new_disruption():
    global new_disruption_window
    new_disruption_window = tk.Toplevel()
    new_disruption_window.title("Nieuwe Storing invoeren")
    icon = tk.PhotoImage(file="proRail_Logo.png")
    new_disruption_window.iconphoto(False, icon)

    description_label = tk.Label(new_disruption_window, text="Beschrijving van de storing:")
    description_label.pack(pady=5)

    description_entry = tk.Entry(new_disruption_window)
    description_entry.pack(pady=5)

    priority_label = tk.Label(new_disruption_window, text="Prioriteit:")
    priority_label.pack(pady=5)

    priority_entry = tk.Entry(new_disruption_window)
    priority_entry.pack(pady=5)

    cause_code_label = tk.Label(new_disruption_window, text="Oorzaak Code:")
    cause_code_label.pack(pady=5)

    cause_code_entry = tk.Entry(new_disruption_window)
    cause_code_entry.pack(pady=5)

    save_button = tk.Button(new_disruption_window, text="Opslaan", command=lambda: save_new_disruption([priority_entry.get(), cause_code_entry.get()]))
    save_button.pack(pady=20)
    new_disruption_window.bind('<Return>', lambda event: save_new_disruption([priority_entry.get(), cause_code_entry.get(), description_entry.get()]))
    new_disruption_window.mainloop()


def save_new_disruption(disruption_information):
    disruption_information.append(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    disruption_information.append("in proces")
    disruption_information.append(np.NaN)
    new_disruption_information = {
        "stm_prioriteit": float(disruption_information[0]),
        "stm_oorz_code": float(disruption_information[1]),
        "stm_sap_meldtijd": disruption_information[3],
        "status_storing": disruption_information[4],
        "status_storing_aanvulling": disruption_information[5],
        "storing_beschrijving": disruption_information[2]
    }

    df = pd.read_csv("storing_Gegevens_3_features.csv", sep=";")
    df = df._append(new_disruption_information, ignore_index=True)
    df.to_csv("storing_Gegevens_3_features.csv", sep=";", index=False)
    messagebox.showinfo("Succes", "Storing aangemaakt!")
    new_disruption_window.destroy()


    time = disruption_information[3].split(" ")[1]
    time_split = time.split(":")
    total_minutes = (int(time_split[0]) * 60) + int(time_split[1]) + (int(time_split[2]) / 60)
    model_input = [float(disruption_information[0]), float(disruption_information[1]), total_minutes]
    run_model_thread = Thread(target=run_base_model, args=model_input)
    run_model_thread.start()


def update_csv_with_prediction(disruption_input, prediction_result):
    df = pd.read_csv("storing_Gegevens_3_features.csv", sep=";")
    disruption_criteria = (df["stm_sap_meldtijd"] == disruption_input[3])
    wanted_disruption = df[disruption_criteria]
    if not wanted_disruption.empty:
        df.loc[wanted_disruption.index[0], "status_storing"] = prediction_result
        with open("storing_Gegevens_3_features.csv", mode="w", newline="", encoding="utf-8") as file:
            df.to_csv(file, sep=";", index=False)


def run_base_model(storing_input):
    with open("../base_model.pkl", "rb") as file:
        base_model = pickle.load(file)
    prediction_result = base_model.predict(storing_input)
    update_csv_with_prediction(storing_input, prediction_result)
