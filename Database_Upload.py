import mariadb
import sys


def main(username, password):
    # Connect to AWS MariaDB
    try:
        conn = mariadb.connect(
            user=dbUsername,
            password=password,
            host="reecipy-2.c5gknunzqmr7.us-west-2.rds.amazonaws.com",
            port=3306,
            database="Recipes"
        )
    except mariadb.Error as e:
        print(f"Error connecting to MariaDB Platform: {e}")
        sys.exit(1)

    cur = conn.cursor()


if __name__ == '__main__':
    dbUsername = input("Enter database username: ")
    dbPassword = input("Enter database password: ")
    main(dbUsername, dbPassword)
