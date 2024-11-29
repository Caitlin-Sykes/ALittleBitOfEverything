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

        # Create the stacked widget (for content panel)
        self.stacked_widget = QStackedWidget()

        # Create the mainSidebar (pass the stacked_widget to it)
        self.mainSidebar = MainSidebar(icons, tools, self.stacked_widget)

        # Add the sidebar and stacked widget to the main layout
        self.main_layout.addWidget(self.mainSidebar)  # Add Sidebar (on the left)
        self.main_layout.addWidget(self.stacked_widget)  # Add Stacked Widget (content panel)

        # Ensure the stacked widget takes up the remaining space
        self.main_layout.setStretch(1, 1)

        # Set the main layout for the MainInterface widget
        self.setLayout(self.main_layout)