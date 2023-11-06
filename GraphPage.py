from PyQt6.QtWidgets import (
    QMessageBox,
    QSizePolicy,
    QWidget,
    QVBoxLayout,
    QRadioButton,
    QButtonGroup,
    QHBoxLayout,
)
from PyQt6 import QtCore
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
from matplotlib.ticker import MaxNLocator


class GraphPage(QWidget):
    def __init__(self, coin_data, tabs, main_window, calculation_tab):
        super().__init__()
        Qt = QtCore.Qt
        self.calculation_tab = calculation_tab
        # Create a main layout for the custom widget
        main_layout = QVBoxLayout()

        # Create the Matplotlib graph widget
        self.matplotlib_widget = MatplotlibWidget(
            coin_data, tabs, main_window, self.calculation_tab
        )

        self.button_group = QButtonGroup()
        self.radio_button_layout = QHBoxLayout()

        self.initialize_radio_buttons()
        self.clicked_button = None
        self.button_group.buttonClicked.connect(
            lambda button: self.handle_radio_button_change(button)
        )
        self.radio_button_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # Add the horizontal layout with radio buttons to the main layout
        main_layout.addLayout(self.radio_button_layout)

        # Add the Matplotlib widget to the main layout
        main_layout.addWidget(self.matplotlib_widget)

        # Set the main layout for the custom widget
        self.setLayout(main_layout)

    def initialize_radio_buttons(self):
        self.clear_layout()
        self.clear_button_group()
        portfolio = self.calculation_tab.get_full_portfolio()
        for i in range(1, len(portfolio)):
            radio_button = QRadioButton(portfolio[i][0])
            self.button_group.addButton(radio_button)
            self.radio_button_layout.addWidget(radio_button)
            if i == 1:
                radio_button.setChecked(True)
                self.clicked_button = radio_button

    def clear_layout(self):
        while self.radio_button_layout.count():
            item = self.radio_button_layout.takeAt(0)
            widget = item.widget()
            if widget:
                widget.deleteLater()

    def clear_button_group(self):
        for button in self.button_group.buttons():
            self.button_group.removeButton(button)
            button.deleteLater()

    def handle_radio_button_change(self, button):
        self.clicked_button = button
        self.matplotlib_widget.plot(button)

    def plot_graph(self):
        print(self.clicked_button)
        self.matplotlib_widget.plot(self.clicked_button)


class MatplotlibWidget(FigureCanvas):
    def __init__(
        self, coin_data, tabs, main_window, calculation_tab, width=5, height=5, dpi=100
    ):
        self.coin_data = coin_data
        self.tabs = tabs
        self.main_window = main_window
        self.calculation_tab = calculation_tab
        self.fig = Figure(figsize=(width, height), dpi=dpi)
        self.axes = self.fig.add_subplot(111)
        self.fig.subplots_adjust(left=0.175)
        FigureCanvas.__init__(self, self.fig)
        FigureCanvas.setSizePolicy(
            self, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding
        )
        FigureCanvas.updateGeometry(self)

    # def plot(self, portfolio):
    #     self.axes.clear()
    #     purchase_date = portfolio[0][2]
    #     selling_date = portfolio[0][3]
    #     if purchase_date == selling_date:
    #         QMessageBox.critical(
    #             self,
    #             "Error",
    #             "Purchase Date is on or after Selling Date (which is not possible). Please Select a new pair of dates.",
    #         )
    #         self.switch_tabs()
    #         return
    #     self.main_window.resize(600, 525)
    #     for stock in portfolio:
    #         data = []
    #         name = stock[0]
    #         days_between = purchase_date.daysTo(selling_date) + 1

    #         for i in range(0, days_between):
    #             print("day" + str(i))
    #             print(self.coin_data[name][purchase_date.addDays(i)])
    #             data.append(self.coin_data[name][purchase_date.addDays(i)])
    #         self.axes.plot(data, "r-")

    #     self.axes.set_title("Stock Price Graph")
    #     self.axes.xaxis.set_major_locator(MaxNLocator(integer=True))
    #     self.axes.set_xlabel(
    #         "Days since " + purchase_date.toString("dd-MM-yyyy")
    #     )  # Set the label for the x-axis
    #     self.axes.set_ylabel("Price")
    #     self.draw()

    def plot(self, radio_button):
        self.axes.clear()
        portfolio = self.calculation_tab.get_full_portfolio()
        purchase_date = portfolio[0][0]
        selling_date = portfolio[0][1]
        if purchase_date == selling_date:
            QMessageBox.critical(
                self,
                "Error",
                "Purchase Date is on or after Selling Date (which is not possible). Please Select a new pair of dates.",
            )
            self.switch_tabs()
            return
        self.main_window.resize(600, 525)

        data = []
        name = radio_button.text()
        days_between = purchase_date.daysTo(selling_date) + 1

        for i in range(0, days_between):
            print("day" + str(i))
            print(self.coin_data[name][purchase_date.addDays(i)])
            data.append(self.coin_data[name][purchase_date.addDays(i)])
        self.axes.plot(data, "r-")

        self.axes.set_title("Stock Price Graph")
        self.axes.xaxis.set_major_locator(MaxNLocator(integer=True))
        self.axes.set_xlabel(
            "Days since " + purchase_date.toString("dd-MM-yyyy")
        )  # Set the label for the x-axis
        self.axes.set_ylabel("Price")
        self.draw()

    def switch_tabs(self):
        self.tabs.setCurrentIndex(0)
