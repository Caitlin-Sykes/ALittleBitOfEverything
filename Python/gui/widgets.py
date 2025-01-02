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

        # Store the icon and initialize the labels
        self.original_icon = QIcon(icon) if isinstance(icon, str) else icon
        self.icon_label = QLabel()
        self.text_label = QLabel(text)

        # Layout setup for icon and text
        self.icon_layout = QHBoxLayout(self)
        self.icon_layout.addWidget(self.icon_label)  # Add icon
        self.icon_layout.setContentsMargins(0, 0, 0, 0)
        self.icon_layout.setSpacing(5)  # Space between icon and text

        # Add the text label dynamically if it has text
        if text:
            self.icon_layout.addWidget(self.text_label)

    def set_icon(self, pixmap_size=32, alignment=Qt.AlignLeft):
        """Set the icon with the specified size and alignment."""
        # Ensure pixmap_size is an integer
        pixmap_size = int(pixmap_size)

        # Create the pixmap with the correct size
        pixmap = self.original_icon.pixmap(QSize(pixmap_size, pixmap_size))
        self.icon_label.setPixmap(pixmap)
        self.icon_layout.setAlignment(alignment)

    def set_text(self, text, collapsed=False):
        """Set the text for the icon widget and adjust its visibility.
        :param text: The text to display.
        :param collapsed: Whether the nav is collapsed or not."""
        
        # Update the text content
        self.text_label.setText(text)

        # If collapsed, removes the text label
        if collapsed:
            # Remove the text_label from the layout when collapsed
            if self.text_label.parent() == self:
                self.icon_layout.removeWidget(self.text_label)
                self.text_label.hide()
        # If fully expanded, shows the text
        else:
            # Add the text_label to the layout when expanded
            self.icon_layout.addWidget(self.text_label)
            self.text_label.show()


class MenuWidget(BaseIconWidget):
    """Widget for displaying menu items with text and button functionality."""

    def __init__(self, tool_name: str, icon):
        super().__init__(icon)

        # Store the tool name and add custom layout elements
        self.tool_name = tool_name

        # Set initial icon alignment and size
        self.set_icon(collapsed=False)
        self.set_text(self.tool_name, collapsed=False)

    def set_icon(self, collapsed=False):
        """Set icon size and adjust alignment based on collapse state."""
        pixmap_size = 24 if collapsed else 20
        alignment = Qt.AlignCenter if collapsed else Qt.AlignLeft
        super().set_icon(pixmap_size=pixmap_size, alignment=alignment)


class CenteredIconWidget(BaseIconWidget):
    """Widget for displaying a centered icon, unaffected by sidebar collapse state."""

    def __init__(self, icon):
        super().__init__(icon)
        # Always center the icon for this widget
        self.set_icon(always_centered=True)

    def set_icon(self, always_centered=True, pixmap_size=30):
        """Set the icon size and center alignment.
        :param always_centered: Whether to center the icon or not.
        :param pixmap_size: size of the icon"""
        alignment = Qt.AlignCenter
        super().set_icon(pixmap_size=pixmap_size, alignment=alignment)
