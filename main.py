import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
import csv
import os
from datetime import datetime

CSV_FILE = 'awards.csv'

def load_awards():
    if not os.path.exists(CSV_FILE):
        return []
    with open(CSV_FILE, newline='', encoding='utf-8') as f:
        reader = csv.reader(f)
        return list(reader)

def save_awards(awards):
    with open(CSV_FILE, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerows(awards)

def calculate_days_left(date_str):
    try:
        date = datetime.strptime(date_str, "%Y-%m-%d")
        today = datetime.today()
        delta = (date - today).days
        return f"{delta} 日" if delta >= 0 else "締切済み"
    except Exception:
        return "日付エラー"

def parse_word_limit(text):
    try:
        return int(text.split('～')[-1])
    except:
        return 100000

def calculate_progress(current_str, limit_str):
    try:
        current = int(current_str)
        total = parse_word_limit(limit_str)
        percentage = (current / total) * 100
        return min(int(percentage), 100)
    except:
        return 0

def show_award_details(award):
    messagebox.showinfo("賞の詳細", f"""
賞名: {award[0]}
応募開始日: {award[1]}
締め切り日: {award[2]}
文字数制限: {award[3]}
現在の文字数: {award[4]}
""")

def add_award():
    name = simpledialog.askstring("賞の追加", "賞の名前は？")
    if not name:
        return
    start = simpledialog.askstring("応募開始日", "形式: 2025-05-01")
    end = simpledialog.askstring("締切日", "形式: 2025-07-31")
    limit = simpledialog.askstring("文字数制限", "例: 30000～100000")
    current = simpledialog.askstring("現在の文字数", "数字のみ")
    if None in (start, end, limit, current):
        return
    awards.append([name, start, end, limit, current])
    save_awards(awards)
    refresh_ui()

def edit_award(index):
    award = awards[index]
    name = simpledialog.askstring("賞名編集", "賞名:", initialvalue=award[0])
    start = simpledialog.askstring("応募開始日", "形式: 2025-05-01", initialvalue=award[1])
    end = simpledialog.askstring("締切日", "形式: 2025-07-31", initialvalue=award[2])
    limit = simpledialog.askstring("文字数制限", "例: 30000～100000", initialvalue=award[3])
    current = simpledialog.askstring("現在の文字数", "数字のみ", initialvalue=award[4])
    if None in (name, start, end, limit, current):
        return
    awards[index] = [name, start, end, limit, current]
    save_awards(awards)
    refresh_ui()

def delete_award(index):
    if messagebox.askyesno("削除確認", f"{awards[index][0]} を削除しますか？"):
        del awards[index]
        save_awards(awards)
        refresh_ui()

def refresh_ui():
    for widget in frame.winfo_children():
        widget.destroy()
    for i, award in enumerate(awards):
        name, start, end, limit, current = award
        days = calculate_days_left(end)
        progress = calculate_progress(current, limit)

        tk.Button(frame, text=name, fg="blue", cursor="hand2", relief=tk.FLAT,
                  command=lambda a=award: show_award_details(a)).grid(row=i, column=0, sticky="w")
        tk.Label(frame, text=f"開始: {start}").grid(row=i, column=1)
        tk.Label(frame, text=f"締切: {end}").grid(row=i, column=2)
        tk.Label(frame, text=f"残り: {days}").grid(row=i, column=3)
        tk.Label(frame, text=f"進捗: {progress}%").grid(row=i, column=4)

        progress_bar = ttk.Progressbar(frame, length=100, value=progress)
        progress_bar.grid(row=i, column=5, padx=5)

        tk.Button(frame, text="編集", command=lambda i=i: edit_award(i)).grid(row=i, column=6)
        tk.Button(frame, text="削除", command=lambda i=i: delete_award(i)).grid(row=i, column=7)

# GUIセットアップ
root = tk.Tk()
root.title("小説賞カレンダー")
root.geometry("800x400")

tk.Button(root, text="賞を追加", command=add_award).pack(pady=5)

canvas = tk.Canvas(root)
scrollbar = tk.Scrollbar(root, orient="vertical", command=canvas.yview)
scrollable_frame = tk.Frame(canvas)

scrollable_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
canvas.configure(yscrollcommand=scrollbar.set)

canvas.pack(side="left", fill="both", expand=True)
scrollbar.pack(side="right", fill="y")

frame = scrollable_frame
awards = load_awards()
refresh_ui()

root.mainloop()
