import sys
import os
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QPushButton, QLineEdit, QHBoxLayout, QFileDialog
from PyQt5.QtGui import QPixmap

class GlassLabelingApp(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        # Set window title and layout
        self.setWindowTitle('Glass Image Labeling')
        layout = QVBoxLayout()

        # Create input field for image path
        self.path_input = QLineEdit(self)
        self.path_input.setPlaceholderText('Enter PNG image path or click "Browse"')
        layout.addWidget(self.path_input)

        # Browse button to select PNG file
        browse_button = QPushButton('Browse', self)
        browse_button.clicked.connect(self.browse_image)
        layout.addWidget(browse_button)

        # Label to display the image
        self.image_label = QLabel(self)
        self.image_label.setFixedSize(400, 400)
        layout.addWidget(self.image_label)

        # Buttons for labeling as "Glass" or "Not Glass"
        buttons_layout = QHBoxLayout()
        
        glass_button = QPushButton('Is Glass', self)
        glass_button.clicked.connect(lambda: self.label_image(1))
        buttons_layout.addWidget(glass_button)

        not_glass_button = QPushButton('Is Not Glass', self)
        not_glass_button.clicked.connect(lambda: self.label_image(0))
        buttons_layout.addWidget(not_glass_button)

        layout.addLayout(buttons_layout)

        # Set the layout to the window
        self.setLayout(layout)
        self.setGeometry(300, 300, 500, 500)

    def browse_image(self):
        # Open file dialog to select an image file
        file_name, _ = QFileDialog.getOpenFileName(self, "Select PNG Image", "", "PNG Files (*.png)")
        if file_name:
            self.path_input.setText(file_name)
            self.display_image(file_name)

    def display_image(self, file_path):
        # Load and display the image in the label
        pixmap = QPixmap(file_path)
        pixmap = pixmap.scaled(self.image_label.width(), self.image_label.height())
        self.image_label.setPixmap(pixmap)

    def label_image(self, label):
        # Get the image file path from input
        image_path = self.path_input.text()
        if not os.path.isfile(image_path):
            print("Invalid file path")
            return

        # Extract the base name of the image and create a text file with the same name
        base_name = os.path.splitext(image_path)[0]
        text_file_path = f"{base_name}.txt"

        # Write the label (1 or 0) to the text file
        with open(text_file_path, 'w') as file:
            file.write(f"{label}")

        print(f"Labeled {image_path} as {'Glass' if label == 1 else 'Not Glass'}")

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = GlassLabelingApp()
    ex.show()
    sys.exit(app.exec_())
