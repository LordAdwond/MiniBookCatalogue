from PyQt5.QtWidgets import QWidget
from PyQt5.QtWidgets import QPushButton, QGridLayout, QLineEdit, QLabel, QComboBox
import pyodbc


class AddBookItemWindow(QWidget):
    def __init__(self, main_window):
        super().__init__(None)
        self.main_window = main_window
        self.conn = pyodbc.connect(self.main_window.main_window.params)
        self.cursor = self.conn.cursor()

        # widgets
        self.new_book_item_line = QLineEdit("")
        self.add_item_button = QPushButton("Add book item")
        self.registered_book_items = QComboBox()

        # data forming
        self.load_registered_items()

        # main layout
        main_layout = QGridLayout()
        main_layout.cellRect(3, 2)

        main_layout.addWidget(QLabel("New book item"), 0, 0)
        main_layout.addWidget(self.new_book_item_line, 0, 1)
        main_layout.addWidget(QLabel("Registered book items"), 1, 0)
        main_layout.addWidget(self.registered_book_items, 1, 1)
        main_layout.addWidget(self.add_item_button, 2, 0, 1, 2)
        self.setLayout(main_layout)

        # connections
        self.add_item_button.clicked.connect(self.add_new_book_item)

        # additional settings
        self.setWindowTitle("Mini Book catalogue")

    def load_registered_items(self):
        self.cursor.execute("SELECT ITEM_NAME FROM BOOK_ITEMS")
        items_list = [item[0] for item in self.cursor.fetchall()]
        self.registered_book_items.addItems(items_list)

    def add_new_book_item(self):
        try:
            self.registered_book_items.addItem(self.new_book_item_line.text())
            self.main_window.book_items.addItem(self.new_book_item_line.text())

            self.cursor.execute("SELECT ITEM_ID FROM BOOK_ITEMS")
            old_items_list = self.cursor.fetchall()
            self.cursor.execute(f"INSERT INTO BOOK_ITEMS(ITEM_ID, ITEM_NAME) VALUES ({len(old_items_list)+1}, '{self.new_book_item_line.text()}');")
            self.conn.commit()

            self.new_book_item_line.clear()
        except Exception as ex:
            print(ex.__str__())

