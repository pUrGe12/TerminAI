import sys
import os
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QTextEdit, QLineEdit
from PyQt5.QtGui import QFont, QTextCursor, QColor
from PyQt5.QtCore import Qt

class ModernTerminal(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()
        self.command_history = []
        self.history_index = -1
        
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
        
        prompt_text = f"➜ {current_dir} git:(main) "
        self.terminal_display.append(prompt_text)
        self.terminal_display.moveCursor(QTextCursor.End)
        
    def process_command(self):
        command = self.input_field.text()
        
        # Display the entered command in the terminal display
        self.terminal_display.insertPlainText(command + "\n")
        
        # Echo command result in gray (replace this with actual command processing output if needed)
        if command.strip():
            self.command_history.append(command)
            self.history_index = len(self.command_history)
            self.terminal_display.append(f'<span style="color: #BBBBBB;">You entered: {command}</span>\n')
        
        

        # Clear input field and add new prompt
        self.input_field.clear()
        self.append_prompt()
        
        # Scroll to bottom
        self.terminal_display.moveCursor(QTextCursor.End)

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
