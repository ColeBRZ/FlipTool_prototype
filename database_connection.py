import mysql.connector


def db_connection():
    try:
        db = mysql.connector.connect(
            host="localhost",
            user="coleb",
            passwd="computerscience101!?!",
            database="flipdata"
        )
        return db
    except:
        print("Unsuccessful connection to DB")
        return None


def db_cursor(db):
    cursor = db.cursor()
    return cursor


def add_table(num_int, cursor):
    try:
        num = str(num_int)
        create_table_query = """
        CREATE TABLE flip_train{} (
            zpid INT,
            description TEXT,
            class BOOL
        )
        """.format(num)
        cursor.execute(create_table_query)
        print(f"Successfully created table 'flip_train{num}'")
    except mysql.connector.Error as err:
        if err.errno == 1050:  # Error number for "Table already exists"
            print(f"Table 'flip_train{num}' already exists")
        else:
            print(f"MySQL Error: {err}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")


def add_training_data(db, cursor, data):
    table_name = "flip_train1"
    if table_exists(db, cursor, table_name):
        try:
            insert_query = f"""
            INSERT INTO {table_name} (zpid, description, class)
            VALUES (%s, %s, %s)
            """
            cursor.execute(insert_query, data)
            print(f"Data inserted for ZPID: {data[0]}")
        except mysql.connector.Error as err:
            print(f"Error inserting data for ZPID {data[0]}: {err}")
    else:
        print(f"Table {table_name} does not exist")


def table_exists(db, cursor, table_name):
    query = """
    SELECT COUNT(*) 
    FROM information_schema.tables 
    WHERE table_schema = %s 
    AND table_name = %s
    """
    cursor.execute(query, (db.database, table_name))
    count = cursor.fetchone()[0]
    return count > 0


def main():
    db = db_connection()
    cursor = db_cursor(db)
    cursor.execute("SELECT SCHEMA_NAME FROM information_schema.SCHEMATA WHERE SCHEMA_NAME = 'flipdata'")
    result = cursor.fetchone()

    if result:
        print("Database exists")
    else:
        try:
            print("Database does not exist.\n"
                  "Creating database now...")
            create_db_query = "CREATE DATABASE flipdata"
            cursor.execute(create_db_query)
            print("Database 'flipdata' created")
        except:
            print("Database creation unsuccessful")
            return None

    add_table(1, cursor)

    db.commit()
    cursor.close()
    db.close()

if __name__ == "__main__":
    main()