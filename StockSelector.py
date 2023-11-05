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
)
from PyQt6.QtGui import QFont
from PyQt6 import QtCore
from decimal import Decimal


class StockSelector(QGridLayout):
    def __init__(self, coin_data, update_calculations):
        super().__init__()
        Qt = QtCore.Qt

        self.coin_data = coin_data
        self.stock_names = sorted(self.coin_data.keys())
        self.update_calculations = update_calculations
        self.color_red = "color:#b30406;"
        self.color_black = "color:black;"
        self.color_green = "color:#098709;"

        self.stock_form_array = []
        self.count = 0

        # Create a QGridLayout for Stcok Purchased and Amount
        # stock_fields_grid_layout = QGridLayout()
        # label_stock_purchased = QLabel("Stock Purchased:")
        # label_amount_purchased = QLabel("Amount Purchased:")
        # self.combo_for_stocks = (
        #     QComboBox()
        # )  # for selecting one out of different stock names

        # for x in self.stock_names:
        #     self.combo_for_stocks.addItem(x)

        # self.stock_amount_spin = QSpinBox()  # to select the number of stocks to buy
        # self.stock_amount_spin.setMaximum(1000000)
        # self.stock_amount_spin.setMinimum(1)

        # label_stock_purchased.setSizePolicy(
        #     QSizePolicy.Policy.Maximum, QSizePolicy.Policy.Maximum
        # )
        # label_amount_purchased.setSizePolicy(
        #     QSizePolicy.Policy.Maximum, QSizePolicy.Policy.Maximum
        # )
        # self.combo_for_stocks.setMinimumSize(100, 30)
        # self.combo_for_stocks.setMaximumSize(200, 30)
        # self.stock_amount_spin.setMinimumSize(70, 30)
        # self.stock_amount_spin.setMaximumSize(200, 30)

        # self.addWidget(label_stock_purchased, 0, 0)
        # self.addWidget(self.combo_for_stocks, 0, 1)
        # self.addWidget(label_amount_purchased, 0, 2)
        # self.addWidget(self.stock_amount_spin, 0, 3)
        # Set vertical spacing (gutter)

        # self.setVerticalSpacing(2)
        self.add_stock_option()
        self.add_stock_option()
        self.add_stock_option()
        self.update_stock_costs([QDate(2021, 7, 6), QDate(2021, 7, 6)])

    def get_stock_portfolio(self):
        portfolio = []
        stock_purchased = self.combo_for_stocks.currentText()
        amount_purchased = self.stock_amount_spin.value()
        portfolio.append([stock_purchased, amount_purchased])
        return portfolio

    def add_stock_option(self):
        label_stock_purchased = QLabel("Stock Purchased:")
        label_amount_purchased = QLabel("Amount Purchased:")
        purchase_cost_label = QLabel("Cost per unit:")
        selling_price_label = QLabel("Selling Price:")
        purchase_cost_value_label = QLabel("")
        selling_price_value_label = QLabel("")
        delete_stock_button = QPushButton()
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

        self.addWidget(label_stock_purchased, self.count, 0, 1, 2)
        self.addWidget(combo_for_stocks, self.count, 2, 1, 2)
        self.addWidget(purchase_cost_label, self.count, 5, 1, 1)
        self.addWidget(purchase_cost_value_label, self.count, 6, 1, 1)
        self.addWidget(label_amount_purchased, self.count + 1, 0, 1, 2)
        self.addWidget(stock_amount_spin, self.count + 1, 2, 1, 2)
        self.addWidget(selling_price_label, self.count + 1, 5, 1, 1)
        self.addWidget(selling_price_value_label, self.count + 1, 6, 1, 1)
        self.addWidget(delete_stock_button, self.count, 8, 1, 1)

        combo_for_stocks.currentIndexChanged.connect(self.update_calculations)
        stock_amount_spin.valueChanged.connect(self.update_calculations)

        self.stock_form_array.append(
            [
                combo_for_stocks,
                stock_amount_spin,
                purchase_cost_value_label,
                selling_price_value_label,
            ]
        )
        self.count += 2

        # Add a spacer to create space between stock options
        spacer = QWidget()
        spacer.setSizePolicy(
            QSizePolicy.Policy.MinimumExpanding, QSizePolicy.Policy.MinimumExpanding
        )
        spacer.setMinimumHeight(20)
        self.addWidget(spacer, self.count, 0, 1, 9)
        self.count += 1

    def update_stock_costs(self, dates):
        purchase_date = dates[0]
        selling_date = dates[1]
        for stock in self.stock_form_array:
            print(stock)
            stock_purchased = stock[0].currentText()
            amount_purchased = stock[1].value()
            print(stock_purchased, amount_purchased)
            buying_price = self.coin_data[stock_purchased][purchase_date] * int(
                amount_purchased
            )
            buying_price = round(buying_price, 3)
            selling_price = self.coin_data[stock_purchased][selling_date] * int(
                amount_purchased
            )
            selling_price = round(selling_price, 3)
            profit = round(selling_price - buying_price, 3)
            stock[2].setText(str(buying_price))
            stock[3].setText(str(selling_price))
