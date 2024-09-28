from scapy.all import *
import threading
import time
import tkinter as tk
from tkinter import scrolledtext
class NetworkListener:
    def __init__(self):
        self.sniffing = False
        self.root = tk.Tk()
        self.root.title("Network Listener")
        self.text_box = scrolledtext.ScrolledText(self.root, width=80, height=20)
        self.text_box.pack()
        self.start_button = tk.Button(self.root, text="Start Sniffing", command=self.start_sniffing)
        self.start_button.pack()
        self.stop_button = tk.Button(self.root, text="Stop Sniffing", command=self.stop_sniffing)
        self.stop_button.pack()

    def start_sniffing(self):
        self.sniffing = True
        sniff_thread = threading.Thread(target=self.sniff_packets)
        sniff_thread.start()

    def stop_sniffing(self):
        self.sniffing = False

    def sniff_packets(self):
        sniff(prn=self.process_packet, store=False)

    def process_packet(self, packet):
        if packet.haslayer(IP):
            src_ip = packet[IP].src
            dst_ip = packet[IP].dst
            protocol = packet[IP].proto

            if packet.haslayer(TCP):
                src_port = packet[TCP].sport
                dst_port = packet[TCP].dport
                self.text_box.insert(tk.END, f"TCP packet from {src_ip}:{src_port} to {dst_ip}:{dst_port}\n")
            elif packet.haslayer(UDP):
                src_port = packet[UDP].sport
                dst_port = packet[UDP].dport
                self.text_box.insert(tk.END, f"UDP packet from {src_ip}:{src_port} to {dst_ip}:{dst_port}\n")
            elif packet.haslayer(ICMP):
                self.text_box.insert(tk.END, f"ICMP packet from {src_ip} to {dst_ip}\n")
            else:
                self.text_box.insert(tk.END, f"Unknown protocol packet from {src_ip} to {dst_ip}\n")

        if not self.sniffing:
            return False

        self.text_box.see(tk.END)

    def run(self):
        self.root.mainloop()

listener = NetworkListener()
listener.run()