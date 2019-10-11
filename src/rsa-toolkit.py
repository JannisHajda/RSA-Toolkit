import os, json
from textwrap import wrap
from random import getrandbits

ascii_to_dec = lambda ascii_string : list(map(lambda char : ord(char), ascii_string))

dec_to_ascii = lambda dec_array : list(map(lambda num : str(chr(num)), dec_array))

class RSAToolkit:
    def __init__(self):
        self.p = 7
        self.q = 13
        self.e = 5
        self.d = 29
        self.N = self.p * self.q
    
    # Konfiguration
    def save_config(self):
        # Speichert die aktuelle Konfiguration in der Datei "config.json"
        with open("config.json", "w") as config:
            json.dump({
                "p": self.p,
                "q": self.q,
                "e": self.e,
                "d": self.d,
                "N": self.N
            }, config)
    
    def load_config(self):
        # Lädt die Konfiguration aus der Datei "config.json". Wenn diese Datei nicht existiert, wird sie angelegt.
        if os.path.exists("config.json"):
            with open("config.json") as config:
                data = json.load(config)
                self.p = data["p"]
                self.q = data["q"]
                self.e = data["e"]
                self.d = data["d"]
                self.N = data["N"]
        else:
            self.save_config()
    
    enc_message = lambda self, m : pow(m, self.e, self.N)

    dec_message = lambda self, c : pow(c, self.d, self.N)

def main_menu():
    print("************ RSA-Toolkit - Jannis Hajda **************")
    while True:
        try:
            choice = int(input('1: Schlüssel generieren \n2: Nachricht verschlüsseln \n3: Nachricht entschlüsseln \n4: Bruteforce RSA-Verschlüsselung \n5: Konfiguration speichern/laden \n6: Verlassen \n\nWählen Sie eine Funktion:  '))
            print("")
            if choice == 1:
                print(1)
            elif choice == 2:
                enc_menu()
            elif choice == 3:
                dec_menu()
            elif choice == 4:
                print(4)
            elif choice == 5:
                config_menu()
            elif choice == 6:
                break
            else:
                print("Bite wählen Sie eine verfügbare Funktion! \n")
        except ValueError:
            print("Bitte wählen Sie eine verfügbare Funktion! \n")

    print("RSA-Toolkit wird beendet.")
    exit()

def config_menu():
    while True:
        try:
            print("*** Konfiguration ***")
            choice = int(input("1: Aktuelle Konfiguration speichern \n2: Konfiguration laden \n3: Zum Hauptmenü \n\nWählen Sie eine Funktion: "))
            if choice == 1:
                toolkit.save_config()
                print("Die aktuelle Konfiguration wurde gespeichert! \n")
            elif choice == 2:
                toolkit.load_config()
                print("Die Konfiguration wurde geladen! \n")
            elif choice == 3:
                print("")
                break
            else:
                print("Bite wählen Sie eine verfügbare Funktion! \n")
        except ValueError:
            print("Bite wählen Sie eine verfügbare Funktion! \n")

    main_menu()

def enc_menu():
    print("*** Nachricht verschlüsseln ***")
    m = input("Nachricht: ")
    c = toolkit.enc_message(int(m))
    print(c)
    print("")
    main_menu()

def dec_menu():
    print("*** Nachricht entschlüsseln ***")
    c = input("Verschlüsselte Nachricht: ")
    m = toolkit.dec_message(int(c))
    print(m)
    print("")
    main_menu()

toolkit = RSAToolkit()
main_menu()
