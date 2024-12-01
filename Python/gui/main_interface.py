from PySide6.QtCore import Signal, Slot, Qt
from PySide6.QtWidgets import QWidget, QHBoxLayout, QStackedWidget, QListWidget, QListWidgetItem, QVBoxLayout, QLabel, \
    QSizePolicy

from Python.gui.sidebar import MainSidebar
from Python.gui.widgets import CenteredIconWidget, MenuWidget


class MainInterface(QWidget):
    def __init__(self, icons, tools):
        super().__init__()

        # Store tools and icons
        self.icons = icons
        self.tools = tools

        # Main layout setup (horizontal layout)
        self.main_layout = QHBoxLayout(self)
        self.main_layout.setContentsMargins(0, 0, 0, 0)  # Remove margins
        self.main_layout.setSpacing(0)  # Remove spacing

        # Create the stacked widget (for content panel)
        self.stacked_widget = QStackedWidget()
        self.stacked_widget.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        # Create the mainSidebar (pass the stacked_widget to it)
        self.mainSidebar = MainSidebar(icons, tools, self.stacked_widget)
        self.mainSidebar.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Expanding)

        # Add the sidebar and stacked widget to the main layout
        self.main_layout.addWidget(self.mainSidebar, alignment=Qt.AlignLeft)  # Sidebar on the left
        self.main_layout.addWidget(self.stacked_widget)  # Content panel on the right

        # Set the main layout for the MainInterface widget
        self.setLayout(self.main_layout)