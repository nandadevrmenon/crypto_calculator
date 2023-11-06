from PyQt6.QtWidgets import QPushButton
from PyQt6.QtGui import QIcon


class DeleteButton(QPushButton):
    def __init__(self, id, remove_stock):
        super().__init__()
        self.remove_stock = remove_stock
        self.id = id
        self.setIcon(QIcon("./delete_icon.png"))  # Set the delete icon
        self.setStyleSheet("background-color: gray;")
        # self.setText("Delete")  # Set the button text
        self.clicked.connect(
            lambda: self.remove_stock(self.id)
        )  # Connect the click signal to the action
