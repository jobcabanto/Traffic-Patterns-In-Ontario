
import sqlite3
from datetime import datetime
dbConnect, dbCursor = None, None

class DatabaseManagement(object):

    def connect():

        global dbConnect

        # Connect to database and create one if not already created

        if dbConnect == None:
            try:
                dbConnect = sqlite3.connect("gmpDatabase")
            except:
                dbConnect = sqlite3.connect("gmpDatabase.db")
        dbCursor = dbConnect.cursor()
        dataTable = """ CREATE TABLE IF NOT EXISTS gmpDatabase (Day_of_Week text, Date text, Local_Time text, Origin text, Destination text, Travel_Time text, Distance text,
                    Transportation text, Traffic_Model text) """
        try:
            dbCursor.execute(dataTable)
            dbConnect.commit(dataTable)
        except:
            pass
        return dbConnect, dbCursor
    
    def epochTimeCalculator():
        time, days = 1691755200, 28
        for i in range(1, days + 1):
            print(time + (86400 * (i)))

    def dateFormatter():
        departureTime = 1691755200
        print(datetime.fromtimestamp(departureTime).strftime('%A'))
        pass

# time = DatabaseManagement()
# time.dateFormatter()

