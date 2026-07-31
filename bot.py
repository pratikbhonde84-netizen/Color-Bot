import telebot
import requests
import sqlite3
import time
from flask import Flask
from threading import Thread

# TERA NAYA BOT TOKEN 
bot = telebot.TeleBot("8965203772:AAEQS9Qqiab_81Ckq9lLiJvTvV6frRId0HQ")

# Tera Personal Telegram Chat ID 
CHANNEL_ID = "7793467471" 

API_URL = "https://draw.ar-lottery01.com/WinGo/WinGo_1M/GetHistoryIssuePage.json"

# --- FLASK SERVER ---
app = Flask(__name__)
@app.route('/')
def home():
    return "10-Logic Pro Engine is Live 24/7!"

def run_server():
    app.run(host="0.0.0.0", port=8080)

# --- DATABASE SETUP ---
conn = sqlite3.connect('results.db', check_same_thread=False)
cursor = conn.cursor()
cursor.execute('''CREATE TABLE IF NOT EXISTS history (issue_no TEXT PRIMARY KEY, result TEXT, number INTEGER)''')
cursor.execute('''CREATE TABLE IF NOT EXISTS predictions (issue_no TEXT PRIMARY KEY, predicted_result TEXT)''')
conn.commit()

@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    bot.reply_to(message, "🚀 Hello Pratik! \n\n10-LOGIC ADVANCED MATRIX ENGINE 24/7 chalu hai. \n\n📊 Type /status to check LIVE API connection!")

# --- HARDCORE MOBILE HEADERS (ANTI-403) ---
def get_bypass_headers():
    return {
        "User-Agent": "Mozilla/5.0 (Linux; Android 13; SM-S918B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Mobile Safari/537.36",
        "Accept": "application/json, text/plain, */*",
        "Accept-Language": "en-IN,en-US;q=0.9,en;q=0.8",
        "Referer": "https://ar-lottery01.com/",
        "Origin": "https://ar-lottery01.com",
        "Connection": "keep-alive",
        "Sec-Fetch-Dest": "empty",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Site": "same-site",
        "Cache-Control": "no-cache",
        "Pragma": "no-cache"
    }

# --- LIVE STATUS & API DEBUGGER ---
@bot.message_handler(commands=['status'])
def check_status(message):
    try:
        cursor.execute("SELECT COUNT(*) FROM history")
        count = cursor.fetchone()[0]
        
        url = f"{API_URL}?ts={int(time.time()*1000)}"
        res = requests.get(url, headers=get_bypass_headers(), timeout=5)
        
        api_reply = f"Status Code: {res.status_code}\n"
        if res.status_code == 200:
            try:
                json_data = res.json()
                items = json_data.get('data', {}).get('list', [])
                if not items and isinstance(json_data, list): items = json_data
                api_reply += f"🟢 Data Received: {len(items)} records in 1 hit!"
            except:
                api_reply += "🔴 Error: JSON parse fail (Cloudflare HTML page blocked it)"
        else:
            api_reply += f"🔴 Error: API Blocked Request (Code {res.status_code})"

        bot.reply_to(message, f"🟢 **BOT ZINDA HAI!**\n\n📊 DB History Count: {count}\n\n🔍 **LIVE API TEST:**\n{api_reply}")
    except Exception as e:
        bot.reply_to(message, f"Error: {e}")

def fetch_api_data():
    try:
        url = f"{API_URL}?ts={int(time.time()*1000)}"
        response = requests.get(url, headers=get_bypass_headers(), timeout=10)
        
        if response.status_code != 200:
            return 0, f"Error {response.status_code}"
            
        data = response.json()
        items = data.get('data', {}).get('list', [])
        if not items and isinstance(data, list):
            items = data
            
        new_records = []
        for item in items:
            issue_no = str(item.get('issueNumber') or item.get('issue') or item.get('period'))
            number = item.get('number')
            
            if number is not None:
                result = "Big" if int(number) >= 5 else "Small"
                new_records.append((issue_no, result, int(number)))
                
        new_records.reverse()
        inserted = 0
        for issue_no, result, number in new_records:
            cursor.execute("INSERT OR IGNORE INTO history (issue_no, result, number) VALUES (?, ?, ?)", (issue_no, result, number))
            if cursor.rowcount > 0: inserted += 1
        conn.commit()
        return inserted, f"SUCCESS (Got {len(items)})"
    except Exception as e:
        return 0, str(e)

# --- 🧠 THE 10-LOGIC ADVANCED ENGINE ---
def ten_logic_matrix_engine(recent_data, db_cursor):
    if len(recent_data) < 10:
        return "Big", 50, "⚙️ GATHERING DATA", [0, 5]

    nums = [x[1] for x in recent_data]
    res = [x[0] for x in recent_data]
    
    votes = {"Big": 0.0, "Small": 0.0}

    # Logic 1: WMA
    w = [1.0, 0.9, 0.8, 0.7, 0.6, 0.5, 0.4, 0.3, 0.2, 0.1]
    limit = min(len(nums), 10)
    w_sum = sum(v * weight for v, weight in zip(nums[:limit], w[:limit]))
    weight_total = sum(w[:limit])
    if (w_sum / weight_total) >= 4.5: votes["Big"] += 1.5 
    else: votes["Small"] += 1.5

    # Logic 2: Volatility
    avg = sum(nums[:limit]) / limit
    variance = sum((x - avg)**2 for x in nums[:limit]) / limit
    if (variance ** 0.5) > 2.8: votes["Small" if nums[0] >= 5 else "Big"] += 1.2
    else: votes["Big" if nums[0] >= 5 else "Small"] += 1.2

    # Logic 3: RSI
    rsi_list = res[:14]
    rsi = (rsi_list.count('Big') / len(rsi_list)) * 100 if rsi_list else 50
    if rsi > 70: votes["Small"] += 1.5
    elif rsi < 30: votes["Big"] += 1.5
    else: votes[res[0]] += 0.5

    # Logic 4: Markov
    if len(res) >= 4:
        seq_3 = tuple(res[:3])
        b_nxt, s_nxt = 0, 0
        for i in range(3, len(res)-1):
            if tuple(res[i:i+3]) == seq_3:
                if res[i-1] == 'Big': b_nxt += 1
                else: s_nxt += 1
        if b_nxt > s_nxt: votes["Big"] += 1.5
        elif s_nxt > b_nxt: votes["Small"] += 1.5
        else: votes[res[0]] += 0.5
    else:
        votes[res[0]] += 0.5

    # Logic 5: Fibonacci
    fib_avg = (sum(nums[:3])/min(len(nums), 3) * 0.5) + (sum(nums[:5])/min(len(nums), 5) * 0.3) + (sum(nums[:8])/min(len(nums), 8) * 0.2)
    if fib_avg >= 4.5: votes["Big"] += 1.0
    else: votes["Small"] += 1.0

    # Logic 6: ROC
    roc = nums[0] - nums[-1]
    if roc > 0: votes["Big"] += 1.0
    elif roc < 0: votes["Small"] += 1.0
    else: votes[res[0]] += 0.5

    # Logic 7: Parity
    odds = sum(1 for n in nums[:limit] if n % 2 != 0)
    evens = limit - odds
    if odds > evens and res[0] == 'Small': votes["Small"] += 0.8
    elif evens > odds and res[0] == 'Big': votes["Big"] += 0.8
    else: votes["Big" if nums[0] >= 5 else "Small"] += 0.8

    # Logic 8: Streak
    streak = 0
    for r in res:
        if r == res[0]: streak += 1
        else: break
    if streak >= 4: votes["Small" if res[0] == "Big" else "Big"] += 2.0 
    else: votes[res[0]] += 1.0

    # Logic 9: Gravity
    grav_list = nums[:50]
    cg_50 = sum(grav_list) / len(grav_list) if grav_list else 4.5
    if cg_50 > 4.7: votes["Small"] += 1.0
    elif cg_50 < 4.3: votes["Big"] += 1.0
    else: votes[res[0]] += 0.5

    # Logic 10: Recovery
    db_cursor.execute('SELECT h.result, p.predicted_result FROM history h JOIN predictions p ON h.issue_no = p.issue_no ORDER BY h.issue_no DESC LIMIT 2')
    recent_db = db_cursor.fetchall()
    loss_streak = 0
    if recent_db:
        for act, pre in recent_db:
            if act and pre and act != pre: loss_streak += 1
            else: break
    if loss_streak == 1: votes[res[0]] += 2.0
    elif loss_streak >= 2: votes["Small" if res[0] == "Big" else "Big"] += 3.0
    else: votes[res[0]] += 1.0

    # Confidence calculation
    total_votes = votes["Big"] + votes["Small"]
    if votes["Big"] >= votes["Small"]:
        pred = "Big"
        conf_pct = (votes["Big"] / total_votes) * 100 if total_votes > 0 else 50
    else:
        pred = "Small"
        conf_pct = (votes["Small"] / total_votes) * 100 if total_votes > 0 else 50

    target_vals = [nums[0], (nums[0] + 5) % 10]
    return pred, int(conf_pct), "⚙️ 10-LOGIC MATRIX PRO", target_vals

def generate_last_10_message():
    cursor.execute('''
        SELECT h.issue_no, h.result, h.number, p.predicted_result 
        FROM history h 
        LEFT JOIN predictions p ON h.issue_no = p.issue_no 
        ORDER BY h.issue_no DESC LIMIT 10
    ''')
    rows = cursor.fetchall()
    rows.reverse()
    
    msg = ""
    for row in rows:
        issue = row[0][-4:]
        actual_res = "BIG" if row[1] == "Big" else "SML"
        num = row[2]
        predicted = row[3]
        
        if not predicted:
            status = "---"
            icon = "⚪"
        else:
            status = "WINN" if row[1] == predicted else "LOSS"
            icon = "✅" if status == "WINN" else "❌"
            
        msg += f"║ {icon} #{issue} ──► {actual_res}={num}  {status}\n"
    return msg

def bot_main_loop():
    last_notify_time = 0
    while True:
        try:
            inserted, api_status = fetch_api_data()
            cursor.execute("SELECT COUNT(*) FROM history")
            total_count = cursor.fetchone()[0]
            
            if total_count < 10:
                if time.time() - last_notify_time > 60:
                    bot.send_message(int(CHANNEL_ID), f"⏳ **Data Collect Ho Raha Hai...**\n\n📊 Collected: {total_count} / 10\n⚠️ API Last Ping: {api_status}")
                    last_notify_time = time.time()
            else:
                cursor.execute("SELECT issue_no, result, number FROM history ORDER BY issue_no DESC")
                all_data = cursor.fetchall()
                latest_issue = all_data[0][0]
                next_issue = str(int(latest_issue) + 1)
                
                cursor.execute("SELECT * FROM predictions WHERE issue_no = ?", (next_issue,))
                if not cursor.fetchone():
                    recent_data = [(row[1], row[2]) for row in all_data[:100]] 
                    
                    prediction, confidence, strat_name, target_vals = ten_logic_matrix_engine(recent_data, cursor)
                    
                    cursor.execute("INSERT INTO predictions (issue_no, predicted_result) VALUES (?, ?)", (next_issue, prediction))
                    conn.commit()
                    
                    period_disp = next_issue[-6:]
                    pred_col = "🔴" if prediction == "Big" else "🔵"
                    last_10 = generate_last_10_message()
                    target_str = ", ".join(map(str, target_vals))
                    
                    final_msg = f"""╭────────────────╮
      🌿 𝗣𝗘𝗥𝗜𝗢𝗗 : {period_disp}
▰▰▰▰▰▰▰▰▰▰▰▰▰▰
📊 ENGINE      ➤  {strat_name}
▰▰▰▰▰▰▰▰▰▰▰▰▰▰
🎯 Action      ➤  BET {prediction.upper()} {pred_col}
🚀 Target Vals ➤  ⟦ {target_str} ⟧
🔥 Confidence  ➤  {confidence}% REAL
▰▰▰▰▰▰▰▰▰▰▰▰▰▰
    24/7 ᴩᴀɪᴅ ᴛ00𝗟 
▰▰▰▰▰▰▰▰▰▰▰▰▰▰
╔     📋 LAST 10 RESULTS

{last_10}╰─────────────────╯"""
                    bot.send_message(int(CHANNEL_ID), final_msg)
                    
        except Exception as e:
            print("Main Loop Error:", e)
            
        time.sleep(15)

if __name__ == "__main__":
    server_thread = Thread(target=run_server)
    server_thread.start()
    
    bot_thread = Thread(target=bot_main_loop)
    bot_thread.start()
    
    print("Clearing old webhooks...")
    try:
        bot.remove_webhook()
    except Exception:
        pass
        
    print("Bot is starting afresh with Anti-403 Mobile Headers...")
    
    while True:
        try:
            bot.polling(none_stop=True, skip_pending=True)
        except Exception as e:
            print(f"Telegram API Conflict Aaya! 15 sec wait... Error: {e}")
            time.sleep(15)
