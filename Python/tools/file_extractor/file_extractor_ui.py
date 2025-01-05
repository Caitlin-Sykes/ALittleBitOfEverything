from PySide6.QtGui import QColor
from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QHBoxLayout, QPushButton, QTextEdit, QProgressBar, \
    QFileDialog

from Python.tools.file_extractor.file_extractor_functionality import FileExtractorFunctionality


class FileExtractorUI(QWidget):
    def __init__(self):
        super().__init__()

        self.setObjectName("FileExtractorUI")  # Optionally give it an object name for styling/debugging

        # Layout
        main_layout = QVBoxLayout()
        self.setLayout(main_layout)

        # Source Folder Selection
        self.source_label = QLabel("Source Folder:")
        self.source_button = QPushButton("Select Source Folder")
        self.source_button.clicked.connect(self.select_source_folder)

        source_layout = QHBoxLayout()
        source_layout.addWidget(self.source_label)
        source_layout.addWidget(self.source_button)

        # Destination Folder Selection
        self.destination_label = QLabel("Destination Folder:")
        self.destination_button = QPushButton("Select Destination Folder")
        self.destination_button.clicked.connect(self.select_destination_folder)

        destination_layout = QHBoxLayout()
        destination_layout.addWidget(self.destination_label)
        destination_layout.addWidget(self.destination_button)

        # Progress Bar
        self.progress_bar = QProgressBar()
        self.progress_bar.setRange(0, 100)

        # Status Text Area
        self.status_text = QTextEdit()
        self.status_text.setReadOnly(True)

        # Start Extraction Button
        self.extract_button = QPushButton("Start Extraction")
        self.extract_button.clicked.connect(self.start_extraction)
        self.extract_button.setEnabled(False)  # Initially disabled

        # Add widgets to main layout
        main_layout.addLayout(source_layout)
        main_layout.addLayout(destination_layout)
        main_layout.addWidget(self.progress_bar)
        main_layout.addWidget(self.status_text)
        main_layout.addWidget(self.extract_button)

        # Initialize folders
        self.source_folder = ""
        self.destination_folder = ""

    def select_source_folder(self):
        """Open a file dialog to select the source folder."""
        folder = QFileDialog.getExistingDirectory(self, "Select Source Folder")
        if folder:
            self.source_folder = folder
            self.source_label.setText(f"Source Folder: {folder}")
            self.check_for_valid_paths()

    def select_destination_folder(self):
        """Open a file dialog to select the destination folder."""
        folder = QFileDialog.getExistingDirectory(self, "Select Destination Folder")
        if folder:
            self.destination_folder = folder
            self.destination_label.setText(f"Destination Folder: {folder}")
            self.check_for_valid_paths()

    def check_for_valid_paths(self):
        """Enable the Start Extraction button if both folders are set."""
        if self.source_folder and self.destination_folder:
            self.extract_button.setEnabled(True)

    def start_extraction(self):
        """Start the extraction process."""
        self.status_text.clear()
        self.status_text.setTextColor(QColor("green"))
        self.status_text.append("Starting extraction...")

        # Disable the button and start extraction in a separate thread
        self.extract_button.setEnabled(False)
        self.worker = FileExtractorFunctionality(self.source_folder, self.destination_folder)
        
        # Connects listeners for certain events
        self.worker.progress_updated.connect(self.update_progress)
        self.worker.extraction_done.connect(self.extraction_done)
        self.worker.extraction_write_message.connect(self.write_message)
        self.worker.extraction_failed.connect(self.extraction_failed)


        # Starts worker
        self.worker.start()

    def update_progress(self, progress):
        """Update the progress bar.
        :param progress: how much of the process is complete"""
        self.progress_bar.setValue(progress)

    def extraction_done(self, message):
        """Handle completion of extraction.
        :param message: message to display"""
        self.status_text.setTextColor(QColor("green"))
        self.status_text.append(message)
        self.extract_button.setEnabled(True)  # Re-enable the button
    
    def write_message(self, message):
        """Write message to the screen
        :param message: message to display"""
        self.status_text.setTextColor(QColor("white"))
        self.status_text.append(message)
    
    def extraction_failed(self, message):
        """Writes error message to screen.
        :param message: message to display"""
        self.status_text.setTextColor(QColor("red"))
        self.status_text.append(message)

        

        
