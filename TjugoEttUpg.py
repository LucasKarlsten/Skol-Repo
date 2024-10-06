import random
from typing import List, Tuple
import pyinputplus as pyip
from time import sleep

class Kort:
    # Initierar klassen Kort med en suit, valör, och poäng för valören
    def __init__(self, suit: str, valör: str, nmrValör: int) -> None:
        self.suit = suit
        self.valör = valör
        self.nmrValör = nmrValör

    def __str__(self) -> str:
        # Definierar hur ett kort kommer se ut som en sträng ex. "Hjärter 6"
        return f"{self.suit} {self.valör}"
    
class Deck:
    def __init__(self) -> None:
        # Här initierar jag att self.kort är en lista från klassen Kort
        # Jag skapar sen en lista med strängar för suitsen i en kortlek tack vare import typing
        # För valörerna så kunde deklarerade jag en lista med tuples, där varje tuple innehåller en sträng och en int
        self.kort: List[Kort] = []
        suits: List[str] = ['Hjärter', 'Klöver', 'Ruter', 'Spader']
        valörer: List[Tuple[str, int]] = [
            ('2', 2), ('3', 3), ('4', 4), ('5', 5), ('6', 6), ('7', 7), ('8', 8), ('9', 9),
            ('10', 10), ('Knekt', 11), ('Dam', 12), ('Kung', 13), ('Ess', 14)
        ]
        # Lägger in alla möjliga kort kombinationer av färger och valörer
        for suit in suits:
            for valör, nmrValör in valörer:
                self.kort.append(Kort(suit, valör, nmrValör))
        random.shuffle(self.kort)

    def draKort(self) -> Kort: 
        # Drar det översta kortet och returnerar till self.kort
        return self.kort.pop()
    
class Spelare:
    # Initiera klassen Spelare, och ger den ett namn, en lista med kort (som kommer representera ens hand) - 
    # - poäng och en bool för esshantering som kommer senare i koden
    def __init__(self, namn: str) -> None:
        self.namn = namn
        self.hand: List[Kort] = []
        self.pts: int = 0
        self.dator_spelar: bool = (namn == 'Dealer')

    # Funktion för att lägga till ett nytt kort hos spelaren och uppdaterar sedan poängen
    def nyttKort(self, kort: Kort) -> None:
        self.hand.append(kort)
        if kort.valör == 'Ess':
            # Om datorn spelar så hanteras ess:ets poäng automatiskt
            if self.dator_spelar == True:
                if self.pts + 14 <= 21:
                    self.pts += 14
                else:
                    self.pts += 1

            if self.pts + 14 <= 21:
                # Om "spelaren" spelar så hanteras esset med en inputChoice från pyinputplus
                if self.dator_spelar == False:
                    response = pyip.inputChoice(['1', '14'],
                        prompt = 'Du drog ett ess, vill du välja 1 eller 14?',
                )
                    if response == '14':
                        self.pts += 14
                    elif response == '1':
                        self.pts += 1
        else:
            self.pts += kort.nmrValör
        
    def kortPåHand(self) -> str:
        # Returnerar en sträng som representerar korten på handen och spelarens poäng
        kort_strängar = [str(kort) for kort in self.hand]
        kort_lista = "\n".join(kort_strängar)
        return (f"Kort på hand:\n{kort_lista}\nTotal poäng: {self.pts}")

class Spel:
    # Skapa klassen Spel och initerar den med en spelare, en dealer, och kortleken som funktioner
    def __init__(self) -> None:
        self.spelare : Spelare = Spelare('Spelare')
        self.dealer: Spelare = Spelare('Dealer')
        self.kort: Deck = Deck()

    def tjugoettSpel(self) -> None:
        # Spelets huvudlogik
        svar: str = input('Välkommen till TjugoEtt! Redo att börja? y/n ').lower()
        if svar == 'y':
            # Spelarens tur
            while True:
                sleep(0.5)
                # Ett kort dras och läggs till i handen
                kort: Kort = self.kort.draKort()
                self.spelare.nyttKort(kort)
                print(self.spelare.kortPåHand())

                if self.spelare.pts > 21:
                    print('Du blev tjock! Datorn vinner!')
                    return
                elif self.spelare.pts == 21:
                    print('Du fick 21! Låt oss nu se vad datorn får.')
                    break
            
                # Frågar om man vill dra ett nytt kort
                svar2: str = input('Vill du dra ett till kort? y/n ').lower()
                if svar2 != 'y':
                    break

            # Datorns tur
            print('Datorns tur!')
            while self.dealer.pts < 17:
                sleep(0.5)
                kort: Kort = self.kort.draKort()
                self.dealer.nyttKort(kort)
                print(self.dealer.kortPåHand())

            
            # Jämför resultat
            print(f"Spelare: {self.spelare.pts}, Dealer: {self.dealer.pts}")
            if self.dealer.pts > 21 or self.spelare.pts > self.dealer.pts:
                print('Du vinner!')
            elif self.spelare.pts == self.dealer.pts:
                print('Tyvärr vinner datorn på lika poäng!')
            else:
                print('Datorn vinner!')
        else:
            print('Nehe, vad gör du här då?')

def main() -> None:
    # Huvudfunktionen som i sin tur startar spelet
    game: Spel = Spel()
    game.tjugoettSpel()

if __name__ == "__main__":
    main()
