import requests
import sqlite3
import tkinter as tk
from tkinter import ttk

api_key = "239fdbdba241e9568631b0cc02966241"

def fetch_and_store_weather_data(city):
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric&lang=en"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        temperature = data["main"]["temp"]
        min_temp = data["main"]["temp_min"]
        max_temp = data["main"]["temp_max"]
        pressure = data["main"]["pressure"]
        humidity = data["main"]["humidity"]
        visibility = data["visibility"]
        weather_main = data["weather"][0]["main"]
        description = data["weather"][0]["description"]
        wind_speed=data["wind"]["speed"]

        conn = sqlite3.connect("weather.db")
        cursor = conn.cursor()
        cursor.execute("CREATE TABLE IF NOT EXISTS weather_app_final (city TEXT, temperature REAL, min_temp REAL, max_temp REAL, pressure INTEGER, humidity INTEGER, visibility INTEGER, weather_main TEXT, description TEXT, wind_speed INTEGER)")
        cursor.execute("INSERT INTO weather_app_final VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", (city, temperature, min_temp, max_temp, pressure, humidity, visibility, weather_main, description, wind_speed))
        conn.commit()
        conn.close()

        #Display the weather data in the UI
        temp_label.config(text=f"Temperature: {temperature} C")
        min_temp_label.config(text=f"Min Temperature: {min_temp} C")
        max_temp_label.config(text=f"Max Temperature: {max_temp} C")
        pressure_label.config(text=f"Pressure: {pressure} hPa")
        humidity_label.config(text=f"Humidity: {humidity} %")
        visibility_label.config(text=f"Visibility: {visibility} m")
        weather_main_label.config(text=f"Weather: {weather_main}")
        desc_label.config(text=f"Description: {description}")
        wind_speed_label.config(text=f"Wind speed: {wind_speed}km/s")
    else:
        #Display an error message in the UI
        error_label.config(text="Failed to fetch weather data.")

def print_database():
    conn = sqlite3.connect("weather.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM weather_app_final")
    rows = cursor.fetchall()
    db_output.config(state=tk.NORMAL) 
    db_output.delete(1.0, tk.END)  
    for row in rows:
        db_output.insert(tk.END, str(row) + '\n')
    db_output.config(state=tk.DISABLED)
    conn.close()

window = tk.Tk()
window.title("Weather App")
window.configure(bg='#87CEEB')

#Create a frame
frame = ttk.Frame(window)
frame.pack(padx=50, pady=40)

city_label = ttk.Label(frame, text="Enter a city name:", font=("Arial", 40, "bold"), foreground='blue')
city_label.grid(column=0, row=0, padx=10)
city_label = ttk.Label(frame, text="Enter a city name:", font=("Arial", 40, "bold"), foreground='blue')
city_label.grid(column=0, row=0, padx=10)

city_entry = ttk.Entry(frame)
city_entry.grid(column=1, row=0, padx=10)

fetch_button = ttk.Button(frame, text="SUBMIT", command=lambda: fetch_and_store_weather_data(city_entry.get()))
fetch_button.grid(column=2, row=0, padx=10)

print_button = ttk.Button(frame, text="PRINT DATABASE", command=print_database)
print_button.grid(column=3, row=0, padx=10)

temp_label = ttk.Label(frame, text="", borderwidth=2, relief="groove", foreground='blue')
temp_label.grid(column=0, row=1, padx=10)
min_temp_label = ttk.Label(frame, text="", borderwidth=2, relief="groove", foreground='blue')
min_temp_label.grid(column=1, row=1, padx=10)
max_temp_label = ttk.Label(frame, text="", borderwidth=2, relief="groove", foreground='blue')
max_temp_label.grid(column=2, row=1, padx=10)
pressure_label = ttk.Label(frame, text="", borderwidth=2, relief="groove", foreground='blue')
pressure_label.grid(column=3, row=1, padx=10)
humidity_label = ttk.Label(frame, text="", borderwidth=2, relief="groove", foreground='blue')
humidity_label.grid(column=0, row=2, padx=10)
visibility_label = ttk.Label(frame, text="", borderwidth=2, relief="groove", foreground='blue')
visibility_label.grid(column=1,row=2,padx=10)
weather_main_label = ttk.Label(frame,text="",borderwidth=2 ,relief="groove",foreground='blue')
weather_main_label.grid(column = 2,row = 2,padx = 10)
desc_label = ttk.Label(frame,text="",borderwidth = 2 ,relief="groove",foreground='blue')
desc_label.grid(column = 3,row = 2,padx = 10)
wind_speed_label = ttk.Label(frame,text="",borderwidth = 2 ,relief="groove",foreground='blue')
wind_speed_label.grid(column = 0,row = 3,padx = 10)

error_label = ttk.Label(window, text="", foreground="red")
error_label.pack()

#label database output
db_output_label = ttk.Label(window, text="The Database Appears Here:", font=("Arial", 20, "bold"))
db_output_label.pack()

#Text widget datatbase output
db_output = tk.Text(window, state="disabled", width=100, height=20)
db_output.pack()

window.mainloop()
