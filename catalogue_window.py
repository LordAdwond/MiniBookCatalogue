from PyQt5.QtWidgets import QWidget
from PyQt5.QtWidgets import QPushButton, QTableWidget, QTableWidgetItem, QGridLayout, QTextEdit
import pyodbc
import pandas as pd

from add_book_window import BookAdditionWindow


class CatalogueWindow(QWidget):
    def __init__(self, parameters : str):
        super().__init__(None)
        self.params = parameters
        self.conn = pyodbc.connect(self.params)
        self.stat_text = ""
        self.result_columns_names = []
        self.book_addition_widget = BookAdditionWindow(self)

        # window widgets
        self.main_table = QTableWidget()
        self.stat_text_widget = QTextEdit()
        add_book_button = QPushButton("Add book")

        # window layout
        main_layout = QGridLayout()
        main_layout.cellRect(3, 2)
        main_layout.addWidget(self.main_table, 0, 0, 3, 1)
        main_layout.addWidget(add_book_button, 0, 1, 1, 2)
        main_layout.addWidget(self.stat_text_widget, 1, 1, 2, 1)
        self.setLayout(main_layout)

        # forming of primary table content
        cursor = self.conn.cursor()

        with open("books_table_columns.txt", "r") as file:
            lines = file.readlines()
            self.main_table.setColumnCount(len(lines))
            col_names = [col.replace('\n', "") for col in lines]

            for col in col_names:
                res_name = ""
                for word in col.split('_'):
                    res_name += f"{word} "
                self.result_columns_names.append(res_name)

            self.main_table.setHorizontalHeaderLabels(self.result_columns_names)
            file.close()

        cursor.execute("SELECT * FROM BOOKS")
        books_table_rows = cursor.fetchall()
        self.main_table.setRowCount(len(books_table_rows))  # setting of rows number

        cursor.execute("SELECT * FROM BOOK_ITEMS")
        books_items_table_rows = [[row[0], row[1]] for row in cursor.fetchall()]
        books_items_table_rows = {row[0]: row[1] for row in books_items_table_rows}

        cursor.execute("SELECT book_item_id FROM BOOKS")
        book_item_ids_sequence = [row[0] for row in cursor.fetchall()]
        for i in range(len(books_table_rows)):
            for j in range(len(books_table_rows[i])):
                new_item = QTableWidgetItem()
                if j<5:
                    new_item.setText(str(books_table_rows[i][j]))
                else:
                    new_item.setText(books_items_table_rows[book_item_ids_sequence[i]])
                self.main_table.setItem(i, j, new_item)

        # additional settings
        self.setWindowTitle("Mini book catalogue")
        self.setFixedHeight(400)
        self.setFixedWidth(1450)

        self.main_table.setFixedHeight(350)
        self.main_table.setFixedWidth(1100)
        self.stat_text_widget.setReadOnly(True)

        # connections
        add_book_button.clicked.connect(self.book_addition_widget.show)

        # additional actions
        self.form_stats()

    def form_stats(self):
        stats_text = ""
        cursor = self.conn.cursor()

        cursor.execute("SELECT * FROM BOOKS")
        data_books = cursor.fetchall()
        data_books = [list(row[:-1]) for row in data_books]
        data = pd.DataFrame(data_books, columns=self.result_columns_names)

        cursor.execute("SELECT * FROM BOOK_ITEMS")
        items_dict = {row[0] : row[1] for row in cursor.fetchall()}
        items = [items_dict[ID] for ID in data["book item "]]
        data["item"] = items
        data.drop("book item ", axis=1)

        stats_text += f"General number of books: {len(data.index)}\n"
        stats_text += f"Mean pages number: {data['book pages number '].mean()}\n"
        stats_text += f"Most popular book item: {data['item'].value_counts().index[0]}\n"

        self.stat_text_widget.setText(stats_text)

    def update_table_data(self, new_data_row : list):
        self.main_table.setRowCount(self.main_table.rowCount()+1)
        new_item = QTableWidgetItem()
        new_item.setText(str(self.main_table.rowCount()))
        self.main_table.setItem(self.main_table.rowCount()-1, 0, new_item)
        for i in range(1, 6):
            new_item = QTableWidgetItem()
            new_item.setText(str(new_data_row[i-1]))
            self.main_table.setItem(self.main_table.rowCount()-1, i, new_item)
