# Name: Nandadev Rajeev Menon
# Student Number : 3069713


# TODO: Delete the above, and include in a comment your name and student number
# TODO: Remember to fully comment your code
# TODO: Include a comment 'EXTRA FEATURE' and explain what your Extra Feature does
# TODO: Don't forget to document your design choices in your UI Design Document


# standard imports
import sys
from PyQt6.QtCore import QDate
from PyQt6.QtWidgets import (
    QApplication,
    QMainWindow,
    QTabWidget,
)
from PyQt6.QtGui import QFont
from PyQt6 import QtCore
from PortfolioPage import PortfolioPage
from GraphPage import MatplotlibWidget


class CryptoTradeProfitCalculator(QMainWindow):
    def __init__(self):
        super().__init__()
        Qt = QtCore.Qt

        arial_font = QFont("Helvetica", 12)
        self.data = self.make_data()
        self.tabs = QTabWidget()

        self.tabs.currentChanged.connect(self.tab_changed)

        self.calculation_tab = PortfolioPage(self.data)
        # self.graph_tab = GraphPage(self.data, [])
        self.graph_tab = MatplotlibWidget(self.data, self.tabs, self)

        self.calculation_tab.setFont(arial_font)
        self.graph_tab.setFont(arial_font)

        self.tabs.addTab(self.calculation_tab, "Portfolio")
        self.tabs.addTab(self.graph_tab, "Graph")

        self.setCentralWidget(self.tabs)

        self.setWindowTitle("Two Tab App")
        self.resize(500, 525)
        self.setMaximumSize(610, 900)
        self.setWindowTitle("CryptoCalculator")
        # self.setStyleSheet("QMainWindow{background-color: #d4d4d4;}")

    def tab_changed(self, index):
        if index == 1:  # Check if the "Graph" tab is selected (index 1)
            self.graph_tab.plot(self.calculation_tab.get_portfolio())
        else:  # or if the portoflio tab is selected
            self.resize(500, 525)  # bring down the size of the window

    ################ YOU DO NOT HAVE TO EDIT CODE BELOW THIS POINT  ########################################################

    def make_data(self):
        """
        This code is complete
         Data source is derived from https://www.kaggle.com/sudalairajkumar/cryptocurrencypricehistory but use the provided file to avoid confusion

         Stock   -> Date      -> Close
            BTC     -> 29/04/2013 -> 144.54
                    -> 30/04/2013 -> 139
                    .....
                    -> 06/07/2021 -> 34235.19345

                    ...

        Helpful tutorials to understand this
        - https://stackoverflow.com/questions/482410/how-do-i-convert-a-string-to-a-double-in-python
        - nested dictionaries https://stackoverflow.com/questions/16333296/how-do-you-create-nested-dict-in-python
        - https://www.tutorialspoint.com/python3/python_strings.htm
        :return: a dictionary of dictionaries
        """
        data = {}  # empty data dictionary (will store what we read from the file here)
        try:
            file = open(
                ".//combined.csv", "r"
            )  # open a CSV file for reading https://docs.python.org/3/library/functions.html#open
            file_rows = []  # empty list of file rows
            # add rows to the file_rows list
            for row in file:
                file_rows.append(
                    row.strip()
                )  # https://www.geeksforgeeks.org/python-string-strip-2/
            print(
                "**************************************************************************"
            )
            print(
                "combined.csv read successfully. Rows read from file: "
                + str(len(file_rows))
            )

            # get the column headings of the CSV file
            print("____________________________________________________")
            print("Headings of file:")
            row0 = file_rows[0]
            line = row0.split(",")
            column_headings = line
            print(column_headings)

            # get the unique list of CryptoCurrencies from the CSV file
            non_unique_cryptos = []
            file_rows_from_row1_to_end = file_rows[1 : len(file_rows) - 1]
            for row in file_rows_from_row1_to_end:
                line = row.split(",")
                non_unique_cryptos.append(line[6])
            cryptos = self.unique(non_unique_cryptos)
            print("____________________________________________________")
            print("Total Currencies found: " + str(len(cryptos)))
            print(str(cryptos))

            # build the base dictionary of CryptoCurrencies
            for crypto in cryptos:
                data[crypto] = {}

            # build the dictionary of dictionaries
            for row in file_rows_from_row1_to_end:
                line = row.split(",")
                date = self.string_date_into_QDate(line[0])
                crypto = line[6]
                close_price = line[4]
                # include error handling code if close price is incorrect
                data[crypto][date] = float(close_price)
        except:
            print("Error: combined.csv file not found. ")
            print("Make sure you have imported this file into your project.")
        # return the data
        print("____________________________________________________")
        print(
            "Amount of Currencies stored in data:", len(data)
        )  # will be 0 if empty/error
        print(
            "**************************************************************************"
        )
        return data

    def string_date_into_QDate(self, date_String):
        """
        This method is complete
        Converts a data in a string format like that in a CSV file to QDate Objects for use with QCalendarWidget
        :param date_String: data in a string format
        :return:
        """
        date_list = date_String.split("-")
        date_QDate = QDate(int(date_list[0]), int(date_list[1]), int(date_list[2]))
        return date_QDate

    def unique(self, non_unique_list):
        """
        This method is complete
        Converts a list of non-unique values into a list of unique values
        Developed from https://www.geeksforgeeks.org/python-get-unique-values-list/
        :param non_unique_list: a list of non-unique values
        :return: a list of unique values
        """
        # intilize a null list
        unique_list = []

        # traverse for all elements
        for x in non_unique_list:
            # check if exists in unique_list or not
            if x not in unique_list:
                unique_list.append(x)
                # print list
        return unique_list


if __name__ == "__main__":
    app = QApplication(sys.argv)
    currency_converter = CryptoTradeProfitCalculator()
    currency_converter.show()
    sys.exit(app.exec())
