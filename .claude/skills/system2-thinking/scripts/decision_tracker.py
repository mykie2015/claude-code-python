#!/usr/bin/env python3
import sqlite3
import argparse
import json
import sys
from datetime import datetime
from pathlib import Path

# Database path: stored in .claude/thinking_history.db
DB_PATH = Path(".claude/thinking_history.db")

def get_db():
    """Connect to the database, ensuring directory exists."""
    if not DB_PATH.parent.exists():
        DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    """Initialize the decisions table."""
    conn = get_db()
    conn.execute("""
        CREATE TABLE IF NOT EXISTS decisions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp TEXT NOT NULL,
            topic TEXT NOT NULL,
            system1_draft TEXT,
            system2_critique TEXT,
            final_decision TEXT,
            tags TEXT
        )
    """)
    conn.execute("""
        CREATE TABLE IF NOT EXISTS feedback (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            decision_id INTEGER NOT NULL,
            timestamp TEXT NOT NULL,
            content TEXT NOT NULL,
            FOREIGN KEY(decision_id) REFERENCES decisions(id)
        )
    """)
    conn.commit()
    conn.close()

def log_decision(topic, draft, critique, final, tags=None):
    """Log a new decision process."""
    init_db()
    conn = get_db()
    conn.execute("""
        INSERT INTO decisions (timestamp, topic, system1_draft, system2_critique, final_decision, tags)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (datetime.now().isoformat(), topic, draft, critique, final, tags))
    conn.commit()
    print(f"✅ Logged decision: '{topic}'")
    conn.close()

def add_feedback(decision_id, content):
    """Add feedback to an existing decision."""
    init_db()
    conn = get_db()
    
    # Check if decision exists
    cur = conn.execute("SELECT topic FROM decisions WHERE id = ?", (decision_id,))
    row = cur.fetchone()
    if not row:
        print(f"❌ Error: Decision ID {decision_id} not found.")
        return

    conn.execute("""
        INSERT INTO feedback (decision_id, timestamp, content)
        VALUES (?, ?, ?)
    """, (decision_id, datetime.now().isoformat(), content))
    conn.commit()
    print(f"✅ Added feedback to decision {decision_id}: '{row['topic']}'")
    conn.close()

def search_decisions(query=None, limit=5):
    """Search historical decisions."""
    init_db()
    conn = get_db()
    sql = "SELECT id, timestamp, topic, final_decision FROM decisions"
    params = []
    
    if query:
        sql += " WHERE topic LIKE ? OR tags LIKE ?"
        params = [f"%{query}%", f"%{query}%"]
    
    sql += " ORDER BY id DESC LIMIT ?"
    params.append(limit)
    
    cursor = conn.execute(sql, params)
    rows = cursor.fetchall()
    
    if not rows:
        print("No matching decisions found.")
        return

    print(f"\nrunning search for: {query if query else 'all'}\n")
    print(f"{'ID':<4} | {'Date':<16} | {'Topic':<30} | {'Decision'}")
    print("-" * 80)
    for row in rows:
        date_str = row['timestamp'][:16].replace('T', ' ')
        topic = (row['topic'][:27] + '...') if len(row['topic']) > 27 else row['topic']
        decision = (row['final_decision'][:30] + '...') if row['final_decision'] and len(row['final_decision']) > 30 else row['final_decision']
        print(f"{row['id']:<4} | {date_str:<16} | {topic:<30} | {decision}")
        
        # Fetch feedback
        f_cursor = conn.execute("SELECT timestamp, content FROM feedback WHERE decision_id = ?", (row['id'],))
        f_rows = f_cursor.fetchall()
        if f_rows:
            print(f"     └── 📝 Feedback:")
            for f_row in f_rows:
                f_date = f_row['timestamp'][:10]
                print(f"         [{f_date}] {f_row['content']}")
            print("")

    print("\n")
    conn.close()

def main():
    parser = argparse.ArgumentParser(description="Track System 2 Thinking Decisions")
    subparsers = parser.add_subparsers(dest="command", required=True)

    # Log command
    log_parser = subparsers.add_parser("log", help="Log a new thinking process")
    log_parser.add_argument("--topic", required=True, help="What is being decided?")
    log_parser.add_argument("--draft", required=True, help="Initial System 1 draft/thought")
    log_parser.add_argument("--critique", required=True, help="System 2 critique/analysis")
    log_parser.add_argument("--final", required=True, help="Final decision")
    log_parser.add_argument("--tags", help="Comma-separated tags (e.g., 'architecture,db')")

    # Search command
    search_parser.add_argument("query", nargs="?", help="Search term for topic/tags")
    search_parser.add_argument("--limit", type=int, default=5, help="Number of results")

    # Feedback command
    feedback_parser = subparsers.add_parser("add-feedback", help="Add feedback to a decision")
    feedback_parser.add_argument("--id", type=int, required=True, help="Decision ID")
    feedback_parser.add_argument("--content", required=True, help="Feedback content")

    args = parser.parse_args()

    if args.command == "log":
        log_decision(args.topic, args.draft, args.critique, args.final, args.tags)
    elif args.command == "search":
        search_decisions(args.query, args.limit)
    elif args.command == "add-feedback":
        add_feedback(args.id, args.content)

if __name__ == "__main__":
    main()
