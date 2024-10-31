import sys
import os
import threading
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QTextEdit, QLineEdit
from PyQt5.QtGui import QFont, QTextCursor, QColor
from PyQt5.QtCore import Qt
import socket

host = '127.0.0.1'
port = 64920

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((host, port))
print("Connected to the server")

class ModernTerminal(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()
        self.command_history = []
        self.history_index = -1
        
        # Start the receive thread
        self.receive_thread = threading.Thread(target=self.receive_data)
        self.receive_thread.daemon = True
        self.receive_thread.start()
        
    def init_ui(self):
        # Set up the main window
        self.setWindowTitle("Modern Terminal")
        self.setGeometry(100, 100, 800, 500)
        
        # Set up the main layout
        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(10, 10, 10, 10)
        
        # Terminal display area
        self.terminal_display = QTextEdit()
        self.terminal_display.setReadOnly(True)
        self.terminal_display.setStyleSheet("""
            QTextEdit {
                background-color: #282828;
                color: #FFFFFF;
                border: none;
                padding: 10px;
            }
        """)
        self.terminal_display.setFont(QFont("Monospace", 11))
        
        # Input field (hidden by default, only used for capturing input)
        self.input_field = QLineEdit()
        self.input_field.setFont(QFont("Monospace", 11))
        self.input_field.setStyleSheet("""
            QLineEdit {
                background-color: #282828;
                color: #FFFFFF;
                border: none;
                padding: 5px;
            }
        """)
        self.input_field.returnPressed.connect(self.process_command)
        
        # Add widgets to main layout
        main_layout.addWidget(self.terminal_display)
        main_layout.addWidget(self.input_field)
        
        # Set main layout
        self.setLayout(main_layout)
        
        # Initial prompt
        self.append_prompt()

    def append_prompt(self):
        current_dir = os.getcwd()
        home = os.path.expanduser("~")
        if current_dir.startswith(home):
            current_dir = "~" + current_dir[len(home):]
        
        # Define colors for each part of the prompt
        arrow_color = "#98C379"  # Green color for the arrow
        path_color = "#56B6C2"   # Blue color for the current directory path
        symbol_color = "#C678DD" # Purple color for the "$" symbol
        
        # Styled prompt with HTML
        prompt_text = (
            f'<span style="color: {arrow_color};">➜</span> '
            f'<span style="color: {path_color};">{current_dir}</span> '
            f'<span style="color: {symbol_color};">$</span> '
        )
        
        # Append the prompt with colors to the terminal display
        self.terminal_display.append(prompt_text)
        self.terminal_display.moveCursor(QTextCursor.End)
        
    def process_command(self):
        command = self.input_field.text()
        
        self.terminal_display.insertPlainText(command + "\n")
        
        if command.strip():
            self.command_history.append(command)
            self.history_index = len(self.command_history)
            try:
                client_socket.sendall(command.encode())  # Send command to server
            except (KeyboardInterrupt, EOFError):
                print("\nDetected interrupt or EOF, closing connection...")
        
        # Clear input field and add new prompt
        self.input_field.clear()
        
        # Scroll to bottom
        self.terminal_display.moveCursor(QTextCursor.End)

    def receive_data(self):
        while True:
            try:
                data = client_socket.recv(2048).decode()
                if data:
                    self.terminal_display.append(f'<span style="color: #BBBBBB;">Server: {data}</span>\n')
                    self.terminal_display.moveCursor(QTextCursor.End)
                    self.append_prompt()
            except Exception as e:
                print(f"Error receiving data: {e}")
                break

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Up:
            if self.history_index > 0:
                self.history_index -= 1
                self.input_field.setText(self.command_history[self.history_index])
        elif event.key() == Qt.Key_Down:
            if self.history_index < len(self.command_history) - 1:
                self.history_index += 1
                self.input_field.setText(self.command_history[self.history_index])
            elif self.history_index == len(self.command_history) - 1:
                self.history_index = len(self.command_history)
                self.input_field.clear()
        else:
            super().keyPressEvent(event)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    terminal = ModernTerminal()
    terminal.show()
    sys.exit(app.exec_())
