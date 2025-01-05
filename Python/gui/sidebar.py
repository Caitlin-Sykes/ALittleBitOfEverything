import importlib

from PySide6.QtCore import Signal, Qt
from PySide6.QtWidgets import QListWidget, QListWidgetItem, QWidget, QVBoxLayout, QLabel

from Python.gui.widgets import MenuWidget, CenteredIconWidget


class Sidebar(QWidget):
    """ A base sidebar class"""
    sidebar_state_changed = Signal(bool)

    def __init__(self, icons, titles):
        """Inits the navbar
        :param icons: list of icons
        :param titles: list of titles for nav
        """
        super().__init__()

        # Track sidebar state and icon widgets
        self.is_sidebar_collapsed = False
        self.icon_widgets = []
        self.icons = icons
        self.titles = titles

        # Sidebar layout setup, no margins and no spacing
        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout.setSpacing(0)

        # Create the list widget for sidebar items
        self.list_widget = self.create_sidebar()
        self.layout.addWidget(self.list_widget)

        # Init burger widget for sidebar
        self.burger_widget = CenteredIconWidget(self.icons.get("Collapse Menu", ""))

        # Populate sidebar with icons
        self.populate_sidebar()

        # Notify about initial sidebar state, collapsed or not collapsed
        self.sidebar_state_changed.connect(self.update_sidebar_state)

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

        list_widget.itemClicked.connect(self.handle_item_click)
        return list_widget

    def populate_sidebar(self):
        """Adds burger icon and tool icons to the sidebar."""

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
                icon_widget.set_icon(collapsed)
                icon_widget.set_text(icon_widget.tool_name, collapsed)
            else:
                # Resize for burger widget
                icon_widget.set_icon(pixmap_size=24 if collapsed else 30)

    def toggle_sidebar(self):
        """Toggles sidebar between collapsed and expanded."""
        self.is_sidebar_collapsed = not self.is_sidebar_collapsed
        self.list_widget.setFixedWidth(60 if self.is_sidebar_collapsed else 150)

        new_icon = "Expand Menu" if self.is_sidebar_collapsed else "Collapse Menu"
        self.burger_widget.set_icon(self.icons.get(new_icon, ""))

        for i in range(1, self.list_widget.count()):
            item = self.list_widget.item(i)
            item.setText("" if self.is_sidebar_collapsed else self.titles[i - 1]["name"])

        self.sidebar_state_changed.emit(self.is_sidebar_collapsed)


class MainSidebar(Sidebar):
    """This is the main sidebar class for navigation"""

    def __init__(self, icons, titles, stacked_widget):
        super().__init__(icons, titles)
        self.stacked_widget = stacked_widget
        self.create_tool_pages()

    def create_tool_pages(self):
        """Create pages for each tool and add them to the stacked_widget."""

        # Add a default page
        default_page = QWidget()
        default_layout = QVBoxLayout(default_page)
        default_label = QLabel("Welcome to the Default Page!", default_page)
        default_label.setAlignment(Qt.AlignCenter)
        default_layout.addWidget(default_label)
        self.stacked_widget.addWidget(default_page)
    
        # Add other tool pages dynamically
        for tool in self.titles:
            # Gets the tool name and the tool page (stored in tools/)
            tool_name = tool['name']
            tool_page = tool['page']
    
            # Dynamically import the tool's page script
            try:
                # Convert the file path to a valid Python module name
                module_name = tool_page.replace(".py", "").replace("/", ".")
                file_path = tool_page
    
                # Create a module spec
                spec = importlib.util.spec_from_file_location(module_name, file_path)
                tool_module = importlib.util.module_from_spec(spec)
    
                # Load the module
                spec.loader.exec_module(tool_module)
    
                # Assuming the class name in the script matches the tool name (e.g., "PDFCombinerPage" for "PDF Combiner")
                class_name = f"{tool_name.replace(' ', '')}UI"
                tool_class = getattr(tool_module, class_name)
    
                # Create the page widget
                page_widget = tool_class()
    
                # Add the page to the stacked widget
                self.stacked_widget.addWidget(page_widget)
    
            except ImportError as e:
                print(f"Error importing {tool_name}: {e}")

    def handle_item_click(self, item):
        """Handles sidebar clicks.
        :param item: QListWidgetItem, the item that is clicked in the nav"""
        index = self.list_widget.indexFromItem(item).row()

        if index == 0:
            self.toggle_sidebar()
            self.stacked_widget.setCurrentIndex(0)
        else:
            # Update the stacked widget panel
            self.stacked_widget.setCurrentIndex(index)
