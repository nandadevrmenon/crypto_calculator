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


class StockSelector(QGridLayout):
    def __init__(self, parent, coin_data, update_calculations):
        super().__init__()
        Qt = QtCore.Qt

        self.parent_component = parent
        self.coin_data = coin_data
        self.stock_names = sorted(self.coin_data.keys())
        self.update_main_calculations = update_calculations
        self.dates = [QDate(2021, 7, 6), QDate(2021, 7, 6)]
        self.bold_font = QFont("Helvetica", 12)
        self.bold_font.setBold(True)
        self.color_red = "color:#b30406;"
        self.color_black = "color:black;"
        self.color_green = "color:#098709;"

        self.stock_forms_dict = {}
        self.grid_row_count = 0
        self.stock_id_count = 0
        self.stock_count = 0

        self.add_new_stock_button = QPushButton("Add Another Stock")
        self.add_new_stock_button.setMaximumWidth(200)
        self.add_new_stock_button.clicked.connect(self.add_stock_option)
        self.addWidget(self.add_new_stock_button, 0, 8, 1, 1)

        self.add_stock_option()

        self.update_stock_costs(self.dates)

    def add_stock_option(self):
        if self.stock_count == 2:
            self.add_new_stock_button.setEnabled(False)
        label_stock_purchased = QLabel("Stock Purchased:")
        label_stock_purchased.setFont(self.bold_font)
        label_amount_purchased = QLabel("Amount Purchased:")
        purchase_cost_label = QLabel("Cost per unit:")
        selling_price_label = QLabel("Selling Price:")
        purchase_cost_value_label = QLabel("")
        selling_price_value_label = QLabel("")
        delete_stock_button = DeleteButton(
            self.stock_id_count, self.remove_stock_option
        )
        combo_for_stocks = QComboBox()  # for selecting one out of different stock names

        for x in self.stock_names:
            combo_for_stocks.addItem(x)

        stock_amount_spin = QSpinBox()  # to select the number of stocks to buy
        stock_amount_spin.setMaximum(1000000)
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

        self.removeWidget(self.add_new_stock_button)

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

        self.grid_row_count += 2

        self.addWidget(self.add_new_stock_button, self.grid_row_count, 6, 1, 2)

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
        ]
        self.stock_id_count += 1
        self.stock_count += 1
        self.update_stock_costs(self.dates)
        self.update_main_calculations()

    def remove_stock_option(self, id):
        if self.stock_count == 1:
            QMessageBox.critical(
                self.parent_component,
                "Error",
                "Application needs to have at least 1 stock",
            )
            return
        if self.stock_count == 3:  # when we remove the last stock option
            self.add_new_stock_button.setEnabled(True)

        for widget in self.stock_forms_dict[id]:
            self.removeWidget(widget)
            widget.deleteLater()

        del self.stock_forms_dict[id]
        self.update()

        self.stock_count -= 1
        self.update_stock_costs(self.dates)
        self.update_main_calculations()

    def stock_change_handler(self):
        self.update_stock_costs(self.dates)

    def update_stock_costs(self, dates):
        self.dates = dates
        purchase_date = self.dates[0]
        selling_date = self.dates[1]

        print(purchase_date, selling_date)
        for stock in self.stock_forms_dict.values():
            stock_purchased = stock[0].currentText()
            amount_purchased = stock[1].value()
            if self.coin_data[stock_purchased].get(dates[0]) != None and self.coin_data[
                stock_purchased
            ].get(dates[1] != None):
                buying_price = self.coin_data[stock_purchased][purchase_date] * int(
                    amount_purchased
                )
                buying_price = round(buying_price, 3)
                selling_price = self.coin_data[stock_purchased][selling_date] * int(
                    amount_purchased
                )
                selling_price = round(selling_price, 3)
            else:
                date_range = list(self.coin_data[stock_purchased].keys())
                actual_dates = [
                    date_range[0],
                    date_range[-1],
                ]
                buying_price = "The stock" + str(stock_purchased) + " has a date range "
                selling_price = (
                    "of " + str(actual_dates[0]) + " " + str(actual_dates[1])
                )
            stock[2].setText(str(buying_price))
            stock[3].setText(str(selling_price))

        self.update_main_calculations()

    def get_stock_portfolio(self):
        portfolio = []
        dates = self.dates
        for stock in self.stock_forms_dict.values():
            stock_purchased = stock[0].currentText()
            amount_purchased = stock[1].value()
            if self.coin_data[stock_purchased].get(dates[0]) != None and self.coin_data[
                stock_purchased
            ].get(dates[1] != None):
                portfolio.append([stock_purchased, amount_purchased])

        return portfolio
