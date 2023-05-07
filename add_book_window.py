from PyQt5.QtWidgets import QWidget
from PyQt5.QtWidgets import QPushButton, QGridLayout, QLabel, QComboBox, QLineEdit
import pyodbc

from add_book_item_window import AddBookItemWindow


class BookAdditionWindow(QWidget):
    def __init__(self, main_window):
        super().__init__(None)
        self.main_window = main_window
        self.conn = pyodbc.connect(self.main_window.params)
        self.add_items_window = AddBookItemWindow(self)

        # widgets
        add_book_button = QPushButton("Add book")
        add_book_item_book = QPushButton("Add book item")
        self.book_name = QLineEdit()
        self.book_authors = QLineEdit()
        self.book_pages_number = QLineEdit()
        self.book_publication_year = QLineEdit()
        self.book_items = QComboBox()

        # widgets forming
        self.load_registered_book_items()

        # main layout
        main_layout = QGridLayout()
        main_layout.cellRect(3, 8)

        main_layout.addWidget(QLabel("Name"), 0, 0)
        main_layout.addWidget(self.book_name, 0, 1)
        main_layout.addWidget(QLabel("Authors"), 0, 2)
        main_layout.addWidget(self.book_authors, 0, 3)
        main_layout.addWidget(QLabel("Pages number"), 0, 4)
        main_layout.addWidget(self.book_pages_number, 0, 5)
        main_layout.addWidget(QLabel("Publication year"), 0, 6)
        main_layout.addWidget(self.book_publication_year, 0, 7)

        main_layout.addWidget(self.book_items, 1, 0, 1, 5)
        main_layout.addWidget(add_book_item_book, 1, 5, 1, 3)

        main_layout.addWidget(add_book_button, 2, 0, 1, 8)

        self.setLayout(main_layout)

        # additional settings
        self.setWindowTitle("Mini book catalogue")
        self.setFixedHeight(125)
        self.setFixedWidth(1450)

        # connections
        add_book_button.clicked.connect(self.update_books_data)
        add_book_item_book.clicked.connect(self.add_items_window.show)

    def load_registered_book_items(self):
        cursor = self.conn.cursor()
        cursor.execute("SELECT ITEM_NAME FROM BOOK_ITEMS")
        self.book_items.addItems([item[0] for item in cursor.fetchall()])

    def update_books_data(self):
        try:
            data_raw = [self.book_name.text(), self.book_authors.text(), self.book_pages_number.text()]
            data_raw += [self.book_publication_year.text()]

            cursor = self.conn.cursor()
            cursor.execute("SELECT ITEM_NAME FROM BOOK_ITEMS")
            data_raw += [cursor.fetchall()[self.book_items.currentIndex()][0]]
            self.main_window.update_table_data(data_raw)

            cursor = self.conn.cursor()
            cursor.execute(f"INSERT INTO BOOKS VALUES ({self.main_window.main_table.rowCount()+1}, '{self.book_name.text()}', '{self.book_authors.text()}', {self.book_pages_number.text()}, {self.book_publication_year.text()}, {self.book_items.currentIndex() + 1})")
            self.conn.commit()

            self.main_window.form_stats()

            self.book_name.clear()
            self.book_authors.clear()
            self.book_pages_number.clear()
            self.book_publication_year.clear()
        except Exception as ex:
            print(ex.__str__())
