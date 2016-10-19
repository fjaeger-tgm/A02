import threading
import string
import random
import textwrap
from Tools.scripts.treesync import raw_input

#Alphabet-Liste
number = list(string.ascii_lowercase)
#Dictionary mit random Buchstaben als Keys und Values
letters = dict(zip(string.ascii_lowercase, random.sample(number, len(number))))
letters[" "] = " "
ausgabe = ""
print("")
print(letters)


class Threadclass(threading.Thread):
    """ :param textB: Buchstaben die zu verändern sind von dem Thread
        :param anzahlThreads: Die Threadnummer"""
    def __init__(self, textB, anzahlThreads):
        """Konstruktor"""
        threading.Thread.__init__(self)
        self.text = textB
        self.anzahlTreads = anzahlThreads
        self.ausgabe = ""

    def run(self):
        """Setzt den Stringteil in einen String"""
        for i in range(len(self.text)):
            self.ausgabe += letters[self.text[i]]


def erzeugeKey():
    """ Erzeugt zwei Keys zur Entschlüsselung des Textes"""
    key1 = ""
    for i in letters:
        key1 += letters[i]
    print("Key1: %s" % (key1))
    key2 = ""
    for i in letters.keys():
        key2 += str(i)
    print("Key2: %s" % (key2))


def verschluesseln():
    """Verschlüsselt einen eingegeben Text und ordnet Teile des Textes einzelnen Threads zu"""
    while True:
        #Eingabe Text
        text = raw_input("Bitte den Text eingeben")
        if isinstance(text, str):
            text = text.lower()
            break
        print("Falsche Eingabe! Nochmal")
    while True:
        #Eingabe Threadanzahl
        threadInput = raw_input("Bitte Threadanzahl eingeben!")
        if int(threadInput) <= len(text):
            threadInput = int(threadInput)
            break
        else:
            print("Falsche Eingabe!")
    threadList = []
    textBuchstaben = []
    vText = ""
    #Teilung des Textes in eine Liste
    if len(text) % threadInput != 0:
        width = int(len(text) / threadInput)
        print(width)
        widths = []
        for i in range(threadInput-1):
            widths.append(width)
        widths.append(width+int(len(text) % threadInput)-1)
        my_start = 0
        my_end = 0
        for w in widths:
            my_end += w
            textBuchstaben.append(text[my_start:my_end])
            my_start += w
    else:
        textBuchstaben = textwrap.wrap(text,int(len(text)/threadInput))
    #Erzeugung von Objekten der Klasse Threadclass
    for i in range(1, threadInput + 1):
        t = Threadclass(textBuchstaben[i - 1], i)
        threadList += [t]
        t.start()
    #Ausgabe des verschlüsselten Textes
    for i in threadList:
        i.join()
        vText += i.ausgabe
    print("Der verschlüsselte Text: %s" % (vText))
    erzeugeKey()


def entschluesseln():
    """Enschlüsselt den verschlüsselten Text mithilfe von 2 Keys"""
    #Abfrage nach den Enschlüsselungskeys
    key1Eingabe = raw_input("Bitte Key1 eingeben!")
    key2Eingabe = raw_input("Bitte Key2 eingeben!")
    count = 0
    nLetters = {}
    for i in key2Eingabe:
        nLetters[i] = key1Eingabe[count]
        count += 1

    print(nLetters)
    #Eingabe des verschlüsselter Textes
    verText = raw_input("Bitte den verschlüsselten Text eingeben")
    nText = ""
    for i in verText:
        for j in nLetters.keys():
            if (nLetters[j] == i):
                nText += j
    #Ausgabe des entschlüsselten Textes
    print("Der entschlüsselte Text: %s" % (nText))


def eingabe():
    """Abfragung ob man verschlüsselen oder entschlüsselen will"""
    while True:
        #Auswahl ob verschlüsselt oder entschlüsselt wir
        inputVE = input("Bitte 'v' zur Verschlüsselung oder 'e' zur Entschlüsselung eingeben!")
        print(inputVE)
        if inputVE == 'v':
            verschluesseln()
        elif inputVE == "e":
            entschluesseln()
        else:
            print("Falsche Eingabe")
eingabe()