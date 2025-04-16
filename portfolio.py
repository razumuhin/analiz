
import sqlite3
from datetime import datetime

class Portfolio:
    def __init__(self):
        self.conn = sqlite3.connect('portfolio.db')
        self.create_tables()
        self.create_watchlist_table()
        
    def create_tables(self):
        cursor = self.conn.cursor()
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS transactions (
            id INTEGER PRIMARY KEY,
            symbol TEXT NOT NULL,
            operation TEXT NOT NULL,
            price REAL NOT NULL,
            quantity INTEGER NOT NULL,
            date TEXT NOT NULL
        )''')
        self.conn.commit()
        
    def create_watchlist_table(self):
        """İzleme listesi tablosunu oluşturur"""
        cursor = self.conn.cursor()
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS watchlist (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            symbol TEXT NOT NULL UNIQUE,
            added_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
        )''')
        self.conn.commit()
        
    def add_to_watchlist(self, symbol):
        """İzleme listesine hisse ekler"""
        cursor = self.conn.cursor()
        try:
            cursor.execute('''
            INSERT INTO watchlist (symbol, added_at)
            VALUES (?, ?)
            ''', (symbol.upper(), datetime.now().strftime('%Y-%m-%d %H:%M:%S')))
            self.conn.commit()
            return True
        except sqlite3.IntegrityError:
            return False
            
    def remove_from_watchlist(self, symbol):
        """İzleme listesinden hisse çıkarır"""
        cursor = self.conn.cursor()
        cursor.execute('DELETE FROM watchlist WHERE symbol=?', (symbol.upper(),))
        self.conn.commit()
        
    def get_watchlist(self):
        """İzleme listesini getirir"""
        cursor = self.conn.cursor()
        cursor.execute('SELECT symbol, added_at FROM watchlist ORDER BY added_at DESC')
        return cursor.fetchall()
        
    def add_transaction(self, symbol, operation, price, quantity, date=None):
        cursor = self.conn.cursor()
        if date is None:
            date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        cursor.execute('''
        INSERT INTO transactions (symbol, operation, price, quantity, date)
        VALUES (?, ?, ?, ?, ?)
        ''', (symbol.upper(), operation, price, quantity, date))
        self.conn.commit()
        
    def get_portfolio(self):
        cursor = self.conn.cursor()
        cursor.execute('''
        WITH PortfolioSummary AS (
            SELECT 
                symbol,
                SUM(CASE WHEN operation='BUY' THEN quantity ELSE -quantity END) as total_quantity,
                SUM(CASE WHEN operation='BUY' THEN price*quantity ELSE -price*quantity END) as total_cost,
                MAX(date) as last_transaction_date
            FROM transactions
            GROUP BY symbol
            HAVING total_quantity > 0
        )
        SELECT 
            symbol,
            total_quantity,
            ABS(total_cost) as total_cost,
            last_transaction_date,
            ABS(total_cost/total_quantity) as avg_cost
        FROM PortfolioSummary
        ORDER BY last_transaction_date DESC
        ''')
        return cursor.fetchall()
        
    def get_transactions(self, symbol=None):
        cursor = self.conn.cursor()
        if symbol:
            cursor.execute('SELECT * FROM transactions WHERE symbol=? ORDER BY date DESC', (symbol.upper(),))
        else:
            cursor.execute('SELECT * FROM transactions ORDER BY date DESC')
        return cursor.fetchall()

    def get_portfolio_summary(self):
        """Portföy özet bilgilerini döndürür"""
        cursor = self.conn.cursor()
        cursor.execute('''
        SELECT 
            COUNT(DISTINCT symbol) as total_stocks,
            SUM(CASE WHEN operation='BUY' THEN price*quantity ELSE -price*quantity END) as total_investment,
            SUM(CASE WHEN operation='BUY' THEN quantity ELSE -quantity END) as total_shares
        FROM transactions
        ''')
        return cursor.fetchone()

    def create_alarm_table(self):
        """Alarm tablosunu oluşturur"""
        cursor = self.conn.cursor()
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS alarms (
            id INTEGER PRIMARY KEY,
            symbol TEXT NOT NULL,
            target_price REAL NOT NULL,
            condition TEXT NOT NULL,
            active INTEGER DEFAULT 1,
            created_at TEXT NOT NULL
        )''')
        self.conn.commit()

    def add_alarm(self, symbol, target_price, condition):
        """Yeni alarm ekler"""
        cursor = self.conn.cursor()
        cursor.execute('''
        INSERT INTO alarms (symbol, target_price, condition, created_at)
        VALUES (?, ?, ?, ?)
        ''', (symbol.upper(), target_price, condition, datetime.now().strftime('%Y-%m-%d %H:%M:%S')))
        self.conn.commit()

    def get_alarms(self, active_only=True):
        """Alarmları getirir"""
        cursor = self.conn.cursor()
        if active_only:
            cursor.execute('SELECT * FROM alarms WHERE active=1')
        else:
            cursor.execute('SELECT * FROM alarms')
        return cursor.fetchall()

    def deactivate_alarm(self, alarm_id):
        """Alarmı deaktif eder"""
        cursor = self.conn.cursor()
        cursor.execute('UPDATE alarms SET active=0 WHERE id=?', (alarm_id,))
        self.conn.commit()
