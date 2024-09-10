import numpy as np
import matplotlib.pyplot as plt
import random
import tkinter as tk
import csv
import pygame
import time

#Alustetaan pygame
pygame.mixer.init()
#Ladataan äänitiedostot
ernestin_askel = pygame.mixer.Sound('ernesti_askel.wav')
kernestin_askel = pygame.mixer.Sound('kernesti_askel.wav')

#Luodaan funktio joka soittaa äänen
def play_sound(sound):
    sound.stop()
    sound.play()
    #pygame.time.wait(int(sound.get_length() * 1000))

#Alustetaan tkinter ikkuna
root = tk.Tk()
canvas = tk.Canvas(root, width=400, height=400)
canvas.pack()

#Luodaan teksti laatikko
teksti_label = tk.Label(root, text='Ernesti ja kernesti juoksee!')
teksti_label.pack()

# Piirretään lähtöviiva ja maaliviiva
canvas.create_line(20, 400, 20, 22, fill='black', width=2)
canvas.create_line(350, 400, 350, 20, fill='white', width=2)

# Luodaan label tulokselle:
tulos_label = tk.Label(root, text='Tulokset näkyvät tässä!')
tulos_label.pack()

# Keksitään Ernestille ja Kernestille keskiaika juoksulle
ernesti_keskiaika = 12.00
kernesti_keskiaika = 12.00



# luodaa funktio tulosten näyttämiseen
#def tulokset_teksti(tulos_tulokset):
    #ernesti_aika = tulos_tulokset.get['Ernesti']
    #kernesti_aika = tulos_tulokset.get['Kernesti']
    #return f"Ernesti: {ernesti_aika} s\nKernesti: {kernesti_aika} s"

def ilmoita_voittaja(tulos_tulokset):
    ernestin_aika = tulos_tulokset.get('Ernesti',float('inf'))
    kernestin_aika = tulos_tulokset.get('Kernesti',float('inf'))

    if ernestin_aika < kernestin_aika:
        voittaja = 'Ernesti voitti!'
    elif kernestin_aika < ernestin_aika:
        voittaja = 'Kernesti voitti!'
    else:
        voittaja = 'Tasapeli!'
    #siivoillaan tulokset
    tulokset_teksti_siivottuna = (
       f"Ernesti:{ernestin_aika:.2f} s\n"
       f"Kernesti:{kernestin_aika:.2f} s"
      
   )
    tulos_label.config(text=f"{tulokset_teksti_siivottuna}\n{voittaja}")

# Ernestin ja kernestin juoksu animaatio
def animate_hahmo(nimi, hahmon_juoksu_aika,hahmon_vari, y_alku):
 
    # lähtöpaikka ja nopeuden määrittely
    x_loppu = 330
    x_alku = 20
    matka = x_loppu - x_alku

    #Määritellään nopeus pikseleinä per sekuntti
    perus_nopeus = matka / hahmon_juoksu_aika
    vaihtelu = 50.0

    #Piirretään Ernesti tai Kernesti
    hahmo_kuva = canvas.create_oval(x_alku,y_alku,x_alku +20,y_alku + 20, fill=hahmon_vari) 

    # Alustetaan askel laskuri
    askel_laskuri = 0
    askel_vali = 10

    # Päivitetään ernestin sijaintia, kunnes hän on maalissa
    def liikuta():
        nonlocal x_alku, askel_laskuri
        global tulos_tulokset
        if x_alku < x_loppu:
            # Satunnaistetaan nopeus
            satunnais_nopeus = perus_nopeus + random.uniform(-vaihtelu, vaihtelu)
            x_alku += satunnais_nopeus * 0.01 
            canvas.move(hahmo_kuva, satunnais_nopeus * 0.01, 0) #liikuttaa hahmoa
            # Päivitetään askel laskuria
            askel_laskuri += satunnais_nopeus * 0.01
            # Jos askel laskuri on suurempi kuin askel väli, soita ääni ja nollaa askel laskuri
            if askel_laskuri >= askel_vali:
                if nimi == 'Ernesti':
                    play_sound(ernestin_askel)
                if nimi == 'Kernesti':
                    play_sound(kernestin_askel)
                askel_laskuri = 0
            # Päivitetään ikkunaa
            root.after(10, liikuta) # odottaa 10ms ja liikuttaa ernestiä uudestaan
        else:
            pygame.mixer.stop()
            print(nimi, 'on maalissa!')
            tulos_tulokset[nimi]=hahmon_juoksu_aika
            print(tulos_tulokset)
            if len(tulos_tulokset) == 2:
                print('Kilpailu on päättynyt!')
                ilmoita_voittaja(tulos_tulokset)
                

    liikuta()
# Tehdän harjoittelulle oma funktio
def harjoittelu_animaatio(nimi, hahmon_juoksu_aika, hahmon_vari, y_alku, harjoituksen_kesto):
    print("Harjoitellaan!")
    x_loppu = 330
    x_alku = 20
    matka = x_loppu - x_alku
    perus_nopeus = matka / hahmon_juoksu_aika
    vaihtelu = 50.0

    hahmo_kuva = canvas.create_oval(x_alku,y_alku,x_alku +20,y_alku + 20, fill=hahmon_vari)

    askel_laskuri = 0
    askel_vali = 15
    harjoittelun_alku = time.time()

    def liikuta():
        nonlocal x_alku, askel_laskuri
        aikaskaaluskerroin = 28800/60
        nykyinen_aika = time.time()
        skaalattu_aika = (nykyinen_aika - harjoittelun_alku)*aikaskaaluskerroin
        #tarkistetaan onko harjoitusaika päättynyt
        if nykyinen_aika - harjoittelun_alku > harjoituksen_kesto:
            print('Harjoittelu on päättynyt!')
            return
        if x_alku < x_loppu:
            # Satunnaistetaan nopeus
            satunnais_nopeus = perus_nopeus + random.uniform(-vaihtelu, vaihtelu) * aikaskaaluskerroin
            x_alku += satunnais_nopeus * 0.01 
            canvas.move(hahmo_kuva, satunnais_nopeus * 0.01, 0) #liikuttaa hahmoa
            # Päivitetään askel laskuria
            askel_laskuri += satunnais_nopeus * 0.01
            # Jos askel laskuri on suurempi kuin askel väli, soita ääni ja nollaa askel laskuri
            if askel_laskuri >= askel_vali:
                if nimi == 'Ernesti':
                    play_sound(ernestin_askel)
                if nimi == 'Kernesti':
                    play_sound(kernestin_askel)
                askel_laskuri = 0
            # Päivitetään ikkunaa
            root.after(10, liikuta) # odottaa 10ms ja liikuttaa ernestiä uudestaan
        else:
            print("Aloitetaan uusi harjoitus!")
            pygame.mixer.stop()
            x_alku = 20
            canvas.coords(hahmo_kuva, x_alku, y_alku, x_alku + 20, y_alku + 20)
            kernesti_lepo = random.randint(10000, 20000)
            ernesti_lepo = random.randint(10000, 20000)
            if nimi == 'Ernesti':
                root.after(ernesti_lepo, liikuta)
                print('Ernesti lepää', ernesti_lepo, 'millisekuntia')
            else:
                root.after(kernesti_lepo, liikuta)
                print('Kernesti lepää', kernesti_lepo, 'millisekuntia')
    liikuta()

# Tehdään dictionary maailman ennätys ajoista. Tiedoista löytyy aika, vuosi, kuka on tehnyt. 
# world_records = {}
# with open('100m_records_only.csv') as file:
#     reader = csv.DictReader(file, delimiter=';')
#     for row in reader:
#         time = float (row['Time'].strip())
#         athlete = row['Athlete'].strip()
#         date = row['Date'].strip()

#         year = int(date.split('-')[0])  # Erotetaan datesta vuosi 
#         world_records[year] = [time, athlete]
   
# # Erotellaan vuodet ja ajat listaksi graafia varten
# years = list(world_records.keys())
# times = [world_records[year][0] for year in years]

# # Ennustetaan ajankehitys vuoteen 2050 yksinkertaisella extrapolaatiolla
# future_years = list(range(max(years) + 1, 2051))
# last_time = times[-1]

# # Tässä yksinkertaisessa esimerkissä oletetaan, että aika paranee tasaisesti (noin 0.01 sekuntia vuodessa)
# predicted_times = [last_time - 0.01 * (year - max(years)) for year in future_years]

# # Päivitetään sanakirja ennustetuilla arvoilla
# for year, time in zip(future_years, predicted_times):
#     world_records[year] = [time, "Predicted"]

# # Päivitetään vuodet ja ajat listaksi
# all_years = list(world_records.keys())
# all_times = [world_records[year][0] for year in all_years]

# Luodaan graafi
#plt.figure(figsize=(12, 6))
#plt.plot(years, times, marker='o', linestyle='-', color='blue', label="Nykyiset ennätykset")
#plt.plot(future_years, predicted_times, linestyle='--', color='red', label="Ennustetut ennätykset")
#plt.title("100 metrin maailmanennätysajan kehittyminen (1912-2050)")
#plt.xlabel("Vuosi")
#plt.ylabel("Aika (sekunteina)")
#plt.legend()
#plt.grid(True)
#plt.show()

# Seuraavaksi luodaa leijonia sanakirjaan. Leijonista on seuraavat tiedot: nimi ja juoksu nopeus.
lions = {
    'Simba': 6.00,
    'Nala': 6.10,
    'Mufasa': 6.20,
    'Scar': 6.30,
    'Zazu': 6.40,
    'Leo': 6.50,
    'Kovu': 6.60,
    'Kiara': 10.70,
    'Timon': 6.80,
    'Pumbaa': 7.90
}
# Lisätään leijonatiedot sanakirjaan
# world_records['lions'] = lions

# Funktio joka tapahtuu kun nappia painaa
def ernesti_juoksee():

    # satunnaistetaan Ernestin juoksu aika
    ernestin_juoksu_aika = ernesti_keskiaika + random.uniform(-1, 1)
    print('Ernersti juoksi 100 metriä ajassa', ernestin_juoksu_aika, 'sekuntia')

    # Käynnistetään Ernestin animaatio
    animate_hahmo("Ernesti", ernestin_juoksu_aika, 'blue',y_alku=30)

def kernesti_juoksee():
    # satunnaistetaan Kernestin juoksu aika
    kernestin_juoksu_aika = kernesti_keskiaika + random.uniform(-1, 1)
    print('Kernesti juoksi 100 metriä ajassa', kernestin_juoksu_aika, 'sekuntia')

    # Käynnistetään Kernestin animaatio
    animate_hahmo("Kernesti", kernestin_juoksu_aika, 'red',y_alku=60)

def yhteislahto():
    ernestin_juoksu_aika = ernesti_keskiaika + random.uniform(-1, 1)
    kernestin_juoksu_aika = kernesti_keskiaika + random.uniform(-1, 1)
    #Luodaan globaali muuttuja tuloksille
    global tulos_tulokset
    tulos_tulokset = {}
    animate_hahmo("Ernesti", ernestin_juoksu_aika, 'blue',y_alku=180)
    animate_hahmo("Kernesti", kernestin_juoksu_aika, 'red',y_alku=220)

def harjoittele_paiva():
    harjoittelu_animaatio("Ernesti", ernesti_keskiaika, 'blue',y_alku=180,harjoituksen_kesto=28800)
    harjoittelu_animaatio("Kernesti", kernesti_keskiaika, 'red',y_alku=220,harjoituksen_kesto=28800)
    


# Täällä on napit
Ernesti_nappi = tk.Button(root, text='Ernesti', command=ernesti_juoksee)
Ernesti_nappi.pack()
Kernesti_nappi = tk.Button(root, text='Kernesti', command=kernesti_juoksee)
Kernesti_nappi.pack()
yhteis_nappi = tk.Button(root, text='kisa lähtö', command=yhteislahto)
yhteis_nappi.pack()
harjoittele_paiva = tk.Button(root, text='Harjoittele päivä', command=harjoittele_paiva)
harjoittele_paiva.pack()



root.mainloop()
