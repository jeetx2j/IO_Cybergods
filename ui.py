import tkinter as tk
from tkinter import messagebox
import os
import time
import sys

class EternityGUI:
    def __init__(self, master):
        self.master = master
        master.title("ETERNITY: An Automated M.L based Industrial Maintenance Toolkit")
        master.geometry("800x600")

        # Create header frame
        self.header_frame = tk.Frame(master, bg="#333")
        self.header_frame.pack(fill="x")

        # Create header widgets
        self.header_label = tk.Label(self.header_frame, text="ETERNITY", font=("Arial", 24), fg="#fff", bg="#333")
        self.header_label.pack(side="left", padx=10)

        # Create content frame
        self.content_frame = tk.Frame(master, bg="#f0f0f0")
        self.content_frame.pack(fill="both", expand=True)

        # Create content widgets
        self.content_label = tk.Label(self.content_frame, text="Welcome to ETERNITY!", font=("Arial", 18), fg="#333")
        self.content_label.pack(pady=20)

        # Create option frame
        self.option_frame = tk.Frame(self.content_frame, bg="#f0f0f0")
        self.option_frame.pack(fill="x", pady=20)

        self.option_labels = []
        for i, option in enumerate(["Check Health", "Check Mentainance", "Check DisasterManagement", "Firewall", "Exit Tool"]):
            label = tk.Label(self.option_frame, text=f"[{i+1}] {option}", font=("Arial", 14), fg="#333")
            label.pack(side="left", padx=10)
            self.option_labels.append(label)

        # Create entry frame
        self.entry_frame = tk.Frame(self.content_frame, bg="#f0f0f0")
        self.entry_frame.pack(fill="x", pady=20)

        self.entry_label = tk.Label(self.entry_frame, text="Choose an option:", font=("Arial", 14), fg="#333")
        self.entry_label.pack(side="left", padx=10)

        self.entry = tk.Entry(self.entry_frame, width=20, font=("Arial", 14))
        self.entry.pack(side="left", padx=10)

        self.submit_button = tk.Button(self.entry_frame, text="Submit", command=self.submit_option)
        self.submit_button.pack(side="left", padx=10)

    def submit_option(self):
        option = self.entry.get()
        if option == "1":
            os.system("python3 /home/cybergod/Documents/hacathonsmartodisha/healthworker.py")
        elif option == "2":
            os.system("/home/cybergod/Documents/hacathonsmartodisha/mentainancesystem.py")
        elif option == "3":
            os.system("/home/cybergod/Documents/hacathonsmartodisha/disastertwin.py")
        elif option == "4":
            os.system("/home/cybergod/Documents/hacathonsmartodisha/firewall/firewall.py")
        elif option == "00":
            if messagebox.askyesno("Exit", "Are you sure you want to exit?"):
                self.master.destroy()
        else:
            messagebox.showerror("Invalid option", "Please choose a valid option.")

root = tk.Tk()
my_gui = EternityGUI(root)
root.mainloop()