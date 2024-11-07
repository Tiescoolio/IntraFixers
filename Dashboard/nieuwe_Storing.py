import pickle
import tkinter as tk
from tkinter import messagebox
import time
import pandas as pd
from threading import Thread
import csv
import datetime
from tkcalendar import Calendar


def new_disruption():
    global new_disruption_window
    new_disruption_window = tk.Toplevel()
    new_disruption_window.title("Nieuwe Storing invoeren")
    new_disruption_window.configure(background="#f0f0f0")
    new_disruption_window.geometry("+150+0")
    icon = tk.PhotoImage(file="proRail_Logo.png")
    new_disruption_window.iconphoto(False, icon)

    info = [
        ("Beschrijving van de storing:", "storing_beschrijving"),
        ("Prioriteit:", "stm_prioriteit"),
        ("Oorzaak Code:", "stm_oorz_code"),
        ("Geografische locatie melding:", "stm_geo_mld"),
        ("Oorzaak Groep:", "stm_oorz_groep"),
        ("Contractgebied aannnemer:", "stm_contractgeb_gst"),
        ("Techniekveld melding:", "stm_techn_gst"),
        ("Prognose aannemer functiehersteltijd:", "stm_progfh_in_duur"),
        ("Fh Status:", "stm_fh_status")
    ]

    # Dictionary om entries te bewaren
    entries = {}

    # Dynamisch labels en invoervelden aanmaken
    for label_text, entry_key in info:
        label = tk.Label(new_disruption_window, text=label_text, background="#FFFFFF", foreground="#003373",
                         font=("Helvetica", 14, "bold italic"))
        label.pack(pady=5)

        entry = tk.Entry(new_disruption_window, font=("Helvetica", 14, "bold italic"), borderwidth=0,
                         highlightthickness=0)
        entry.pack(pady=5)

        entries[entry_key] = entry

    declaration_date_label = tk.Label(new_disruption_window, text="Aangifte datum:", background="#FFFFFF",
                                      foreground="#003373", font=("Helvetica", 14, "bold italic"))
    declaration_date_label.pack(pady=5)

    def select_date():
        global declaration_date_seconds
        # Roep open_calendar aan om de tijd in seconden te krijgen
        declaration_date_seconds = open_calendar()
        print(declaration_date_seconds)

    calendar_button = tk.Button(new_disruption_window, text="Selecteer Datum en Tijd",
                                command=select_date, background="#003373",
                                foreground="#FFFFFF", font=("Helvetica", 14, "bold italic"))
    calendar_button.pack(pady=10)
    save_button = tk.Button(new_disruption_window, text="Opslaan", command=lambda: save_new_disruption(entries, declaration_date_seconds),
                            background="#CC0033", foreground="#FFFFFF", activebackground="#880000",
                            font=("Helvetica", 14, "bold italic"))
    save_button.pack(pady=20)
    new_disruption_window.bind('<Return>', lambda event: save_new_disruption(entries, declaration_date_seconds))

    new_disruption_window.mainloop()


def save_new_disruption(disruption_information, declaration_date):
    disruption_information_keys = {key: entry.get() for key, entry in disruption_information.items()}
    oorz_groep_mapping = {
        "ONR-DERD": 0,
        "ONR-RIB": 1,
        "TECHONV": 2,
        "WEER": 3
    }
    if disruption_information_keys["stm_oorz_groep"] in oorz_groep_mapping:
        disruption_information["stm_oorz_groep"] = oorz_groep_mapping[disruption_information_keys["stm_oorz_groep"]]
    else:
        messagebox.showwarning("Ongeldige invoer",
                               "Vul een geldige waarde in voor Oorzaak Groep: 'ONR-DERD', 'WEER', 'ONR-RIB' of 'TECHONV'")
        return

    tijd = datetime.datetime.now()

    disruption_information["stm_sap_meld_ddt"] = int(time.time())
    disruption_information["melding_datum"] = tijd.strftime("%Y-%m-%d %H:%M:%S")
    disruption_information["status_storing"] = "in proces"
    disruption_information["stm_aanngeb_dd"] = declaration_date

    csv_data = {
        "storing_beschrijving": disruption_information["storing_beschrijving"].get(),
        "stm_prioriteit": disruption_information["stm_prioriteit"].get(),
        "stm_oorz_code": disruption_information["stm_oorz_code"].get(),
        "stm_sap_meld_ddt": disruption_information["stm_sap_meld_ddt"],
        "stm_geo_mld": disruption_information["stm_geo_mld"].get(),
        "stm_aanngeb_dd": disruption_information["stm_aanngeb_dd"],
        "stm_oorz_groep": disruption_information["stm_oorz_groep"],
        "stm_contractgeb_gst": disruption_information["stm_contractgeb_gst"].get(),
        "stm_techn_gst": disruption_information["stm_techn_gst"].get(),
        "stm_progfh_in_duur": disruption_information["stm_progfh_in_duur"].get(),
        "stm_fh_status": disruption_information["stm_fh_status"].get(),
        "status_storing": disruption_information["status_storing"],
        "melding_datum": disruption_information["melding_datum"]
    }

    with open("storing_Gegevens.csv", "a", newline='', encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=csv_data.keys(), delimiter=";")
        if file.tell() == 0:
            writer.writeheader()
        writer.writerow(csv_data)

    run_model_thread = Thread(target=run_base_model, args=(disruption_information,))
    run_model_thread.start()

    messagebox.showwarning("Succes!", "Storing succesvol opgeslagen")
    new_disruption_window.destroy()


def update_csv_with_prediction(disruption_input, prediction_result):
    df = pd.read_csv("storing_Gegevens.csv", sep=";")
    disruption_criteria = (df["stm_sap_meld_ddt"] == disruption_input["stm_sap_meld_ddt"])
    wanted_disruption = df[disruption_criteria]
    if not wanted_disruption.empty:
        df.loc[wanted_disruption.index[0], "status_storing"] = prediction_result
        with open("storing_Gegevens.csv", mode="w", newline="", encoding="utf-8") as file:
            df.to_csv(file, sep=";", index=False)


def run_base_model(disruption_input):
    input_data = {
        key: entry.get() if isinstance(entry, tk.Entry) else entry
        for key, entry in disruption_input.items()
    }

    used_input_data = {
        "stm_sap_meld_ddt": input_data["stm_sap_meld_ddt"],
        "stm_geo_mld": input_data["stm_geo_mld"],
        "stm_prioriteit": input_data["stm_prioriteit"],
        "stm_aanngeb_dd": input_data["stm_aanngeb_dd"],
        "stm_oorz_groep": input_data["stm_oorz_groep"],
        "stm_oorz_code": input_data["stm_oorz_code"],
        "stm_contractgeb_gst": input_data["stm_contractgeb_gst"],
        "stm_techn_gst": input_data["stm_techn_gst"],
        "stm_progfh_in_duur": input_data["stm_progfh_in_duur"],
        "stm_fh_status": input_data["stm_fh_status"]
    }

    with open("../model.pkl", "rb") as file:
        loaded_model = pickle.load(file)
    model = loaded_model.get("model")

    used_input_df = pd.DataFrame([used_input_data])
    input_df_dummies = pd.get_dummies(used_input_df)
    model_columns = model.feature_names_in_
    input_df_dummies = input_df_dummies.reindex(columns=model_columns, fill_value=0)

    prediction_result = model.predict(input_df_dummies)
    rmse = loaded_model.get("rmse")

    min_estimate = prediction_result - (rmse / 2)
    max_estimate = prediction_result + (rmse / 2)
    time_estimate = f"{int(min_estimate)}-{int(max_estimate)}"
    update_csv_with_prediction(input_data, time_estimate)


def open_calendar():
    # Nieuwe window om de kalender te tonen
    calendar_window = tk.Toplevel()
    calendar_window.title("Selecteer Datum en Tijd")
    calendar_window.geometry("+200+100")

    # Kalender widget
    cal = Calendar(calendar_window, selectmode="day", year=2023, month=11, day=7)
    cal.pack(pady=10)

    # Tijd invoer voor uur en minuten
    time_frame = tk.Frame(calendar_window)
    time_frame.pack(pady=10)

    hour_var = tk.IntVar(value=0)
    minute_var = tk.IntVar(value=0)

    hour_label = tk.Label(time_frame, text="Uur:")
    hour_label.grid(row=0, column=0)
    hour_entry = tk.Spinbox(time_frame, from_=0, to=23, textvariable=hour_var, width=5)
    hour_entry.grid(row=0, column=1)

    minute_label = tk.Label(time_frame, text="Minuten:")
    minute_label.grid(row=0, column=2)
    minute_entry = tk.Spinbox(time_frame, from_=0, to=59, textvariable=minute_var, width=5)
    minute_entry.grid(row=0, column=3)

    # Variabele om de gekozen datum in seconden op te slaan
    selected_timestamp = tk.IntVar(value=0)

    def save_date_time():
        # Datum en tijd uit de widgets halen
        selected_date = cal.get_date()
        selected_hour = hour_var.get()
        selected_minute = minute_var.get()

        # Omzetten naar datetime object
        date_time_str = f"{selected_date} {selected_hour}:{selected_minute}"
        date_time_obj = datetime.datetime.strptime(date_time_str, "%m/%d/%y %H:%M")

        # Omzetten naar seconden sinds 1970
        selected_timestamp.set(int(date_time_obj.timestamp()))
        calendar_window.destroy()

    # Opslaan knop om de datum en tijd in entries te zetten
    save_button = tk.Button(calendar_window, text="Opslaan", command=save_date_time)
    save_button.pack(pady=10)

    # Wacht totdat het kalender venster is gesloten, dan geef de timestamp terug
    calendar_window.wait_window()
    return selected_timestamp.get()
