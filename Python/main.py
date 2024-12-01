import sys
from PySide6.QtWidgets import QApplication, QMainWindow
import json
from Python.gui.main_interface import MainInterface


def load_icons(file_path):
    """Loads icons from a JSON file.
    :param file_path: Path to the JSON file containing the icons."""
    try:
        with open(file_path, "r") as f:
            return json.load(f)
    except json.JSONDecodeError as e:
        print(f"Error loading JSON: {e}")
        return {}


class MainWindow(QMainWindow):
    """Main window."""
    def __init__(self):
        super().__init__()

        # Basic window properties
        self.setWindowTitle("A Little Bit of Everything")
        self.setGeometry(100, 100, 800, 600)

        # Load icons and tools
        icons = load_icons("icons_mapping.json")
        tools = icons.get("tools", [])

        # Initialize main interface
        self.main_interface = MainInterface(icons, tools)
        self.setCentralWidget(self.main_interface)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    app.exec()
