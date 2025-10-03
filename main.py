import sqlite3
from pathlib import Path

DBPATH = Path("rockyou_md5.db")

def lookup_md5(md5hex: str):
    conn = sqlite3.connect(str(DBPATH))
    cur = conn.cursor()
    cur.execute("SELECT password FROM rockyou WHERE md5 = ?;", (md5hex,))
    row = cur.fetchone()
    conn.close()
    if row is None:
        return None
    return row[0]  # bytes

if __name__ == "__main__":
    targets = [
        "3173784ba37c4575c6a26bd23f62a45d",
        "457f8cf0fc9af872df765130c9031de0",
        "56979302a7e8a87673e8334a9d085e8b",
        "f30aa7a662c728b7407c54ae6bfd27d1"
    ]
    for t in targets:
        pw = lookup_md5(t)
        if pw is None:
            print(f"{t} => Strong Password")
        else:
            try:
                print(f"{t} => Weak Password (password: {pw.decode('utf-8')})")
            except UnicodeDecodeError:
                print(t, "=>", pw)  # bytes fallback
