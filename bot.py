import telebot
import sqlite3
import time
from flask import Flask
from threading import Thread

# Tumhara Bot Token
bot = telebot.TeleBot("8965203772:AAHdx_rTZJpYTDsAdRf7UHH7sfvDPa0lS_Q")

# Free server ko 24/7 zinda rakhne ke liye Flask
app = Flask(__name__)
@app.route('/')
def home():
    return "Pratik ka Bot Zinda Hai!"

def run_server():
    app.run(host="0.0.0.0", port=8080)

# Database setup 1000 results jama karne ke liye
conn = sqlite3.connect('results.db', check_same_thread=False)
cursor = conn.cursor()
cursor.execute('''CREATE TABLE IF NOT EXISTS history (id INTEGER PRIMARY KEY, result TEXT)''')
conn.commit()

def fetch_and_analyze():
    while True:
        try:
            # Abhi ke liye demo result (Baad mein yaha API lagayenge)
            fake_result = "Big" 
            
            cursor.execute("INSERT INTO history (result) VALUES (?)", (fake_result,))
            conn.commit()
            
            cursor.execute("SELECT COUNT(*) FROM history")
            count = cursor.fetchone()[0]
            print(f"Data Collected: {count}/1000")
            
            if count >= 1000:
                print("1000 Results Done!")
                # Yaha aage ka prediction logic chalega
        except Exception as e:
            print("Error:", e)
        
        time.sleep(60)

if __name__ == "__main__":
    server_thread = Thread(target=run_server)
    server_thread.start()
    
    bot_thread = Thread(target=fetch_and_analyze)
    bot_thread.start()
    
    bot.polling(none_stop=True)

