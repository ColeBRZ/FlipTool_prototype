import time
from zillow_api import get_home_description
from database_connection import db_connection, db_cursor, add_training_data
from random import uniform

# Lines of SQL for analyzing the data
# 1. View everything in database table -> SELECT * FROM flipdata.flip_train1;
# 2. Get row count -> SELECT COUNT(*) FROM flipdata.flip_train1;
# 3. Get all flips -> SELECT * FROM flipdata.flip_train1 WHERE class = 1;
# 4. Get flips count -> SELECT COUNT(*) FROM flipdata.flip_train1 WHERE class = 1;
# 5. Newest row insert -> SELECT * FROM flipdata.flip_train1 ORDER BY zpid ASC LIMIT 1;

def get_training_data(file_path):
    keywords = ["fixer", "fixer-upper", "preforeclosure", "pre-foreclosure", "investment", "investor",
                "investors", "as-is", "repair", "repairs", "rehabilitation", "rehab", "flip"]
    db = db_connection()
    cursor = db_cursor(db)
    try:
        with open(file_path, "r") as file:
            for zpid in file:
                zpid = zpid.strip()
                if zpid:
                    print(f"Processing ZPID: {zpid}")
                    description = get_home_description(zpid)
                    cursor.execute("SELECT COUNT(*) FROM flip_train1 WHERE zpid = %s", (zpid,)) # check for zpid in database # saves time
                    if cursor.fetchone()[0] > 0:
                        print(f"ZPID {zpid} already exists in the database. Skipping.")
                        time.sleep(uniform(.4, .8))
                        continue

                    if description is None or description.strip() == "": # check if description is none # saves time
                        print(f"Warning: No description found for ZPID {zpid}. Skipping this entry.")
                        time.sleep(uniform(.4, .8))
                        continue  # Skip to the next ZPID without adding to the database

                    tokenized_home_details = description.lower().split()
                    is_flip = any(keyword in tokenized_home_details for keyword in keywords)
                    data = (zpid, description, 1 if is_flip else 0)
                    add_training_data(db, cursor, data)
                    db.commit()
                    time.sleep(uniform(.4, .8))
    except Exception as e:
        print(f"An error occurred: {e}")
        db.rollback()
    finally:
        cursor.close()
        db.close()

def main():
    zpid_files = [
        "for-sale-by-agent_zpids.txt",
        "for-sale-by-owner_zpids.txt",
        "auction_zpids.txt"
    ]
    for file in zpid_files:
        get_training_data(file)

if __name__ == "__main__":
    main()