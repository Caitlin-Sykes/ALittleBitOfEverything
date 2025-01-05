from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel


class PDFCombinerUI(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout(self)
        label = QLabel("PDF Combiner Tool", self)
        layout.addWidget(label)
