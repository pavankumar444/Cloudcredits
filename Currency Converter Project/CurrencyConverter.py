import requests
import customtkinter as ctk
from tkinter import messagebox

class Converter:
    def __init__(self, url):
        try:
            data = requests.get(url).json()
            if "rates" not in data:
                raise ValueError("Invalid API response")
            self.base_currency = data.get("base", "USD")
            self.rates = data["rates"]
            print(f"Exchange rates loaded successfully. Base currency is {self.base_currency}")
        except Exception as e:
            print(f"Error fetching exchange rates: {e}")
            self.rates = {}

    def convert(self, amount, from_currency, to_currency):
        if from_currency not in self.rates or to_currency not in self.rates:
            raise ValueError("Invalid currency selection.")

        if from_currency != self.base_currency:
            amount = amount / self.rates[from_currency]
        amount = round(amount * self.rates[to_currency], 2)
        return amount


class CurrencyConverterApp:
    def __init__(self, root, converter):
        self.converter = converter
        self.root = root
        self.root.title("Currency Converter")
        self.root.geometry("350x450")
        self.root.resizable(False, False)
        ctk.set_appearance_mode("System") 
        ctk.set_default_color_theme("blue")  

        # Title Label
        self.title_label = ctk.CTkLabel(root, text="Currency Converter", font=ctk.CTkFont(size=20, weight="bold"))
        self.title_label.pack(pady=20)

        # Amount Entry
        self.amount_label = ctk.CTkLabel(root, text="Enter Amount:", font=ctk.CTkFont(size=14, weight="bold"))
        self.amount_label.pack(pady=5)
        self.amount_entry = ctk.CTkEntry(root, font=ctk.CTkFont(size=14))
        self.amount_entry.pack(pady=10)

        # From Currency Dropdown
        self.from_label = ctk.CTkLabel(root, text="From Currency:", font=ctk.CTkFont(size=14, weight="bold"))
        self.from_label.pack(pady=5)
        self.from_currency = ctk.CTkComboBox(root, values=list(self.converter.rates.keys()), font=ctk.CTkFont(size=12))
        self.from_currency.pack(pady=10)

        # To Currency Dropdown
        self.to_label = ctk.CTkLabel(root, text="To Currency:", font=ctk.CTkFont(size=14, weight="bold"))
        self.to_label.pack(pady=5)
        self.to_currency = ctk.CTkComboBox(root, values=list(self.converter.rates.keys()), font=ctk.CTkFont(size=12))
        self.to_currency.pack(pady=10)

        # Convert Button
        self.convert_button = ctk.CTkButton(root, text="Convert", command=self.perform_conversion, font=ctk.CTkFont(size=14, weight="bold"))
        self.convert_button.pack(pady=20)

        # Result Label
        self.result_label = ctk.CTkLabel(root, text="", font=ctk.CTkFont(size=16, weight="bold"))
        self.result_label.pack(pady=10)

    def perform_conversion(self):
        try:
            # Get user input
            amount = float(self.amount_entry.get())
            from_currency = self.from_currency.get().upper()
            to_currency = self.to_currency.get().upper()

            # Validate inputs
            if not from_currency or not to_currency:
                raise ValueError("Please select both currencies.")
            if from_currency not in self.converter.rates or to_currency not in self.converter.rates:
                raise ValueError("Invalid currency code.")

            # Perform conversion
            converted_amount = self.converter.convert(amount, from_currency, to_currency)

            # Display result
            self.result_label.configure(text=f"{amount} {from_currency} = {converted_amount} {to_currency}")
        except ValueError as ve:
            messagebox.showerror("Input Error", str(ve))
        except Exception as e:
            messagebox.showerror("Error", str(e))


if __name__ == "__main__":
    url = "https://api.exchangerate-api.com/v4/latest/USD"
    converter = Converter(url)
    if converter.rates:
        root = ctk.CTk()
        app = CurrencyConverterApp(root, converter)
        root.mainloop()