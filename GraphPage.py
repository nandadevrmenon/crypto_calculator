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
        self.calculation_tab = calculation_tab  # we need instance of calc_tab because we get the portfolio from that tab

        main_layout = QVBoxLayout()

        # we pass in coin_data ref,the tabs(so we can change tabs  from this class), the main window ( so we can put up errors) and the calc_tab ref (so we can get latest instance of the portfolio)
        self.matplotlib_widget = MatplotlibWidget(
            coin_data, tabs, main_window, self.calculation_tab
        )

        self.button_group = QButtonGroup()
        self.radio_button_layout = QHBoxLayout()

        self.initialize_radio_buttons()

        self.clicked_button = (
            None  # we use this variable for deciding which stock's graph to plot
        )
        self.button_group.buttonClicked.connect(  # even thoguh we pass in a radio_button when it changes, we can't rely on this approach to draw the graph the first time as we hardcode button1 as the selected button
            lambda button: self.handle_radio_button_change(button)
        )

        self.radio_button_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        main_layout.addLayout(self.radio_button_layout)
        main_layout.addWidget(self.matplotlib_widget)
        self.setLayout(main_layout)

    def initialize_radio_buttons(self):
        self.clear_layout()  # clear old button layout
        self.clear_button_group()  # clear old button group
        portfolio = (
            self.calculation_tab.get_full_portfolio()
        )  # get the latest portfolio
        for i in range(1, len(portfolio)):  # for stock in portfolio
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

    def plot(self, radio_button):
        if radio_button is None:
            QMessageBox.critical(
                self,
                "Error",
                "No valid date ranges provided for graph.Please select a Valid Date range and try again.",
            )
            self.switch_tabs()
            return
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

        if data[0] >= data[-1]:
            self.axes.plot(data, "r-")
        else:
            self.axes.plot(data, "g-")

        self.axes.set_title("Stock Price Graph")
        self.axes.xaxis.set_major_locator(MaxNLocator(integer=True))
        self.axes.set_xlabel(
            "Days since " + purchase_date.toString("dd-MM-yyyy")
        )  # Sset x axis label
        self.axes.set_ylabel("Price")  # set y axis label
        self.draw()

    def switch_tabs(self):
        self.tabs.setCurrentIndex(0)
