import sys
import os
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QPushButton, QLineEdit, QHBoxLayout, QFileDialog, QListWidget
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt

class GlassLabelingApp(QWidget):
    def __init__(self):
        super().__init__()
        self.image_list = []
        self.processed_images = []
        self.labeled_as_glass = []
        self.labeled_as_not_glass = []
        self.current_index = 0
        self.txt_folder = ""
        self.remaining_files = 0
        self.initUI()

    def initUI(self):
        # Set window title and layout
        self.setWindowTitle('Glass Image Labeling')
        layout = QVBoxLayout()

        # Create input field for image folder
        self.path_input = QLineEdit(self)
        self.path_input.setPlaceholderText('Enter PNG image folder or click "Browse"')
        layout.addWidget(self.path_input)

        # Browse button to select image folder
        browse_button = QPushButton('Browse Images', self)
        browse_button.clicked.connect(self.browse_image_folder)
        layout.addWidget(browse_button)

        # Create input field for text folder path
        self.txt_folder_input = QLineEdit(self)
        self.txt_folder_input.setPlaceholderText('Enter folder to store TXT files or click "Browse"')
        layout.addWidget(self.txt_folder_input)

        # Browse button to select folder for text files
        browse_txt_button = QPushButton('Browse TXT Folder', self)
        browse_txt_button.clicked.connect(self.browse_txt_folder)
        layout.addWidget(browse_txt_button)

        # Label to show the image file name
        self.image_name_label = QLabel(self)
        layout.addWidget(self.image_name_label)

        # Label to display the image
        self.image_label = QLabel(self)
        self.image_label.setFixedSize(400, 400)
        layout.addWidget(self.image_label)

        # List widget for displaying processed files
        self.txt_list_widget = QListWidget(self)
        layout.addWidget(self.txt_list_widget)

        # Count labels for glass and not glass files
        self.glass_count_label = QLabel('Labeled as Glass: 0', self)
        layout.addWidget(self.glass_count_label)

        self.not_glass_count_label = QLabel('Labeled as Not Glass: 0', self)
        layout.addWidget(self.not_glass_count_label)

        # Buttons for labeling as "Glass" or "Not Glass"
        buttons_layout = QHBoxLayout()
        
        glass_button = QPushButton('Is Glass (j)', self)
        glass_button.clicked.connect(lambda: self.label_image(1))
        buttons_layout.addWidget(glass_button)

        not_glass_button = QPushButton('Is Not Glass (l)', self)
        not_glass_button.clicked.connect(lambda: self.label_image(0))
        buttons_layout.addWidget(not_glass_button)

        layout.addLayout(buttons_layout)

        # Label to show the remaining files to be processed
        self.remaining_files_label = QLabel(self)
        layout.addWidget(self.remaining_files_label)

        # Set the layout to the window
        self.setLayout(layout)
        self.setGeometry(300, 300, 500, 800)

        # Enable keyboard shortcuts
        self.setFocusPolicy(Qt.StrongFocus)

    def browse_image_folder(self):
        # Open file dialog to select an image folder
        folder_name = QFileDialog.getExistingDirectory(self, "Select Image Folder")
        if folder_name:
            self.path_input.setText(folder_name)
            self.load_image_list(folder_name)

    def browse_txt_folder(self):
        # Open file dialog to select folder for text files
        folder_name = QFileDialog.getExistingDirectory(self, "Select TXT Folder")
        if folder_name:
            self.txt_folder_input.setText(folder_name)
            self.txt_folder = folder_name
            self.process_files()

    def load_image_list(self, folder):
        # Get the list of PNG files in the folder
        self.image_list = [f for f in os.listdir(folder) if f.endswith('.png')]
        self.image_list.sort()  # Sort to keep consistent ordering
        self.current_index = 0

    def process_files(self):
        # Filter image files to exclude those that already have non-empty text files
        filtered_image_list = []
        self.processed_images = []

        for image_file in self.image_list:
            base_name = os.path.splitext(image_file)[0]
            text_file_path = os.path.join(self.txt_folder, f"{base_name}.txt")
            
            if not os.path.exists(text_file_path) or os.path.getsize(text_file_path) == 0:
                filtered_image_list.append(image_file)
            else:
                # Read the content to check how it was labeled
                with open(text_file_path, 'r') as file:
                    content = file.read().strip()
                    if content == '1':
                        self.labeled_as_glass.append(image_file)
                    elif content == '0':
                        self.labeled_as_not_glass.append(image_file)

        self.image_list = filtered_image_list
        self.remaining_files = len(self.image_list)

        if self.image_list:
            image_folder = self.path_input.text()
            self.display_image(os.path.join(image_folder, self.image_list[self.current_index]))

        # Update labels
        self.update_count_labels()
        self.update_remaining_files_label()

    def display_image(self, file_path):
        # Load and display the image in the label
        pixmap = QPixmap(file_path)
        pixmap = pixmap.scaled(self.image_label.width(), self.image_label.height())
        self.image_label.setPixmap(pixmap)

        # Show the image name
        image_name = os.path.basename(file_path)
        self.image_name_label.setText(f"Image: {image_name}")

    def label_image(self, label):
        # Get the image folder path
        image_folder = self.path_input.text()
        if not os.path.isdir(image_folder) or not self.image_list:
            print("Invalid image folder or no images found")
            return

        # Get the current image path
        image_file = self.image_list[self.current_index]
        image_path = os.path.join(image_folder, image_file)

        # Ensure the txt folder is set
        if not os.path.isdir(self.txt_folder):
            print("Invalid TXT folder")
            return

        # Extract the base name of the image and create a text file in the specified folder
        base_name = os.path.splitext(image_file)[0]
        text_file_path = os.path.join(self.txt_folder, f"{base_name}.txt")

        # Write the label (1 or 0) to the text file
        with open(text_file_path, 'w') as file:
            file.write(f"{label}")

        print(f"Labeled {image_file} as {'Glass' if label == 1 else 'Not Glass'}")

        # Add to the appropriate list and update display
        if label == 1:
            self.labeled_as_glass.append(image_file)
        else:
            self.labeled_as_not_glass.append(image_file)

        self.txt_list_widget.addItem(f"{image_file} - Labeled as {'Glass' if label == 1 else 'Not Glass'}")

        # Update count labels
        self.update_count_labels()

        # Move to the next image
        self.next_image()

    def next_image(self):
        # Move to the next image in the list
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

    def update_count_labels(self):
        # Update the labels showing the counts for glass and not glass files
        self.glass_count_label.setText(f"Labeled as Glass: {len(self.labeled_as_glass)}")
        self.not_glass_count_label.setText(f"Labeled as Not Glass: {len(self.labeled_as_not_glass)}")

    def update_remaining_files_label(self):
        # Update the label showing the number of remaining files
        self.remaining_files_label.setText(f"Files remaining: {self.remaining_files}")

    def keyPressEvent(self, event):
        # Handle key press events for 'j' and 'l' keys
        if event.key() == Qt.Key_J:
            self.label_image(1)  # Label as "Is Glass"
        elif event.key() == Qt.Key_L:
            self.label_image(0)  # Label as "Is Not Glass"

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = GlassLabelingApp()
    ex.show()
    sys.exit(app.exec_())
