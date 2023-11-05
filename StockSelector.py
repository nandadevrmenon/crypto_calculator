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
)
from PyQt6.QtGui import QFont
from PyQt6 import QtCore
from decimal import Decimal


class StockSelector(QGridLayout):
    def __init__(self, stock_names, update_calculations):
        super().__init__()
        Qt = QtCore.Qt

        self.stock_names = stock_names
        self.update_calculations = update_calculations
        self.color_red = "color:#b30406;"
        self.color_black = "color:black;"
        self.color_green = "color:#098709;"

        # Create a QGridLayout for Stcok Purchased and Amount
        # stock_fields_grid_layout = QGridLayout()
        label_stock_purchased = QLabel("Stock Purchased:")
        label_amount_purchased = QLabel("Amount Purchased:")
        self.combo_for_stocks = (
            QComboBox()
        )  # for selecting one out of different stock names

        for x in self.stock_names:
            self.combo_for_stocks.addItem(x)

        self.stock_amount_spin = QSpinBox()  # to select the number of stocks to buy
        self.stock_amount_spin.setMaximum(1000000)
        self.stock_amount_spin.setMinimum(1)

        label_stock_purchased.setSizePolicy(
            QSizePolicy.Policy.Maximum, QSizePolicy.Policy.Maximum
        )
        label_amount_purchased.setSizePolicy(
            QSizePolicy.Policy.Maximum, QSizePolicy.Policy.Maximum
        )
        self.combo_for_stocks.setMinimumSize(100, 30)
        self.combo_for_stocks.setMaximumSize(200, 30)
        self.stock_amount_spin.setMinimumSize(70, 30)
        self.stock_amount_spin.setMaximumSize(200, 30)

        self.addWidget(label_stock_purchased, 0, 0)
        self.addWidget(self.combo_for_stocks, 0, 1)
        self.addWidget(label_amount_purchased, 0, 2)
        self.addWidget(self.stock_amount_spin, 0, 3)

    def get_portfolio(self):
        portfolio = []
        stock_purchased = self.combo_for_stocks.currentText()
        amount_purchased = self.stock_amount_spin.value()
        purchase_date = self.date_purchased_selector.selectedDate()
        selling_date = self.date_sold_selector.selectedDate()
        portfolio.append(
            [stock_purchased, amount_purchased, purchase_date, selling_date]
        )
        return portfolio
