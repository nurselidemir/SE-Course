import threading
import time
import random


sira_semaforu = threading.Semaphore(0) 
kontrol_kilidi = threading.Lock() 
binis_tamamlandi = threading.Semaphore(0) 
inis_tamamlandi = threading.Semaphore(0)  

trendeki_yolcular = []  
tren_yolcu_sayisi = 0 
tren_kilidi = threading.Lock()  


class Yolcu(threading.Thread):
    def __init__(self, yolcu_id, kapasite):
        super().__init__()
        self.yolcu_id = yolcu_id
        self.kapasite = kapasite

    def trene_bin(self):
        global tren_yolcu_sayisi

       
        sira_semaforu.acquire()
        with kontrol_kilidi:  
            global trendeki_yolcular
            trendeki_yolcular.append(self.yolcu_id)
            tren_yolcu_sayisi += 1
            print(f"Yolcu {self.yolcu_id} trene bindi.")

            
            if tren_yolcu_sayisi == self.kapasite:
                binis_tamamlandi.release()

        
        inis_tamamlandi.acquire()

    def run(self):
        while True:
            time.sleep(random.uniform(0.1, 1))
            self.trene_bin() 
class Tren(threading.Thread):
    def _init_(self, kapasite, tur_sayisi):
        super()._init_()
        self.kapasite = kapasite
        self.tur_sayisi = tur_sayisi

    def run(self):
        global tren_yolcu_sayisi
        for tur in range(1, self.tur_sayisi + 1):
           
            for _ in range(self.kapasite):
                sira_semaforu.release()

            
            binis_tamamlandi.acquire()

            
            print(f"Tren {tur}. turda şu yolcularla hareket ediyor: {trendeki_yolcular}")
            time.sleep(random.uniform(0.5, 1))  

            
            for _ in range(self.kapasite):
                inis_tamamlandi.release()

           
            with tren_kilidi:
                tren_yolcu_sayisi = 0
                trendeki_yolcular.clear()

        print("Tren bakım için durduruldu.")


