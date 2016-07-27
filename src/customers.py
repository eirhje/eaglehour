class Customers():
    customers = []
    
    def __init__(self, sql):
        self.customers = []
        self.sql = sql   
 
    def get_customers(self):
        return self.customers
    
    def add_customer(self, custname):
        sqlid = self.sql.getCustomerId(custname)
        if len(sqlid) != 1:
            id = self.sql.createCustomerId(custname)
        else:
            id = sqlid[0]
        self.customers.append(custname)
