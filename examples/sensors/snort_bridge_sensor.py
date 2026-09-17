#!/usr/bin/env python3
"""
Sample Student Blue Team Sensor Script:
Monitors industrial telemetry and pushes high-priority alerts to the SOC dashboard.
"""
import requests
import time
import random

SOC_URL = "http://localhost:5000/api/report"

def report_threat(message, severity="HIGH"):
    payload = {
        "source": "Student-BlueTeam-Sensor-01",
        "severity": severity,
        "message": message
    }
    try:
        res = requests.post(SOC_URL, json=payload, timeout=3)
        if res.status_code == 201:
            print(f"[+] Alert successfully transmitted: {message}")
    except Exception as e:
        print(f"[-] Could not reach SOC dashboard: {e}")

if __name__ == "__main__":
    print("[*] Starting OT Security Sensor Simulator...")
    threats = [
        "Unauthorized S7comm function code 0x05 (STOP CPU) received from 192.168.1.189",
        "Repeated invalid handshake packets targeting Siemens CP 1243-1 communication module",
        "Rogue ARP broadcast spoofing the Botlek Bridge PLC gateway IP"
    ]
    for threat in threats:
        time.sleep(random.uniform(1.0, 3.0))
        report_threat(threat)
