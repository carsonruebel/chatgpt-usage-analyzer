import json
import os
from datetime import datetime, timedelta
from collections import defaultdict
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
import tiktoken
import textwrap

# === SETTINGS ===
search_paths = [
    "conversations.json",  # Current directory
    os.path.join("..", "conversations.json"),  # One level up
    os.path.join("../..", "conversations.json"),  # Two levels up
    os.path.join("resources", "conversations.json"),  # In a 'resources' subfolder
]

for path in search_paths:
    if os.path.exists(path):
        json_path = path
        break
else:
    print("❌ File not found in any expected location.")
    exit()

cutoff_date_str = "2020-01-01"
model = "gpt-4"

# === TOKENIZER ===
try:
    enc = tiktoken.encoding_for_model(model)
except KeyError:
    enc = tiktoken.get_encoding("cl100k_base")

cutoff_date = datetime.strptime(cutoff_date_str, "%Y-%m-%d")

# === LOAD JSON DATA ===
with open(json_path, "r", encoding="utf-8") as f:
    conversations = json.load(f)

# === COUNT MESSAGES, TOKENS, WORDS PER DAY ===
daily_message_counts = defaultdict(int)
daily_token_counts = defaultdict(int)
daily_word_counts = defaultdict(int)

total_messages = 0
total_tokens = 0
total_words = 0

for conv in conversations:
    mapping = conv.get("mapping", {})
    for msg_data in mapping.values():
        msg = msg_data.get("message")
        if msg:
            role = msg.get("author", {}).get("role")
            ts = msg.get("create_time")
            if not ts:
                continue
            date = datetime.fromtimestamp(ts)
            if date < cutoff_date:
                continue
            date_str = date.strftime("%Y-%m-%d")

            parts = msg.get("content", {}).get("parts", [])
            text = " ".join(str(p) if isinstance(p, str) else "" for p in parts)
            token_count = len(enc.encode(text))
            word_count = len(text.split())

            # Count for both user and assistant messages (left infobox)
            daily_message_counts[date_str] += 1
            total_messages += 1
            daily_token_counts[date_str] += token_count
            total_tokens += token_count

            if role == "assistant":
                # Assistant word/token counts (right infobox)
                daily_word_counts[date_str] += word_count
                total_words += word_count

# === FILL MISSING DATES ===
all_dates = sorted(set(daily_message_counts.keys()) | set(daily_token_counts.keys()))
start_date = datetime.strptime(all_dates[0], "%Y-%m-%d")
end_date = datetime.strptime(all_dates[-1], "%Y-%m-%d")
full_range = (end_date - start_date).days + 1

dates = []
msg_counts = []
tok_counts = []
word_counts = []

for i in range(full_range):
    date = start_date + timedelta(days=i)
    date_str = date.strftime("%Y-%m-%d")
    dates.append(date_str)
    msg_counts.append(daily_message_counts.get(date_str, 0))
    tok_counts.append(daily_token_counts.get(date_str, 0))
    word_counts.append(daily_word_counts.get(date_str, 0))

# === STATS CALCULATION ===
active_days = sum(1 for c in msg_counts if c > 0)
avg_msg_all = total_messages / len(msg_counts)
avg_msg_active = total_messages / active_days if active_days else 0
avg_tok_all = total_tokens / len(msg_counts)
avg_tok_active = total_tokens / active_days if active_days else 0
avg_word_all = total_words / len(msg_counts)
avg_word_active = total_words / active_days if active_days else 0

# === PRINT STATS TO CONSOLE ===
print("\n📊 ChatGPT Combined Usage Summary")
print("-----------------------------------")
print(f"Start date: {dates[0]}")
print(f"End date:   {dates[-1]}")
print(f"Total messages: {total_messages}")
print(f"Total tokens:   {total_tokens}")
print(f"Total words:    {total_words}")
print(f"Total days:     {len(dates)}")
print(f"Days used:      {active_days}")
print(f"▶ Avg msgs/day (all):    {avg_msg_all:.2f}")
print(f"▶ Avg msgs/day (active): {avg_msg_active:.2f}")
print(f"▶ Avg tokens/day (all):    {avg_tok_all:.2f}")
print(f"▶ Avg tokens/day (active): {avg_tok_active:.2f}")
print(f"▶ Avg words/day (all):    {avg_word_all:.2f}")
print(f"▶ Avg words/day (active): {avg_word_active:.2f}")

# === SUMMARY TEXT BOXES ===
max_msg = max(zip(msg_counts, dates), key=lambda x: x[0])
max_tok = max(zip(tok_counts, dates), key=lambda x: x[0])
max_word = max(zip(word_counts, dates), key=lambda x: x[0])

summary_text = (
    f"START: {dates[0]} | END: {dates[-1]}\n"
    f"TOTAL MESSAGES: {total_messages}\n"
    f"TOTAL TOKENS: {total_tokens}\n\n"
    f"ACTIVE DAYS: {active_days}/{len(dates)}\n"
    f"MSGS/DAY (ALL): {avg_msg_all:.2f} | MSGS/DAY (ACTIVE): {avg_msg_active:.2f}\n"
    f"TOKENS/DAY (ALL): {avg_tok_all:.2f} | TOKENS/DAY (ACTIVE): {avg_tok_active:.2f}\n\n"
    f"MAX MESSAGES: {max_msg[0]} on {max_msg[1]}\n"
    f"MAX TOKENS:   {max_tok[0]} on {max_tok[1]}"

)


def fun_equivalent(n):
    if n >= 22_000_000:
        return "That’s more text than the entire United States Code of federal law."
    elif n >= 17_500_000:
        return "That’s like rewriting the entire Game of Thrones series ten times."
    elif n >= 14_750_000:
        return "That’s the entire Dungeons & Dragons 5th Edition core rulebooks... multiplied thirty times."
    elif n >= 11_000_000:
        return "That’s about one‑quarter of the entire 32‑volume Encyclopedia Britannica"
    elif n >= 8_600_000:
        return "That’s twice the entire Wheel of Time series."
    elif n >= 5_400_000:
        return "That’s longer than the King James Bible seven times over."
    elif n >= 3_300_000:
        return "That’s the full Discworld series by Terry Pratchett, 41 novels worth."
    elif n >= 2_000_000:
        return "That’s double the total word count of the entire Harry Potter series."
    elif n >= 1_300_000:
        return "That’s the entire Lord of the Rings trilogy, plus The Hobbit, twice over."
    elif n >= 700_000:
        return "That’s longer than the complete Sherlock Holmes collection."
    elif n >= 400_000:
        return "That’s about the length of Les Misérables in English translation."
    elif n >= 180_000:
        return "That’s the combined word count of The Fellowship of the Ring."
    elif n >= 100_000:
        return "That’s the full word count of To Kill a Mockingbird, all 100,388 words of it."
    elif n >= 60_000:
        return "That’s more than a typical debut novel or thesis paper, easily."
    elif n >= 30_000:
        return "That’s longer than a technical manual or a short novella for sure."
    elif n >= 11_000:
        return "That’s the full transcript of Steve Jobs’ Stanford commencement speech... 50 times over."
    elif n >= 2_000:
        return "That’s more than a short blog post or product review online."
    elif n >= 500:
        return "That’s about the length of a very active Twitter thread these days."
    else:
        return "That’s barely a paragraph, you’re just getting started, friend."


# === Compose and format right box content ===
main_line = f"ChatGPT has written {total_words:,} words for you"
fun_line = " " * 54 + fun_equivalent(total_words)

# Configure the wrapper to preserve that space and wrap by word
wrapper = textwrap.TextWrapper(width=55, drop_whitespace=False)
fun_line_wrapped = wrapper.wrap(fun_line)

# Insert one blank line between intro and fun equivalent
equiv_lines = [main_line, ""] + fun_line_wrapped

# Combine and pad to match height of left box
left_line_count = summary_text.count("\n") + 1
equiv_lines += [""] * max(0, left_line_count - len(equiv_lines))

equiv_text = "\n".join(equiv_lines)

# === PLOT ===
plt.figure(figsize=(11, 7.5))
fig = plt.gcf()
fig.canvas.manager.set_window_title("ChatGPT Usage Summary")

N = max(1, len(dates) // 20)
plt.plot(dates, msg_counts, marker='o', linestyle='-', color='blue', label="Messages/day")
plt.title("Daily ChatGPT Message Count with Token & Word Summary")
plt.xlabel("Date")
plt.ylabel("# Messages")
plt.xticks(
    ticks=range(0, len(dates), N),
    labels=[dates[i] for i in range(0, len(dates), N)],
    rotation=45
)
plt.grid(True)
plt.legend()
plt.tight_layout(rect=[0, 0.18, 1, 0.94])

# Add white background for summary boxes
fig.patches.extend([
    Rectangle((0, 0), 1, 0.17, transform=fig.transFigure, color='white', zorder=2)
])

box_style = dict(fontsize=8.5, family='monospace', verticalalignment='top')

# Left summary box
fig.text(
    0.01, 0.17, summary_text,
    ha='left',
    bbox=dict(facecolor='white', edgecolor='black', alpha=0.85),
    **box_style
)

# Right word count box (matched spacing, left-aligned text)
fig.text(
    0.635, 0.17, equiv_text,
    ha='left',
    bbox=dict(facecolor='white', edgecolor='black', alpha=0.85),
    **box_style
)

# Attribution text at bottom right
# Attribution text positioned via a custom invisible axis
attribution_ax = fig.add_axes([0.76, -0.03, 0.22, 0.03], zorder=10)  # [left, bottom, width, height]
attribution_ax.axis("off")
attribution_ax.text(
    1, 0, "Tool courtesy of carsonruebel.com",
    ha="right",
    va="bottom",
    fontsize=7.5,
    family="monospace",
    color="#222222"
)

# Left scoping label: *scoped to all messages*
scope_left_ax = fig.add_axes([0.11, 0.18, 0.3, 0.03], zorder=10)  # [left, bottom, width, height]
scope_left_ax.axis("off")
scope_left_ax.text(
    0, 0, "*scoped to all messages*",
    ha="left",
    va="bottom",
    fontsize=8.5,
    family="monospace",
    color="#222222"
)

# Right scoping label: *scoped to assistant responses*
scope_right_ax = fig.add_axes([0.7, 0.18, 0.2, 0.03], zorder=10)
scope_right_ax.axis("off")
scope_right_ax.text(
    0, 0, "*scoped to assistant responses*",
    ha="left",
    va="bottom",
    fontsize=8.5,
    family="monospace",
    color="#222222"
)

# Save and view
plt.savefig("chatgpt_usage.png", bbox_inches="tight")
print("Plot saved as chatgpt_usage.png")
os.startfile("chatgpt_usage.png")
