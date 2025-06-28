from pymongo import MongoClient

# Verbindung zur MongoDB herstellen
client = MongoClient('mongodb://localhost:27017/')
db = client['spiele']
collection = db['pcgames']

# ASCII Logo
def ascii_logo():
    print("   ▄████████    ▄███████▄  ▄█     ▄████████  ▄█            ████████▄  ▀█████████▄  ")
    print("  ███    ███   ███    ███ ███    ███    ███ ███            ███   ▀███   ███    ███ ")
    print("  ███    █▀    ███    ███ ███▌   ███    █▀  ███            ███    ███   ███    ███ ")
    print("  ███          ███    ███ ███▌  ▄███▄▄▄     ███            ███    ███  ▄███▄▄▄██▀  ")
    print("▀███████████ ▀█████████▀  ███▌ ▀▀███▀▀▀     ███            ███    ███ ▀▀███▀▀▀██▄  ")
    print("         ███   ███        ███    ███    █▄  ███            ███    ███   ███    ██▄ ")
    print("   ▄█    ███   ███        ███    ███    ███ ███▌    ▄      ███   ▄███   ███    ███ ")
    print(" ▄████████▀   ▄████▀      █▀     ██████████ █████▄▄██      ████████▀  ▄█████████▀  ")
    print("")

# Funktion zum Hinzufügen eines Spiels
def spiel_hinzufuegen():
    titel = input("Titel des Spiels: ")
    jahr = int(input("Erscheinungsjahr: "))
    downloads = int(input("Download-Zahlen: "))
    altersgrenze = int(input("Altersgrenze: "))
    art = input("Art des Spiels (getrennt durch Kommas): ").split(',')
    wertung = float(input("Wertung (0-10): "))

    neues_spiel = {
        "titel": titel,
        "jahr": jahr,
        "downloads": downloads,
        "altersgrenze": altersgrenze,
        "art": art,
        "wertung": wertung
    }
    
    collection.insert_one(neues_spiel)
    print(titel + " wurde erfolgreich hinzugefügt.")

# Funktion um alle Spiele anzuzeigen
def spiele_anzeigen():
    print("Alle Spiele in der Datenbank:")
    spiele = collection.find()
    if collection.count_documents({}) == 0:
        print("Keine Spiele gefunden.")
    else:
        for spiel in spiele:
            print(spiel['titel'] + " - " + str(spiel['jahr']) + " - Wertung: " + str(spiel['wertung']))
    print("")

# Funktion um Spiele zu suchen
def spiele_suchen():
    suchkriterium = input("Nach welchem Titel suchen Sie? ").lower()
    print("Suchkriterium: " + suchkriterium)
    spiele = collection.find({"titel": {"$regex": suchkriterium, "$options": "i"}})

    spiele_liste = list(spiele)
    if not spiele_liste:
        print("Kein Spiel mit dem Titel '" + suchkriterium + "' gefunden.")
    else:
        for spiel in spiele_liste:
            print("Titel: " + spiel['titel'])
            print("Erscheinungsjahr: " + str(spiel['jahr']))
            print("Downloads: " + str(spiel['downloads']))
            print("Altersgrenze: " + str(spiel['altersgrenze']))
            print("Art: " + ", ".join(spiel['art']))
            print("Wertung: " + str(spiel['wertung']))
            print("")

# Funktion um ein Spiel zu bearbeiten
def spiel_bearbeiten():
    suchkriterium = input("Welches Spiel möchten Sie bearbeiten? ")
    spiel = collection.find_one({"titel": {"$regex": suchkriterium, "$options": "i"}})

    if spiel:
        neues_jahr = int(input("Neues Erscheinungsjahr (aktuell " + str(spiel['jahr']) + "): "))
        neue_downloads = int(input("Neue Download-Zahlen (aktuell " + str(spiel['downloads']) + "): "))
        neue_wertung = float(input("Neue Wertung (0-10) (aktuell " + str(spiel['wertung']) + "): "))

        collection.update_one(
            {"titel": spiel['titel']},
            {"$set": {"jahr": neues_jahr, "downloads": neue_downloads, "wertung": neue_wertung}}
        )
        print(spiel['titel'] + " wurde erfolgreich aktualisiert.")
    else:
        print("Kein Spiel mit dem Titel '" + suchkriterium + "' gefunden.")

# Funktion um ein Spiel zu löschen
def spiel_loeschen():
    titel = input("Welches Spiel möchten Sie löschen? ")
    ergebnis = collection.delete_one({"titel": {"$regex": titel, "$options": "i"}})

    if ergebnis.deleted_count > 0:
        print(titel + " wurde erfolgreich gelöscht.")
    else:
        print("Kein Spiel mit dem Titel '" + titel + "' gefunden.")

# Hauptmenü
def hauptmenue():
    ascii_logo()
    while True:
        print("1. Spiel hinzufügen")
        print("2. Spiele anzeigen")
        print("3. Spiel suchen")
        print("4. Spiel bearbeiten")
        print("5. Spiel löschen")
        print("6. Beenden")

        auswahl = input("Ihre Auswahl: ")

        if auswahl == "1":
            spiel_hinzufuegen()
        elif auswahl == "2":
            spiele_anzeigen()
        elif auswahl == "3":
            spiele_suchen()
        elif auswahl == "4":
            spiel_bearbeiten()
        elif auswahl == "5":
            spiel_loeschen()
        elif auswahl == "6":
            print("Programm beendet.")
            break
        else:
            print("Ungültige Auswahl, bitte versuchen Sie es erneut.")

# Programm starten
if __name__ == "__main__":
    hauptmenue()
