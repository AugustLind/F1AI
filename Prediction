import numpy as np
import tensorflow as tf
from sklearn.model_selection import train_test_split
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense
import requests

# URL til API-en som gir resultater for alle løp i 2023-sesongen
base_url = "http://ergast.com/api/f1/2023/results.json?limit=1000"

# Opprett en tom diksjonær for å lagre plasseringene til førerne
driver_positions = {}

# Hent data fra API-en
response = requests.get(base_url)

# Sjekk om forespørselen var vellykket
if response.status_code == 200:
    # Hent JSON-data fra responsen
    data = response.json()

    # Hent resultatene fra alle løpene i 2023-sesongen
    races = data.get("MRData", {}).get("RaceTable", {}).get("Races", [])

    # Gå gjennom hvert løp og hent plasseringene til førerne
    for race in races:
        results = race.get("Results", [])

        # Gå gjennom resultatene for hvert løp
        for result in results:
            position = result.get("position", "N/A")
            driver_name = f"{result['Driver']['givenName']} {result['Driver']['familyName']}"

            # Legg til førerens plassering i diksjonæren
            if driver_name not in driver_positions:
                driver_positions[driver_name] = []
            driver_positions[driver_name].append(position)

    # Skriv ut plasseringene til hver fører
    for driver, positions in driver_positions.items():
        print(f"{driver}: {positions}")

    # Funksjon for å konvertere plasseringer til tallverdier
    def convert_positions(positions):
        converted_positions = []
        for pos in positions:
            if pos == "N/A":
                converted_positions.append(0)  # Erstatt med 0 for manglende data
            else:
                converted_positions.append(int(pos))  # Konverter til heltall
        return converted_positions

    # Data: Liste over førere og deres plasseringer
    drivers = list(driver_positions.keys())
    driver_results = [convert_positions(driver_positions[driver]) for driver in drivers]

    # Lag inputdata og målverdier for LSTM-modellen
    X = []
    y = []

    for driver_index in range(len(drivers)):
        positions = driver_results[driver_index]
        
        # Sjekk om føreren har minst 15 løp før vi legger til data
        if len(positions) >= 15:
            for i in range(len(positions) - 15):
                X.append(positions[i:i+15])  # De første 15 løpene som input
                y.append(positions[i+15])    # Den 16. plasseringen som målverdi

    X = np.array(X)
    y = np.array(y)

    # Del dataen inn i trening og testsett
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # Lag LSTM-modellen
    model = Sequential([
        LSTM(64, activation='relu', input_shape=(15, 1)),
        Dense(1)
    ])

    model.compile(optimizer='adam', loss='mse')

    # Tren modellen
    model.fit(X_train.reshape((-1, 15, 1)), y_train, epochs=50, batch_size=32, validation_data=(X_test.reshape((-1, 15, 1)), y_test))

    # Bruk modellen til å forutsi neste plassering for en fører
    driver_to_predict = "Liam Lawson"
    
    # Sjekk om føreren har minst 15 løp før vi prøver å lage en forutsigelse
    if driver_to_predict in drivers and len(driver_results[drivers.index(driver_to_predict)]) >= 15:
        last_15_positions = np.array(driver_results[drivers.index(driver_to_predict)][-15:])
        last_15_positions = last_15_positions.reshape((1, 15, 1))
        next_position = model.predict(last_15_positions)
        print(f"Neste plassering for {driver_to_predict}: {int(next_position[0][0])}")
    else:
        print(f"Ikke nok data tilgjengelig for å foruts")
