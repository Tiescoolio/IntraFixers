import requests
import tkinter as tk
import datetime
from nieuwe_Storing_3_features import nieuwe_storing as ns

def gui():
    global tijd_label
    global weer_informatie
    global storingen

    window = tk.Tk()
    window.title("Dashboard")
    window.geometry("800x600")
    window.configure(background="#f7d417")
    window.attributes('-fullscreen', True)

    icon = tk.PhotoImage(file="proRail_Logo.png")
    window.iconphoto(False, icon)

    storingen = tk.Label(window, text="", background="#f7d417", foreground="#003373",
                                     font=("Helvetica", 16, "bold italic"))
    storingen.pack(pady=60)

    tijd_label = tk.Label(window, font=("Helvetica", 24), background="#f7d417", foreground="#003373")
    tijd_label.pack(pady=20)

    weer_informatie = tk.Label(window, text="", background="#f7d417", foreground="#003373",
                                      font=("Helvetica", 16, "bold italic"))
    weer_informatie.pack(pady=20)

    nieuwe_storing = tk.Button(window, text="Storing Invoeren", command=ns)
    nieuwe_storing.pack(pady=20)

    update_tijd()
    update_weerinformatie()
    update_storingen()

    window.mainloop()

def update_tijd():
    tijd = datetime.datetime.now().strftime("%H:%M:%S")
    tijd_label.config(text=tijd)
    tijd_label.after(200, update_tijd)

def update_weerinformatie():
    lattitude = 52.0990
    longitude = 5.1091
    api = "811567671a6186280e165c81ca4f0c93"
    url = f"https://api.openweathermap.org/data/2.5/weather?lat={lattitude}&lon={longitude}&appid={api}&lang=nl&units=metric"
    response = requests.get(url)
    data = response.json()

    temperatuur = data["main"]["temp"]
    min_temperatuur = data['main']["temp_min"]
    max_temperatuur = data["main"]["temp_max"]
    weer = data['weather'][0]['description']

    weer_informatie.config(text=f"Temperatuur: {temperatuur} Graden Celsius\n"
                                         f"Minimale Temperatuur: {min_temperatuur} Graden Celsius\n"
                                         f"Maximale Temperatuur: {max_temperatuur} Graden Celsius\n"
                                         f"Weer: {weer}")
    weer_informatie.after(60000, update_weerinformatie)

def update_storingen():
    with open("storing_Gegevens.txt", "r") as bestand:
        lijnen = bestand.readlines()
        laatste_drie = lijnen[-3:] if len(lijnen) > 3 else lijnen
        storing_text = '\n'.join(regel.strip() for regel in laatste_drie)
        storing_weergave_text = ""
        if storing_text:
            regels = storing_text.split("\n")
            for regel in regels:
                storing_informatie, storing_tijd = regel.split("|", 1)
                storing_weergave_text += f"{storing_informatie.strip()}\n{storing_tijd.strip()}\n\n\n"
        else:
            storing_weergave_text = "Er zijn momenteel geen storingen"
    storingen.config(text=storing_weergave_text.strip())
    storingen.after(5000, update_storingen)


if __name__ == "__main__":
    gui()