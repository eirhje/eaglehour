#!/usr/bin/env python

#Import the required files
from statusicon import StatusIcon
from window import WindowGUI
from customers import Customers
from sql import SQLInterface

import os, sys

def main():
    """ Connect to SQL """
    sql = SQLInterface()

    """ Get a list of the customers """
    c = Customers(sql)
    file = open("customers.txt")
    for cust in file.readlines():
        c.add_customer(cust)

    """ Start the main window thread with a customer object """
    wg = WindowGUI(c, sql)
    """ Pass the control object, wg, to the statusicon thread object """
    StatusIcon(wg)
    print '\n [eaglehour] Launched statusIcon, find me there :-)'

""" Launch into the background """
if os.fork() == 0:
	main()
