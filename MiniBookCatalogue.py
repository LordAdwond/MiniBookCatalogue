from PyQt5.QtWidgets import QApplication
from catalogue_window import CatalogueWindow
import sys

conn_string = ""
with open("config.txt", "r") as file:
    parameters = [param.replace('\n', '') for param in file.readlines()]
    conn_string = "Driver={PostgreSQL Unicode};"
    conn_string = conn_string + f"DATABASE={parameters[0]};"
    conn_string = conn_string + f"UID={parameters[1]};"
    conn_string = conn_string + f"PWD={parameters[2]};"
    conn_string = conn_string + f"SERVER={parameters[3]};"
    conn_string = conn_string + f"PORT={parameters[4]}"

app = QApplication(sys.argv)
catalogue = CatalogueWindow(conn_string)
catalogue.show()
app.exec_()
