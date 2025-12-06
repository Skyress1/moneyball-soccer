"""
FBref'ten gerçek futbol verilerini çekme scripti
2024-2025 sezonu için Avrupa'nın top 5 liginden oyuncu istatistikleri
"""

import pandas as pd
import time
import warnings
warnings.filterwarnings('ignore')

print("=" * 60)
print("GERÇEK FUTBOL VERİLERİ İNDİRİLİYOR")
print("Kaynak: FBref.com (StatsBomb)")
print("=" * 60)

try:
    # soccerdata paketini kullan
    import soccerdata as sd
    
    print("\n[1/5] Soccerdata paketi yüklendi...")
    
    # FBref reader oluştur
    fbref = sd.FBref(leagues=['ENG-Premier League', 'ESP-La Liga', 'ITA-Serie A', 
                              'GER-Bundesliga', 'FRA-Ligue 1'], 
                     seasons='2024-2025')
    
    print("[2/5] FBref bağlantısı kuruldu...")
    print("      Ligler: Premier League, La Liga, Serie A, Bundesliga, Ligue 1")
    print("      Sezon: 2024-2025")
    
    # Oyuncu istatistiklerini çek
    print("\n[3/5] Oyuncu istatistikleri indiriliyor...")
    print("      (Bu işlem birkaç dakika sürebilir, lütfen bekleyin...)")
    
    # Standard stats
    stats = fbref.read_player_season_stats(stat_type='standard')
    print("      [OK] Standard istatistikler indirildi")
    
    time.sleep(6)  # FBref rate limit: 6 saniye bekle
    
    # Shooting stats
    shooting = fbref.read_player_season_stats(stat_type='shooting')
    print("      [OK] Sut istatistikleri indirildi")
    
    time.sleep(6)
    
    # Passing stats
    passing = fbref.read_player_season_stats(stat_type='passing')
    print("      [OK] Pas istatistikleri indirildi")
    
    time.sleep(6)
    
    # Defensive stats
    defense = fbref.read_player_season_stats(stat_type='defense')
    print("      [OK] Defansif istatistikler indirildi")
    
    time.sleep(6)
    
    # Possession stats
    possession = fbref.read_player_season_stats(stat_type='possession')
    print("      [OK] Top hakimiyeti istatistikleri indirildi")
    
    print("\n[4/5] Veriler birleştiriliyor...")
    
    # Tüm verileri birleştir
    df = stats.reset_index()
    
    # Diğer istatistikleri ekle
    for stat_df in [shooting, passing, defense, possession]:
        stat_df_reset = stat_df.reset_index()
        df = df.merge(stat_df_reset, on=['player', 'team', 'league', 'season'], 
                     how='left', suffixes=('', '_dup'))
    
    # MultiIndex kolonları düzelt (eğer varsa)
    if isinstance(df.columns, pd.MultiIndex):
        df.columns = ['_'.join(map(str, col)).strip('_') for col in df.columns.values]
    
    # Duplicate kolonları temizle
    dup_cols = [col for col in df.columns if col.endswith('_dup')]
    df = df.drop(columns=dup_cols)
    
    print(f"      [OK] Toplam {len(df)} oyuncu verisi birlestirildi")
    
    # Veriyi kaydet
    df.to_csv('players_real_data.csv', index=False, encoding='utf-8')
    print("\n[5/5] Veriler 'players_real_data.csv' dosyasına kaydedildi")
    
    # Özet bilgiler
    print("\n" + "=" * 60)
    print("VERİ SETİ ÖZETİ")
    print("=" * 60)
    print(f"Toplam Oyuncu: {len(df)}")
    print(f"\nLiglere Göre Dağılım:")
    print(df['league'].value_counts())
    print(f"\nİlk 5 Satır:")
    print(df.head())
    
    print("\n[OK] Islem basariyla tamamlandi!")
    print("  Dosya: players_real_data.csv")
    
except ImportError:
    print("\n[HATA] 'soccerdata' paketi bulunamadi!")
    print("\nYükleme için:")
    print("  pip install soccerdata")
    print("\nAlternatif olarak manuel web scraping kullanılacak...")
    
    # Manuel scraping alternatifi
    import requests
    from bs4 import BeautifulSoup
    
    print("\n" + "=" * 60)
    print("MANUEL WEB SCRAPING BAŞLATILIYOR")
    print("=" * 60)
    
    # Premier League Big 5 Stats URL
    url = "https://fbref.com/en/comps/Big5/stats/players/Big-5-European-Leagues-Stats"
    
    print(f"\n[1/3] FBref'e bağlanılıyor...")
    print(f"      URL: {url}")
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
    }
    
    try:
        response = requests.get(url, headers=headers, timeout=30)
        response.raise_for_status()
        
        print("[2/3] HTML parse ediliyor...")
        
        # Pandas ile HTML tablolarını oku
        tables = pd.read_html(response.content)
        
        if len(tables) > 0:
            df = tables[0]  # İlk tablo genellikle oyuncu istatistikleridir
            
            # Çoklu seviye kolonları düzelt
            if isinstance(df.columns, pd.MultiIndex):
                df.columns = ['_'.join(col).strip() for col in df.columns.values]
            
            print(f"      [OK] {len(df)} oyuncu verisi cekildi")
            
            # Veriyi kaydet
            df.to_csv('players_real_data.csv', index=False, encoding='utf-8')
            print("\n[3/3] Veriler 'players_real_data.csv' dosyasına kaydedildi")
            
            # Özet
            print("\n" + "=" * 60)
            print("VERİ SETİ ÖZETİ")
            print("=" * 60)
            print(f"Toplam Oyuncu: {len(df)}")
            print(f"\nKolonlar: {len(df.columns)}")
            print(f"\nİlk 5 kolon:")
            print(df.columns[:5].tolist())
            
            print("\n[OK] Islem basariyla tamamlandi!")
            
        else:
            print("[HATA] Tablo bulunamadi!")
            
    except Exception as e:
        print(f"\n[HATA]: {str(e)}")
        print("\nManuel indirme başarısız oldu.")
        print("Lütfen şu adımları deneyin:")
        print("1. pip install soccerdata")
        print("2. Script'i tekrar çalıştırın")

except Exception as e:
    print(f"\n[HATA]: {str(e)}")
    print("\nDetaylar:")
    import traceback
    traceback.print_exc()
