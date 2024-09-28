import scapy.all as scapy
from scapy.layers.inet import IP, TCP, UDP, ICMP
from scapy.layers.l2 import Ether
import subprocess
import virustotal_python

# Initialize VirusTotal
virustotal_vt = virustotal_python.Virustotal(apikey)

# Define a function to filter packets
def filter_packet(packet):
    # Reject null packets
    if packet.haslayer(Ether) and packet[Ether].src == "00:00:00:00:00:00":
        return False

    # Reject packets with invalid TCP flags
    if packet.haslayer(TCP) and (packet[TCP].flags & 0x80):  # 0x80 = SYN, ACK, FIN, RST
        return False

    # Reject ICMP echo requests (ping)
    if packet.haslayer(ICMP) and packet[ICMP].type == 8:
        return False

    # Reject UDP packets with invalid checksums
    if packet.haslayer(UDP) and packet[UDP].chksum == 0:
        return False

    # Reject packets with spoofed source IP addresses
    if packet.haslayer(IP) and packet[IP].src == "0.0.0.0":
        return False

    # Scan packet payload for viruses
    if packet.haslayer(Raw):
        payload = bytes(packet[Raw].load)
        virus_scan_results = []

        # par2deep
        par2deep_result = subprocess.run(['par2deep', '-c', '-', '-'], input=payload, capture_output=True, text=True)
        if par2deep_result.returncode == 0:
            virus_scan_results.append("par2deep: Virus detected")

        # VirusTotal
        vt_result = virustotal_vt.file_scan(payload, apikey='e57b52d1fccc825377635e5398e1ac74b04f0bcf1162629cc51307518df358f6')
        if vt_result.positives > 0:
            virus_scan_results.append("VirusTotal: " + vt_result.scan_id)

        if virus_scan_results:
            print("Virus detected:", ", ".join(virus_scan_results))
            return False

    # Accept all other packets
    return True

# Define a function to handle incoming packets
def handle_packet(packet):
    if filter_packet(packet):
        # Accept the packet and forward it to the next hop
        packet.show()
        scapy.send(packet, iface="eth0")  # Replace with your outgoing interface
    else:
        # Reject the packet
        print("Rejected packet:")
        packet.show()

# Start sniffing incoming packets on the gateway interface
scapy.sniff(iface="eth0", prn=handle_packet)  # Replace with your incoming interface