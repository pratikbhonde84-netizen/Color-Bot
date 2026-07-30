import telebot
import requests
import sqlite3
import time
from flask import Flask
from threading import Thread

# Tumhara Bot Token
bot = telebot.TeleBot("8965203772:AAHdx_rTZJpYTDsAdRf7UHH7sfvDPa0lS_Q")

# YAHAN APNE TELEGRAM CHANNEL KA USERNAME DAALNA (Jahan bot messages bhejega)
# Example: CHANNEL_ID = "@PratikVIPPredictions"
CHANNEL_ID = "@TUMHARA_CHANNEL_USERNAME" 

API_URL = "https://draw.ar-lottery01.com/WinGo/WinGo_1M/GetHistoryIssuePage.json"

app = Flask(__name__)
@app.route('/')
def home():
    return "Pratik's 20-Logic Pro Engine is Live 24/7!"

def run_server():
    app.run(host="0.0.0.0", port=8080)

# Database Setup (Actual data + Predictions track karne ke liye)
conn = sqlite3.connect('results.db', check_same_thread=False)
cursor = conn.cursor()
cursor.execute('''CREATE TABLE IF NOT EXISTS history (issue_no TEXT PRIMARY KEY, result TEXT, number INTEGER)''')
cursor.execute('''CREATE TABLE IF NOT EXISTS predictions (issue_no TEXT PRIMARY KEY, predicted_result TEXT)''')
conn.commit()

def fetch_api_data():
    try:
        headers = {"User-Agent": "Mozilla/5.0"}
        response = requests.get(API_URL, headers=headers, timeout=10)
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
        return inserted
    except Exception as e:
        print("API Fetch Error:", e)
        return 0

def get_20_tagde_logics(results_list):
    """
    Exactly 20 Real Quantitative Logics.
    Har logic history analyze karke 1 vote dega. Total 20 Votes.
    """
    votes = {'Big': 0, 'Small': 0}
    
    def add_vote(choice):
        if choice in votes: votes[choice] += 1

    if len(results_list) < 100:
        return results_list[0] if results_list else "Big", 0, 0

    last_res = results_list[0]
    
    # --- LOGIC 1 to 3: Historical Pattern Echoes ---
    def check_pattern(depth):
        seq = tuple(results_list[:depth])
        b, s = 0, 0
        for i in range(1, len(results_list) - depth):
            if tuple(results_list[i:i+depth]) == seq:
                if results_list[i-1] == 'Big': b += 1
                else: s += 1
        return 'Big' if b > s else ('Small' if s > b else last_res)

    add_vote(check_pattern(3))  # Logic 1: Last 3 sequence
    add_vote(check_pattern(4))  # Logic 2: Last 4 sequence
    add_vote(check_pattern(5))  # Logic 3: Last 5 sequence

    # --- LOGIC 4 to 6: Moving Trend Pressure ---
    def check_trend(window):
        b = results_list[:window].count('Big')
        s = results_list[:window].count('Small')
        return 'Small' if b > s else ('Big' if s > b else last_res)

    add_vote(check_trend(15))   # Logic 4: 15-Game Reversion
    add_vote(check_trend(50))   # Logic 5: 50-Game Reversion
    add_vote(check_trend(100))  # Logic 6: 100-Game Reversion

    # --- LOGIC 7 & 8: Streak Momentum vs Exhaustion ---
    current_streak = 0
    for r in results_list:
        if r == last_res: current_streak += 1
        else: break
        
    # Logic 7: Keep following trend if streak is new
    if current_streak < 3: add_vote(last_res)
    else: add_vote('Small' if last_res == 'Big' else 'Big')
    
    # Logic 8: Reversal expectation if streak is long
    if current_streak >= 4: add_vote('Small' if last_res == 'Big' else 'Big')
    else: add_vote(last_res)

    # --- LOGIC 9 & 10: Alternating/Choppy Market Detectors ---
    # Logic 9: Volatility in last 6 (ABAB detection)
    trans_6 = sum(1 for i in range(5) if results_list[i] != results_list[i+1])
    if trans_6 >= 4: add_vote('Small' if last_res == 'Big' else 'Big')
    else: add_vote(last_res)

    # Logic 10: Twin matching in last 8 (AABB detection)
    twin_count = sum(1 for i in range(0, 6, 2) if results_list[i] == results_list[i+1])
    if twin_count >= 2: add_vote(last_res)
    else: add_vote('Small' if last_res == 'Big' else 'Big')

    # --- LOGIC 11 to 13: Transition & Bounce Probabilities ---
    def bounce_logic(target_seq):
        b, s = 0, 0
        for i in range(1, len(results_list) - len(target_seq)):
            if tuple(results_list[i:i+len(target_seq)]) == target_seq:
                if results_list[i-1] == 'Big': b += 1
                else: s += 1
        return 'Big' if b > s else ('Small' if s > b else last_res)

    add_vote(bounce_logic(('Small', 'Big')))         # Logic 11: Single Bounce transition
    add_vote(bounce_logic(('Small', 'Big', 'Big')))  # Logic 12: Twin Bounce transition
    
    # Logic 13: Rebound Strength
    if results_list[0] != results_list[1] and results_list[1] == results_list[2]:
        add_vote(results_list[1])
    else:
        add_vote(results_list[0])

    # --- LOGIC 14 to 20: Global History & Support/Resistance ---
    add_vote(check_trend(61))   # Logic 14: Golden Ratio Window Reversion
    add_vote(check_trend(1000)) # Logic 15: Grand History 1000-Game Pull

    # Logic 16: Immediate 5-Game Mirroring
    if results_list[:5] == results_list[5:10]: add_vote(results_list[5])
    else: add_vote('Small' if results_list[5] == 'Big' else 'Big')

    # Logic 17: Extreme Historical Resistance
    max_hist = 0
    curr_hist = 1
    for i in range(1, len(results_list)):
        if results_list[i] == results_list[i-1]: curr_hist += 1
        else:
            if curr_hist > max_hist: max_hist = curr_hist
            curr_hist = 1
            
    if current_streak >= (max_hist - 1): add_vote('Small' if last_res == 'Big' else 'Big')
    else: add_vote(last_res)

    # Logic 18: 30-Game Trailing Volatility Average
    trans_30 = sum(1 for i in range(29) if results_list[i] != results_list[i+1])
    if trans_30 > 16: add_vote('Small' if last_res == 'Big' else 'Big')
    else: add_vote(last_res)

    # Logic 19: Weighted Recent 5 Average
    w_b, w_s = 0, 0
    weights = [5, 4, 3, 2, 1]
    for i in range(5):
        if results_list[i] == 'Big': w_b += weights[i]
        else: w_s += weights[i]
    add_vote('Big' if w_b > w_s else 'Small')

    # Logic 20: 500-Game Median Balance
    add_vote(check_trend(500))

    # ==========================================
    # FINAL VOTING & CONFIDENCE
    # ==========================================
    final_pred = "Big" if votes['Big'] >= votes['Small'] else "Small"
    return final_pred, votes['Big'], votes['Small']

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
            status = "SKIP"
            icon = "⚪"
        else:
            status = "WINN" if row[1] == predicted else "LOSS"
            icon = "✅" if status == "WINN" else "❌"
            
        msg += f"║ {icon} #{issue} ──► {actual_res}={num}  {status}\n"
    return msg

last_notified = 0

def bot_main_loop():
    global last_notified
    
    while True:
        fetch_api_data()
        cursor.execute("SELECT COUNT(*) FROM history")
        total_count = cursor.fetchone()[0]
        
        if total_count < 1000:
            print(f"Collecting Data: {total_count}/1000")
            milestone = total_count // 100
            if milestone > last_notified:
                try:
                    bot.send_message(CHANNEL_ID, f"⏳ **System Data Collection...**\n\n📊 High Accuracy Real Data Collection.\n📈 Collected: {total_count} / 1000\n\n*20 Tagde Logics Engine will trigger automatically at 1000 results!*", parse_mode="Markdown")
                    last_notified = milestone
                except Exception as e:
                    print("Notify Error (Check Channel ID):", e)
        else:
            cursor.execute("SELECT issue_no, result FROM history ORDER BY issue_no DESC")
            all_data = cursor.fetchall()
            latest_issue = all_data[0][0]
            next_issue = str(int(latest_issue) + 1)
            
            cursor.execute("SELECT * FROM predictions WHERE issue_no = ?", (next_issue,))
            if not cursor.fetchone():
                results_list = [row[1] for row in all_data[:1000]]
                
                # EXECUTE 20 REAL LOGICS
                prediction, big_votes, small_votes = get_20_tagde_logics(results_list)
                
                # Calculate Confidence (%)
                win_votes = big_votes if prediction == "Big" else small_votes
                confidence = int((win_votes / 20) * 100)
                
                cursor.execute("INSERT INTO predictions (issue_no, predicted_result) VALUES (?, ?)", (next_issue, prediction))
                conn.commit()
                
                period_disp = next_issue[-6:]
                pred_col = "🔴" if prediction == "Big" else "🔵"
                last_10 = generate_last_10_message()
                
                final_msg = f"""╭────────────────╮
      🌿 𝗣𝗘𝗥𝗜𝗢𝗗 : {period_disp}
▰▰▰▰▰▰▰▰▰▰▰▰▰▰
📊 MATCHES     ➤  1000 / 1000
⚙️ 20 PRO LOGICS VOTING:
   • Small Votes ➤ {small_votes}/20
   • Big Votes   ➤ {big_votes}/20
▰▰▰▰▰▰▰▰▰▰▰▰▰▰
🎯 Action      ➤  BET {prediction.upper()} {pred_col}
🔥 Confidence  ➤  {confidence}% REAL
▰▰▰▰▰▰▰▰▰▰▰▰▰▰
    24/7 ᴩᴀɪᴅ ᴛᴏᴏʟ 
▰▰▰▰▰▰▰▰▰▰▰▰▰▰
╔     📋 LAST 10 RESULTS

{last_10}╰─────────────────╯"""

                try:
                    bot.send_message(CHANNEL_ID, final_msg)
                    print(f"Prediction Sent {next_issue} | Big: {big_votes}, Small: {small_votes}")
                except Exception as e:
                    print("Telegram Error (Check Channel ID & Admin Rights):", e)

        time.sleep(15)

if __name__ == "__main__":
    server_thread = Thread(target=run_server)
    server_thread.start()
    bot_thread = Thread(target=bot_main_loop)
    bot_thread.start()
    bot.polling(none_stop=True)

