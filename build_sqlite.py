#!/usr/bin/env python3
import hashlib
import sqlite3
from pathlib import Path
import time

ROCKYOU = Path("rockyou.txt")
DBPATH = Path("rockyou_md5.db")
BATCH_SIZE = 100_000

def md5_bytes(b: bytes) -> str:
    return hashlib.md5(b).hexdigest()

def prepare_db(dbpath: Path):
    if dbpath.exists():
        print("Reusing existing DB:", dbpath)
    conn = sqlite3.connect(str(dbpath))
    cur = conn.cursor()
    cur.execute("PRAGMA synchronous = OFF;")
    cur.execute("PRAGMA journal_mode = WAL;")
    cur.execute("PRAGMA temp_store = MEMORY;")
    cur.execute("""
    CREATE TABLE IF NOT EXISTS rockyou (
        md5 TEXT PRIMARY KEY,
        password BLOB
    );
    """)
    conn.commit()
    return conn

def build_index(rockyou_path: Path, dbpath: Path):
    conn = prepare_db(dbpath)
    cur = conn.cursor()
    inserted = 0
    batch = []
    start = time.time()
    with rockyou_path.open("rb") as fh:
        for i, line in enumerate(fh, start=1):
            pw_bytes = line.rstrip(b"\r\n")
            h = md5_bytes(pw_bytes)
            batch.append((h, pw_bytes))
            if len(batch) >= BATCH_SIZE:
                cur.executemany("INSERT OR IGNORE INTO rockyou (md5, password) VALUES (?, ?);", batch)
                conn.commit()
                inserted += len(batch)
                elapsed = time.time() - start
                print(f"Inserted {inserted:,} rows — elapsed {elapsed:.1f}s")
                batch = []
    # final batch
    if batch:
        cur.executemany("INSERT OR IGNORE INTO rockyou (md5, password) VALUES (?, ?);", batch)
        conn.commit()
        inserted += len(batch)
    elapsed = time.time() - start
    print(f"Done. Total inserted (approx): {inserted:,} rows in {elapsed:.1f}s")
    conn.close()

if __name__ == "__main__":
    if not ROCKYOU.exists():
        raise SystemExit("rockyou.txt not found in current directory.")
    build_index(ROCKYOU, DBPATH)
