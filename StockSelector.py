# Name: Nandadev Rajeev Menon
# Student Number : 3069713

import sys
from PyQt6.QtCore import QDate
from PyQt6.QtWidgets import (
    QLabel,
    QComboBox,
    QCalendarWidget,
    QDialog,
    QApplication,
    QGridLayout,
    QSpinBox,
    QWidget,
    QVBoxLayout,
    QSizePolicy,
    QPushButton,
    QMessageBox,
)
from PyQt6.QtGui import QFont
from PyQt6 import QtCore
from DeleteButton import DeleteButton
from decimal import Decimal

# This is an EXTENSION OF THE MAIN FEATURE and it allows selection of mutliple stocks(upto 3) within the same date range if possible (different stocks have a different date range)


class StockSelector(QGridLayout):
    def __init__(self, parent, coin_data, update_calculations):
        super().__init__()
        Qt = QtCore.Qt

        self.parent_component = parent
        self.coin_data = coin_data
        self.stock_names = sorted(self.coin_data.keys())
        self.update_main_calculations = update_calculations
        self.dates = [
            QDate(2021, 7, 5),
            QDate(2021, 7, 6),
        ]  # initial default purchase and sale date
        self.bold_font = QFont("Helvetica", 12)
        self.bold_font.setBold(True)
        self.color_red = "color:#b30406;"
        self.color_black = "color:black;"
        self.color_green = "color:#098709;"

        self.stock_forms_dict = (
            {}
        )  # caontains all the elements that make up the "form" for the different stock names and amounts
        self.grid_row_count = 0  # used for the addition of new stock forms
        self.stock_id_count = (
            0  # used to keep track of a unique new id for each added stock
        )
        self.stock_count = 0  # actual number of stocks in portfolio

        self.add_new_stock_button = QPushButton("Add Another Stock")
        self.add_new_stock_button.setMaximumWidth(200)
        self.add_new_stock_button.clicked.connect(self.add_stock_option)

        self.addWidget(self.add_new_stock_button, 0, 8, 1, 1)

        self.add_stock_option()  # add one stock option by default

        self.update_stock_costs(self.dates)  # update the costs for that stock option

    def add_stock_option(self):  # to add a new stock option form
        if self.stock_count == 2:
            self.add_new_stock_button.setEnabled(
                False
            )  # disable the button after adding the third stock option

        label_stock_purchased = QLabel("Stock Purchased:")
        label_stock_purchased.setFont(self.bold_font)
        label_amount_purchased = QLabel("Amount Purchased:")
        purchase_cost_label = QLabel("Cost Price:")
        selling_price_label = QLabel("Selling Price:")
        purchase_cost_value_label = QLabel("")  # shows total cost price
        selling_price_value_label = QLabel("")  # shows total sale price
        delete_stock_button = DeleteButton(
            self.stock_id_count,  # make a delete button with a unique ID
            self.remove_stock_option,  # pass in reference to remove_stock_option method
        )
        combo_for_stocks = QComboBox()  # for selecting one out of different stock names

        for x in self.stock_names:
            combo_for_stocks.addItem(x)  # add the stock names to the combobox

        stock_amount_spin = QSpinBox()  # to select the number of stocks to buy
        stock_amount_spin.setMaximum(1000000)  # reasonable maximum chosen
        stock_amount_spin.setMinimum(1)

        label_stock_purchased.setSizePolicy(
            QSizePolicy.Policy.Maximum, QSizePolicy.Policy.Maximum
        )
        label_amount_purchased.setSizePolicy(
            QSizePolicy.Policy.Maximum, QSizePolicy.Policy.Maximum
        )
        combo_for_stocks.setMinimumSize(100, 30)
        combo_for_stocks.setMaximumSize(200, 30)
        stock_amount_spin.setMinimumSize(70, 25)
        stock_amount_spin.setMaximumSize(100, 25)

        self.removeWidget(
            self.add_new_stock_button
        )  # remove add_stock button from the current position to add it back after adding the stock optiob=on

        self.addWidget(label_stock_purchased, self.grid_row_count, 0, 1, 2)
        self.addWidget(combo_for_stocks, self.grid_row_count, 2, 1, 2)
        self.addWidget(purchase_cost_label, self.grid_row_count, 5, 1, 1)
        self.addWidget(purchase_cost_value_label, self.grid_row_count, 6, 1, 1)
        self.addWidget(label_amount_purchased, self.grid_row_count + 1, 0, 1, 2)
        self.addWidget(stock_amount_spin, self.grid_row_count + 1, 2, 1, 2)
        self.addWidget(selling_price_label, self.grid_row_count + 1, 5, 1, 1)
        self.addWidget(selling_price_value_label, self.grid_row_count + 1, 6, 1, 1)
        self.addWidget(delete_stock_button, self.grid_row_count, 7)

        combo_for_stocks.currentIndexChanged.connect(self.stock_change_handler)
        stock_amount_spin.valueChanged.connect(self.stock_change_handler)

        self.grid_row_count += (
            2  # after adding the stock option we update the current row count
        )

        self.addWidget(
            self.add_new_stock_button, self.grid_row_count, 6, 1, 2
        )  # then we add the add_new_stock_button again

        self.stock_forms_dict[self.stock_id_count] = [
            combo_for_stocks,
            stock_amount_spin,
            purchase_cost_value_label,
            selling_price_value_label,
            purchase_cost_label,
            selling_price_label,
            label_stock_purchased,
            label_amount_purchased,
            delete_stock_button,
        ]  # we store all the components ina dictionary with that unique stock option id
        self.stock_id_count += 1  # create new unique id for next stock
        self.stock_count += 1  # increment stock count
        self.update_stock_costs(self.dates)  # updaet all stock costs again
        self.update_main_calculations()  # update main calculation while taking into consideration the new stock option

    def remove_stock_option(self, id):  # to remove stock option form
        if self.stock_count == 1:  # cannot remove stock option if there is only 1 left
            QMessageBox.critical(
                self.parent_component,
                "Error",
                "Application needs to have at least 1 stock",
            )
            return
        if self.stock_count == 3:  # when we remove the last stock option
            self.add_new_stock_button.setEnabled(
                True
            )  # we enable the add_new_stock_option button as we can now add more stock options

        for widget in self.stock_forms_dict[
            id
        ]:  # using the id we find that stocks form
            self.removeWidget(widget)  # then we remove all the form components
            widget.deleteLater()  # delete those components

        del self.stock_forms_dict[
            id
        ]  # delete the reference for those compoenets from the dictionary
        self.update()  # squash empty rows if present

        self.stock_count -= 1  # decrease stock count
        self.update_stock_costs(self.dates)
        self.update_main_calculations()

    def stock_change_handler(self):
        self.update_stock_costs(self.dates)  # update stock costs based on dates

    def update_stock_costs(self, dates):
        self.dates = dates  # update to latest instance of purchase and sale dates
        purchase_date = self.dates[0]
        selling_date = self.dates[1]

        for (
            stock
        ) in (
            self.stock_forms_dict.values()
        ):  # for each stock in the stock forms dictionary
            stock_purchased = stock[0].currentText()  # get name
            amount_purchased = stock[1].value()  # and amount

            if (
                self.coin_data[stock_purchased].get(dates[0]) is not None
                and self.coin_data[stock_purchased].get(dates[1]) is not None
            ):  # is the price exists for that stock for given date rage
                buying_price = self.coin_data[stock_purchased][purchase_date] * int(
                    amount_purchased
                )
                buying_price = round(buying_price, 3)
                selling_price = self.coin_data[stock_purchased][selling_date] * int(
                    amount_purchased
                )
                selling_price = round(selling_price, 3)  # calculate prices
                stock[2].setStyleSheet(
                    self.color_black
                )  # cancels out any previous colour settings
                stock[3].setStyleSheet(self.color_black)
            else:  # is no price is found, find actual date range for that stock
                date_range = list(
                    self.coin_data[stock_purchased].keys()
                )  # get the dates available for that stock
                actual_dates = [
                    date_range[0],  # get the first
                    date_range[-1],  # and last date
                ]
                buying_price = (
                    "The stock " + str(stock_purchased) + "only has a date range "
                )
                selling_price = (
                    "of "
                    + actual_dates[0].toString("dd-MM-yyyy")
                    + " to "
                    + actual_dates[1].toString("dd-MM-yyyy")
                )
                stock[2].setStyleSheet(self.color_red)  # make it an error colour
                stock[3].setStyleSheet(self.color_red)
            # set the actual price or error depending on the condition
            stock[2].setText(str(buying_price))
            stock[3].setText(str(selling_price))

        self.update_main_calculations()  # update main profit calculations

    def get_stock_portfolio(self):
        portfolio = []
        dates = self.dates  # get dates
        for (
            stock
        ) in self.stock_forms_dict.values():  # for stock in stock from dictionary
            stock_purchased = stock[0].currentText()
            amount_purchased = stock[1].value()
            if (  # is price for thet stock in that given dat range exists
                self.coin_data[stock_purchased].get(dates[0]) is not None
                and self.coin_data[stock_purchased].get(dates[1]) is not None
            ):
                portfolio.append(
                    [stock_purchased, amount_purchased]
                )  # add that stock to the portfolio

        return portfolio  # portoflio is of the format

    #       [[stock_name,stock_amnount],[stock2_name,_stock2_amount]]
