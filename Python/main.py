import sys
from PySide6.QtCore import QSize
from PySide6.QtWidgets import QApplication, QMainWindow, QWidget, QStackedWidget, QHBoxLayout, QListWidget, \
    QListWidgetItem, QLabel
from PySide6.QtGui import QIcon
import json

from Python.widgets import CenteredIconWidget, MenuWidget


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("A Little Bit of Everything")
        self.setGeometry(100, 100, 800, 600)

        # Load the tool icons from the JSON file
        try:
            with open("icons_mapping.json", "r") as f:
                self.icons = json.load(f)
        except json.JSONDecodeError as e:
            print(f"Error loading JSON: {e}")
            self.icons = {}

        self.tools = self.icons.get("tools", [])
        self.is_sidebar_collapsed = False  # Track sidebar state

        # Main layout to divide the left panel (list) and right panel (stacked widgets)
        main_layout = QHBoxLayout()

        # Create a stacked widget to manage pages
        self.stacked_widget = QStackedWidget()

        # Create a list widget for the vertical tabs (icons and text)
        self.list_widget = QListWidget()
        self.list_widget.setFixedWidth(150)
        self.list_widget.setStyleSheet("""
            QListWidget {
                border: none;
                padding: 0;
                margin: 0;
            }
            QListWidget::item {
                height: 50px;
                padding-left: 10px;
                padding-right: 10px;
            }
        """)

        # Add the burger (collapse/expand) icon as the first item using CenteredIconWidget
        self.burger_widget = CenteredIconWidget(self.icons.get("Collapse Menu", ""))
        burger_item = QListWidgetItem()
        self.list_widget.addItem(burger_item)
        self.list_widget.setItemWidget(burger_item, self.burger_widget)

        # Add the tools (File Extractor, PDF Combiner) as separate items
        for tool in self.tools:
            item = QListWidgetItem(QIcon(tool["icon"]), tool["name"])
            self.list_widget.addItem(item)

        # Add color widgets to stacked widget
        for tool in self.tools:
            self.stacked_widget.addWidget(MenuWidget(tool["name"]))

        # Connect list item click to change the stacked widget's current index and toggle sidebar
        self.list_widget.currentRowChanged.connect(self.stacked_widget.setCurrentIndex)
        self.list_widget.itemClicked.connect(self.handle_item_click)

        # Add list widget and stacked widget to the main layout
        main_layout.addWidget(self.list_widget)
        main_layout.addWidget(self.stacked_widget)

        # Set the central widget layout
        central_widget = QWidget()
        central_widget.setLayout(main_layout)
        self.setCentralWidget(central_widget)

        # Configure margins and layout stretch
        self.setContentsMargins(0, 0, 0, 0)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setStretch(1, 1)

    def handle_item_click(self, item):
        """ 
        Handles clicks of the mav nar
        :param self
        :param item - the item clicked
        """
        
        # Check if the burger icon was clicked
        if self.list_widget.indexFromItem(item).row() == 0:
            self.toggle_sidebar()

    def toggle_sidebar(self):
        """ 
        Toggle sidebar state and update its width
        :param self
        """
        
        self.is_sidebar_collapsed = not self.is_sidebar_collapsed
        self.list_widget.setFixedWidth(40 if self.is_sidebar_collapsed else 150)

        # Update the burger icon to reflect the new state
        new_icon = "Expand Menu" if self.is_sidebar_collapsed else "Collapse Menu"
        self.burger_widget.set_icon(self.icons.get(new_icon, ""))

        # Set text visibility based on sidebar state
        for i in range(1, self.list_widget.count()):  # Start from 1 to skip the burger icon
            item = self.list_widget.item(i)
            item.setText("" if self.is_sidebar_collapsed else self.tools[i - 1]["name"])


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()  # Show the main window
    app.exec()  # Start the event loop