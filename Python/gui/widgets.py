from PySide6.QtCore import Qt, QSize
from PySide6.QtGui import QIcon
from PySide6.QtWidgets import QLabel, QWidget, QHBoxLayout


class BaseIconWidget(QWidget):
    """Base widget class to handle common icon and alignment behavior."""

    def __init__(self, icon, text=""):
        """Initialise the base widget.
        :param icon: The icon to display.
        :param text: The text to display.
        """

        super().__init__()

        # Store the icon and initialize the label
        self.original_icon = QIcon(icon) if isinstance(icon, str) else icon
        self.icon_label = QLabel()
        self.text_label = QLabel(text)

        # Layout setup for icon
        self.icon_layout = QHBoxLayout(self)
        self.icon_layout.addWidget(self.icon_label)
        self.icon_layout.setContentsMargins(0, 0, 0, 0)

        # Set default alignment and visibility for the text
        self.text_label.setVisible(bool(text))

    def set_icon(self, pixmap_size=32, alignment=Qt.AlignLeft):
        """Set the icon with the specified size and alignment."""
        # Ensure pixmap_size is an integer
        pixmap_size = int(pixmap_size)

        # Create the pixmap with the correct size
        pixmap = self.original_icon.pixmap(QSize(pixmap_size, pixmap_size))
        self.icon_label.setPixmap(pixmap)
        self.icon_layout.setAlignment(alignment)

    def set_text(self, text):
        """Update the text displayed in the widget."""
        print("HIA")
        self.text_label.setText(text)
        self.text_label.setVisible(bool(text))


class MenuWidget(BaseIconWidget):
    """Widget for displaying menu items with text and button functionality."""

    def __init__(self, tool_name: str, icon):
        super().__init__(icon)

        # Store the tool name and add custom layout elements
        self.tool_name = tool_name

        # Set initial icon alignment and size
        self.set_icon(collapsed=False)

    def set_icon(self, collapsed=False):
        """Set icon size and adjust alignment based on collapse state."""
        pixmap_size = 16 if collapsed else 24
        alignment = Qt.AlignCenter if collapsed else Qt.AlignLeft
        super().set_icon(pixmap_size=pixmap_size, alignment=alignment)

    def on_button_click(self):
        """Handles the button click event."""
        print(f"{self.tool_name} started!")


class CenteredIconWidget(BaseIconWidget):
    """Widget for displaying a centered icon, unaffected by sidebar collapse state."""

    def __init__(self, icon):
        super().__init__(icon)
        # Always center the icon for this widget
        self.set_icon(always_centered=True)

    def set_icon(self, always_centered=True, pixmap_size=30):
        """Set the icon size and center alignment.
        :param always_centered: Whether to center the icon or not."""
        alignment = Qt.AlignCenter
        super().set_icon(pixmap_size=pixmap_size, alignment=alignment)
