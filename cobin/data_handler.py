import sqlite3
import sys
import argparse


def connect(db_path):
    return sqlite3.connect(db_path)


def list_tables(conn):
    cursor = conn.cursor()
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    return [row[0] for row in cursor.fetchall()]


def print_db(conn, output_path):
    cursor = conn.cursor()
    with open(output_path, 'w', encoding='utf-8') as f:
        for table in list_tables(conn):
            f.write(f"Table: {table}\n")
            cursor.execute(f"PRAGMA table_info({table});")
            cols = [col[1] for col in cursor.fetchall()]
            f.write("\t" + "\t".join(cols) + "\n")
            cursor.execute(f"SELECT * FROM {table}")
            for row in cursor.fetchall():
                f.write("\t" + "\t".join(str(item) for item in row) + "\n")
            f.write("\n")


def create_table(conn, table_name, schema):
    cursor = conn.cursor()
    cursor.execute(f"CREATE TABLE IF NOT EXISTS {table_name} ({schema});")
    conn.commit()
    print(f"Table '{table_name}' created or already exists.")


def insert_row(conn, table_name, values):
    cursor = conn.cursor()
    placeholders = ",".join("?" for _ in values)
    cursor.execute(f"INSERT INTO {table_name} VALUES ({placeholders})", values)
    conn.commit()
    print("Row inserted.")


def update_row(conn, table_name, set_clause, where_clause):
    cursor = conn.cursor()
    cursor.execute(f"UPDATE {table_name} SET {set_clause} WHERE {where_clause};")
    conn.commit()
    print(f"Rows updated: {cursor.rowcount}")


def delete_row(conn, table_name, where_clause):
    cursor = conn.cursor()
    cursor.execute(f"DELETE FROM {table_name} WHERE {where_clause};")
    conn.commit()
    print(f"Rows deleted: {cursor.rowcount}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="SQLite CRUD and dump utility.")
    parser.add_argument("db", help="Path to SQLite database file.")
    sub = parser.add_subparsers(dest="cmd", required=True)

    # Dump command
    dump = sub.add_parser("dump", help="Dump all tables to a text file.")
    dump.add_argument("output", nargs="?", default="db_dump.txt", help="Output text file path.")

    # Create table command
    ct = sub.add_parser("create", help="Create a new table.")
    ct.add_argument("table", help="Table name.")
    ct.add_argument("schema", help="Column definitions, e.g. 'id INTEGER PRIMARY KEY, name TEXT'.")

    # Insert command
    ins = sub.add_parser("insert", help="Insert a row into a table.")
    ins.add_argument("table", help="Table name.")
    ins.add_argument("values", nargs='+', help="Values for the row, in order.")

    # Update command
    upd = sub.add_parser("update", help="Update rows in a table.")
    upd.add_argument("table", help="Table name.")
    upd.add_argument("set", dest="set_clause", help='SET clause, e.g. \'name="Alice"\'.')
    upd.add_argument("where", dest="where_clause", help="WHERE clause, e.g. 'id=1'.")

    # Delete command
    dlt = sub.add_parser("delete", help="Delete rows from a table.")
    dlt.add_argument("table", help="Table name.")
    dlt.add_argument("where", dest="where_clause", help="WHERE clause, e.g. 'id=1'.")

    args = parser.parse_args()
    conn = connect(args.db)

    if args.cmd == "dump":
        print_db(conn, args.output)
        print(f"Data has been saved to {args.output}")
    elif args.cmd == "create":
        create_table(conn, args.table, args.schema)
    elif args.cmd == "insert":
        insert_row(conn, args.table, args.values)
    elif args.cmd == "update":
        update_row(conn, args.table, args.set_clause, args.where_clause)
    elif args.cmd == "delete":
        delete_row(conn, args.table, args.where_clause)

    conn.close()
