#!/bin/bash

URL="https://raw.githubusercontent.com/josuamarcelc/common-password-list/refs/heads/main/rockyou_2025_00.txt"
LOCAL_FILE="rockyou.txt"
DB_FILE="rockyou_md5.db"
PYTHON_SCRIPT="build_sqlite.py"
EXTRA_WORDS=("hello123@")

if [ ! -f "$LOCAL_FILE" ]; then
    echo "[INFO] $LOCAL_FILE not found. Downloading..."
    curl -L -o "$LOCAL_FILE" "$URL"
    if [ $? -ne 0 ]; then
        echo "[ERROR] Failed to download $URL"
        exit 1
    fi
else
    echo "[INFO] $LOCAL_FILE already exists. Skipping download."
fi

for line in "${EXTRA_WORDS[@]}"; do
    if ! grep -Fxq "$line" "$LOCAL_FILE"; then
        echo "$line" >> "$LOCAL_FILE"
        echo "[INFO] Added extra line: $line"
    fi
done

if [ ! -f "$DB_FILE" ]; then
    echo "[INFO] $DB_FILE not found. Running $PYTHON_SCRIPT..."
    python3 "$PYTHON_SCRIPT"
    if [ $? -ne 0 ]; then
        echo "[ERROR] Failed to generate $DB_FILE using $PYTHON_SCRIPT"
        exit 1
    fi
else
    echo "[INFO] $DB_FILE already exists. Skipping DB generation."
fi
