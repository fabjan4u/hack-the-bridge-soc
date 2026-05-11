# Blue Team SOC Dashboard: Handleiding

Deze map bevat het "Security Operations Center" (SOC) dashboard. Dit is ontworpen als basisapplicatie waar de Software Developers (Team Blue) op verder kunnen bouwen, of die ze direct kunnen inzetten om de fabriek in de gaten te houden.

## 1. Het Dashboard Starten
Het dashboard draait op Python met het Flask framework.
1. Zorg dat Python is geïnstalleerd.
2. Open een terminal/powershell in deze map (`dashboard`).
3. Installeer Flask (indien nodig): `pip install flask`
4. Start de server: `python app.py`
5. Open een browser en ga naar: `http://localhost:5000` (of het IP-adres van deze laptop als je vanaf een andere pc kijkt).

---

## 2. Koppelen van de Echte PLC (Voor Developers)
Momenteel toont het dashboard *gesimuleerde* PLC-data. De Developers kunnen dit koppelen aan de **echte** Siemens PLC door een script te schrijven (bijv. met de `python-snap7` library) dat de fysieke status uitleest.

**Hoe update je de status op het dashboard?**
Stuur een `POST` request met JSON data naar `/api/update_plc`.

**Voorbeeld (Python script dat de PLC uitleest en het dashboard update):**
```python
import requests
import time

# Dit is het IP van de laptop waar het dashboard (app.py) op draait
DASHBOARD_URL = "http://localhost:5000/api/update_plc"

while True:
    # --- Hier zou je SNAP7 code staan om de PLC te lezen ---
    echte_status = "RUN" # of "STOP" als hij gehackt is
    echte_snelheid = 1450
    # -------------------------------------------------------

    data = {
        "status": echte_status,
        "speed": echte_snelheid,
        "temperature": 42.1
    }
    
    try:
        requests.post(DASHBOARD_URL, json=data)
    except:
        print("Kan dashboard niet bereiken.")
        
    time.sleep(2) # Update elke 2 seconden
```

---

## 3. Alerts Sturen (Vanuit Firewall, Honeypots of Logs)
Het dashboard heeft een live "Security Alerts" feed. Team Blue kan hier meldingen naartoe sturen als ze iets verdachts detecteren op het netwerk.

**Hoe stuur je een alert?**
Stuur een `POST` request naar `/api/report`.

**Voorbeeld (Python script - Nmap detector):**
```python
import requests

DASHBOARD_URL = "http://localhost:5000/api/report"

alert_data = {
    "severity": "HIGH",     # Opties: HIGH, MEDIUM, LOW
    "source": "pfSense Firewall", 
    "message": "Nmap Port Scan gedetecteerd vanaf IP 192.168.1.55!"
}

requests.post(DASHBOARD_URL, json=alert_data)
```

**Voorbeeld (Powershell/Curl):**
Je kunt zelfs vanuit de Windows commandline alerts schieten:
```powershell
Invoke-RestMethod -Uri "http://localhost:5000/api/report" -Method Post -ContentType "application/json" -Body '{"severity":"LOW", "source":"TIA Portal Server", "message":"Foutieve inlogpoging op administrator account."}'
```

## 4. De Opdracht voor de Developers
Jullie missie:
1.  **Integreer:** Zorg dat scripts live de status en incidenten naar dit dashboard schieten.
2.  **Breid uit:** (Optioneel) Voeg grafieken toe (bijv. Chart.js) om netwerkverkeer (bytes/sec) live in beeld te brengen.
3.  **Monitor:** Gebruik dit scherm op een grote tv tijdens "The Breach" (De aanvalsdag in Week 2) om Team Red in de gaten te houden.
