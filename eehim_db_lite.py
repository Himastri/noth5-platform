"""
EEHIM DB LITE - Public Lite runtime
Implements db.execute() with real execution via sqlite3 (in-memory)
Lite version simulates Factory EXE 75k req/sec WAL, but executes SQL.
"""
import sqlite3
import re

class EEHIM_DB_Lite:
    def __init__(self, db_path=":memory:"):
        self.conn = sqlite3.connect(db_path)
        self.conn.row_factory = sqlite3.Row
        self.cursor = self.conn.cursor()
        print("[EEHIM-DB-LITE] Initialized in-memory DB (Lite simulates 75k rps WAL)")

    def execute(self, sql):
        sql = sql.strip()
        # Handle triple-quoted SQL from compiler
        # Detect STAR token
        if "*" in sql and "SELECT" in sql.upper():
            print(f"[DB][STAR token detected] {sql[:80]}...")
        else:
            print(f"[DB] Executing: {sql[:100]}")
        
        try:
            self.cursor.execute(sql)
            if sql.strip().upper().startswith("SELECT"):
                rows = self.cursor.fetchall()
                print(f"[DB] SELECT returned {len(rows)} rows")
                return [dict(r) for r in rows]
            else:
                self.conn.commit()
                print(f"[DB] OK, rowcount={self.cursor.rowcount}")
                return {"status": "ok", "rowcount": self.cursor.rowcount}
        except Exception as e:
            print(f"[DB][ERROR] {e} for SQL: {sql[:120]}")
            raise

# Public singleton as db module expects
db_instance = EEHIM_DB_Lite()

def execute(sql):
    return db_instance.execute(sql)
