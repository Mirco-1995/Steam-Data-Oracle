from fastapi import FastAPI
import sqlite3
import requests
import threading
import time
from datetime import datetime
import os

app = FastAPI()
DB_PATH = "data/market_data.db"
os.makedirs('data', exist_ok=True)

def init_db():
    conn = sqlite3.connect(DB_PATH)
    conn.execute('CREATE TABLE IF NOT EXISTS prices (item_name TEXT, price REAL, timestamp DATETIME)')
    conn.commit()
    conn.close()

def worker_logic():
    init_db()
    while True:
        try:
            url = "https://steamcommunity.com/market/priceoverview/"
            params = {'appid': 730, 'currency': 3, 'market_hash_name': 'Recoil Case'}
            r = requests.get(url, params=params)
            data = r.json()
            if data.get('success'):
                price_num = float(data.get('lowest_price').replace('€', '').replace(',', '.').strip())
                conn = sqlite3.connect(DB_PATH)
                conn.execute("INSERT INTO prices VALUES (?, ?, ?)", ('Recoil Case', price_num, datetime.now()))
                conn.commit()
                conn.close()
        except:
            pass
        time.sleep(600)

threading.Thread(target=worker_logic, daemon=True).start()

@app.get("/prezzo/{item_name}")
def get_price(item_name: str):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.execute("SELECT price, timestamp FROM prices WHERE item_name = ? ORDER BY timestamp DESC LIMIT 1", (item_name,))
    row = cursor.fetchone()
    conn.close()
    if row:
        return {"item": item_name, "price": row[0], "time": row[1]}
    return {"error": "Non trovato"}