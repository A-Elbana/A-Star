import heapq
from manim import *
import math

def astar(graph, start, goal, heuristic, circles, self):
  """
  Performs A* search to find the shortest path between start and goal.

  Args:
    graph: A dictionary representing the graph, where keys are nodes and values are
           lists of tuples (neighbor, cost).
    start: The starting node.
    goal: The goal node.
    heuristic: A function that estimates the cost from a node to the goal.

  Returns:
    The shortest path as a list of nodes, or None if no path found.
  """

  open_set = []
  heapq.heappush(open_set, (0, start))  # (f_score, node)
  came_from = {}
  g_score = {node: float('inf') for node in graph}
  g_score[start] = 0
  f_score = {node: float('inf') for node in graph}
  f_score[start] = heuristic(start)

  

  while open_set:
      
    current = heapq.heappop(open_set)[1]
    circle = circles[current - 1]
    self.play(circle.animate.set_fill(YELLOW, opacity=0.5),run_time=0.3)
    if current == goal:
      return reconstruct_path(came_from, current)
    

    


    for neighbor, cost in graph[current]:

      tentative_g_score = g_score[current] + cost
      if tentative_g_score < g_score[neighbor]:
        came_from[neighbor] = current
        g_score[neighbor] = tentative_g_score
        f_score[neighbor] = g_score[neighbor] + heuristic(neighbor)
        heapq.heappush(open_set, (f_score[neighbor], neighbor))
        
        
        

def reconstruct_path(came_from, current):

  """
  Reconstructs the path from start to goal.
  """
  total_path = [current]
  while current in came_from:
    current = came_from[current]
    total_path.insert(0, current)
  return total_path







# Changing this heuristic function affects the overall performance of the algorithm and I found Manhattan distance to achieve a better result for the given sample graph so I stuck with it.

def my_heuristic(node):
  
  # return math.sqrt(((nodes[node-1][1] - nodes[11][1])**2) + ((nodes[node-1][2] - nodes[11][2])**2)) # Euclidean Distance

  return abs(nodes[node-1][1] - nodes[11][1]) + abs(nodes[node-1][2] - nodes[11][2]) # Manhattan Distance

start_node = 1  # Starting node
goal_node = 12  # Goal node

# Sample Edges
edges = [(1,2),(2,3),(2,4),(3,5),(3,6),(3,7),(4,5),(5,8),(7,11),(8,9),(9,7),(9,11),(9,10),(10,12),(11,12)
]
# Sample Nodes
nodes = [
  [1, -3, -2],
  [2, -0.94, -1.67],
  [3, 0.16, -0.71],
  [4, -1, -0.13],
  [5, 1.76, -0.13],
  [6, 2, -2],
  [7, 1.26, 1.45],
  [8, 3.38, 1.59],
  [9, 1.32, 3.21],
  [10, -1.18, 2.55],
  [11, -0.58, 1.13],
  [12, -2.12, 1.25]
]

# Adding Costs to edge representation
for i in range(len(edges)):
    edge:tuple = edges[i]
    cost = math.dist(nodes[edge[0] - 1][1:], nodes[edge[1] -1][1:])
    edges[i] = (edge[0],edge[1],cost)


# Building Graph
graph = {node: [] for node in range(1, 13)}
for u, v, w in edges:
  graph[u].append((v,w))
  graph[v].append((u,w))





# To fix a visual glitch with manim
def shorten_line(x1, y1, x2, y2, distance):
  """Shortens a line segment by a given distance.

  Args:
    x1: x-coordinate of the first point.
    y1: y-coordinate of the first point.
    x2: x-coordinate of the second point.
    y2: y-coordinate of the second point.   

    distance: Distance to shorten the line by.

  Returns:
    A tuple containing the new start and end points: ((new_x1, new_y1), (new_x2, new_y2))
  """

  # Calculate the direction vector
  dx = x2 - x1
  dy = y2 - y1

  # Calculate the length of the line
  length = math.sqrt(dx**2 + dy**2)

  # Normalize the direction vector
  if length == 0:
    return ((x1, y1), (x2, y2))  # Handle the case where points are identical
  dx /= length
  dy /= length

  # Calculate the new start and end points
  new_x1 = x1 + distance * dx
  new_y1 = y1 + distance * dy
  new_x2 = x2 - distance * dx
  new_y2 = y2 - distance * dy

  return ((new_x1, new_y1), (new_x2, new_y2))


# This is a mess, I have to admit, but I was a beginner in manim and things get messy with beginners. Forgive my 2024 code and may the next years' code be better. Thanks!
class CreateGraph(Scene):
    def construct(self):
        name = Text("A* Search Algorithm Visualisation", color=WHITE, width=5, height=5)
        name2 = Text("By Abdelrahman Elbana", width=4, height=4).set_color_by_gradient(GREEN,GREEN,DARK_BLUE)
        name.move_to(-4.5*RIGHT+ -0.5 * DOWN)
        name2.move_to(-4.5*RIGHT+ 0 * DOWN)
        self.play(Create(name, run_time=0.3))
        self.play(Create(name2, run_time=0.3))
        circleList = []
        linesList = {}
        lines = []
        for i in range(len(nodes)):
          node = nodes[i]
          size = 0.2
          if i+1 >9:
            size = 0.4
          if i == 0:
            start = Text("Start", color=WHITE, width=1, height=1)
            start.move_to(node[1]*RIGHT - 1.1*RIGHT + node[2]*UP)
            self.play(Create(start, run_time=0.3))
          if i == len(nodes) - 1:
            end = Text("End", color=WHITE, width=1, height=1)
            end.move_to(node[1]*RIGHT + 1.1*LEFT + node[2]*UP)
            self.play(Create(end, run_time=0.3))
          num = Text(str(i + 1), color=WHITE, width=size, height=size)
          circle = Circle(radius=0.4,color=WHITE,arc_center=node[1]*RIGHT + node[2]*UP)
          circle.set_fill(GREEN, opacity=0)
  
          circleList.append(circle)
          num.move_to(node[1]*RIGHT + node[2]*UP)
          self.play(Create(circle, run_time=0.3), Create(num, run_time=0.2))

        for i in range(len(nodes)):
          node = nodes[i]
          for edge in graph[node[0]]:
            p1, p2 = shorten_line(node[1],node[2],nodes[edge[0] - 1][1],nodes[edge[0] - 1][2], 0.4)
            line = Line([p1[0], p1[1], 0.],[p2[0], p2[1], 0.])
            linesList[(node[0],nodes[edge[0] - 1][0])] = line
            lines.append(Create(line))
        self.play(*lines,  run_time=0.5)
        path = astar(graph, start_node, goal_node, my_heuristic, circleList, self)
        for i in range(len(path)):
          node = path[i]
          if node != 12:
            next_node = path[i + 1]
            line = linesList[(node,next_node)]
          
          circle = circleList[node-1]
          self.play(
              circle.animate.set_fill(GREEN, opacity=0.5),run_time=0.3
          )
          if node != 12:
            self.add(line)
            self.play(
                line.animate.set_color(GREEN),run_time=0.3
            )
        self.wait(1)
