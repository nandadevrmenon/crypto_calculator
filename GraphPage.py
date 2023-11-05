from PyQt6.QtWidgets import QMessageBox, QSizePolicy
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
from matplotlib.ticker import MaxNLocator


class MatplotlibWidget(FigureCanvas):
    def __init__(self, coin_data, tabs, main_window, width=5, height=5, dpi=100):
        self.coin_data = coin_data
        self.tabs = tabs
        self.main_window = main_window
        self.fig = Figure(figsize=(width, height), dpi=dpi)
        self.axes = self.fig.add_subplot(111)
        self.fig.subplots_adjust(left=0.175)
        FigureCanvas.__init__(self, self.fig)
        FigureCanvas.setSizePolicy(
            self, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding
        )
        FigureCanvas.updateGeometry(self)

    def plot(self, portfolio):
        self.axes.clear()
        purchase_date = portfolio[0][2]
        selling_date = portfolio[0][3]
        if purchase_date == selling_date:
            QMessageBox.critical(
                self,
                "Error",
                "Purchase Date is on or after Selling Date (which is not possible). Please Select a new pair of dates.",
            )
            self.switch_tabs()
            return
        self.main_window.resize(600, 525)
        for stock in portfolio:
            data = []
            name = stock[0]
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

    # def __init__(self, coin_data, portfolio):
    #     super().__init__()

    #     # Create a layout for the custom widget
    #     layout = QVBoxLayout()

    #     # Create a Matplotlib graph using pyplot
    #     portfolio = [["BTC", 1, QDate(2019, 1, 1), QDate(2019, 1, 5)]]

    #     plt.figure()
    #     plt.xlabel("Date")
    #     plt.ylabel("Price")
    #     plt.legend()
    #     plt.title("Stock Price Graph")

    #     for stock in portfolio:
    #         name=stock[0]

    #     x = list(i in range())
    #     # # Convert QDate objects to Python datetime objects
    #     # dates = [datetime(qdate.year(), qdate.month(), qdate.day()) for qdate in x]

    #     # # Convert dates to numerical values
    #     # x = date2num(dates)
    #     y = [2, 4, 1, 5, 7]
    #     plt.plot(x, y)
    #     plt.title("Matplotlib Graph Example")

    #     # Save the Matplotlib graph to a buffer
    #     buffer = BytesIO()
    #     plt.savefig(buffer, format="png")
    #     buffer.seek(0)

    #     # Create a QPixmap from the buffer
    #     pixmap = QPixmap()
    #     pixmap.loadFromData(buffer.read())

    #     # Create a QLabel and set the QPixmap
    #     label = QLabel(self)
    #     label.setPixmap(pixmap)

    #     # Add the QLabel to the layout
    #     layout.addWidget(label)

    #     self.setLayout(layout)
