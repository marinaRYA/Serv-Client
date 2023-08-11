import os
from PyQt5.QtCore import Qt
import sys
from PyQt5.QtWidgets import QApplication,QWidget, QMainWindow, QListWidget, QGridLayout,QPushButton,QLineEdit,QPlainTextEdit,QTableWidgetItem
from PyQt5.QtCore import QModelIndex
import socket

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.init_ui()
    def init_ui(self):
        self.setWindowTitle('Client')
        self.list_widget = QListWidget(self)
        self.list_widget.itemClicked.connect(self.on_list_item_clicked)
        self.output1_textedit = QPlainTextEdit(self)
        self.output2_textedit = QPlainTextEdit(self)

        self.input_lineedit = QLineEdit(self)
        self.connect_button = QPushButton('Connect')
        self.sendclient_button = QPushButton('Send client')
        self.sendserver_button = QPushButton('Send server')
        self.disconnect_button = QPushButton('Disconnect')
        self.exit_button = QPushButton('exit')

        central_widget = QWidget(self)
        self.setCentralWidget(central_widget)
        layout = QGridLayout(central_widget)
        layout.addWidget(self.list_widget, 0, 0, 1, 2)
        layout.addWidget(self.output1_textedit, 0, 2,4,1)
        layout.addWidget(self.output2_textedit, 0, 3,4,1)
        layout.addWidget(self.input_lineedit, 1, 0, 1, 2)
        layout.addWidget(self.connect_button, 2, 0)
        layout.addWidget(self.disconnect_button, 2, 1)
        layout.addWidget(self.sendclient_button, 3, 0)
        layout.addWidget(self.sendserver_button, 3, 1)
        layout.addWidget(self.exit_button, 4, 0, 2, 2)

        self.setLayout(layout)

        self.exit_button.clicked.connect(self.exit)
        self.connect_button.clicked.connect(self.connect_to_server)
        self.disconnect_button.clicked.connect(self.disconnect_from_server)
        self.sendserver_button.clicked.connect(self.send_to_server)
        self.sendclient_button.clicked.connect(self.data_from_server)
        self.client_socket = None
        self.selected_item_text = None

    def exit(self):
        sys.exit(app.exec_())

    def update_list(self, data):
        self.list_widget.clear()
        data = data.split('\n')
        for item in data:
            self.list_widget.addItem(item)

    def send_to_server(self):
        if self.client_socket:
            if self.selected_item_text:
                try:
                    # Отправка данных на сервер
                    self.client_socket.sendall( self.selected_item_text.encode())
                    self.output1_textedit.appendPlainText("Отправлено на сервер")
                except ConnectionError:
                    self.output1_textedit.appendPlainText("Ошибка при отправке на сервер")
    def data_from_server(self):
        if self.client_socket:
            try:
                response = self.client_socket.recv(1024).decode()
                if not response:
                    self.output2_textedit.appendPlainText("Получен пустой ответ от сервера.")
                else:
                    self.output2_textedit.appendPlainText("Ответ от сервера: " + response)
                    self.update_list(response)
            except Exception as e:
                self.output2_textedit.appendPlainText("Ошибка при получении ответа от сервера:" + str(e))

    def on_list_item_clicked(self, item):
        self.selected_item_text = item.text()
        self.output1_textedit.appendPlainText("Отправить на сервер?"+self.selected_item_text)

    def disconnect_from_server(self):
        if self.client_socket:
            self.client_socket.close()
            self.client_socket = None
            self.output2_textedit.appendPlainText("Соединение с сервером закрыто")

    def connect_to_server(self):
        server_address = self.input_lineedit.text()
        try:
            # Установка соединения с сервером
            self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.client_socket.connect((server_address, 1234))
            self.output2_textedit.appendPlainText("Подключение к серверу")
            response = self.client_socket.recv(1024).decode()
            self.output2_textedit.appendPlainText("Ответ от сервера: " + response)
            self.update_list(response)

        except ConnectionRefusedError:
            self.output2_textedit.appendPlainText("Ошибка при подключении")


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())

