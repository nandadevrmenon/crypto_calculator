# Name: Nandadev Rajeev Menon
# Student Number : 3069713

from PyQt6.QtCore import QDate
from PyQt6.QtWidgets import (
    QLabel,
    QCalendarWidget,
    QGridLayout,
    QWidget,
    QVBoxLayout,
    QSizePolicy,
    QSpacerItem,
)
from PyQt6.QtGui import QFont
from PyQt6 import QtCore
from decimal import Decimal
from StockSelector import StockSelector


class PortfolioPage(QWidget):
    def __init__(self, coin_data):
        super().__init__()
        self.Qt = QtCore.Qt

        self.coin_data = coin_data
        self.stocks = sorted(self.coin_data.keys())  # stock names
        self.default_max_calender_value = sorted(self.coin_data["BTC"].keys())[
            -1
        ]  # gte the highest date in the dictionary
        self.default_min_calender_value = sorted(self.coin_data["BTC"].keys())[
            0
        ]  # get the smallest date in the dictionary

        self.bold_font = QFont("Helvetica", 12)
        self.bold_font.setBold(True)
        self.bigger_font = QFont("Helvetica", 14)
        self.color_red = "color:#b30406;"
        self.color_black = "color:black;"
        self.color_green = "color:#098709;"

        main_layout = QVBoxLayout(self)

        self.stock_fields_grid_layout = StockSelector(
            self, self.coin_data, self.update_calculations
        )

        # Create a Grid Layout for the Date Form
        date_field_grid = QGridLayout()
        date_bought_label = QLabel("Date Purchased:")
        date_sold_label = QLabel("Date Sold:")
        self.date_bought_value = QLabel("05/07/2021")
        self.date_bought_value.setFont(self.bold_font)
        self.date_sold_value = QLabel("06/07/2021")
        self.date_sold_value.setFont(self.bold_font)
        self.date_purchased_selector = QCalendarWidget()
        self.date_sold_selector = QCalendarWidget()

        # remove week numbers from the calender widgets
        self.date_purchased_selector.setVerticalHeaderFormat(
            QCalendarWidget.VerticalHeaderFormat.NoVerticalHeader
        )
        self.date_sold_selector.setVerticalHeaderFormat(
            QCalendarWidget.VerticalHeaderFormat.NoVerticalHeader
        )
        # make them expanding horizontally
        self.date_purchased_selector.setSizePolicy(
            QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed
        )
        self.date_sold_selector.setSizePolicy(
            QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed
        )

        self.date_purchased_selector.setSelectedDate(QDate(2022, 1, 1))
        self.date_sold_selector.setSelectedDate(QDate(2022, 1, 1))
        self.date_purchased_selector.setMinimumDate(self.default_min_calender_value)
        self.date_purchased_selector.setMaximumDate(
            self.default_max_calender_value.addDays(-1)
        )  # brings back the max purcahse date by one so that there is at least a difference of 1 between initial purchase and start date
        self.date_sold_selector.setMinimumDate(
            self.default_min_calender_value.addDays(1)
        )
        self.date_sold_selector.setMaximumDate(self.default_max_calender_value)
        # after setting minimum and maximum, the calenders will point to the lastest date available in each range

        date_field_grid.addWidget(date_bought_label, 1, 0, 1, 1)
        date_field_grid.addWidget(self.date_bought_value, 2, 0, 1, 1)
        date_field_grid.addWidget(self.date_purchased_selector, 0, 1, 7, 1)
        date_field_grid.addWidget(date_sold_label, 8, 0)
        date_field_grid.addWidget(self.date_sold_value, 9, 0, 1, 1)
        date_field_grid.addWidget(self.date_sold_selector, 7, 1, 7, 1)

        # Any change in date should trigger change in all the ui in portoflio page
        self.date_purchased_selector.selectionChanged.connect(
            self.purchase_date_change_handler
        )
        self.date_sold_selector.selectionChanged.connect(
            self.selling_date_change_handler
        )

        # Create  grid Layout for the prices and the profit
        calculations_grid = QGridLayout()
        purchase_price_label = QLabel("Total Purchase Cost:")
        selling_price_label = QLabel("Total Selling Price:")
        self.purchase_price_value = QLabel("")
        self.selling_price_value = QLabel("")
        self.profit_label = QLabel("Profit Made:")
        self.profit_value = QLabel("")
        self.profit_value.setFont(self.bigger_font)

        purchase_price_label.setSizePolicy(
            QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed
        )
        selling_price_label.setSizePolicy(
            QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed
        )
        self.profit_label.setSizePolicy(
            QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed
        )

        calculations_grid.addWidget(purchase_price_label, 0, 0)
        calculations_grid.addWidget(self.purchase_price_value, 0, 1)
        calculations_grid.addWidget(selling_price_label, 1, 0)
        calculations_grid.addWidget(self.selling_price_value, 1, 1)
        calculations_grid.addWidget(self.profit_label, 2, 0)
        calculations_grid.addWidget(self.profit_value, 2, 1)

        horizontal_spacer = (
            QSpacerItem(  # spacer that allows all the calculation labels to be together
                40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding
            )
        )
        calculations_grid.addItem(horizontal_spacer, 3, 0)

        main_layout.addLayout(date_field_grid)
        main_layout.addLayout(self.stock_fields_grid_layout)
        main_layout.addLayout(calculations_grid)

        # update profit loss calculations and also update date value labels on app start
        self.update_calculations()

    def purchase_date_change_handler(self):
        purchase_date = self.date_purchased_selector.selectedDate()
        selling_date = self.date_sold_selector.selectedDate()

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
            self.date_bought_value.setText(purchase_date.toString("dd-MM-yyyy"))
            self.date_sold_value.setText(selling_date.toString("dd-MM-yyyy"))
            self.stock_fields_grid_layout.update_stock_costs(self.get_dates())

    def selling_date_change_handler(self):
        selling_date = self.date_sold_selector.selectedDate()
        self.date_sold_value.setStyleSheet(self.color_black)
        self.date_bought_value.setStyleSheet(self.color_black)
        self.update_calculations()
        self.date_sold_value.setText(selling_date.toString("dd-MM-yyyy"))
        self.stock_fields_grid_layout.update_stock_costs(self.get_dates())

    def update_calculations(self):
        try:
            portfolio = self.stock_fields_grid_layout.get_stock_portfolio()
            dates = self.get_dates()

            total_purchase_cost = 0
            total_selling_price = 0

            for stock in portfolio:
                buying_cost = self.coin_data[stock[0]][dates[0]] * int(stock[1])
                selling_price = self.coin_data[stock[0]][dates[1]] * int(stock[1])
                total_purchase_cost += buying_cost
                total_selling_price += selling_price

            total_selling_price = round(total_selling_price, 3)
            total_purchase_cost = round(total_purchase_cost, 3)
            profit = round(total_selling_price - total_purchase_cost, 3)
            self.purchase_price_value.setText("€" + str(total_purchase_cost))
            self.selling_price_value.setText("€" + str(total_selling_price))
            self.profit_value.setText("€" + str(profit))
            if profit < 0:
                self.profit_value.setStyleSheet(self.color_red)
            else:
                self.profit_value.setStyleSheet(self.color_green)

        except Exception as e:
            print(e)

    # def get_portfolio(self):
    #     portfolio = []
    #     stock_purchased = self.combo_for_stocks.currentText()
    #     amount_purchased = self.stock_amount_spin.value()
    #     purchase_date = self.date_purchased_selector.selectedDate()
    #     selling_date = self.date_sold_selector.selectedDate()
    #     portfolio.append(
    #         [stock_purchased, amount_purchased, purchase_date, selling_date]
    #     )
    #     return portfolio

    def get_full_portfolio(self):
        portfolio = self.stock_fields_grid_layout.get_stock_portfolio()
        portfolio.insert(0, self.get_dates())
        return portfolio

    def get_dates(self):
        return [
            self.date_purchased_selector.selectedDate(),
            self.date_sold_selector.selectedDate(),
        ]
