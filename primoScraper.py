import asyncio
import time
from pprint import pprint
import bs4, requests, webbrowser, argparse
from telegram import Bot
import csv
import os
import telebot, requests

parser = argparse.ArgumentParser()
parser.add_argument("--object", dest='object', help="name of new tracking")
parser.add_argument("--category", dest='category', help="name of tracking category")
parser.add_argument("--minPrice", dest='minPrice', help="minimum price for the tracking")
parser.add_argument("--maxPrice", dest='maxPrice', help="maximum price for the tracking")
parser.add_argument("--annata", dest='annata', help="annata")
#parser.add_argument("--memory", dest='memory', help="memory space")
args = parser.parse_args()

BOT_TOKEN = TOKEN

CHAT_ID = 5106577808

async def invia_messaggio(msg):
    bot = Bot(token=BOT_TOKEN)
    await bot.send_message(chat_id=CHAT_ID, text=msg)

async def main():

    if args.object is not None and args.category is not None:

        LINK = "https://www.subito.it/annunci-italia/vendita/usato/?q=" + args.object
        PRE_LINK_ANNUNCIO = "https://www.subito.it/"+args.category

        minPrice = -1
        maxPrice = -1
        kmMin = -1
        kmMax = -1
        carburante = -1
        annoImmatricolazione = -1
        preferenze = -1


        response = requests.get(LINK)
        response.raise_for_status()
        soup=bs4.BeautifulSoup(response.text, 'html.parser')
        div_annunci=soup.find('div', class_='ListingContainer_col__1TZpb ListingContainer_items__3lMdo col items')

        a_annunci=div_annunci.find_all('a')
        p_paragraf = div_annunci.find_all('p')
        link_annunci = []
        prezzi_annunci = []

        if args.minPrice:
            minPrice = args.minPrice

        if args.maxPrice:
            maxPrice = args.maxPrice

        if args.annata:
            annata = args.annata

        #if args.memory:
        #    memory = args.memory
        ###for heading in soup.find_all(["h1", "h2", "h3"]):
        ###    print(heading.name + ' ' + heading.text.strip())

        with open('risultati_salvati.csv', newline='') as csvfile:
            data = list(csv.reader(csvfile))
            if len(data)!=0: data_unboxed = data[0]
            else: data_unboxed = None

        for a_annuncio in a_annunci:
            link_annuncio = str(a_annuncio.get('href'))

            price =''.join(text.strip() for text in a_annuncio.p.find_all(text=True, recursive=False))
            #print(soup.find_all("h2"))
            price = price[:-2]
            min_ = int(minPrice)
            max_ = int(maxPrice)
            if len(price)!=0:
                for c in ",.":
                    price = price.replace(c, "")
                p = int(price)

                if (min_ != -1 and min_ <= p) and (max_ != -1 and max_ >= p):
                    try:
                        pprint("")
                        #print(data_unboxed.index(link_annuncio))
                        #print("elemento già in lista")
                    except:
                        f = open('risultati_salvati.csv', 'a')
                        # f.write('%s\s' % link_annuncio)
                        f.write('%s,' % link_annuncio)
                        f.close()
                        await invia_messaggio("Nuovo Annuncio trovato! Prezzo: "+price+", Link: "+link_annuncio)
                    if PRE_LINK_ANNUNCIO in link_annuncio:
                        link_annunci.append(link_annuncio)
    else:
        categoria = input("Inserire la categoria dell'oggetto\n\n1)Macchine/Moto\n2)telefonia\n3)altro\n=>")
        os.system('cls')
        oggetto = input("Inserire l'oggetto per traking (quello che cercheresti su subito)\n=>")
        os.system('cls')
        prezzoMinimo = input("Inserisci il prezzo minimo\n=>")
        os.system('cls')
        prezzoMassimo = input("Inserisci il prezzo massimo\n=>")
        if categoria == "1":
            cat = "auto"

            #risposta = input("Desidera inserire altri filtri (1 si, altrimenti altro)\n=>")
            #os.system('cls')
            #if risposta == "1":
            #    kmMin = input("Inserisci il chilometraggio minimo\n=>")
            #    os.system('cls')
            #    kmMax = input("Inserisci il chilometraggio massimo\n=>")
            #    os.system('cls')
            #    carburante = input("Inserire carburante: \n\n1)Benzina\n2)Diesel\n3)Metano\n4)Elettrico\n=>")
            #    os.system('cls')
            #    annoImmatricolazione = input("Anno Immatricolazione\n=>")
            #    os.system('cls')
            #    preferenze = input("vuoi ricevere anche annunci simili oppure SOLO quelli con i filtri soddisfatti?\n=>")
            #    os.system('cls')


            LINK = "https://www.subito.it/annunci-italia/vendita/usato/?q=" + oggetto
            PRE_LINK_ANNUNCIO = "https://www.subito.it/" + cat

            minPrice = -1
            maxPrice = -1

            response = requests.get(LINK)
            response.raise_for_status()
            soup = bs4.BeautifulSoup(response.text, 'html.parser')
            div_annunci = soup.find('div',
                                        class_='ListingContainer_col__1TZpb ListingContainer_items__3lMdo col items')

            a_annunci = div_annunci.find_all('a')
            p_paragraf = div_annunci.find_all('p')
            link_annunci = []
            prezzi_annunci = []

            #for heading in soup.find_all(["h1", "h2", "h3"]):
            #    print(heading.name + ' ' + heading.text.strip())

            with open('risultati_salvati.csv', newline='') as csvfile:
                data = list(csv.reader(csvfile))
                if len(data) != 0:
                    data_unboxed = data[0]
                else:
                    data_unboxed = None

            for a_annuncio in a_annunci:
                link_annuncio = str(a_annuncio.get('href'))

                price = ''.join(text.strip() for text in a_annuncio.p.find_all(text=True, recursive=False))
                #if carburante == "1":
                #    carb = "Benzina"
                #elif carburante == "2":
                #    carb = "Diesel"
                #elif carburante == "3":
                #    Carb = "Metano"
                #else:
                #    Carb = "Elettrico"

                ##if carburante is None:
                ##    carb = ''.join(text.strip() for text in a_annuncio.p.find_all(text=True, recursive=False))
                ##    pprint(carb)

                # print(soup.find_all("h2"))
                price = price[:-2]
                if len(price) != 0:
                    for c in ",.":
                        price = price.replace(c, "")
                    p = int(price)
                    min_ = int(prezzoMinimo)

                    max_ = int(prezzoMassimo)
                    #pprint("Benzina" in a_annuncio)
                    #pprint(carb)
                    if (min_ != -1 and min_ <= p) and (max_ != -1 and max_ >= p): #and ((carb in a_annuncio)==""):
                        try:
                            print(data_unboxed.index(link_annuncio))
                            print("elemento già in lista")
                        except:
                            f = open('risultati_salvati.csv', 'a')
                            # f.write('%s\s' % link_annuncio)
                            f.write('%s,' % link_annuncio)
                            f.close()
                            await invia_messaggio(
                                "Nuovo Annuncio trovato! Prezzo: " + price + ", Link: " + link_annuncio)
                        if PRE_LINK_ANNUNCIO in link_annuncio:
                            link_annunci.append(link_annuncio)
        if categoria == "2":
            cat = "Telefonia"
            risposta = input("Desidera inserire altri filtri? (si=1)")
            if risposta == "1":
                Memoria = input("Memoria Telefono (GB minimi)\n=>")
                os.system('cls')
                preferenze = input(
                    "vuoi ricevere anche annunci simili oppure SOLO quelli con i filtri soddisfatti?\n=>")
                os.system('cls')

            LINK = "https://www.subito.it/annunci-italia/vendita/usato/?q=" + oggetto
            PRE_LINK_ANNUNCIO = "https://www.subito.it/" + cat

            minPrice = -1
            maxPrice = -1

            response = requests.get(LINK)
            response.raise_for_status()
            soup = bs4.BeautifulSoup(response.text, 'html.parser')
            div_annunci = soup.find('div',
                                    class_='ListingContainer_col__1TZpb ListingContainer_items__3lMdo col items')

            a_annunci = div_annunci.find_all('a')
            p_paragraf = div_annunci.find_all('p')
            link_annunci = []
            prezzi_annunci = []

            for heading in soup.find_all(["h1", "h2", "h3"]):
                print(heading.name + ' ' + heading.text.strip())

            with open('risultati_salvati.csv', newline='') as csvfile:
                data = list(csv.reader(csvfile))
                if len(data) != 0:
                    data_unboxed = data[0]
                else:
                    data_unboxed = None

            for a_annuncio in a_annunci:
                link_annuncio = str(a_annuncio.get('href'))

                price = ''.join(text.strip() for text in a_annuncio.p.find_all(text=True, recursive=False))
                pprint(price)

                # print(soup.find_all("h2"))
                price = price[:-2]
                if len(price) != 0:
                    for c in ",.":
                        price = price.replace(c, "")
                    p = int(price)
                    min_ = int(prezzoMinimo)
                    max_ = int(prezzoMassimo)
                    if (min_ != -1 and min_ <= p) and (max_ != -1 and max_ >= p):
                        try:
                            print(data_unboxed.index(link_annuncio))
                            print("elemento già in lista")
                        except:
                            f = open('risultati_salvati.csv', 'a')
                            # f.write('%s\s' % link_annuncio)
                            f.write('%s,' % link_annuncio)
                            f.close()
                            await invia_messaggio(
                                "Nuovo Annuncio trovato! Prezzo: " + price + ", Link: " + link_annuncio)
                        if PRE_LINK_ANNUNCIO in link_annuncio:
                            link_annunci.append(link_annuncio)

        if categoria != "1" and categoria != "2":
            cat = ""
            LINK = "https://www.subito.it/annunci-italia/vendita/usato/?q=" + oggetto
            PRE_LINK_ANNUNCIO = "https://www.subito.it/" + cat

            minPrice = -1
            maxPrice = -1

            response = requests.get(LINK)
            response.raise_for_status()
            soup = bs4.BeautifulSoup(response.text, 'html.parser')
            div_annunci = soup.find('div',
                                    class_='ListingContainer_col__1TZpb ListingContainer_items__3lMdo col items')

            a_annunci = div_annunci.find_all('a')
            p_paragraf = div_annunci.find_all('p')
            link_annunci = []
            prezzi_annunci = []

            minPrice = prezzoMinimo

            maxPrice = prezzoMassimo

            # if args.memory:
            #    memory = args.memory

            for heading in soup.find_all(["h1", "h2", "h3"]):
                print(heading.name + ' ' + heading.text.strip())

            with open('risultati_salvati.csv', newline='') as csvfile:
                data = list(csv.reader(csvfile))
                if len(data) != 0:
                    data_unboxed = data[0]
                else:
                    data_unboxed = None

            for a_annuncio in a_annunci:
                link_annuncio = str(a_annuncio.get('href'))

                price = ''.join(text.strip() for text in a_annuncio.p.find_all(text=True, recursive=False))

                # print(soup.find_all("h2"))
                price = price[:-2]
                min_ = int(minPrice)
                max_ = int(maxPrice)
                if len(price) != 0:
                    for c in ",.":
                        price = price.replace(c,"")
                        print(price)
                        p = int(price)
                    if (min_ != -1 and min_ <= p) and (max_ != -1 and max_ >= p):
                        try:
                            print(data_unboxed.index(link_annuncio))
                            print("elemento già in lista")
                        except:
                            f = open('risultati_salvati.csv', 'a')
                            # f.write('%s\s' % link_annuncio)
                            f.write('%s,' % link_annuncio)
                            f.close()
                            await invia_messaggio(
                                "Nuovo Annuncio trovato! Prezzo: " + price + ", Link: " + link_annuncio)
                        if PRE_LINK_ANNUNCIO in link_annuncio:
                            link_annunci.append(link_annuncio)



        # Invia una notifica Telegram per ogni nuovo link trovato
        ##for link in links:
        ##    bot = Bot(token=BOT_TOKEN)
        ##    bot.send_message(chat_id=CHAT_ID, text="messaggio")


        #if new_link_annunci: (--> web <--)
        #    print('ci sono nuovi risultati')
        #    for new_link in new_link_annunci:
        #        webbrowser.open(new_link)
        #else:
        #    print('nuovo annuncio')

        #input('tutto apposto bro')


if __name__ == "__main__":
    while True:
        loop = asyncio.get_event_loop()
        loop.run_until_complete(main())
        time.sleep(120)
