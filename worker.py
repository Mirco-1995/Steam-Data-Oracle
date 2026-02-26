import requests
import sqlite3
import time
from datetime import datetime
import os

os.makedirs('data', exist_ok=True)
DB_PATH = "data/market_data.db"

def init_db():
    conn = sqlite3.connect(DB_PATH)
    conn.execute('''CREATE TABLE IF NOT EXISTS prices 
                    (item_name TEXT, price REAL, timestamp DATETIME)''')
    conn.commit()
    conn.close()

def fetch_and_store(item):
    url = "https://steamcommunity.com/market/priceoverview/"
    params = {'appid': 730, 'currency': 3, 'market_hash_name': item}
    
    r = requests.get(url, params=params)
    data = r.json()
    
    if data.get('success'):
        raw_price = data.get('lowest_price')
        price_num = float(raw_price.replace('€', '').replace(',', '.').strip())
        
        conn = sqlite3.connect(DB_PATH)
        conn.execute("INSERT INTO prices VALUES (?, ?, ?)", (item, price_num, datetime.now()))
        conn.commit()
        conn.close()
        print(f"Salvato: {item} - {price_num}€")

if __name__ == "__main__":
    init_db()
    item_to_track = "Recoil Case"
    while True:
        fetch_and_store(item_to_track)
        time.sleep(600)