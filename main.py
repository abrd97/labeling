import sys
import os
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QPushButton, QLineEdit, QHBoxLayout, QFileDialog, QTextEdit, QListWidget, QScrollArea
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt

class GlassLabelingApp(QWidget):
    def __init__(self):
        super().__init__()
        self.image_list = []
        self.processed_images = []
        self.current_index = 0
        self.txt_folder = ""
        self.remaining_files = 0
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Glass Image Labeling')
        layout = QVBoxLayout()

        self.path_input = QLineEdit(self)
        self.path_input.setPlaceholderText('Enter PNG image folder or click "Browse"')
        layout.addWidget(self.path_input)

        browse_button = QPushButton('Browse Images', self)
        browse_button.clicked.connect(self.browse_image_folder)
        layout.addWidget(browse_button)

        self.txt_folder_input = QLineEdit(self)
        self.txt_folder_input.setPlaceholderText('Enter folder to store TXT files or click "Browse"')
        layout.addWidget(self.txt_folder_input)

        browse_txt_button = QPushButton('Browse TXT Folder', self)
        browse_txt_button.clicked.connect(self.browse_txt_folder)
        layout.addWidget(browse_txt_button)

        self.image_name_label = QLabel(self)
        layout.addWidget(self.image_name_label)

        self.image_label = QLabel(self)
        self.image_label.setFixedSize(400, 400)
        layout.addWidget(self.image_label)

        self.txt_list_widget = QListWidget(self)
        layout.addWidget(self.txt_list_widget)

        buttons_layout = QHBoxLayout()
        
        glass_button = QPushButton('Is Glass (j)', self)
        glass_button.clicked.connect(lambda: self.label_image(1))
        buttons_layout.addWidget(glass_button)

        not_glass_button = QPushButton('Is Not Glass (l)', self)
        not_glass_button.clicked.connect(lambda: self.label_image(0))
        buttons_layout.addWidget(not_glass_button)

        layout.addLayout(buttons_layout)

        self.remaining_files_label = QLabel(self)
        layout.addWidget(self.remaining_files_label)

        self.setLayout(layout)
        self.setGeometry(300, 300, 500, 700)

        self.setFocusPolicy(Qt.StrongFocus)

    def browse_image_folder(self):
        folder_name = QFileDialog.getExistingDirectory(self, "Select Image Folder")
        if folder_name:
            self.path_input.setText(folder_name)
            self.load_image_list(folder_name)

    def browse_txt_folder(self):
        folder_name = QFileDialog.getExistingDirectory(self, "Select TXT Folder")
        if folder_name:
            self.txt_folder_input.setText(folder_name)
            self.txt_folder = folder_name
            self.process_files()

    def load_image_list(self, folder):
        self.image_list = [f for f in os.listdir(folder) if f.endswith('.png')]
        self.image_list.sort()  # Sort to keep consistent ordering
        self.current_index = 0

    def process_files(self):
        filtered_image_list = []
        self.processed_images = []

        for image_file in self.image_list:
            base_name = os.path.splitext(image_file)[0]
            text_file_path = os.path.join(self.txt_folder, f"{base_name}.txt")
            
            if not os.path.exists(text_file_path) or os.path.getsize(text_file_path) == 0:
                filtered_image_list.append(image_file)
            else:
                self.processed_images.append(f"{image_file} - Labeled")
                self.txt_list_widget.addItem(f"{image_file} - Already labeled")

        self.image_list = filtered_image_list
        self.remaining_files = len(self.image_list)

        if self.image_list:
            image_folder = self.path_input.text()
            self.display_image(os.path.join(image_folder, self.image_list[self.current_index]))

        self.update_remaining_files_label()

    def display_image(self, file_path):
        pixmap = QPixmap(file_path)
        pixmap = pixmap.scaled(self.image_label.width(), self.image_label.height())
        self.image_label.setPixmap(pixmap)

        image_name = os.path.basename(file_path)
        self.image_name_label.setText(f"Image: {image_name}")

    def label_image(self, label):
        image_folder = self.path_input.text()
        if not os.path.isdir(image_folder) or not self.image_list:
            print("Invalid image folder or no images found")
            return

        image_file = self.image_list[self.current_index]
        image_path = os.path.join(image_folder, image_file)

        if not os.path.isdir(self.txt_folder):
            print("Invalid TXT folder")
            return

        base_name = os.path.splitext(image_file)[0]
        text_file_path = os.path.join(self.txt_folder, f"{base_name}.txt")

        with open(text_file_path, 'w') as file:
            file.write(f"{label}")

        print(f"Labeled {image_file} as {'Glass' if label == 1 else 'Not Glass'}")

        self.processed_images.append(f"{image_file} - Labeled as {'Glass' if label == 1 else 'Not Glass'}")
        self.txt_list_widget.addItem(f"{image_file} - Labeled as {'Glass' if label == 1 else 'Not Glass'}")

        self.next_image()

    def next_image(self):
        self.current_index += 1
        self.remaining_files -= 1

        if self.current_index < len(self.image_list):
            image_folder = self.path_input.text()
            next_image_path = os.path.join(image_folder, self.image_list[self.current_index])
            self.display_image(next_image_path)
        else:
            self.image_label.clear()
            self.image_name_label.setText("No more images to label")

        self.update_remaining_files_label()

    def update_remaining_files_label(self):
        self.remaining_files_label.setText(f"Files remaining: {self.remaining_files}")

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_J:
            self.label_image(1)  # Label as "Is Glass"
        elif event.key() == Qt.Key_L:
            self.label_image(0)  # Label as "Is Not Glass"

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = GlassLabelingApp()
    ex.show()
    sys.exit(app.exec_())
