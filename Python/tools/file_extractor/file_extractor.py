from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel

class FileExtractorPage(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout(self)
        label = QLabel("File Extractor Tool", self)
        layout.addWidget(label)
