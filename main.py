from fastapi import FastAPI
import sqlite3

app = FastAPI()
DB_PATH = "data/market_data.db"

@app.get("/prezzo/{item_name}")
def get_latest_price(item_name: str):
    conn = sqlite3.connect(DB_PATH)
    query = "SELECT price, timestamp FROM prices WHERE item_name = ? ORDER BY timestamp DESC LIMIT 1"
    cursor = conn.execute(query, (item_name,))
    row = cursor.fetchone()
    conn.close()

    if row:
        return {
            "item": item_name,
            "latest_price": row[0],
            "last_update": row[1]
        }
    return {"error": "Oggetto non trovato nel database"}

@app.get("/")
def home():
    return {"status": "API Online", "message": "Benvenuto nell'oracolo di CS2"}