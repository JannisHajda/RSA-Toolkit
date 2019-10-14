import os
import json
import math
import time
from textwrap import wrap
from random import getrandbits, randrange
from sympy import mod_inverse


def miller_rabin_test(p, k=128):
    """ Liefert als Rückgabewert einen Wahrheitswert, welcher bestimmt, ob p prim ist.
    Die Funktion verwendet hierbei den Satz von Euler. """
    if p == 2 or p == 3:  # Wenn p = 2 oder p = 3 muss nicht berechnet werden, ob es sich um eine Primzahl handelt
        return True
    if p <= 1 or p % 2 == 0:  # Wenn p <= 1 oder durch 2 ohne Rest teilbar ist, so handelt es sich um keine Primzahl
        return False

    s = 0
    d = p - 1
    while d % 2 == 0:  # teile d so lange, wie bei der Division mit 2 kein Rest vorhanden ist
        s += 1
        d //= 2

    for _ in range(k):
        a = randrange(2, p - 1)  # Bestimme eine zufällige Zahl 2 <= a <= p-1
        x = pow(a, d, p)  # Berechne (a^d) mod P
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
    """ Bestimmt den größten gemeinsamen Teiler der Zahlen a, b """
    while b != 0:
        a, b = b, a % b

    return a


def ascii_to_dec(ascii_string):
    """ Konvertiert einen ASCII-String in ein Array von Dezimalzahlen """
    return list(map(lambda char: ord(char), ascii_string))


def dec_to_ascii(dec_array):
    """ Konvertiert ein Array von Dezimalzahlen in einen ASCII-String"""
    return ''.join(list(map(lambda num: str(chr(num)), dec_array)))


def dec_to_hex(dec_int):
    """ Bestimmt den Hexadezimalwert einer Dezimalzahl """
    return format(dec_int, 'x')


def hex_to_dec(hex_string):
    """ Bestimmt den Dezimalwert einer Hexadezimalzahl """
    return int(hex_string, 16)


def gen_prime(bits):
    """ Generiert eine Primzahl p in gewünschter Bitgröße """
    p = getrandbits(bits)
    # Überprüft durch Miller-Rabin-Test ob p prim ist
    while not miller_rabin_test(p):
        p = getrandbits(bits)

    return p


def factorize(n):
    """ Versucht n zu faktorisieren, so dass n = p * q"""
    sqrn = math.sqrt(n)
    sqrn = math.trunc(n)
    for p in reversed(range(sqrn)):
        if n % p == 0:
            break

    q = n/p
    return(int(p), int(q))


class RSAToolkit:
    """ RSA-Toolkit Klasse """

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
        """ Verschlüsselt ein Dezimalzahl m als c """
        if not m >= self.N:  # RSA funktioniert nur, wenn die Nachricht m kleiner als das RSA-Modul N ist.
            return pow(m, self.e, self.N)
        else:
            return None

    def dec_message(self, c):
        """ Entschlüsselt eine Dezimalzahl c als m """
        if not c >= self.N:  # RSA funktioniert nur, wenn die Nachricht c kleiner als das RSA-Modul N ist.
            return pow(c, self.d, self.N)
        else:
            return None

    def gen_keys(self, key_size):
        """ Generiert p, q, e, d, N in gewünschter Bitlänge """
        p = gen_prime(key_size//2)
        q = gen_prime(key_size//2)
        N = p * q
        phiN = (p - 1)*(q - 1)

        e = gen_prime(key_size//4)
        # überprüft ob 1 < e < phiN und ggT(e, phiN) = 1
        while not (1 < e < phiN and euklidischer_algorithmus(e, phiN) == 1):
            e = gen_prime(key_size//2)

        # bestimmt multiplikatives Inverse von e mod phiN
        d = mod_inverse(e, phiN)

        self.p = p
        self.q = q
        self.N = N
        self.e = e
        self.d = d

        return N, e, d

    def bruteforce_keys(self, e, N):
        """ Versucht RSA-Verschlüsselung zu brutforcen """
        print("Versuche N zu faktorisieren . . .")
        p, q = factorize(N)  # Faktorisiere N
        print("N wurde erfolgreich faktorisiert: %s * %s = %s" % (p, q, N))
        phiN = (p-1)*(q-1)
        # Berechne d als multiplikatives Inverse von e mod phiN
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
            """ Das RSA System kann nur Zahlen ver- und entschlüsseln. Deshalb wird der ASCII-String zunächst in ein Dezimalzahlen überführt.
            Der Wert dieser Dezimalzahlen wird in das Hexadezimalsystem überführt und anschließend werden die Hexadezimalzahlen aneinander gereiht. 
            Diese neue Hexadezimalzahl wird erneut in das Dezimalsystem überführt und anschließend verschlüsselt. """
            dec = ascii_to_dec(
                m)  # ASCII-String wird in Dezimalzahlen überführt

            # Dezimalzahlen werden in das Hexadezimalsystem überführt
            hexa = list(map(dec_to_hex, dec))
            hexa = ''.join(hexa)  # Hexadezimalzahlen werden aneinandergereiht

            # neue Hexadezimalzahl wird in Dezimalsystem überführt
            m = hex_to_dec(hexa)
            c = toolkit.enc_message(int(m))  # Dezimalzahl wird verschlüsselt

            if c:  # Überprüft ob Verschlüsselung erfolgreich war
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
            # Entschlüsselt verschlüsselte Nachricht c
            m = toolkit.dec_message(int(c))

            if m:  # Überprüft ob Entschlüsselung erfolgreich war
                """ Bei der Entschlüsselung muss genau umgekehrt zur Verschlüsselung vorgegangen werden. 
                Das heißt, dass die entschlüsselte Dezimalzahl zunächst in das Hexadezimalsystem überführt werden muss.
                Danach wird die Hexadezimalzahl in zweier Blöcke aufgeteilt und diese Bläcke werden erneut in das Dezimalsystem überführt.
                Diese Dezimalzahlen kann man nun in einen ASCII-String konvertieren."""
                hexa = dec_to_hex(
                    m)  # Entschlüsselte Dezimalzahl wird in Hexadezimalsystem übertragen
                # Hexadezimalzahl wird in zweier Blöcke aufgeteilt
                hexa = wrap(hexa, 2)

                # Hexadezimalzahlen werden in das Dezimalsystem überführt
                dec = list(map(hex_to_dec, hexa))

                # Dezimalzahlen werden in ASCII-String konvertiert
                m = dec_to_ascii(dec)
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

            if key_size >= 8:  # Überprüft ob die Schlüssellänge mindestens 8 Bit beträgt
                start = time.time()
                N, e, d = toolkit.gen_keys(key_size)
                end = time.time()
                elapsed_time = end - start
                print("Öffentlicher Schlüssel (e, N): (%s, %s)" % (e, N))
                print("Privater Schlüssel d: %s \n" % d)
                print(
                    "Die Schlüsselgenerierung war erfolgreich (%s Sekunden) und die Parameter wurden übernommen." % elapsed_time)
                print(
                    "Im Hauptmenü können Sie nun die Funktionen 3 und 4 zur Ver- und Entschlüsselung von Nachrichten verwenden!")
                break
            else:
                print("Bitte wählen Sie eine Schlüssellänge von mindestens 8 Bit! \n")

        except ValueError:
            print("Bitte wählen Sie eine Schlüssellänge von mindestens 8 Bit! \n")

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
            start = time.time()
            if toolkit.bruteforce_keys(e, N):
                end = time.time()
                elapsed_time = end - start
                print(
                    "Die RSA-Verschlüsselung wurde erfolgreich gebrochen (%s Sekunden) und die Parameter übernommen." % elapsed_time)
                print(
                    "Im Hauptmenü können Sie nun die Funktion 4 aufrufen und empfangene Nachrichten entschlüsseln!")
                break
        except ValueError:
            print("Bitte geben Sie einen validen öffentlichen Schlüssel ein! \n")

    input("Drücken Sie eine beliebige Taste...")
    print("")
    main_menu()


toolkit = RSAToolkit()  # erstelle eine neue Instanz des RSA Toolkits
main_menu()  # rufe das Hauptmenü auf
