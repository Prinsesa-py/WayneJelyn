import tkinter as tk
from tkinter import messagebox
from tkinter import ttk


class SurprisePlannerGUI(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("EUPHORIA: Feel the Magic of Surprises!")
        self.geometry("900x700")
        self.planner = SurprisePlanner()

        self.configure(bg="black")

        tk.Label(self, text="EUPHORIA: Feel the Magic of Surprises!", font=("Georgia", 16, "bold"), fg="white", bg="black").pack(pady=5)

        main_frame = tk.Frame(self, bg="white")
        main_frame.pack(fill="both", expand=True, padx=10, pady=5)

        
        reservation_frame = tk.Frame(main_frame, bg="white")
        reservation_frame.pack(side="left", fill="y", padx=5)
        tk.Label(reservation_frame, text="Reservation Details", font=("Georgia", 12, "bold"), bg="white").pack(anchor="w", pady=5)

        self.create_input("Name:", self.create_entry("customer_name", reservation_frame), reservation_frame)
        self.create_input("Address:", self.create_entry("customer_address", reservation_frame), reservation_frame)
        self.create_input("Contact:", self.create_entry("customer_contact", reservation_frame), reservation_frame)
        self.create_input("Relationship to the Client:", self.create_entry("relationship", reservation_frame), reservation_frame)
        self.create_input("Client Name:", self.create_entry("client_name", reservation_frame), reservation_frame)
        self.create_dropdown("Event:", self.planner.events, "event_var", reservation_frame)
        self.create_dropdown("Theme:", list(self.planner.themes.keys()), "theme_var", reservation_frame)
        self.create_dropdown("Style:", list(self.planner.styles.keys()), "style_var", reservation_frame)
        self.create_dropdown("Event's Place:", list(self.planner.eventplace.keys()), "place_var", reservation_frame)
        self.create_input("Date and time:", self.create_entry("date", reservation_frame), reservation_frame)

        
        customization_frame = tk.Frame(main_frame, bg="white")
        customization_frame.pack(side="left", fill="y", padx=5)
        tk.Label(customization_frame, text="Customizations", font=("Georgia", 12, "bold"), bg="white").pack(anchor="w", pady=5)

        customization_scroll_frame = tk.Frame(customization_frame, bg="white")
        customization_scroll_frame.pack(fill="both", expand=True, pady=5)

        canvas = tk.Canvas(customization_scroll_frame, bg="white", highlightthickness=0)
        scrollbar = tk.Scrollbar(customization_scroll_frame, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas, bg="white")
        scrollable_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))

        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        for customization, price in self.planner.customizations.items():
            var_name = customization.replace(" ", "_").replace("/", "_").replace("'", "").replace("-", "_")
            var = tk.BooleanVar()
            tk.Checkbutton(
                scrollable_frame,
                text=f"{customization} (₱{price:,})",
                variable=var,
                bg="white",
                anchor="w"
            ).pack(fill="x", pady=2)
            setattr(self, f"customization_{var_name}", var)

        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        
        receipt_frame = tk.Frame(main_frame, bg="white")
        receipt_frame.pack(side="left", fill="both", padx=5)

        tk.Label(receipt_frame, text="Receipt", font=("Arial", 12, "bold"), bg="white").pack(anchor="w", pady=5)
        self.receipt_text = tk.Text(receipt_frame, height=15, wrap="word", bg="white", fg="black", font=("Courier", 10))
        self.receipt_text.pack(fill="both", expand=True, padx=5, pady=5)

        
        tk.Button(self, text="Submit", command=self.make_reservation, bg="green", fg="white").pack(pady=10)

    def create_input(self, label, widget, parent):
        tk.Label(parent, text=label, bg="white", fg="blue").pack(anchor="w", pady=2)
        widget.pack(fill="x", pady=2)

    def create_entry(self, var_name, parent):
        entry = tk.Entry(parent, bg="white", fg="black")
        setattr(self, var_name, entry)
        return entry

    def create_dropdown(self, label, values, var_name, parent):
        tk.Label(parent, text=label, bg="white", fg="blue").pack(anchor="w", pady=2)
        combo_var = tk.StringVar()
        combo_box = ttk.Combobox(parent, values=values, textvariable=combo_var, state="readonly")
        combo_box.pack(fill="x", pady=2)
        setattr(self, var_name, combo_var)

    def make_reservation(self):
        customer_name = self.customer_name.get()
        customer_address = self.customer_address.get()
        customer_contact = self.customer_contact.get()
        relationship = self.relationship.get()
        client_name = self.client_name.get()
        event = self.event_var.get()
        theme = self.theme_var.get()
        style = self.style_var.get()
        place = self.place_var.get()
        date = self.date.get()

        if not all([customer_name, customer_address, customer_contact, relationship, client_name, event, theme, style, place, date]):
            messagebox.showerror("Error", "Do Not Leave Empty Spaces!")
            return

        total_price = (
            self.planner.event_prices[event] +
            self.planner.themes[theme] +
            self.planner.styles[style] +
            self.planner.eventplace[place]
        )

        selected_customizations = []
        for customization, price in self.planner.customizations.items():
            var_name = customization.replace(" ", "_").replace("/", "_").replace("'", "").replace("-", "_")
            var = getattr(self, f"customization_{var_name}")
            if var.get():
                total_price += price
                selected_customizations.append(customization)

        self.receipt_text.delete("1.0", tk.END)
        self.receipt_text.insert(
            tk.END,
            f"Receipt:\n"
            f"Customer: {customer_name}\n"
            f"Client: {client_name}\n"
            f"Event: {event}\n"
            f"Theme: {theme}\n"
            f"Style: {style}\n"
            f"Event Place: {place}\n"
            f"Date and Time: {date}\n"
            f"Customizations: {', '.join(selected_customizations) if selected_customizations else 'None'}\n"
            f"Total Price: ₱{total_price:,}\n"
        )


class SurprisePlanner:
    def __init__(self):
        self.events = [
            "Birthday Party",
            "Wedding Anniversary",
            "Anniversary",
            "Graduation Party",
            "Valentines",
            "Marriage Proposal",
            "Gender Reveal",
            "Mother's Day",
            "Father's Day",
            "Teacher's Day",
        ]
        self.event_prices = {event: 1000 for event in self.events}
        self.themes = {
            "Aesthetic": 5000,
            "Modern": 6000,
            "Gold": 4000,
            "Elegant": 7500,
            "Red/Black": 3000,
            "Pink/Blue": 3000,
            "I want to Customize": 0,
        }
        self.styles = {
            "Casual": 5000,
            "Formal": 10000,
            "Themed Costume": 15000,
        }
        self.customizations = {
            "I have already chose the Theme": 0,
            "Silver/Black Balloons": 100,
            "Purple Balloons": 100,
            "Gold/Silver Balloons": 100,
            "Rainbow Balloons": 100,
            "Number Foil Balloon": 100,
            "Confetti": 50,
            "Cake (Single Layer)": 700,
            "Cake (Multi-Layer)": 1400,
            "Money Bouquet (You'll provide the bills)": 500,
            "Chocolate Bouquet": 1200,
            "Rose Bouquet": 1500,
            "Tulips Bouquet": 1500,
            "Boy or Girl Banner": 100,
            "Happy Birthday Banner": 100,
            "Happy Anniversary Banner": 100,
            "Congratulations Banner": 100,
            "I Love You Banner": 100,
            "Small Size Teddy Bear": 500,
            "Human Size Teddy Bear": 1000,
            "Polaroid Photos (20 pcs)": 200,
            "Polaroid Photos (50 pcs)": 300,
            "Polaroid Photos (100 pcs)": 1000,
            "Will you Marry Me? Banner": 100,
        }
        self.eventplace = {
            "Car Surprise": 2000,
            "Event Hall (near your place)": 5000,
        }


if __name__ == "__main__":
    app = SurprisePlannerGUI()
    app.mainloop()
