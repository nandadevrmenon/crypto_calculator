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


class PortfolioPage(QWidget):
    def __init__(self, coin_data):
        super().__init__()
        Qt = QtCore.Qt

        self.coin_data = coin_data
        self.stocks = sorted(self.coin_data.keys())
        self.default_max_calender_value = sorted(self.coin_data["BTC"].keys())[-1]
        self.default_min_calender_value = sorted(self.coin_data["BTC"].keys())[0]
        print("self.sellCalendarStartDate", self.default_max_calender_value)
        print("self.buyCalendarStartDate", self.default_min_calender_value)
        self.color_red = "color:#b30406;"
        self.color_black = "color:black;"
        self.color_green = "color:#098709;"

        main_layout = QVBoxLayout(self)

        # Create a QGridLayout for Stcok Purchased and Amount
        stock_fields_grid_layout = QGridLayout()
        label_stock_purchased = QLabel("Stock Purchased:")
        label_amount_purchased = QLabel("Amount Purchased:")
        self.combo_for_stocks = (
            QComboBox()
        )  # for selecting one out of different stock names

        for x in self.stocks:
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

        stock_fields_grid_layout.addWidget(label_stock_purchased, 0, 0)
        stock_fields_grid_layout.addWidget(self.combo_for_stocks, 0, 1)
        stock_fields_grid_layout.addWidget(label_amount_purchased, 0, 2)
        stock_fields_grid_layout.addWidget(self.stock_amount_spin, 0, 3)

        # Create a Grid Layout for the Date Fields
        date_field_grid = QGridLayout()
        date_bought_label = QLabel("Date Purchased:")
        date_sold_label = QLabel("Date Sold:")
        self.date_bought_value = QLabel("random date ehrer")
        self.date_sold_value = QLabel(" another random daete")
        self.date_purchased_selector = QCalendarWidget()
        self.date_sold_selector = QCalendarWidget()

        self.date_purchased_selector.setVerticalHeaderFormat(
            QCalendarWidget.VerticalHeaderFormat.NoVerticalHeader
        )
        self.date_sold_selector.setVerticalHeaderFormat(
            QCalendarWidget.VerticalHeaderFormat.NoVerticalHeader
        )

        self.date_purchased_selector.setSelectedDate(QDate(2022, 1, 1))
        self.date_sold_selector.setSelectedDate(QDate(2022, 1, 1))
        self.date_purchased_selector.setMinimumDate(self.default_min_calender_value)
        self.date_purchased_selector.setMaximumDate(self.default_max_calender_value)
        self.date_sold_selector.setMinimumDate(self.default_min_calender_value)
        self.date_sold_selector.setMaximumDate(self.default_max_calender_value)

        date_field_grid.addWidget(date_bought_label, 1, 0, 1, 1)
        date_field_grid.addWidget(self.date_bought_value, 2, 0, 1, 1)
        date_field_grid.addWidget(self.date_purchased_selector, 0, 1, 7, 1)
        date_field_grid.addWidget(date_sold_label, 8, 0)
        date_field_grid.addWidget(self.date_sold_value, 9, 0, 1, 1)
        date_field_grid.addWidget(self.date_sold_selector, 7, 1, 7, 1)

        # Create  grid Layout for the prices and the profit
        calculations_grid = QGridLayout()
        purchase_price_label = QLabel("Total Purchase Cost:")
        selling_price_label = QLabel("Total Selling Price:")
        self.purchase_price_value = QLabel("")
        self.selling_price_value = QLabel("")
        self.profit_label = QLabel("Profit Made:")
        self.profit_value = QLabel("")

        calculations_grid.addWidget(purchase_price_label, 0, 0)
        calculations_grid.addWidget(self.purchase_price_value, 0, 1)
        calculations_grid.addWidget(selling_price_label, 1, 0)
        calculations_grid.addWidget(self.selling_price_value, 1, 1)
        calculations_grid.addWidget(self.profit_label, 2, 0)
        calculations_grid.addWidget(self.profit_value, 2, 1)

        # Connect all inputs to the update UI function as change in any Input shiouuld trigger a recalculation and thus an update in the UI
        self.combo_for_stocks.currentIndexChanged.connect(self.update_calculations)
        self.stock_amount_spin.valueChanged.connect(self.update_calculations)
        self.date_purchased_selector.selectionChanged.connect(
            self.purchase_date_change_handler
        )
        self.date_sold_selector.selectionChanged.connect(
            self.selling_date_change_handler
        )

        main_layout.addLayout(stock_fields_grid_layout)
        main_layout.addLayout(date_field_grid)
        main_layout.addLayout(calculations_grid)

        # Apply style to all child QLabel widgets
        self.update_calculations()

    def purchase_date_change_handler(self):
        purchase_date = self.date_purchased_selector.selectedDate()
        selling_date = self.date_sold_selector.selectedDate()
        # stock_purchased = self.combo_for_stocks.currentText()
        # amount_purchased = self.stock_amount_spin.value()
        # price = self.coin_data[stock_purchased][purchase_date] * int(amount_purchased)
        # self.purchase_price_value.setText("€" + str(price))

        self.date_sold_selector.setMinimumDate(purchase_date)
        if selling_date < purchase_date:
            self.date_sold_selector.setSelectedDate(purchase_date)
            self.date_sold_value.setText(
                "Selling Date has to be\nafter Purchase date.\nPlease pick a new date."
            )
            self.date_sold_value.setStyleSheet(self.color_red)
        else:
            self.date_bought_value.setStyleSheet(self.color_black)
            self.date_sold_value.setStyleSheet(self.color_black)
            self.update_calculations()

    def selling_date_change_handler(self):
        selling_date = self.date_sold_selector.selectedDate()
        purchase_date = self.date_purchased_selector.selectedDate()
        stock_purchased = self.combo_for_stocks.currentText()
        amount_sold = self.stock_amount_spin.value()
        price = self.coin_data[stock_purchased][selling_date] * int(amount_sold)
        if selling_date < purchase_date:
            self.date_bought_value.setText("Select New Purchase Date")
            self.date_bought_value.setStyleSheet(self.color_red)
        else:
            self.update_calculations()
            self.date_sold_value.setStyleSheet(self.color_black)
            self.date_bought_value.setStyleSheet(self.color_black)

    def update_calculations(self):
        try:
            stock_purchased = self.combo_for_stocks.currentText()
            amount_purchased = self.stock_amount_spin.value()
            purchase_date = self.date_purchased_selector.selectedDate()
            selling_date = self.date_sold_selector.selectedDate()
            self.date_bought_value.setText(purchase_date.toString("dd-MM-yyyy"))
            self.date_sold_value.setText(selling_date.toString("dd-MM-yyyy"))
            # if selling_date >= purchase_date:
            buying_price = self.coin_data[stock_purchased][purchase_date] * int(
                amount_purchased
            )
            selling_price = self.coin_data[stock_purchased][selling_date] * int(
                amount_purchased
            )
            profit = selling_price - buying_price
            self.purchase_price_value.setText("€" + str(buying_price))
            self.selling_price_value.setText("€" + str(selling_price))
            self.profit_value.setText("€" + str(profit))
            if profit < 0:
                self.profit_value.setStyleSheet(self.color_red)
            else:
                self.profit_value.setStyleSheet(self.color_green)

        except Exception as e:
            print(e)