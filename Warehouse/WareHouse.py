import copy


# Müşterinin Maliyetlerini Sıralayan Fonksiyon
def musterimaliyet():
    global musteriSiralama
    for i in range(0, mSayac):  # Müşteri sayısı kadar dönüyor
        musteriSiralama.append(sorted(range(0, whSayac), key=lambda index: mMaliyet[i][index]))


mMaliyet = []
musteriSiralama = []  # global tanımlama
whSayac = 0
mSayac = 0


def Hesapla():
    deger = 0.0
    for warehouse, musteriListe in wcMap.items():  # wcMap dictionary deki verileri warehouse ve musteriListe listelerine atıyor.
        deger += whMaliyet[warehouse]
        for maliyet in musteriListe:
            deger += mMaliyet[maliyet][warehouse]
    return deger


wcMap = {}
whMaliyet = []


def kontrol(musteri):  # kapasite kontrolü
    global openMap
    global whKapasite
    global wcMap

    ListeMaliyet = musteriSiralama[musteri]

    for warehouse in ListeMaliyet:
        if openMap[warehouse] == False:
            continue
        if whKapasite[warehouse] < mSize[musteri]:
            continue
        else:
            if warehouse in wcMap:
                wcMap[warehouse].append(musteri)
            else:
                wcMap[warehouse] = [musteri]

            whKapasite[warehouse] -= mSize[musteri]
            return True

    return False


def greedy():  # depe işlemleri
    global minDeger
    listeTalep = sorted(range(0, mSayac), key=lambda index: mSize[index], reverse=True)

    for index in listeTalep:
        kontrol(index)

    minDeger = Hesapla()


minDeger = 0.0
mSize = []


def wareHouseCopy(warehouse):  # kopyalama işlemi kontrol
    global wcMap
    global whKapasite
    global minDeger

    localwcMap = copy.deepcopy(wcMap)
    localwhKapasite = copy.deepcopy(whKapasite)
    durum = True

    if warehouse not in wcMap:
        return False

    openMap[warehouse] = False
    listeMusteri = wcMap[warehouse][:]
    for musteri in listeMusteri:
        if kontrol(musteri) == False:
            durum = False
            break

    if durum == False:
        wcMap = localwcMap
        whKapasite = localwhKapasite
        openMap[warehouse] = True
        return False
    else:
        wcMap[warehouse] = []
        del wcMap[warehouse]
        value = Hesapla()
        if value >= minDeger:
            wcMap = localwcMap
            whKapasite = localwhKapasite
            openMap[warehouse] = True
            return False
        else:
            minDeger = value
            return True


whKapasite = []
openMap = {}


def tasi():
    wlist = sorted(range(0, whSayac), key=lambda index: wareHouse[index][1] / wareHouse[index][0],
                   reverse=True)
    for warehouse in wlist:
        if openMap[warehouse] == True:
            wareHouseCopy(warehouse)


wareHouse = []


def listeFormat():
    returnList = [0] * mSayac
    for warehouse, listeMaliyet in wcMap.items():
        for cust in listeMaliyet:
            returnList[cust] = warehouse

    return returnList


def main(data):
    global whSayac
    global mSayac

    lines = data.split('\n')
    parts = lines[0].split()
    whSayac = int(parts[0])  # dosyadan gelen verileri ayırma
    mSayac = int(parts[1])

    global wareHouse
    wareHouse = []
    global whKapasite
    global whMaliyet
    global openMap

    for i in range(1, whSayac + 1):
        line = lines[i]
        parts = line.split()
        wareHouse.append((int(parts[0]), float(parts[1])))  # ayrılmış verileri listeye atama
        whKapasite.append(int(parts[0]))
        whMaliyet.append(float(parts[1]))
        openMap[i - 1] = True

    global mSize
    global mMaliyet
    mSize = []
    mMaliyet = []

    lineIndex = whSayac + 1
    for i in range(0, mSayac):
        musteriSize = int(lines[lineIndex + 2 * i])
        musteriMaliyet = list(map(float, lines[lineIndex + 2 * i + 1].split()))
        mSize.append(musteriSize)
        mMaliyet.append(musteriMaliyet)

    musterimaliyet()
    greedy()
    tasi()
    dataLast = str(Hesapla()) + " 0\n"
    dataLast += " ".join(list(map(str, listeFormat())))  # en düşük değeri ve atanan depoları döndürme
    return dataLast


dosya_adi = open("wl_1000_1", 'r')
data = ''.join(dosya_adi.readlines())
dosya_adi.close()
print(main(data))



