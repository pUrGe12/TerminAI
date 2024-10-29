from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QTextEdit, QHBoxLayout, QLabel, QLineEdit
from PyQt5.QtGui import QColor, QFont, QTextCursor
from PyQt5.QtCore import Qt
import sys

class BashTerminal(QWidget):
    def __init__(self):
        super().__init__()
        
        # Set up the main window
        self.setWindowTitle("Bash Terminal")
        self.setGeometry(100, 100, 800, 400)
        self.setWindowOpacity(0.9)  # Semi-transparent background
        
        # Set up background color and layout
        self.setStyleSheet("background-color: rgba(0, 0, 0, 230);")
        main_layout = QVBoxLayout()
        
        # Create the prompt bar at the top
        prompt_layout = QHBoxLayout()
        
        # Prompt label on the left side
        self.prompt_label = QLabel("user@bash:~$ ", self)
        self.prompt_label.setStyleSheet("color: #00FF00;")
        self.prompt_label.setFont(QFont("Courier", 12))
        
        # Input field where the user enters text
        self.prompt_input = QLineEdit(self)
        self.prompt_input.setStyleSheet("color: #00FF00; background-color: rgba(0, 0, 0, 0);")
        self.prompt_input.setFont(QFont("Courier", 12))
        
        # Add the label and input field to the prompt layout
        prompt_layout.addWidget(self.prompt_label)
        prompt_layout.addWidget(self.prompt_input)
        
        # Connect the return key press to handling input
        self.prompt_input.returnPressed.connect(self.process_command)
        
        # Create the display area (QTextEdit) for showing commands and responses
        self.terminal_display = QTextEdit(self)
        self.terminal_display.setReadOnly(True)
        self.terminal_display.setStyleSheet("color: #00FF00; background-color: rgba(0, 0, 0, 0);")
        self.terminal_display.setFont(QFont("Courier", 12))
        
        # Add the prompt bar at the top and the terminal display below it
        main_layout.addLayout(prompt_layout)
        main_layout.addWidget(self.terminal_display)
        
        self.setLayout(main_layout)
    
    def process_command(self):
        # Get the command entered by the user
        command = self.prompt_input.text()
        
        # Display the command in the terminal display
        self.terminal_display.append(f"user@bash:~$ {command}")
        
        # For now, just echo back the command as if it's "executed"
        self.terminal_display.append(command)
        self.terminal_display.append("")  # Add a newline for spacing
        
        # Scroll to the bottom of the display
        self.terminal_display.moveCursor(QTextCursor.End)
        
        # Clear the prompt input
        self.prompt_input.clear()

# Main application execution
app = QApplication(sys.argv)
window = BashTerminal()
window.show()
sys.exit(app.exec_())
