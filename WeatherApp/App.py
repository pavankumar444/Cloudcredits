import requests
import customtkinter as ctk
from tkinter import messagebox, Toplevel
import threading

class WeatherApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Weather App (India Only)")
        self.root.geometry("500x500")
        self.root.resizable(False, False)
        ctk.set_appearance_mode("System")
        ctk.set_default_color_theme("blue")

        # Title Label
        self.title_label = ctk.CTkLabel(root, text="Weather App (India Only)", font=ctk.CTkFont(size=20, weight="bold"))
        self.title_label.pack(pady=20)

        # City Input
        self.city_label = ctk.CTkLabel(root, text="Enter City:", font=ctk.CTkFont(size=14, weight="bold"))
        self.city_label.pack(pady=5)
        self.city_entry = ctk.CTkEntry(root, font=ctk.CTkFont(size=14))
        self.city_entry.pack(pady=10)

        # Fetch Weather Button
        self.fetch_button = ctk.CTkButton(
            root, text="Fetch Weather", command=self.fetch_weather, font=ctk.CTkFont(size=14, weight="bold")
        )
        self.fetch_button.pack(pady=20)

    def fetch_weather(self):
        api_key = "47a4fa1e66894c9395c63959251501"
        city = self.city_entry.get().strip()

        if not api_key:
            messagebox.showerror("API Key Missing", "Please provide a valid WeatherAPI key.")
            return

        if not city:
            messagebox.showerror("Input Error", "Please enter a city name.")
            return

        try:
            # Default country is India
            location = f"{city},India"
            response = requests.get(
                "http://api.weatherapi.com/v1/forecast.json",
                params={"key": api_key, "q": location, "days": 1}
            )

            if response.status_code == 200:
                weather_data = response.json()
                current_weather = weather_data['current']
                forecast_weather = weather_data['forecast']['forecastday'][0]['day']

                details = {
                    "city": city.capitalize(),
                    "temperature": f"{current_weather['temp_c']}°C",
                    "condition": current_weather['condition']['text'],
                    "min_temp": f"{forecast_weather['mintemp_c']}°C",
                    "max_temp": f"{forecast_weather['maxtemp_c']}°C",
                }

                # Create a new window to show weather results
                self.show_weather_screen(details)
            else:
                error_message = response.json().get("error", {}).get("message", "Unable to fetch weather data.")
                messagebox.showerror("Error", error_message)
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {e}")

    def show_weather_screen(self, details):
        new_window = Toplevel(self.root)
        new_window.title("Weather Details")
        new_window.geometry("500x400")
        new_window.resizable(False, False)
        new_window.configure(bg="#2c2c2c")  # Set background to dark

        # Create labels
        city_label = ctk.CTkLabel(new_window, text="", font=ctk.CTkFont(size=18, weight="bold"), text_color="white")
        temp_label = ctk.CTkLabel(new_window, text="", font=ctk.CTkFont(size=18, weight="bold"), text_color="white")
        condition_label = ctk.CTkLabel(new_window, text="", font=ctk.CTkFont(size=18, weight="bold"), text_color="white")
        min_temp_label = ctk.CTkLabel(new_window, text="", font=ctk.CTkFont(size=18, weight="bold"), text_color="white")
        max_temp_label = ctk.CTkLabel(new_window, text="", font=ctk.CTkFont(size=18, weight="bold"), text_color="white")

        #labels
        city_label.pack(pady=10)
        temp_label.pack(pady=10)
        condition_label.pack(pady=10)
        min_temp_label.pack(pady=10)
        max_temp_label.pack(pady=10)

        # Display information
        self.animate_label(city_label, f"City Name: {details['city']}", 0)
        self.animate_label(temp_label, f"Temperature: {details['temperature']}", 1)
        self.animate_label(condition_label, f"Condition: {details['condition']}", 2)
        self.animate_label(min_temp_label, f"Min Temperature: {details['min_temp']}", 3)
        self.animate_label(max_temp_label, f"Max Temperature: {details['max_temp']}", 4)

    def animate_label(self, label, text, delay):
        # Animation
        def fade_in():
            label.configure(text=text)
        threading.Timer(delay * 0.5, fade_in).start()


if __name__ == "__main__":
    root = ctk.CTk()
    app = WeatherApp(root)
    root.mainloop()
