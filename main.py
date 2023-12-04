import requests
import tkinter as tk
from tkinter import Label, Entry, Button, messagebox
import folium
import ipaddress
import webbrowser


#WoxicDEV
#İnstagram : woxicdev | mert.js_
#Yorum Satırları Eklenmiştir.
#Bazı kütüphaneleri ilk defa kullandım folium,ipadress vb. geliştirme aşamasındadır.

class IPKonumTakipUygulamasi:
    def __init__(self, ana_pencere):
        self.ana_pencere = ana_pencere
        ana_pencere.title('IP Sorgulama v1')
        ana_pencere.geometry('400x400')
        ana_pencere.configure(bg='#2E2E2E')  # Arka plan rengini ayarlayabilirsiniz buradan.


        self.arayuz_elemanlarini_olustur()

    def arayuz_elemanlarini_olustur(self):
        # Arayüz öğelerini oluşturduğum kısım
        self.ip_etiket = Label(self.ana_pencere, text='IP adresini girin:', bg='#2E2E2E', fg='white', font=('Arial', 12))
        self.ip_giris = Entry(self.ana_pencere, font=('Helvetica', 14), borderwidth=2, relief='solid')
        self.sonuc_etiket = Label(self.ana_pencere, text='IP bilgileri burada gösterilecek.', fg='white', bg='#2E2E2E', font=('Arial', 10))

        self.takip_butonu = Button(self.ana_pencere, text='IP Sorgula', command=self.ip_takip_et, bg='#4CAF50', fg='white', font=('Arial', 12), relief='flat', padx=10, pady=5, borderwidth=0, cursor='hand2')

        self.harita_butonu = Button(self.ana_pencere, text='Haritada Göster', command=self.haritada_goster, bg='#2196F3', fg='white', font=('Arial', 12), relief='flat', padx=10, pady=5, borderwidth=0, cursor='hand2')

        self.hakkinda_butonu = Button(self.ana_pencere, text='Hakkımda', command=self.hakkinda_goster, bg='#607D8B', fg='white', font=('Arial', 12), relief='flat', padx=10, pady=5, borderwidth=0, cursor='hand2')

        # Öğeleri yerleştirme bölümü
        self.ip_etiket.pack(pady=10)
        self.ip_giris.pack(pady=10)
        self.takip_butonu.pack(pady=10)
        self.harita_butonu.pack(pady=10)
        self.hakkinda_butonu.pack(pady=10)
        self.sonuc_etiket.pack(pady=10)

    def ip_takip_et(self):
        try:
            # IP takip et butonu tıklandığında çalışan fonksiyon
            ip_adresi = self.ip_giris.get()

            # IP adresi yazılan yer boşmu kontrol etme
            if not ip_adresi:
                raise ValueError("IP adresi boş olamaz.")

            # IP adresi formatına uygun mu kontrol etme
            ipaddress.IPv4Address(ip_adresi)

            ip_bilgisi = self.ip_bilgisini_al(ip_adresi)

            if 'error' in ip_bilgisi:
                self.sonuc_etiket.config(text=f"Hata: {ip_bilgisi['error']['info']}", fg='red')
            else:
                sonuc_metni = (
                    f"IP Adresi: {ip_bilgisi['ip']}\n"
                    f"Şehir: {ip_bilgisi.get('city', 'N/A')}\n"
                    f"Bölge: {ip_bilgisi.get('region', 'N/A')}\n"
                    f"Ülke: {ip_bilgisi.get('country', 'N/A')}\n"
                    f"Enlem: {ip_bilgisi.get('loc', 'N/A').split(',')[0]}\n"
                    f"Boylam: {ip_bilgisi.get('loc', 'N/A').split(',')[1]}\n"
                )
                self.sonuc_etiket.config(text=sonuc_metni, fg='white')
        except ValueError:
            self.sonuc_etiket.config(text="Hata: Geçersiz IP adresi formatı.", fg='red')

    def ip_bilgisini_al(self, ip_adresi):
        # API Kısmı ipstack kadar detaylı değil fakat daha kolay bence
        base_url = f'https://ipinfo.io/{ip_adresi}/json'
        response = requests.get(base_url)
        ip_bilgisi = response.json()
        return ip_bilgisi

    def haritada_goster(self):
        try:
            # Haritada göster butonu tıklandığında çalışan fonksiyon
            ip_adresi = self.ip_giris.get()

            # IP adresi boş mu kontrol etme
            if not ip_adresi:
                raise ValueError("IP adresi boş olamaz.")

            # IP adresi formatına uygun mu kontrol etme
            ipaddress.IPv4Address(ip_adresi)

            ip_bilgisi = self.ip_bilgisini_al(ip_adresi)

            if 'loc' in ip_bilgisi:
                enlem, boylam = ip_bilgisi['loc'].split(',')
                harita_dosya_adi = f'woxicdev_{ip_adresi.replace(".", "_")}.html'
                self.haritayi_goster(float(enlem), float(boylam), harita_dosya_adi)
            else:
                self.sonuc_etiket.config(text="Konum bilgisi mevcut değil.", fg='red')
        except ValueError:
            self.sonuc_etiket.config(text="Hata: Geçersiz IP adresi formatı.", fg='red')

    def haritayi_goster(self, enlem, boylam, harita_dosya_adi):
        # Haritayı oluştur ve göster
        harita = folium.Map(location=[enlem, boylam], zoom_start=12)
        folium.Marker(location=[enlem, boylam], popup='IP Konumu', icon=folium.Icon(color='red')).add_to(harita)
        harita.save(harita_dosya_adi)
        messagebox.showinfo('Harita Gösterildi', f'Harita "{harita_dosya_adi}" adlı dosyaya kaydedildi.')
        webbrowser.open(harita_dosya_adi, new=2)  # Haritayı tarayıcıda aç(varsayılan)

    def hakkinda_goster(self):
        messagebox.showinfo('Hakkında', 'LinkedIn :  Mert Ali Kaya | Github : Majestyy01')

if __name__ == "__main__":
    root = tk.Tk()
    app = IPKonumTakipUygulamasi(root)
    root.mainloop()
