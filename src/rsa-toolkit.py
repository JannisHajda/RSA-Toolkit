import os
import json
import math
from textwrap import wrap
from random import getrandbits, randrange
from sympy import mod_inverse


def miller_rabin_test(p, k=128):
    if p == 2 or p == 3:
        return True
    if p <= 1 or p % 2 == 0:
        return False

    s = 0
    d = p - 1
    while d % 2 == 0:
        s += 1
        d //= 2

    for _ in range(k):
        a = randrange(2, p - 1)
        x = pow(a, d, p)
        if x != 1 and x != p - 1:
            j = 1
            while j < s and x != p - 1:
                x = pow(x, 2, p)
                if x == 1:
                    return False
                j += 1
            if x != p - 1:
                return False
    return True


def euklidischer_algorithmus(a, b):
    while b != 0:
        a, b = b, a % b

    return a


def ascii_to_dec(ascii_string):
    return list(map(lambda char: ord(char), ascii_string))


def dec_to_ascii(dec_array):
    return list(map(lambda num: str(chr(num)), dec_array))


def dec_to_hex(dec_int):
    return format(dec_int, 'x')


def hex_to_dec(hex_string):
    return int(hex_string, 16)


def gen_prime(bits):
    p = getrandbits(bits)
    while not miller_rabin_test(p):
        p = getrandbits(bits)

    return p


def factorize(n):
    sqrn = math.sqrt(n)
    sqrn = math.trunc(n)
    for p in reversed(range(sqrn)):
        if n % p == 0:
            break

    q = n/p
    return(int(p), int(q))


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

    def enc_message(self, m):
        if not m >= self.N:
            return pow(m, self.e, self.N)
        else:
            return None

    def dec_message(self, c):
        if not c >= self.N:
            return pow(c, self.d, self.N)
        else:
            return None

    def gen_keys(self, key_size):
        p = gen_prime(key_size)
        q = gen_prime(key_size)
        N = p * q
        phiN = (p - 1)*(q - 1)

        e = gen_prime(key_size//2)
        while not (1 < e < phiN and euklidischer_algorithmus(e, phiN) == 1):
            e = gen_prime(key_size//2)

        d = mod_inverse(e, phiN)

        self.p = p
        self.q = q
        self.N = N
        self.e = e
        self.d = d

        return N, e, d

    def bruteforce_keys(self, e, N):
        print("Versuche N zu faktorisieren . . .")
        p, q = factorize(N)
        print("N wurde erfolgreich faktorisiert: %s * %s = %s" % (p, q, N))
        phiN = (p-1)*(q-1)
        d = mod_inverse(e, phiN)
        print("Privaten Schlüssel berechnet: d = %s \n" % (d))

        self.p = p
        self.q = q
        self.e = e
        self.d = d
        self.N = N

        return True


def main_menu():
    print("************ RSA-Toolkit - Jannis Hajda **************")
    while True:
        try:
            choice = int(input('1: Schlüssel generieren \n2: Nachricht verschlüsseln \n3: Nachricht entschlüsseln \n4: Bruteforce RSA-Verschlüsselung \n5: Konfiguration speichern/laden \n6: Verlassen \n\nWählen Sie eine Funktion:  '))
            print("")
            if choice == 1:
                gen_menu()
            elif choice == 2:
                enc_menu()
            elif choice == 3:
                dec_menu()
            elif choice == 4:
                bruteforce_message()
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
            choice = int(input(
                "1: Aktuelle Konfiguration speichern \n2: Konfiguration laden \n3: Zum Hauptmenü \n\nWählen Sie eine Funktion: "))
            if choice == 1:
                toolkit.save_config()
                print("Die aktuelle Konfiguration wurde gespeichert!")
                break
            elif choice == 2:
                toolkit.load_config()
                print("Die Konfiguration wurde geladen!")
                break
            elif choice == 3:
                break
            else:
                print("Bite wählen Sie eine verfügbare Funktion! \n")
        except ValueError:
            print("Bite wählen Sie eine verfügbare Funktion! \n")

    input("Drücken Sie eine beliebige Taste...")
    print("")
    main_menu()


def enc_menu():
    while True:
        print("*** Nachricht verschlüsseln ***")
        m = input("Nachricht: ")

        if m:
            dec = ascii_to_dec(m)

            hexa = list(map(dec_to_hex, dec))
            hexa = ''.join(hexa)

            m = hex_to_dec(hexa)
            c = toolkit.enc_message(int(m))

            if c:
                print("Verschlüsselte Nachricht: ", str(c))
                break
            else:
                print("Die zu verschlüsselnde Nachricht darf nicht größer als N sein.")
                print(
                    "Bitte generieren Sie größere p und q oder wählen Sie eine kleinere Nachricht! \n")
                break
        else:
            print("Bitte geben Sie eine gültige ASCII codierte Nachricht ein! \n")

    input("Drücken Sie eine beliebige Taste...")
    print("")
    main_menu()


def dec_menu():
    while True:
        try:
            print("*** Nachricht entschlüsseln ***")
            c = input("Verschlüsselte Nachricht: ")
            m = toolkit.dec_message(int(c))

            if m:
                hexa = dec_to_hex(m)
                hexa = wrap(hexa, 2)

                dec = list(map(hex_to_dec, hexa))

                m = dec_to_ascii(dec)
                m = ''.join(m)
                print("Entschlüsselte Nachricht: ", m)
            else:
                print("Die zu entschlüsselnde Nachricht darf nicht größer als N sein!")
                print(
                    "Bitte generieren Sie größere p und q oder wählen Sie eine kleinere Nachricht!")

            break
        except ValueError:
            print("Bitte geben Sie eine gültige verschlüsselte Nachricht ein! \n")

    input("Drücken Sie eine beliebige Taste...")
    print("")
    main_menu()


def gen_menu():
    while True:
        try:
            print("*** Schlüsselgenerierung ***")
            print("ACHTUNG: Die Geschwindigkeit dieser Funktion ist von der verfügbaren Rechenleistung und der Schlüssellänge abhängig.")
            print("Es kann sein, dass die Berechnung der Schlüssel sehr lange dauert! \n")
            key_size = int(input("Schlüssellänge in Bit: "))

            if key_size >= 4:
                N, e, d = toolkit.gen_keys(key_size)
                print("Öffentlicher Schlüssel (e, N): (%s, %s)" % (e, N))
                print("Privater Schlüssel d: %s \n" % d)
                print(
                    "Die Schlüsselgenerierung war erfolgreich und die Parameter wurden übernommen.")
                print(
                    "Im Hauptmenü können Sie nun die Funktionen 3 und 4 zur Ver- und Entschlüsselung von Nachrichten verwenden!")
                break
            else:
                print("Bitte wählen Sie eine Schlüssellänge von mindestens 4 Bit! \n")

        except ValueError:
            print("Bitte wählen Sie eine Schlüssellänge von mindestens 4 Bit! \n")

    input("Drücken Sie eine beliebige Taste...")
    print("")
    main_menu()


def bruteforce_message():
    while True:
        try:
            print("*** Bruteforce RSA-Verschlüsselung ***")
            print("ACHTUNG: Die Geschwindigkeit dieser Funktion ist von der verfügbaren Rechenleistung und der Schlüssellänge abhängig.")
            print("Es kann sein, dass die Berechnung der Schlüssel sehr lange dauert! \n")
            e = int(input("e: "))
            N = int(input("N: "))
            print("")

            if toolkit.bruteforce_keys(e, N):
                print(
                    "Die RSA-Verschlüsselung wurde erfolgreich gebrochen und die Parameter übernommen.")
                print(
                    "Im Hauptmenü können Sie nun die Funktion 4 aufrufen und empfangene Nachrichten entschlüsseln!")
                break
        except ValueError:
            print("Bitte geben Sie einen validen öffentlichen Schlüssel ein! \n")

    input("Drücken Sie eine beliebige Taste...")
    print("")
    main_menu()


toolkit = RSAToolkit()
main_menu()
