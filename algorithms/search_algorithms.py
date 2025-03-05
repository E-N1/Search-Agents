
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
        from collections import deque
        queue = deque([(0, 0)])
        visited = [[False] * width for _ in range(height)]
        visited[0][0] = True
        parent = { (0, 0): None }

        while queue:
            x, y = queue.popleft()
            if (x, y) == (width - 1, height - 1):
                break

            directions = [(1, 0), (0, 1), (-1, 0), (0, -1)]
            for dx, dy in directions:
                nx, ny = x + dx, y + dy
                if 0 <= nx < width and 0 <= ny < height and not visited[ny][nx] and maze[ny][nx] == 1:
                    queue.append((nx, ny))
                    visited[ny][nx] = True
                    parent[(nx, ny)] = (x, y)

        path = []
        step = (width - 1, height - 1)
        while step:
            path.append(step)
            step = parent[step]
        path.reverse()
        return path