import requests
import tkinter as tk
import datetime
from nieuwe_Storing import new_disruption as ns
import pandas as pd


def gui():
    global time_label
    global weather_label
    global disruptions

    # Gegevens van de window opgeven
    dashboard_window = tk.Tk()
    dashboard_window.title("Dashboard")
    dashboard_window.geometry("800x600")
    dashboard_window.configure(background="#f0f0f0")
    dashboard_window.attributes('-fullscreen', True)

    # Icoon aanmaken voor de window
    icon = tk.PhotoImage(file="proRail_Logo.png")
    dashboard_window.iconphoto(False, icon)

    # Label aanmaken voor de storingen
    disruptions = tk.Label(dashboard_window, text="", background="#f0f0f0", foreground="#003373",
                              font=("Helvetica", 16, "bold italic"))
    disruptions.pack(pady=60)

    # Label aanmaken voor de tijd
    time_label = tk.Label(dashboard_window, background="#f0f0f0", foreground="#003373",
                              font=("Helvetica", 16, "bold italic"))
    time_label.pack(pady=20)

    # Label aanmaken voor het weer
    weather_label = tk.Label(dashboard_window, text="", background="#f0f0f0", foreground="#003373",
                              font=("Helvetica", 16, "bold italic"))
    weather_label.pack(pady=20)

    # Knop aanmaken om een storing in te voeren
    new_disruption = tk.Button(dashboard_window, text="Storing Invoeren", command=ns,
                               background="#CC0033", foreground="#FFFFFF",
                               activebackground="#880000", font=("Helvetica", 16, "bold italic"))
    new_disruption.pack(pady=20)

    # Update de tijd, weer en storing labels herhalend
    update_time()
    update_weatherinformation()
    update_disruptions()

    dashboard_window.mainloop()

def update_time():
    # Update de tijd label om de 0.2 seconden met de nieuwe tijd
    time = datetime.datetime.now().strftime("%H:%M:%S")
    time_label.config(text=time)
    time_label.after(200, update_time)


def update_weatherinformation():
    # Update het weer label om de minuut met het weer, met de HU als locatie
    latitude = 52.0990
    longitude = 5.1091
    api = "811567671a6186280e165c81ca4f0c93"
    url = f"https://api.openweathermap.org/data/2.5/weather?lat={latitude}&lon={longitude}&appid={api}&lang=nl&units=metric"
    response = requests.get(url)
    data = response.json()

    temperature = data["main"]["temp"]
    min_temperature = data['main']["temp_min"]
    max_temperature = data["main"]["temp_max"]
    weather = data['weather'][0]['description']

    weather_label.config(text=f"Temperatuur: {temperature} Graden Celsius\n"
                                    f"Minimale Temperatuur: {min_temperature} Graden Celsius\n"
                                    f"Maximale Temperatuur: {max_temperature} Graden Celsius\n"
                                    f"Weer: {weather}")
    weather_label.after(60000, update_weatherinformation)


def update_disruptions():
    # Update de storingen label om de 5 seconden met de laatste 3 storingen uit het bestand
    df = pd.read_csv("storing_Gegevens.csv", sep=";")
    display_disruptions = df.tail(3)
    disruption_display_text = ""
    if not display_disruptions.empty:
        for _, disruption in display_disruptions.iterrows():
            if disruption["status_storing"] == "in proces":
                addon = ""
            else:
                addon = "minuten"
            disruption_display_text += f"Storing: {disruption['storing_beschrijving']}\n"
            disruption_display_text += f"Prioriteitscode: {disruption['stm_prioriteit']}\n"
            disruption_display_text += f"Meldtijd: {disruption['melding_datum']}\n"
            disruption_display_text += f"Tijd Schatting: {disruption['status_storing']} {addon}\n\n"
    else:
        disruption_display_text = "Er zijn momenteel geen storingen om te tonen"
    disruptions.config(text=disruption_display_text.strip())
    disruptions.after(5000, update_disruptions)


if __name__ == "__main__":
    gui()
