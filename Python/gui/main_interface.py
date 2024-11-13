from PySide6.QtCore import Signal, Slot
from PySide6.QtWidgets import QWidget, QHBoxLayout, QStackedWidget, QListWidget, QListWidgetItem

from Python.widgets import CenteredIconWidget, MenuWidget


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
            icon_widget = CenteredIconWidget(tool["icon"])
            self.icon_widgets.append(icon_widget)
            item = QListWidgetItem()
            self.list_widget.addItem(item)
            self.list_widget.setItemWidget(item, icon_widget)

    def create_tool_pages(self):
        """Creates a page for each tool in the stacked widget."""
        for tool in self.tools:
            self.stacked_widget.addWidget(MenuWidget(tool["name"]))

    @Slot(bool)
    def update_sidebar_state(self, collapsed):
        """Updates icon alignment when sidebar state changes."""
        for icon_widget in self.icon_widgets:
            icon_widget.update_icon(collapsed)

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
        if self.list_widget.indexFromItem(item).row() == 0:
            self.toggle_sidebar()