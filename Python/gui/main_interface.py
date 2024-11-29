from PySide6.QtCore import Signal, Slot, Qt
from PySide6.QtWidgets import QWidget, QHBoxLayout, QStackedWidget, QListWidget, QListWidgetItem, QVBoxLayout, QLabel

from Python.gui.widgets import CenteredIconWidget, MenuWidget


class MainInterface(QWidget):
    sidebar_state_changed = Signal(bool)

    def __init__(self, icons, tools):
        super().__init__()

        # Track sidebar state and icon widgets
        self.is_sidebar_collapsed = False
        self.icon_widgets = []
        self.icons = icons
        self.tools = tools

        # Main layout setup
        self.main_layout = QHBoxLayout(self)

        # Create and define stacked widget first
        self.stacked_widget = QStackedWidget()

        # Create the sidebar after defining stacked_widget
        self.list_widget = self.create_sidebar()

        # Populate sidebar and create tool pages
        self.populate_sidebar()
        self.create_tool_pages()

        # Add sidebar and main content to layout
        self.main_layout.addWidget(self.list_widget)
        self.main_layout.addWidget(self.stacked_widget)
        self.main_layout.setContentsMargins(0, 0, 0, 0)
        self.main_layout.setStretch(1, 1)

        # Initial sidebar state notification
        self.sidebar_state_changed.connect(self.update_sidebar_state)
        self.sidebar_state_changed.emit(self.is_sidebar_collapsed)

    def create_sidebar(self):
        """Creates the sidebar list widget with styling and connections."""
        list_widget = QListWidget()
        list_widget.setFixedWidth(150)
        list_widget.setStyleSheet("""
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
        list_widget.currentRowChanged.connect(self.stacked_widget.setCurrentIndex)
        list_widget.itemClicked.connect(self.handle_item_click)
        return list_widget

    def populate_sidebar(self):
        """Adds burger icon and tool icons to the sidebar."""
        self.burger_widget = CenteredIconWidget(self.icons.get("Collapse Menu", ""))
        self.icon_widgets.append(self.burger_widget)

        burger_item = QListWidgetItem()
        self.list_widget.addItem(burger_item)
        self.list_widget.setItemWidget(burger_item, self.burger_widget)

        for tool in self.tools:
            icon_widget = MenuWidget(tool["name"], tool["icon"])
            self.icon_widgets.append(icon_widget)
            item = QListWidgetItem()
            self.list_widget.addItem(item)
            self.list_widget.setItemWidget(item, icon_widget)

    def create_tool_pages(self):
        """Creates the home page and a page for each tool in the stacked widget."""
        # Create a home page
        home_page = QWidget()
        home_layout = QVBoxLayout(home_page)
        home_label = QLabel("Welcome to the Home Page!", home_page)
        home_label.setAlignment(Qt.AlignCenter)  # Center-align text
        home_layout.addWidget(home_label)
        self.stacked_widget.addWidget(home_page)  # Add the home page first
    
        # Create a page for each tool
        for tool in self.tools:
            page_widget = QWidget()
            page_layout = QVBoxLayout(page_widget)
    
            # Add content for each tool
            content_label = QLabel(f"Welcome to {tool['name']}!", page_widget)
            content_label.setAlignment(Qt.AlignCenter)
            page_layout.addWidget(content_label)
    
            self.stacked_widget.addWidget(page_widget)

    @Slot(bool)
    def update_sidebar_state(self, collapsed):
        """Updates icon alignment and size when sidebar state changes."""
        for icon_widget in self.icon_widgets:
            if isinstance(icon_widget, MenuWidget):
                icon_widget.update_icon(collapsed)
            else:
                # For the burger and tool icons, resize them when collapsed state changes
                icon_widget.set_icon(pixmap_size=16 if collapsed else 32)

    def toggle_sidebar(self):
        """Toggles sidebar between collapsed and expanded."""
        self.is_sidebar_collapsed = not self.is_sidebar_collapsed
        self.list_widget.setFixedWidth(40 if self.is_sidebar_collapsed else 150)

        new_icon = "Expand Menu" if self.is_sidebar_collapsed else "Collapse Menu"
        self.burger_widget.set_icon(self.icons.get(new_icon, ""))

        for i in range(1, self.list_widget.count()):
            item = self.list_widget.item(i)
            item.setText("" if self.is_sidebar_collapsed else self.tools[i - 1]["name"])

        self.sidebar_state_changed.emit(self.is_sidebar_collapsed)

    def handle_item_click(self, item):
        """Handles sidebar clicks and toggles sidebar if burger icon is clicked."""
        index = self.list_widget.indexFromItem(item).row()

        if index == 0:
            # Show home page and toggle side bar
            self.stacked_widget.setCurrentIndex(0)
            self.toggle_sidebar()

        else:
            # its index -1 because in the tools array, [0] is file extractor, but in the nav bar, its index[1]
            item = self.list_widget.item(index)
            item.setText("" if self.is_sidebar_collapsed else self.tools[index - 1]["name"])

        self.sidebar_state_changed.emit(self.is_sidebar_collapsed)
