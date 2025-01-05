import os
import tarfile
import zipfile

import py7zr
from PySide6.QtCore import QThread, Signal


class FileExtractorFunctionality(QThread):
    progress_updated = Signal(int)
    extraction_done = Signal(str)
    extraction_failed = Signal(str)
    extraction_write_message = Signal(str)

    accepted_extensions = ['.zip', '.7z', '.rar', '.tar', '.tar.gz', '.tar.bz2', '.gz', '.xz']

    def __init__(self, source_folder, destination_folder):
        super().__init__()
        self.source_folder = source_folder
        self.destination_folder = destination_folder

    def run(self):
        extracted_count = 0
        total_files = len(
            [f for f in os.listdir(self.source_folder) if any(f.endswith(ext) for ext in self.accepted_extensions)])

        for filename in os.listdir(self.source_folder):
            if any(filename.endswith(ext) for ext in self.accepted_extensions):
                file_path = os.path.join(self.source_folder, filename)
                folder_name = os.path.splitext(filename)[0]
                extract_folder = os.path.join(self.destination_folder, folder_name)
                os.makedirs(extract_folder, exist_ok=True)

                try:
                    self.extract_file(file_path, extract_folder)
                    extracted_count += 1
                    progress = int((extracted_count / total_files) * 100)
                    self.progress_updated.emit(progress)

                except Exception as e:
                    self.extraction_failed.emit(f"Failed to extract {filename}: {str(e)}")

        self.extraction_done.emit("Extraction Complete!")

    def extract_file(self, file_path, dest_folder):
        """A function to swap extraction method depending on the file extension
        :param file_path: The path to the folder containing the files to be extracted
        :param dest_folder: The folder where it should be extracted to
        :raises ValueError: If the file extension is not one of the accepted extensions
        :raises Exception: If there is an error during extraction
        """
        _, ext = os.path.splitext(file_path)

        try:
            match ext:
                case '.zip':
                    self.extract_zip(file_path, dest_folder)
                case '.7z':
                    self.extract_7z(file_path, dest_folder)
                case '.rar':
                    # TODO: is there a good way to do this without downloading dlls
                    raise NotImplementedError("Rar support is not yet implemented.")
                    # self.extract_rar(file_path, dest_folder)
                case '.tar' | '.tar.gz' | '.tar.bz2' | '.gz' | '.xz':
                    self.extract_tar(file_path, dest_folder)
                case _:
                    raise ValueError(f"Unsupported file type: {ext}")

        except Exception as e:
            print(f"Error extracting {file_path}: {e}")
            self.extraction_failed.emit(f"Error extracting {file_path}: {e}")

    def extract_zip(self, file_path, dest_folder):
        """Extracts files with the .zip extension
       :param file_path: The path to the folder containing the file to be extracted
       :param dest_folder: The folder where it should be extracted to
       :raises Exception: If there is an error during extraction"""
        try:
            with zipfile.ZipFile(file_path, 'r') as zip_ref:
                print(f"Extracting ZIP file from: {file_path}")
                self.extraction_write_message.emit(f"Extracting ZIP file from: {file_path}")
                zip_ref.extractall(dest_folder)
                self.extraction_write_message.emit(f"Extraction complete to {dest_folder}")
                print(f"Extraction complete to {dest_folder}")
        except Exception as e:
            print(f"Error extracting ZIP file: {e}")
            self.extraction_failed.emit(f"Error extracting ZIP file: {e}")

    def extract_7z(self, file_path, dest_folder):
        """Extracts files with the .7z extension
        :param file_path: The path to the folder containing the file to be extracted
        :param dest_folder: The folder where it should be extracted to
        :raises Exception: If there is an error during extraction"""
        try:
            with py7zr.SevenZipFile(file_path, mode='r') as archive:
                print(f"Extracting 7z file from: {file_path}")
                self.extraction_write_message.emit(f"Extracting 7z file from: {file_path}")
                archive.extractall(path=dest_folder)
                print(f"Extraction complete to {dest_folder}")
                self.extraction_write_message.emit(f"Extraction complete to {dest_folder}")
        except Exception as e:
            print(f"Error extracting 7z file: {e}")
            self.extraction_failed.emit(f"Error extracting 7z file: {e}")

    def extract_rar(self, file_path, dest_folder):
        """Extracts files with the .rar extension
        :param file_path: The path to the folder containing the file to be extracted
        :param dest_folder: The folder where it should be extracted to
        :raises Exception: If there is an error during extraction"""
        try:
            import libarchive.extract  # Import here to delay until needed

            print(f"Extracting RAR file from: {file_path}")
            self.extraction_write_message.emit(f"Extracting RAR file from: {file_path}")

            with libarchive.extract.open_archive(file_path) as archive:
                archive.extract(dest_folder)
                print(f"Extraction complete to {dest_folder}")
                self.extraction_write_message.emit(f"Extraction complete to {dest_folder}")

        except Exception as e:
            print(f"Error extracting RAR file: {e}")
            self.extraction_failed.emit(f"Error extracting RAR file: {e}")

    def extract_tar(self, file_path, dest_folder):
        """Extracts files with the .tar extension
       :param file_path: The path to the folder containing the file to be extracted
       :param dest_folder: The folder where it should be extracted to
       :raises Exception: If there is an error during extraction"""
        try:
            with tarfile.open(file_path, "r:*") as tar_ref:
                print(f"Extracting TAR file from: {file_path}")
                self.extraction_write_message.emit(f"Extracting TAR file from: {file_path}")
                tar_ref.extractall(dest_folder)
                print(f"Extraction complete to {dest_folder}")
                self.extraction_write_message.emit(f"Extraction complete to {dest_folder}")
        except Exception as e:
            print(f"Error extracting TAR file: {e}")
            self.extraction_failed.emit(f"Error extracting TAR file: {e}")
