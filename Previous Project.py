#!/usr/bin/env python3

import mysql.connector
import os.path
from db_tunnel import DatabaseTunnel

DB_HOST = "cs.westminstercollege.edu"
DB_SSH_PORT = 2322
DB_SSH_USER = "student"
DB_PORT = 3306

# Default connection information (can be overridden with command-line arguments)
DB_SSH_KEYFILE = "id_rsa.cmpt307"
DB_NAME = "rar0805_Project" \
          ""
DB_USER = "token_fcbf"
DB_PASSWORD = "P38BFobRO4RSDA82"




QUERY1 = """
Select Name, Number, Direction, Date(Callstart) as date_cur, Time(Callstart) as time_cur, Timediff(Callend,Callstart) as
 Call_Length From PhoneCall inner join Contact on PhoneCall.Contact_ID = Contact.ID order by Callstart Desc limit 100;
"""

QUERY2 = """
Select Name, Number, Count(*) from Contact inner join PhoneCall on PhoneCall.Contact_ID = Contact.ID where 
PhoneCall.Callstart between now()-Interval 14 day and now() group by Contact.ID Order by count(*) desc limit 5;
"""

Query3 = """
Select Name, Number, Direction, Date(Callstart) as Date, Time(Callstart) as Time, Timediff(Callend,Callstart) as Length 
From PhoneCall inner join Contact on PhoneCall.Number = Contact.Phone_primary or PhoneCall.Number = Contact.Phone_secondary 
having Name = %(string)s or PhoneCall.Number = %(string)s order by Callstart ;
"""

Query4 = """
Select * from (Select Name, Contact.Phone_primary as Number, text, Direction, Date(Time) as Date, Time(Time) as Time
From Message inner join Contact on Message.Contact_ID = Contact.ID) as Messlist
where Messlist.Name = %(string)s or Messlist.Number = %(string)s  order by Time Desc;

"""

Query5 = """insert into Message (direction,Number,Text,Time) Values ('sent',%s,%s,now());"""

Query6 = """ 
Insert into Contact (Name, Phone_primary, Phone_secondary) Values (%s,%s,%s)
"""

Query7 = """
Select * from Contact Where Name is not %s
"""

Query8 = """
Update Contact set Name = %s Where Name = %s
"""

def FixTime(TD):
    hours = TD.seconds // 3600
    minutes = (TD.seconds - (3600 * hours)) // 60
    return print('Call Length :', hours, 'hours', minutes, 'minutes', TD.seconds - 3600*hours - 60*minutes, 'seconds',end =" ")


class MainQuery:

    def __init__(self, dbHost, dbPort, dbName, dbUser, dbPassword):
        self.dbHost, self.dbPort = dbHost, dbPort
        self.dbName = dbName
        self.dbUser, self.dbPassword = dbUser, dbPassword

    def __enter__(self):
        self.connect()
        return self

    def __exit__(self, *args):
        self.close()

    def connect(self):
        self.connection = mysql.connector.connect(
                host=self.dbHost, port=self.dbPort, database=self.dbName,
                user=self.dbUser, password=self.dbPassword,
                use_pure=True, autocommit=True
        )
        self.cursor = self.connection.cursor()

    def close(self):
        self.connection.close()


    def runApp(self):

        while True:
            line = input("\nTo see your list of contacts, enter 0.\nTo see the full call history, enter 1.\nTo see the 5 most recently called "
                     "people, enter 2.\nTo view call history to a name or number, "
                     "enter 3.\n"
                     "To view the text messages sent between you and someone, enter 4. \n"
                     "To send a text message, enter 5.\nTo add a contact, "
                     "enter 6.\nTo delete a Contact (Calls and contacts will be saved), enter 7.\nTo quit, hit enter: ")
            if not line.strip():
                break
            if line.strip() == '1':
                self.Call_History()
            if line.strip() == '2':
                self.FiveMostRecent()
            if line.strip() == '3':
                line2 = input("What would you like to search (either name or phone number)?:")
                self.ContactSearch(line2)
            if line.strip() == '4':
                line3 = input("Who do you want to see your conversation with (either name or phone number)?:")
                self.MessageContact(line3)
            if line.strip() == '5':
                line4 = input("Who do you want to send a message to (phone number?:")
                line5 = input("What would you like to send (up to 150 characters)?:")
                self.SendText(line4, line5)
            if line.strip() == '6':
                line6 = input("If you would like to add both a primary and secondary phone number, type 1 and hit enter.\nOtherwise, just hit enter:")
                if line6 == '1':
                    line7 = input("Ok, please enter the person's Name:")
                    line8 = input("Now enter their primary phone number:")
                    line9 = input("Lastly, enter their secondary phone number:")
                    self.AddContact(line7, line8, line9)
                else:
                    line10 = input("Ok, please enter the person's Name:")
                    line11 = input("Now enter their phone number:")
                    self.AddContact(line10, line11, None)
            if line.strip() == '7':
                line12 = input("Please enter the name of the person you'd like delete from your contact list:")
                self.DeleteName(None, line12)

            if line.strip() == '0':
                self.ContactList(None)

    def Call_History(self):
        self.cursor.execute(QUERY1)
        for row in self.cursor.fetchall():
            print(row[0], row[1], row[2], row[3], row[4], end='  ')
            FixTime(row[5])
            print()

    def ContactSearch(self, string):
        self.cursor.execute(Query3, {'string': string})
        for row in self.cursor.fetchall():
            print(row[0], row[1], row[2], row[3], row[4], end = '  ')
            FixTime(row[5])
            print()

    def FiveMostRecent(self):
        self.cursor.execute(QUERY2)
        for row in self.cursor.fetchall():
            print(row)

    def MessageContact(self, string):
        self.cursor.execute(Query4, { 'string': string })
        for row in self.cursor.fetchall():
            print(row[0], row[1], row[2], row[3], row[4], row[5])

    def SendText(self, number, message):
        self.cursor.execute(Query5, (number, message))
        print('message sent :) ')

    def AddContact(self, Name, PNumber, SNumber):
        self.cursor.execute(Query6, (Name, PNumber, SNumber))
        print('Contact Added')

    def ContactList(self, adapter):
        self.cursor.execute(Query7, (adapter,))
        for row in self.cursor.fetchall():
            print(row[1], row[2], row[3])

    def DeleteName(self, adapter, Name):
        self.cursor.execute(Query8, (adapter, Name))
        print('Done')


def main():
    import sys
    '''Entry point of the application. Uses command-line parameters to override database connection settings, then invokes runApp().'''
    # Default connection parameters (can be overridden on command line)
    params = {
        'sshkeyfile':   DB_SSH_KEYFILE,
        'dbname':       DB_NAME,
        'user':         DB_USER,
        'password':     DB_PASSWORD
    }

    needToPrintHelp = False

    # Parse command-line arguments, overriding values in params
    i = 1
    while i < len(sys.argv) and not needToPrintHelp:
        arg = sys.argv[i]
        isLast = (i + 1 == len(sys.argv))

        if arg in ("-h", "-help"):
            needToPrintHelp = True
            break

        elif arg in ("-sshkeyfile", "-dbname", "-user", "-password"):
            if isLast:
                needToPrintHelp = True
            else:
                params[arg[1:]] = sys.argv[i + 1]
                i += 1
            break

        else:
            print("Unrecognized option: " + arg, file=sys.stderr)
            needToPrintHelp = True

        i += 1

    # If help was requested, print it and exit
    if needToPrintHelp:
        printHelp()
        return

    try:
        with \
            DatabaseTunnel(params['sshkeyfile']) as tunnel, \
            MainQuery(
                dbHost='localhost', dbPort=tunnel.getForwardedPort(),
                dbName=params['dbname'],
                dbUser=params['user'], dbPassword=params['password']
            ) as app:
            app.runApp()
    except mysql.connector.Error as err:
        print("Error communicating with the database (see full message below).", file=sys.stderr)
        print(err, file=sys.stderr)
        print("\nParameters used to connect to the database:", file=sys.stderr)
        print(f"\tSSH keyfile: {params['sshkeyfile']}\n\tDatabase name: {params['dbname']}\n\tUser: {params['user']}\n\tPassword: {params['password']}", file=sys.stderr)
        print("""
(Did you install mysql-connector-python and sshtunnel with pip3/pip?)
(Are the username and password correct?)""", file=sys.stderr)


def printHelp():
    print(f'''
Accepted command-line arguments:
    -help, -h          display this help text
    -sshkeyfile <path> override ssh keyfile
                       (default: {DB_SSH_KEYFILE})
    -dbname <text>     override name of database to connect to
                       (default: {DB_NAME})
    -user <text>       override database user
                       (default: {DB_USER})
    -password <text>   override database password
    ''')


if __name__ == "__main__":
    main()