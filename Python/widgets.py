from PySide6.QtCore import Qt
from PySide6.QtGui import QIcon
from PySide6.QtWidgets import QLabel, QVBoxLayout, QWidget, QPushButton


class MenuWidget(QWidget):
    def __init__(self, tool_name: str):
        super().__init__()

        # Store the tool name to use in the widget (this can be used in the UI)
        self.tool_name = tool_name

        # Layout for the widget
        layout = QVBoxLayout()

        # Create a label to show the tool name (can be dynamic)
        label = QLabel(f"Welcome to {tool_name}")
        label.setAlignment(Qt.AlignCenter)  # Center align the text for each tab

        # Create a simple button for each tool (this can be customized)
        button = QPushButton(f"Start {tool_name}")
        button.clicked.connect(self.on_button_click)

        # Add the components to the layout
        layout.addWidget(label)
        layout.addWidget(button)

        # Set the layout for the MenuWidget
        self.setLayout(layout)

    def on_button_click(self):
        print(f"{self.tool_name} started!")


class CenteredIconWidget(QWidget):
    """A widget to hold a centered icon with adjustable size."""

    def __init__(self, icon_path):
        super().__init__()
        self.layout = QVBoxLayout()
        self.layout.setAlignment(Qt.AlignCenter)
        self.label = QLabel()
        self.set_icon(icon_path)  # Initial icon setup
        self.layout.addWidget(self.label)
        self.setLayout(self.layout)

    def set_icon(self, icon_path):
        """Set or update the icon displayed in the widget."""
        self.icon_path = icon_path
        self.update_icon_size(30)  # Default size when initialized

    def update_icon_size(self, size):
        """Update the icon size dynamically."""
        self.label.setPixmap(QIcon(self.icon_path).pixmap(size, size))
