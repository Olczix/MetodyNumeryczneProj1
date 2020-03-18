from matplotlib import pyplot as plt
import matplotlib.patches as mpatches
import matplotlib.dates as mdates
import numpy as np
import math

def ExponentialMovingAverageEMA (probki,dzis,ileDniWstecz):
        nawias=1-2/(ileDniWstecz+1)
        licznik=0.0
        mianownik=0.0

        for i in range(ileDniWstecz):
            tmp= pow(nawias,i)
            if (dzis-i>0):
                licznik=licznik+tmp*probki[dzis-1-i]
            else:
                licznik=licznik+tmp*probki[0]

            mianownik=mianownik+tmp

        return licznik/mianownik


def MacdValue(probki, dzis):
    return ExponentialMovingAverageEMA(probki,dzis,12)-ExponentialMovingAverageEMA(probki,dzis,26)


def SignalValue(probki,dzis):
    return ExponentialMovingAverageEMA(probki, dzis, 9)


ileKasy = 1000 # nasz kapital
ileEuro = 0  #ilosc euro w naszej kieszeni
PLN = [None]*1000
PLN[1]=1000.0
EURO =[None]*1000
EURO[1]=0.0

# create Vectors to store information about Euro

N = 1000
dane = [None] * 1000
data = [None] * N
euroValues = [None] * N
macdValues = [None] * N
signalValues = [None] * N
t = [None] * N
kup = [None] * N
sprzedaj = [None] * N
it = 0

#pobranie danych wejsciowych (1000x'dzien,wartoscEuroDanegoDnia')
file = open ("data.txt","r")
for line in file:
    a=line
    dane[it]=a
    it=it+1
file.close()

#rozdzielenie danych - osobno dat i wartości - do dwóch wektorów
for i in range(N):
    x=dane[N-1-i].split(',')
    data[i]=x[0]
    euroValues[i]=float(x[1])

#obliczenie wartosci wskaznika Macd i Signal dla poszczegolnych dni
for i in range(1000):
    t[i]=i
    macdValues[i]=MacdValue(euroValues,i+1)
    signalValues[i]=SignalValue(macdValues,i+1)


print("BEFORE: ")
print("PLN: ",ileKasy," €:", ileEuro)

#detekcja miejsc kiedy kupic/sprzedac
for i in range(999): #dla kazdego dnia
    if (macdValues[i]<signalValues[i] and macdValues[i+1]>=signalValues[i+1] and ileKasy>0): #Macd przecina Signal z dolu - KUP EURO ZA POSIADANE PIENIADZE
        kup[i]=data[i]
        ileEuro += ileKasy/euroValues[i+1]
        ileKasy=0


    elif (macdValues[i]>signalValues[i] and macdValues[i+1]<signalValues[i+1] and ileEuro>0): #Macd przecina Signal z gory - SPRZEDAJ POSIADANE EURO
        sprzedaj[i]=data[i]
        ileKasy += ileEuro*euroValues[i+1]
        ileEuro=0

    EURO[i]=ileEuro
    PLN[i]=ileKasy


print("AFTER: ")
print("PLN: ",ileKasy," €:", ileEuro)


print("\n\n")
for i in range(1000):
    if(kup[i] != None):
        print("BUY: ", kup[i]," PLN: ",PLN[i]," €: ", EURO[i], " EuroValue: ",euroValues[i] )
    if (sprzedaj[i] != None):
        print("SELL: ", sprzedaj[i]," PLN: ",PLN[i]," €: ", EURO[i], " EuroValue: ",euroValues[i])




#wykres
fig = plt.figure()

#First plot - value of euro - one line
ax = fig.add_subplot(2,1,1)
plt.plot(data, euroValues, color='green')
plt.xticks(rotation=60)
plt.xlim(min(data),max(data))
ax.xaxis.set_major_locator(mdates.MonthLocator(bymonth=None, bymonthday=1, interval=1, tz=None))
plt.title('Kurs Euro')
plt.ylabel('Value of Euro')

#Second plot - Macd+Signal - two lines + legend
ax = fig.add_subplot(2,1,2)
plt.title('Wskaznik MACD')
plt.plot(data,macdValues,color='red',label='Macd')
plt.plot(data,signalValues,color='b',label='Signal')
plt.xticks(rotation=60)
plt.xlim(min(data),max(data))
ax.xaxis.set_major_locator(mdates.MonthLocator(bymonth=None, bymonthday=1, interval=1, tz=None))

#Placing a legend
plt.legend(bbox_to_anchor=(1.02, 1), loc='upper left', borderaxespad=0.)

#Showing plots and adjusting them to the screen
plt.subplots_adjust(top=0.95, bottom=0.15, left=0.06, right=0.90, hspace=0.6, wspace=0.5)

plt.show()

