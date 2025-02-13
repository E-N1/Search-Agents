import sys
import random
from PyQt6.QtWidgets import (QApplication, QWidget, QVBoxLayout,
                             QLabel, QLineEdit, QPushButton,
                             QMessageBox, QComboBox)
from PyQt6.QtCore import QRectF, QTimer
from PyQt6.QtGui import QBrush, QColor

from algorithms.search_algorithms import SearchAlgorithms

class MazeGenerator(QWidget):
    CELL_SIZE = 20

    def __init__(self, graphics_view, scene):
        super().__init__()
        self.width_input = QLineEdit()
        self.height_input = QLineEdit()
        self.graphics_view = graphics_view
        self.scene = scene
        self.solution_path = []
        self.current_step = 0
        
        self.algorithms = SearchAlgorithms()
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()
        layout.addWidget(QLabel('Width:'))
        layout.addWidget(self.width_input)
        layout.addWidget(QLabel('Height:'))
        layout.addWidget(self.height_input)

        self.algorithm_selector = QComboBox()
        self.load_algorithms()
        layout.addWidget(self.algorithm_selector)

        generate_button = QPushButton('Generate Maze')
        generate_button.clicked.connect(self.onGenerateMazeClicked)
        layout.addWidget(generate_button)

        self.setLayout(layout)
        self.setWindowTitle('Maze Generator')

    def load_algorithms(self):
        for algorithm in self.algorithms.get_algorithm():
            self.algorithm_selector.addItem(algorithm)

    def onGenerateMazeClicked(self, width, height):
        search_algorithm_name = self.algorithm_selector.currentText()
        search_algorithm = self.algorithms.select_algorithm(search_algorithm_name)
        self.generateMaze(width, height, search_algorithm)

    def generateMaze(self, width, height, search_algorithm):
        try:
            width = int(width)
            height = int(height)
            if width <= 0 or height <= 0:
                raise ValueError("Dimensions must be positive integers.")
            
            maze = self.createMaze(width, height)
            self.solution_path = search_algorithm(maze, width, height)
            self.drawMaze(maze)
            self.current_step = 0
            self.animateSolutionPath()
        except ValueError:
            QMessageBox.warning(self, "Error", "Please enter valid positive integers for width and height.")

    def createMaze(self, width, height):
        maze = [[0] * width for _ in range(height)]

        def carve_path(x, y):
            directions = [(1, 0), (-1, 0), (0, 1), (0, -1)]
            random.shuffle(directions)

            for dx, dy in directions:
                nx, ny = x + dx, y + dy
                if 0 <= nx < width and 0 <= ny < height and maze[ny][nx] == 0:
                    if self.count_neighbours(maze, nx, ny) == 1:
                        maze[ny][nx] = 1
                        carve_path(nx, ny)

        maze[0][0] = 1
        carve_path(0, 0)

        return maze

    def count_neighbours(self, maze, x, y):
        count = 0
        directions = [(1, 0), (-1, 0), (0, 1), (0, -1)]
        for dx, dy in directions:
            nx, ny = x + dx, y + dy
            if 0 <= nx < len(maze[0]) and 0 <= ny < len(maze) and maze[ny][nx] == 1:
                count += 1
        return count

    def drawMaze(self, maze):
        self.scene.clear()
        for y, row in enumerate(maze):
            for x, cell in enumerate(row):
                if (x, y) == (0, 0):
                    brush_color = "red"
                elif (x, y) == (len(maze[0]) - 1, len(maze) - 1):
                    brush_color = "white"
                else:
                    brush_color = "white" if cell == 1 else "black"
                self.drawCell(x, y, self.CELL_SIZE, QColor(brush_color))

    def drawCell(self, x, y, size, color):
        rect = QRectF(x * size, y * size, size, size)
        brush = QBrush(color)
        self.scene.addRect(rect, brush=brush)

    def animateSolutionPath(self):
        if self.current_step < len(self.solution_path):
            x, y = self.solution_path[self.current_step]
            if (x, y) != (0, 0):  # Skip the start point
                self.drawCell(x, y, self.CELL_SIZE, QColor("red"))
            self.current_step += 1
            QTimer.singleShot(100, self.animateSolutionPath)
