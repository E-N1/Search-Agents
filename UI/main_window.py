from PyQt6.QtWidgets import (QMainWindow, QSplitter, QListWidget,
                             QTextEdit, QVBoxLayout, QWidget,
                             QLineEdit, QPushButton, QFormLayout, QGraphicsView, QGraphicsScene)
from PyQt6.QtCore import Qt

from UI.maze_generator import MazeGenerator
from algorithms.search_algorithms import SearchAlgorithms

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.search_algorithms = SearchAlgorithms()

        self.setWindowTitle("Maze Search Algorithms Visualizer")
        self.resize(800, 600)

        # Main splitter to separate sidebar (left) and display area (right)
        main_splitter = QSplitter(Qt.Orientation.Horizontal)

        # Sidebar (left area)
        self.sidebar = QWidget()
        sidebar_layout = QVBoxLayout(self.sidebar)

        # Search algorithm list
        self.algorithm_list = QListWidget()
        self.algorithm_list.addItems(self.search_algorithms.list_of_algorithms)
        self.algorithm_list.currentItemChanged.connect(self.updateDisplayArea)

        sidebar_layout.addWidget(self.algorithm_list)

        # Width and Height input
        form_layout = QFormLayout()
        self.width_input = QLineEdit()
        self.height_input = QLineEdit()
        form_layout.addRow("Width:", self.width_input)
        form_layout.addRow("Height:", self.height_input)
        sidebar_layout.addLayout(form_layout)

        # Generate Maze Button
        self.generate_button = QPushButton("Generate Maze")
        self.generate_button.clicked.connect(self.onGenerateMazeClicked)
        sidebar_layout.addWidget(self.generate_button)

        # Display area (right area)
        self.graphics_view = QGraphicsView()
        self.scene = QGraphicsScene(self)
        self.graphics_view.setScene(self.scene)

        # Adding the widgets to the splitter
        main_splitter.addWidget(self.sidebar)
        main_splitter.addWidget(self.graphics_view)
        main_splitter.setStretchFactor(1, 1)

        # Main widget and layout
        main_widget = QWidget()
        main_layout = QVBoxLayout(main_widget)
        main_layout.addWidget(main_splitter)

        self.setCentralWidget(main_widget)

        # Initialize MazeGenerator with graphics_view and scene
        self.maze_generator = MazeGenerator(self.graphics_view, self.scene)

    def onGenerateMazeClicked(self):
        width = self.width_input.text()
        height = self.height_input.text()
        self.maze_generator.onGenerateMazeClicked(width, height)

    def updateDisplayArea(self):
        current_item = self.algorithm_list.currentItem()
        if current_item:
            algorithm_name = current_item.text()
            visual_text = self.search_algorithms.select_algorithm(algorithm_name)
        else:
            visual_text = "Unknown Algorithm"