import psycopg2, csv, time, logging

# This is a wrapper around the default psycopg2 Postgres module
# It adds records in batches set by the default BATCH_SIZE or by an override

BATCH_SIZE = 500


class PostgresWrapper:
    def __init__(
        self,
        default_database="postgres",
        user="postgres",
        password="postgres",
        host="localhost",
        port="5432",
        default_batch_size=BATCH_SIZE,
    ):
        self.conn = psycopg2.connect(
            f"dbname='{default_database}' user='{user}' host='{host}' password='{password}'"
        )
        self.batch_size = default_batch_size

    def insert_data(self, schema, table, fields, data, primary_key=None):
        # Build standard query parts
        fields_str = ",".join(fields)
        query_prefix = f"""INSERT INTO {schema}.{table} ({fields_str}) VALUES """
        query_suffix = (
            f" on conflict ({primary_key}) do nothing;" if primary_key else ""
        )
        # Execute query in batches
        cur = self.conn.cursor()
        mogrify_str = "(" + (len(data[0]) * "%s,")[:-1] + ")"
        for x in range(0, len(data), self.batch_size):
            print(
                "Inserting records {} to {}".format(
                    str(x), str(x + self.batch_size - 1)
                )
            )
            tupled_data = [tuple(x) for x in data[x : x + self.batch_size - 1]]
            args_str = ",".join(
                cur.mogrify(mogrify_str, i).decode("utf-8") for i in tupled_data
            )
            cur.execute(query_prefix + args_str + query_suffix)

        # Run commit at end to allow rollback if error occurs
        self.conn.commit()
        return "Added"
