
class SearchAlgorithms():
    def __init__(self):
        self.list_of_algorithms = ["Breadth First Search"]

    # Here you can add more search algorithms

    def get_algorithm(self):
        return self.list_of_algorithms

    def select_algorithm(self, algorithm):
        algorithm_name = algorithm.lower().replace(" ", "_")
        if hasattr(self, algorithm_name):
            return getattr(self, algorithm_name)
        else:
            raise ValueError(f"Algorithm '{algorithm}' is not available.")


    def breadth_first_search(self, maze, width, height):
        # Breadth First Search algorithm
        return