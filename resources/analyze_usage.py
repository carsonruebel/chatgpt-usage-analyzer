import json
import os
from datetime import datetime, timedelta
from collections import defaultdict
import matplotlib.pyplot as plt
import tiktoken

# === SETTINGS ===
# Try parent directory first
json_path = os.path.join("..", "conversations.json")

# If not found, try current directory
if not os.path.exists(json_path):
    json_path = "conversations.json"

if not os.path.exists(json_path):
    print(f"❌ File not found: {json_path}")
    exit()
cutoff_date_str = "2020-01-01"
model = "gpt-4"

# === TOKENIZER ===
try:
    enc = tiktoken.encoding_for_model(model)
except KeyError:
    enc = tiktoken.get_encoding("cl100k_base")

cutoff_date = datetime.strptime(cutoff_date_str, "%Y-%m-%d") if cutoff_date_str else None

if not os.path.exists(json_path):
    print(f"❌ File not found: {json_path}")
    exit()

with open(json_path, "r", encoding="utf-8") as f:
    conversations = json.load(f)

# === MESSAGE & TOKEN COUNTING ===
daily_message_counts = defaultdict(int)
daily_token_counts = defaultdict(int)
total_messages = 0
total_tokens = 0

for conv in conversations:
    mapping = conv.get("mapping", {})
    for msg_data in mapping.values():
        msg = msg_data.get("message")
        if msg and msg.get("author", {}).get("role") == "user":
            ts = msg.get("create_time")
            if not ts:
                continue
            date = datetime.fromtimestamp(ts)
            if cutoff_date and date < cutoff_date:
                continue
            date_str = date.strftime("%Y-%m-%d")

            content = msg.get("content", {}).get("parts", [])
            text = " ".join(str(p) if isinstance(p, str) else "" for p in content)
            token_count = len(enc.encode(text))

            daily_message_counts[date_str] += 1
            daily_token_counts[date_str] += token_count
            total_messages += 1
            total_tokens += token_count

# === Fill in all dates (zero-usage included) ===
all_dates = sorted(set(daily_message_counts.keys()) | set(daily_token_counts.keys()))
start_date = datetime.strptime(all_dates[0], "%Y-%m-%d")
end_date = datetime.strptime(all_dates[-1], "%Y-%m-%d")
full_range = (end_date - start_date).days + 1

dates = []
msg_counts = []
tok_counts = []

for i in range(full_range):
    date = start_date + timedelta(days=i)
    date_str = date.strftime("%Y-%m-%d")
    dates.append(date_str)
    msg_counts.append(daily_message_counts.get(date_str, 0))
    tok_counts.append(daily_token_counts.get(date_str, 0))

# === STATS ===
active_days = sum(1 for c in msg_counts if c > 0)
avg_msg_all = total_messages / len(msg_counts)
avg_msg_active = total_messages / active_days if active_days > 0 else 0
avg_tok_all = total_tokens / len(msg_counts)
avg_tok_active = total_tokens / active_days if active_days > 0 else 0

# === PRINT SUMMARY ===
print("\n📊 ChatGPT Combined Usage Summary")
print("-----------------------------------")
print(f"Start date: {dates[0]}")
print(f"End date:   {dates[-1]}")
print(f"Total messages: {total_messages}")
print(f"Total tokens:   {total_tokens}")
print(f"Total days:     {len(dates)}")
print(f"Days used:      {active_days}")
print(f"▶ Avg msgs/day (all):    {avg_msg_all:.2f}")
print(f"▶ Avg msgs/day (active): {avg_msg_active:.2f}")
print(f"▶ Avg tokens/day (all):    {avg_tok_all:.2f}")
print(f"▶ Avg tokens/day (active): {avg_tok_active:.2f}")

# === PLOT ===
N = max(1, len(dates) // 20)
plt.figure(figsize=(11, 7.5))  # taller figure to fit summary text
fig = plt.gcf()
fig.canvas.manager.set_window_title("ChatGPT Usage Summary")

plt.plot(dates, msg_counts, marker='o', linestyle='-', color='blue', label="Messages/day")
plt.xticks(
    ticks=range(0, len(dates), N),
    labels=[dates[i] for i in range(0, len(dates), N)],
    rotation=45
)

# === Layout & Summary
max_msg = max(zip(msg_counts, dates), key=lambda x: x[0])
max_tok = max(zip(tok_counts, dates), key=lambda x: x[0])

summary_text = (
    f"START: {dates[0]}   END: {dates[-1]}\n"
    f"TOTAL MESSAGES: {total_messages}   TOTAL TOKENS: {total_tokens}\n"
    f"ACTIVE DAYS: {active_days}/{len(dates)}\n"
    f"MSGS/DAY (ALL): {avg_msg_all:.2f}   MSGS/DAY (ACTIVE): {avg_msg_active:.2f}\n"
    f"TOKENS/DAY (ALL): {avg_tok_all:.2f}   TOKENS/DAY (ACTIVE): {avg_tok_active:.2f}\n"
    f"MAX MESSAGES: {max_msg[0]} on {max_msg[1]}\n"
    f"MAX TOKENS:   {max_tok[0]} on {max_tok[1]}"
)

plt.tight_layout(rect=[0, 0.12, 1, 0.94])
plt.figtext(0.01, 0.02, summary_text, ha="left", fontsize=8.5, bbox=dict(facecolor='white', alpha=0.85))
plt.subplots_adjust(bottom=0.28)

plt.title("Daily ChatGPT Message Count with Token Summary")
plt.xlabel("Date")
plt.ylabel("# Messages")
plt.grid(True)
plt.legend()
plt.savefig("chatgpt_usage.png", bbox_inches="tight")
print("Plot saved as chatgpt_usage.png")
os.startfile("chatgpt_usage.png")

