from PySide6.QtCore import Qt, Slot
from PySide6.QtGui import QIcon
from PySide6.QtWidgets import QLabel, QVBoxLayout, QWidget, QPushButton, QHBoxLayout


class MenuWidget(QWidget):
    def __init__(self, tool_name: str):
        super().__init__()

        # Store the tool name to use in the widget (this can be used in the UI)
        self.tool_name = tool_name

        # Layout for the widget
        layout = QVBoxLayout()

        # Create a label to show the tool name (can be dynamic)
        label = QLabel(f"Welcome to {tool_name}")
        label.setAlignment(Qt.AlignCenter)

        # Create a simple button for each tool
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

    def __init__(self, icon, collapsed=False):
        super().__init__()

        # Convert icon to QIcon if it's a string (path)
        if isinstance(icon, str):
            icon = QIcon(icon)

        self.original_icon = icon  # Store the original QIcon for resizing
        self.icon_label = QLabel()

        # Define the layout before calling set_icon
        self.icon_layout = QHBoxLayout(self)
        self.icon_layout.addWidget(self.icon_label)
        self.icon_layout.setContentsMargins(0, 0, 0, 0)

        # Set the icon initially based on the collapsed state
        self.set_icon(collapsed)

        # Set initial alignment based on the collapsed state
        self.icon_layout.setAlignment(Qt.AlignCenter if collapsed else Qt.AlignLeft)

    def set_icon(self, collapsed=False):
        """Set the icon and adjust alignment based on sidebar state."""
        # Adjust icon size based on collapsed state
        pixmap_size = 16 if collapsed else 32
        pixmap = self.original_icon.pixmap(pixmap_size, pixmap_size)
        self.icon_label.setPixmap(pixmap)

        # Update alignment based on collapsed state
        self.icon_layout.setAlignment(Qt.AlignCenter if collapsed else Qt.AlignLeft)

    @Slot(bool)
    def update_icon(self, collapsed):
        """Slot to update the icon when sidebar state changes."""
        self.set_icon(collapsed)
