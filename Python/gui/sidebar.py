from PySide6.QtWidgets import QListWidget, QListWidgetItem, QWidget, QVBoxLayout, QLabel, QStackedWidget, QHBoxLayout
from PySide6.QtCore import Signal, Qt

from Python.gui.widgets import MenuWidget, CenteredIconWidget


class Sidebar(QWidget):
    """ A base sidebar class"""
    sidebar_state_changed = Signal(bool)

    def __init__(self, icons, titles):
        """Inits the navbar
        :param icons: list of icons
        :param titles: list of titles
        """
        super().__init__()

        # Track sidebar state and icon widgets
        self.is_sidebar_collapsed = False
        self.icon_widgets = []
        self.icons = icons
        self.titles = titles

        # Sidebar layout setup
        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout.setSpacing(0)

        # Create the list widget for sidebar items
        self.list_widget = self.create_sidebar()
        self.layout.addWidget(self.list_widget)

        # Populate sidebar with icons
        self.populate_sidebar()

        # Notify about initial sidebar state
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
        list_widget.currentRowChanged.connect(self.on_item_select)
        list_widget.itemClicked.connect(self.handle_item_click)
        return list_widget

    def populate_sidebar(self):
        """Adds burger icon and tool icons to the sidebar."""
        self.burger_widget = CenteredIconWidget(self.icons.get("Collapse Menu", ""))
        self.icon_widgets.append(self.burger_widget)

        burger_item = QListWidgetItem()
        self.list_widget.addItem(burger_item)
        self.list_widget.setItemWidget(burger_item, self.burger_widget)

        for tool in self.titles:
            icon_widget = MenuWidget(tool["name"], tool["icon"])
            self.icon_widgets.append(icon_widget)
            item = QListWidgetItem()
            self.list_widget.addItem(item)
            self.list_widget.setItemWidget(item, icon_widget)

    def update_sidebar_state(self, collapsed):
        """Updates icon alignment and size when sidebar state changes."""
        for icon_widget in self.icon_widgets:
            if isinstance(icon_widget, MenuWidget):
                icon_widget.update_icon(collapsed)
            else:
                # Resize for burger widget
                icon_widget.set_icon(pixmap_size=16 if collapsed else 32)

    def toggle_sidebar(self):
        """Toggles sidebar between collapsed and expanded."""
        self.is_sidebar_collapsed = not self.is_sidebar_collapsed
        self.list_widget.setFixedWidth(40 if self.is_sidebar_collapsed else 150)

        new_icon = "Expand Menu" if self.is_sidebar_collapsed else "Collapse Menu"
        self.burger_widget.set_icon(self.icons.get(new_icon, ""))

        for i in range(1, self.list_widget.count()):
            item = self.list_widget.item(i)
            item.setText("" if self.is_sidebar_collapsed else self.titles[i - 1]["name"])

        self.sidebar_state_changed.emit(self.is_sidebar_collapsed)

    def on_item_select(self, index):
        """Handle sidebar item selection."""
        self.sidebar_state_changed.emit(self.is_sidebar_collapsed)

    def handle_item_click(self, item):
        """Handles sidebar clicks and toggles sidebar if burger icon is clicked."""
        index = self.list_widget.indexFromItem(item).row()

        if index == 0:
            # Toggle sidebar when burger icon is clicked
            self.toggle_sidebar()
        else:
            # Update selected item text when collapsed or expanded
            item.setText("" if self.is_sidebar_collapsed else self.titles[index - 1]["name"])
            self.sidebar_state_changed.emit(self.is_sidebar_collapsed)


class MainSidebar(Sidebar):
    def __init__(self, icons, titles, stacked_widget):
        super().__init__(icons, titles)

        # Store the passed stacked_widget (from MainInterface)
        self.stacked_widget = stacked_widget

        # Sidebar layout setup
        self.layout = QVBoxLayout(self)  # Use QVBoxLayout for the sidebar
        self.setLayout(self.layout)     
        
        # Now, set up the tool pages in the stacked_widget
        self.create_tool_pages()

    def create_tool_pages(self):
        """Create pages for each tool and add them to the stacked_widget."""
        # Create a home page
        home_page = QWidget()
        home_layout = QVBoxLayout(home_page)
        home_label = QLabel("Welcome to the Home Page!", home_page)
        home_label.setAlignment(Qt.AlignCenter)
        home_layout.addWidget(home_label)
        self.stacked_widget.addWidget(home_page)

        # Create a page for each tool
        for tool in self.titles:
            page_widget = QWidget()
            page_layout = QVBoxLayout(page_widget)

            # Add content (e.g., a label with the tool's name)
            content_label = QLabel(f"Welcome to {tool['name']}!", page_widget)
            content_label.setAlignment(Qt.AlignCenter)
            page_layout.addWidget(content_label)

            self.stacked_widget.addWidget(page_widget)