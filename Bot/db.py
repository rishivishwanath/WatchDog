import psycopg2
from config import DB_CONFIG  # contains database connection info
from decimal import Decimal

def get_conn():
    return psycopg2.connect(**DB_CONFIG)

def init_db():
    try:
        conn = get_conn()
        cur = conn.cursor()
        cur.execute("""
            CREATE TABLE IF NOT EXISTS subscribers (
                chat_id BIGINT,
                pair_name TEXT,
                min_lot NUMERIC,
                min_percentage NUMERIC,
                PRIMARY KEY (chat_id, pair_name)
            );
        """)
        conn.commit()
        cur.close()
        conn.close()
    except Exception as e:
        print(f"DB Error [init_db]: {e}")


def add_subscriber(chat_id, pair_name, min_lot, min_percentage):
    try:
        init_db()
        conn = get_conn()
        cur = conn.cursor()
        cur.execute("""
            INSERT INTO subscribers (chat_id, pair_name, min_lot, min_percentage)
            VALUES (%s, %s, %s, %s)
            ON CONFLICT (chat_id, pair_name) DO NOTHING;
        """, (chat_id, pair_name, min_lot, min_percentage))
        conn.commit()
        cur.close()
        conn.close()
    except Exception as e:
        print(f"DB Error [add_subscriber]: {e}")


def remove_subscriber(chat_id):
    try:
        init_db()
        conn = get_conn()
        cur = conn.cursor()
        cur.execute("DELETE FROM subscribers WHERE chat_id = %s;", (chat_id,))
        conn.commit()
        cur.close()
        conn.close()
    except Exception as e:
        print(f"DB Error [remove_subscriber]: {e}")

def get_subscribers_by_filters(pair_name, min_percentage_threshold, min_lot_threshold):
    try:
        # Ensure thresholds are Decimal for correct comparison
        min_percentage_threshold = Decimal(str(min_percentage_threshold))
        min_lot_threshold = Decimal(str(min_lot_threshold))

        conn = get_conn()
        cur = conn.cursor()
        cur.execute("""
            SELECT chat_id, pair_name, min_lot, min_percentage
            FROM subscribers
            WHERE pair_name = %s
              AND min_percentage <= %s
              AND min_lot <= %s;
        """, (pair_name, min_percentage_threshold, min_lot_threshold))
        rows = cur.fetchall()
        cur.close()
        conn.close()
        return rows
    except Exception as e:
        print(f"DB Error [get_subscribers_by_filters]: {e}")
        return []

def get_all_subscribers():
    try:    
        conn = get_conn()
        cur = conn.cursor()
        cur.execute("""
            SELECT chat_id, pair_name, min_lot, min_percentage
            FROM subscribers;
        """)
        rows = cur.fetchall()
        cur.close()
        conn.close()
        return rows
    except Exception as e:
        print(f"DB Error [get_all_subscribers]: {e}")
        return []
