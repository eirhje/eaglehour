import sqlite


class SQLInterface:

    def __init__(self):
        self.connection = sqlite.connect("eaglehour.db")
        self.cursor = self.connection.cursor()
        self.__createtable()

    # Create the tables if they dont exist.
    def __createtable(self):
        try:
            self.cursor.execute("CREATE TABLE Hours ("
                                + " HourId INTEGER PRIMARY KEY,"
                                + " CustomerId INTEGER,"
                                + " StartTime TIMESTAMP,"
                                + " StopTime TIMESTAMP,"
                                + " Description CHAR(255) )")
            self.connection.commit()

            self.cursor.execute("CREATE TABLE Customers ("
                                + " CustomerId INTEGER PRIMARY KEY,"
                                + " CustomerName CHAR(255) )")
            self.connection.commit()
        except:
            1

    def __undo(self):
        self.cursor.rollback()

    # Call this when changing customer / starting to work
    def startHour(self, CustomerId):
        self.cursor.execute("INSERT INTO Hours (CustomerId, StartTime) "
                            + "VALUES ('" + str(CustomerId) + "',DATETIME('NOW'))")
        self.connection.commit()

        self.ActiveHoursId = self.cursor.lastrowid

    # Call this every 15 minits
    def keepHour(self, CustomerId):
        self.cursor.execute("UPDATE Hours SET StopTime = DATETIME('NOW') "
                            + "WHERE HourId = '" + str(self.ActiveHoursId) + "'")
        self.connection.commit()

    # Call this when we pause and when we are done with the client
    def doneHour(self, CustomerId, Description):
        self.keepHour(CustomerId)
        self.cursor.execute("UPDATE Hours SET Description = '" + Description + "' "
                            + "WHERE HourId = '" + str(self.ActiveHoursId) + "'")
        self.connection.commit()

    # Create a CustomerId from CustomerName
    def createCustomerId(self, CustomerName):
        self.cursor.execute("INSERT INTO Customers (CustomerName) "
                            + "VALUES ('" + CustomerName + "') ")
        self.connection.commit()
        return self.cursor.lastrowid

    # get the CustomerId from CustomerName
    def getCustomerId(self, CustomerName):
        self.cursor.execute("SELECT CustomerId FROM Customers "
                            + "WHERE CustomerName = '" + CustomerName + "'")
        return self.cursor.fetchall()

    # get the CustomerName from CustomerId
    def getCustomerName(self, CustomerId):
        self.cursor.execute("SELECT CustomerName FROM Customers "
                            + "WHERE CustomerId = '" + str(CustomerId) + "'")
        return self.cursor.fetchall()
