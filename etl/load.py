import pyodbc


class SQLServerLoader:
    def __init__(self, driver, server, database, user, password, table):
        self.driver = driver
        self.server = server
        self.database = database
        self.user = user
        self.password = password
        self.table = table

    def _get_conn(self):
        conn_str = (
            f"DRIVER={self.driver};"
            f"SERVER={self.server};"
            f"DATABASE={self.database};"
            f"UID={self.user};PWD={self.password}"
        )
        return pyodbc.connect(conn_str, autocommit=False)

    def upsert_dataframe(self, df, upsert_key, columns_map):
        """Naive upsert: for each row, try update, else insert. Use transactions."""
        if df.empty:
            return 0
        col_names = list(columns_map.values())
        placeholders = ','.join(['?'] * len(col_names))
        update_set = ','.join([f"{c} = ?" for c in col_names if c != upsert_key])

        insert_sql = f"INSERT INTO {self.table} ({', '.join(col_names)}) VALUES ({placeholders})"
        update_sql = f"UPDATE {self.table} SET {update_set} WHERE {upsert_key} = ?"

        conn = self._get_conn()
        cursor = conn.cursor()
        inserted = 0
        try:
            for _, row in df.iterrows():
                values = [row[c] for c in col_names]
                # try update
                update_values = [row[c] for c in col_names if c != upsert_key] + [row[upsert_key]]
                cursor.execute(update_sql, update_values)
                if cursor.rowcount == 0:
                    cursor.execute(insert_sql, values)
                    inserted += 1
            conn.commit()
        except Exception:
            conn.rollback()
            raise
        finally:
            cursor.close()
            conn.close()
        return inserted
