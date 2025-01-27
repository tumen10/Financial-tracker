# app.py
from flask import Flask, render_template, request, redirect, url_for
import sqlite3
from datetime import datetime

app = Flask(__name__)
DB_PATH = "database.db"

# Инициализация базы данных
def init_db():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS transactions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            amount REAL,
            category TEXT,
            date TEXT,
            description TEXT
        )
    ''')
    conn.commit()
    conn.close()

# Главная страница с балансом
@app.route('/')
def index():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT SUM(amount) FROM transactions")
    balance = cursor.fetchone()[0] or 0
    conn.close()
    return render_template('index.html', balance=balance)

# Страница добавления транзакции
@app.route('/add', methods=['GET', 'POST'])
def add_transaction():
    if request.method == 'POST':
        amount = float(request.form['amount'])
        category = request.form['category']
        date = request.form['date'] or datetime.now().strftime('%Y-%m-%d')
        description = request.form['description']
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute("INSERT INTO transactions (amount, category, date, description) VALUES (?, ?, ?, ?)",
                       (amount, category, date, description))
        conn.commit()
        conn.close()
        return redirect(url_for('index'))
    return render_template('add.html')

# История транзакций
@app.route('/history')
def history():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM transactions ORDER BY date DESC")
    transactions = cursor.fetchall()
    conn.close()
    return render_template('history.html', transactions=transactions)

if __name__ == '__main__':
    init_db()
    app.run(debug=True)
