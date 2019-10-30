import pygame
from pygame.locals import *
import os, sys
from math import sqrt
import heapq

#NEW AND IMPROVED!
#v9_9_6:
 #https://www.youtube.com/watch?v=_904EvOUQ_M&feature=youtu.be&t=8
 #The issues regarding the placement of the starting-node, and the inability to properly progress from start to
#finish, as opposed to the opposite have been resolved. The program functions nominally.

#left-mouse button will generate a start-node if the location is valid (not within an obstacle)
#right-mouse button will generate a goal-node if the location is valid
#centre-mouse button will remove an obstacle if the click is over an obstacle, or it will create a new obstacle
#if it is dragged from one position to another on-screen
#the space-bar will generate/remove the node-field
#shift-bar + space will remove the start and end nodes if they exist, removing the path if it exists as well.

vec = pygame.math.Vector2

WINDOWWIDTH = 1080
WINDOWHEIGHT = 640

FPS = 60

#R G B
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
BLUE = (0, 0, 155)
BRIGHTBLUE = (0, 0, 255)
RED = (155, 0, 0)
BRIGHTRED = (255, 0, 0)
GREEN = (0, 155, 0)
BRIGHTGREEN = (0, 255, 0)
NINETYFOURGREY = (148, 148, 148)
FORTYFOURGREY = (68, 68, 68)
BEIGE = (255, 255, 200)
VIOLET = (185, 132, 255)
BUBBLEGUM = (255, 0, 255)
CYAN = (0, 255, 255)

BGCOLOR = WHITE
CONNECTION_COLOR = (180, 255, 180)
BAD_CONNECTION_COLOR = RED

CURRENT_TIME = 0

class Node():
    def __init__(self, x_pos, y_pos, node_distance):
        self.x_pos = x_pos
        self.y_pos = y_pos
        self.center = (self.x_pos, self.y_pos)
        self.node_distance = node_distance
        self.connections = {'N': [False, None, 0], 'NE': [False, None, 0], 'E': [False, None, 0], 'SE': [False, None, 0], 'S': [False, None, 0], 'SW': [False, None, 0], 'W': [False, None, 0], 'NW': [False, None, 0]}
        self.connections_keys = []
        self.valid_node = True
        self.node_rect = None
        self.create_collision_rect()
        self.valid_connections = []
        self.connection_costs = {}
        self.connection_positions = []
        self.connection_dict = {}
        self.bad_neighbors = {}
        self.not_checked = True


    def locate_neighbors(self, obstacles, tested_nodes):
        node_distance = self.node_distance
        neighbors = [(self.center[0], self.center[1] - node_distance), (self.center[0] + int(node_distance / 2), self.center[1] - int(node_distance / 2)),
                     (self.center[0] + node_distance, self.center[1]), (self.center[0] + int(node_distance / 2), self.center[1] + int(node_distance / 2)),
                     (self.center[0], self.center[1] + node_distance), (self.center[0] - int(node_distance / 2), self.center[1] + int(node_distance / 2)),
                     (self.center[0] - node_distance, self.center[1]), (self.center[0] - int(node_distance / 2), self.center[1] - int(node_distance / 2))]


        connections_keys = [x for x in self.connections.keys()]
        self.connections_keys = connections_keys
                                    
        for x in range(len(connections_keys)):
            self.connections[connections_keys[x]][1] = neighbors[x]
            self.connection_positions.append(neighbors[x])

        self.bad_neighbors = {neighbors_x: False for neighbors_x in neighbors}

        new_nodes = []

        for key_x in self.connections:
            string_nodes = None
            neighbor_node_pos = self.connections[key_x][1]
            string_nodes_a = '{}{}'.format(str(self.center), str(self.connections[key_x][1]))
            string_nodes_b = '{}{}'.format(str(self.connections[key_x][1]), str(self.center))
            
            if string_nodes_a in tested_nodes:
                string_nodes = string_nodes_a
                self.connections[key_x][0] = tested_nodes[string_nodes][0]
                self.connections[key_x][2] = tested_nodes[string_nodes][2]
                self.connection_costs[self.connections[key_x][1]] = tested_nodes[string_nodes][2]
            elif string_nodes_b in tested_nodes:
                string_nodes = string_nodes_b
                self.connections[key_x][0] = tested_nodes[string_nodes][0]
                self.connections[key_x][0] = tested_nodes[string_nodes][2]
                self.connection_costs[self.connections[key_x][1]] = tested_nodes[string_nodes][2]
            else:
                string_nodes = string_nodes_a
                if key_x in ['N', 'E', 'S', 'W']:
                    sight_range = node_distance
                    cost = 2
                else:
                    sight_range = int(node_distance / 2)
                    cost = 1
                self.connection_costs[self.connections[key_x][1]] = cost

                in_bounds = True
                if neighbor_node_pos[0] < 1 or neighbor_node_pos[0] >= WINDOWWIDTH or neighbor_node_pos[1] < 1 or neighbor_node_pos[1] >= WINDOWHEIGHT:
                    in_bounds = False
                if in_bounds == True:
                    check_collision = self.line_of_sight(self.connections[key_x][1], sight_range, obstacles)
                    self.connections[key_x][0] = check_collision
                else:
                    check_collision = in_bounds

                nodes_compared = '{}{}'.format(str(self.center), str(self.connections[key_x][1]))
                node_a = self.center
                node_b = self.connections[key_x][1]
                
                new_nodes.append({'nodes': nodes_compared, 'viable': check_collision, 'node_points': [node_a, node_b], 'cost': cost})
        return new_nodes


    def validate_connection(self, node_pos):
        return self.connection_dict[node_pos]
        

    def line_of_sight(self, target_center, sight_range, obstacles):
        sight = True
        node_distance = self.node_distance
        
        sight_line = get_line(self.center, target_center)
        zone = pygame.Rect(self.center[0] - node_distance, self.center[1] - node_distance, self.node_distance * 2, self.node_distance * 2)
        obstacles_list = obstacles #[x.rect for x in obstacles]

        obstacles_in_sight = zone.collidelistall(obstacles_list)
        for x in range(1, len(sight_line), 5):
            for obs_index in obstacles_in_sight:
                if obstacles_list[obs_index].collidepoint(sight_line[x]):
                    sight = False
                    return False

        return True


    def create_connection_dict(self):
        for connection_x in self.connections:
            self.connection_dict[self.connections[connection_x][1]] = self.connections[connection_x][0]


    def check_validity(self, obstacle_rects):
        invalid_connections = 0
        self.check_node_collision(obstacle_rects)
        if self.valid_node == True:
            for x in range(len(self.connections_keys)):
                if self.connections[self.connections_keys[x]][0] == False:
                    invalid_connections += 1
                if invalid_connections >= 3:
                    self.valid_node = False


    def check_connection_validity(self):
        pass

    


    def create_collision_rect(self):
        self.node_rect = pygame.Rect(self.center[0] - int(self.node_distance / 2), self.center[1] - int(self.node_distance / 2), int(self.node_distance), int(self.node_distance))


    def check_node_collision(self, obstacle_rects):
        if self.node_rect == None:
            self.create_collision_rect()
        for x in range(len(obstacle_rects)):
            if self.node_rect.colliderect(obstacle_rects[x]) == True:
                self.valid_node = False
                return False
        return True

    def check_neighbor_collision(self, obstacle_rects):
        for x in range(len(self.connection_positions)):
            neighbor_node = self.connection_positions[x]

            if neighbor_node[0] < 0 or neighbor_node[0] > WINDOWWIDTH or neighbor_node[1] < 0 or neighbor_node[1] > WINDOWHEIGHT:
                self.bad_neighbors[neighbor_node] = True
            else:
                neighbor_rect = pygame.Rect(neighbor_node[0] - int(self.node_distance / 2), neighbor_node[1] - int(self.node_distance / 2), int(self.node_distance), int(self.node_distance))
                for i in range(len(obstacle_rects)):
                    if neighbor_rect.colliderect(obstacle_rects[i]) == True:
                        self.bad_neighbors[neighbor_node] = True


    def validate_neighbor_collision(self, neighbor_node):
        if self.bad_neighbors[neighbor_node] == False:
            return True
        else:
            return False


    def check_if_not_previously_checked(self):
        if self.not_checked == True:
            return True
        else:
            return False
        

    def draw_self(self, DISPSURF, color=(0, 0, 255)):
        pygame.draw.circle(DISPSURF, color, (self.x_pos, self.y_pos), 3, 0)


class SpecialNode(Node):
    def __init__(self, color, x_pos, y_pos, node_distance):

        super().__init__(x_pos, y_pos, node_distance)
        self.connections = {}
        self.create_collision_rect()
        self.closest_node = None
        self.color = color



    def locate_neighbors(self, graph, obstacle_rects):
        list_of_nodes = graph.nodes_list_omni
        searching_complete = False
        while searching_complete == False:
            for x in range(len(list_of_nodes)):
                if self.node_rect.collidepoint(list_of_nodes[x].center) == True:
                    valid_position = list_of_nodes[x].check_node_collision(obstacle_rects)
                    if valid_position == True:
                        distance = self.distance_to_node(list_of_nodes[x].center)
                        self.connections[str(list_of_nodes[x].center)] = [False, list_of_nodes[x].center, distance]
                        self.connections_keys.append(str(list_of_nodes[x].center))
            if len(self.connections) > 0:
                searching_complete = True
            else:
                self.node_distance = self.node_distance * 2
                self.create_collision_rect()



    def distance_to_node(self, target_node):
        x_distance = abs(self.center[0] - target_node[0])
        y_distance = abs(self.center[1] - target_node[1])
        pyth_dist = x_distance**2 + y_distance**2
        pyth_dist = int(sqrt(pyth_dist))

        return pyth_dist


    def evaluate_connections(self, obstacles):

        for x in range(len(self.connections_keys)):
            sight_range = self.connections[self.connections_keys[x]][2]
            target_center = self.connections[self.connections_keys[x]][1]
            check_validity = self.line_of_sight(target_center, sight_range, obstacles)
            self.connections[self.connections_keys[x]][0] = check_validity
            if check_validity == True:
                if self.closest_node == None or self.connections[self.connections_keys[x]][2] < self.closest_node['distance']:
                    self.closest_node = {'node': self.connections[self.connections_keys[x]][1], 'distance': self.connections[self.connections_keys[x]][2]}

    def draw_self(self, DISPSURF):
        pygame.draw.circle(DISPSURF, self.color, self.center, 3, 0)


    def draw_connection(self, DISPSURF):
        pygame.draw.aaline(DISPSURF, self.color, self.center, self.closest_node['node'], True)


class OmniNodes():
    def __init__(self, nodes_list_omni):
        self.nodes_list_omni = nodes_list_omni
        self.tested_connections = {}
        self.bad_nodes = []
        self.valid_nodes = []
        self.culled_nodes = {}
        self.culled_nodes_positions = []
        self.visited_nodes = []


    def locate_node_neighbors(self, target_node, obstacle_rects):
        newly_tested = target_node.locate_neighbors(obstacle_rects, self.tested_connections)
        for i in range(len(newly_tested)):
            self.tested_connections[newly_tested[i]['nodes']] = [newly_tested[i]['viable'], newly_tested[i]['node_points'], newly_tested[i]['cost']]
        return target_node
        

    def find_neighbors(self, target_node, obstacle_rects):
        self.locate_node_neighbors(target_node, obstacle_rects)
        target_node.create_connection_dict()
        neighbors = filter(target_node.validate_connection, target_node.connection_positions)
        target_node.check_neighbor_collision(obstacle_rects)
        neighbors = filter(target_node.validate_neighbor_collision, neighbors)
        neighbors = filter(self.check_if_culled, neighbors)        
        
        return neighbors


    def get_cost(self, from_node, to_node):
        cost = from_node.connection_costs[to_node.center]
        return cost


    def retrieve_node(self, target_node_pos):
        for x in range(len(self.nodes_list_omni)):
            if self.nodes_list_omni[x].center == target_node_pos:
                return self.nodes_list_omni[x]
##        return 'culled'


    def cull_nodes_omni(self, obstacle_rects):
        for x in range(len(self.nodes_list_omni)):
            node_x = self.nodes_list_omni[x]
            traversable = node_x.check_node_collision(obstacle_rects)
            if traversable == False:
                self.culled_nodes[node_x.center] = node_x
                self.culled_nodes_positions.append(node_x.center)


    def check_if_culled(self, target_node_pos):
        if target_node_pos not in self.culled_nodes_positions:
            return True
        else:
            return False



    def auto_true(self, target_node):
        return True


    def check_if_node_not_checked(self, target_node_pos):
        target_node = self.retrieve_node(target_node_pos)
        not_checked = target_node.check_if_not_previously_checked()
        return not_checked
    

        
        




def generate_nodes(node_distance=40):

    nodes_omni = []

    modifier = int(node_distance / 2)

    total_nodes_width = int(WINDOWWIDTH / node_distance)
    total_nodes_height = int(WINDOWHEIGHT / int(node_distance / 2))

    for x in range(1, total_nodes_height + 1):
        if x * int(node_distance / 2) >= WINDOWHEIGHT:
            break
        for i in range(total_nodes_width + 1):
            if i * node_distance + modifier >= WINDOWWIDTH:
                break
            new_node = (i * node_distance + modifier, x * int(node_distance / 2))
            if new_node[0] != 0:
                nodes_omni.append(new_node)
        if modifier == 0:
            modifier = int(node_distance / 2)
        else:
            modifier = 0
    

    
    list_of_nodes = []
    for x in range(len(nodes_omni)):
        new_node_object = Node(nodes_omni[x][0], nodes_omni[x][1], node_distance)
        list_of_nodes.append(new_node_object)
    return list_of_nodes



###copied code - Bresenham's Algorithm
def get_line(start, end):
    """Bresenham's Line Algorithm
    Produces a list of tuples from start and end
 
    >>> points1 = get_line((0, 0), (3, 4))
    >>> points2 = get_line((3, 4), (0, 0))
    >>> assert(set(points1) == set(points2))
    >>> print points1
    [(0, 0), (1, 1), (1, 2), (2, 3), (3, 4)]
    >>> print points2
    [(3, 4), (2, 3), (1, 2), (1, 1), (0, 0)]
    """
    # Setup initial conditions
    x1, y1 = start
    x2, y2 = end
    dx = x2 - x1
    dy = y2 - y1
 
    # Determine how steep the line is
    is_steep = abs(dy) > abs(dx)
 
    # Rotate line
    if is_steep:
        x1, y1 = y1, x1
        x2, y2 = y2, x2
 
    # Swap start and end points if necessary and store swap state
    swapped = False
    if x1 > x2:
        x1, x2 = x2, x1
        y1, y2 = y2, y1
        swapped = True
 
    # Recalculate differentials
    dx = x2 - x1
    dy = y2 - y1
 
    # Calculate error
    error = int(dx / 2.0)
    ystep = 1 if y1 < y2 else -1
 
    # Iterate over bounding box generating points between start and end
    y = y1
    points = []
    for x in range(x1, x2 + 1):
        coord = (y, x) if is_steep else (x, y)
        points.append(coord)
        error -= abs(dy)
        if error < 0:
            y += ystep
            error += dx
 
    # Reverse the list if the coordinates were swapped
    if swapped:
        points.reverse()
    return points
###end of copied code


def draw_path_connections(path):
    color = (255, 0, 0)
    for x in range(len(path)):
        pygame.draw.circle(DISPSURF, color, path[x], 3, 0)
        if x < len(path) - 1:
            pygame.draw.aaline(DISPSURF, color, path[x], path[x + 1], True)


def remove_bad_tested_nodes_connections(tested_nodes, graph):
    new_tested_nodes = {}
    node_keys = [key for key in tested_nodes.keys()]
    for x in range(len(node_keys)):
        if tested_nodes[node_keys[x]][0] == True:
            if tested_nodes[node_keys[x]][1][0] in graph.culled_nodes_positions or tested_nodes[node_keys[x]][1][1] in graph.culled_nodes_positions:
                tested_nodes[node_keys[x]][0] = False
    return tested_nodes



def draw_node_connections(DISPSURF, tested_nodes, graph):
    node_keys = [key for key in tested_nodes.keys()]
    for x in range(len(node_keys)):
        if tested_nodes[node_keys[x]][0] == False:
            color = BAD_CONNECTION_COLOR
        else:
            color = CONNECTION_COLOR
            pygame.draw.aaline(DISPSURF, color, tested_nodes[node_keys[x]][1][0], tested_nodes[node_keys[x]][1][1], True)


def cull_nodes(list_of_nodes, tested_nodes, obstacle_rects):
    validated_nodes = []
    validated_connections = {}
    for x in range(len(list_of_nodes)):
        list_of_nodes[x].check_validity(obstacle_rects)
        if list_of_nodes[x].valid_node == True:
            validated_nodes.append(list_of_nodes[x])

    validated_nodes_centers = [validated_nodes[x].center for x in range(len(validated_nodes))]

    node_keys = [key_x for key_x in tested_nodes.keys()]
    for x in range(len(node_keys)):
        if tested_nodes[node_keys[x]][0] == True:
            if tested_nodes[node_keys[x]][1][0] in validated_nodes_centers:
                if tested_nodes[node_keys[x]][1][1] in validated_nodes_centers:
                    validated_connections[node_keys[x]] = tested_nodes[node_keys[x]]
    return validated_nodes, validated_connections


def create_node_map(node_distance):
    list_of_nodes_full = generate_nodes(node_distance)

    NodeMap = OmniNodes(list_of_nodes_full)

    return NodeMap


def begin_node_check(obstacle_rects, node_distance):     
    list_of_nodes = generate_nodes(node_distance)

    tested_nodes = {}

    for x in range(len(list_of_nodes)):
        tested_nodes_new = list_of_nodes[x].locate_neighbors(obstacle_rects, tested_nodes)
        for i in range(len(tested_nodes_new)):
            tested_nodes[tested_nodes_new[i]['nodes']] = [tested_nodes_new[i]['viable'], tested_nodes_new[i]['node_points'], tested_nodes_new[i]['cost']]
    return list_of_nodes, tested_nodes


def create_obstacle(x_pos, y_pos, width, height):

    obstacle = pygame.Rect((x_pos, y_pos, width, height))

    return obstacle


def manufacture_obstacle(obstacle_start, obstacle_end, obstacle_rects):

    
    new_obstacle_width = abs(obstacle_start[0] - obstacle_end[0])
    new_obstacle_height = abs(obstacle_start[1] - obstacle_end[1])

    if obstacle_start[0] > obstacle_end[0] or obstacle_start[1] > obstacle_end[1]:
        new_x = obstacle_start[0]
        new_y = obstacle_start[1]
        if obstacle_start[0] > obstacle_end[0]:
            new_x = obstacle_end[0]
        if obstacle_start[1] > obstacle_end[1]:
            new_y = obstacle_end[1]
        obstacle_start = (new_x, new_y)
    
    if new_obstacle_width == 0 or new_obstacle_height == 0:
        return None
    new_obstacle = ((obstacle_start), new_obstacle_width, new_obstacle_height)
    new_obstacle_rect = create_obstacle(new_obstacle[0][0], new_obstacle[0][1], new_obstacle[1], new_obstacle[2])
    for x in range(len(obstacle_rects)):
        if new_obstacle_rect.colliderect(obstacle_rects[x]) == True:
            return None
    
    return new_obstacle
    

def obstacle_remover(position, obstacle_rects):
    new_obstacle_list = []
    for x in range(len(obstacle_rects)):
        if obstacle_rects[x].collidepoint(position) == False:
            new_obstacle_list.append(((obstacle_rects[x].x, obstacle_rects[x].y), obstacle_rects[x].w, obstacle_rects[x].h))
    return new_obstacle_list


def generate_graph_and_map(obstacle_rects, node_distance=40):
    node_distance = abs(node_distance)
    if node_distance == 1 or node_distance == 0:
        node_distance = 40
    elif node_distance % 2 != 0:
        node_distance += 1
        
    list_of_nodes, tested_nodes = begin_node_check(obstacle_rects, node_distance)
    graph = create_node_map(node_distance)
    graph.cull_nodes_omni(obstacle_rects)
    tested_nodes = remove_bad_tested_nodes_connections(tested_nodes, graph)

    return list_of_nodes, tested_nodes, graph, node_distance


def create_obstacle_rects_list(obstacle_list):
    new_obstacle_rects = []
    for x in range(len(obstacle_list)):
        obstacle_rect = create_obstacle(obstacle_list[x][0][0], obstacle_list[x][0][1], obstacle_list[x][1], obstacle_list[x][2])
        new_obstacle_rects.append(obstacle_rect)
    return new_obstacle_rects


def blit_img(img, pos):
    image_rect = img.get_rect()
    image_rect.center = pos
    DISPSURF.blit(img, image_rect)
    

def is_node_in_obstacle(pos, obstacle_rects):
    for x in range(len(obstacle_rects)):
        if obstacle_rects[x].collidepoint(pos) == True:
            return False
    return True



####PATHFINDING A-STAR
class PriorityQueue:
    def __init__(self):
        self.nodes = []

    def put(self, node, cost):
        heapq.heappush(self.nodes, (cost, node))

    def get(self):
        return heapq.heappop(self.nodes)[1]

    def empty(self):
        return len(self.nodes) == 0





def vec2int(v):
    return (int(v.x), int(v.y))

def heuristic(a, b, node_distance):
    #cost_value = abs(a.x - b.x) ** 2 + abs(a.y - b.y) ** 2
    cost_value = int((abs(a.x - b.x) + abs(a.y - b.y)) / int(node_distance / 2))
    return cost_value




def a_star_search(graph, start, end, obstacle_rects, tested_nodes):

    frontier = PriorityQueue()
    frontier.put(start.center, 0)
    path = {}
    cost = {}
    path[start.center] = vec(0, 0)
    cost[start.center] = 0
    goal_found = False

    previously_checked_nodes = []

    if start == end:
        path[start.center] = vec(start.center) - vec(end.center)
        return path, cost, graph
    
    while not frontier.empty():
        current = frontier.get()
        current = graph.retrieve_node(current)

        for next in graph.find_neighbors(current, obstacle_rects):
            next = graph.retrieve_node(next)
            next_cost = cost[current.center] + graph.get_cost(current, next)

            if next.center not in cost or next_cost < cost[next.center]:     
                cost[next.center] = next_cost
                priority = next_cost + heuristic(vec(end.center), vec(next.center), current.node_distance)
                frontier.put(next.center, priority)
                path[next.center] = vec(current.center) - vec(next.center)
        
        if current == end:
            goal_found = True
            break

    new_path = {}
    new_path[end.center] = vec(0, 0)
    current_vec = vec(end.center)
    last_vec = None
    closest_to_end_vec = None
    for x in range(len(path) + 1):
        if vec2int(current_vec) != end.center:                
            new_path[vec2int(current_vec)] = last_vec - current_vec
            if vec2int(current_vec) == start.center:
                break
        last_vec = current_vec
        if vec2int(current_vec) not in path:
            break
        current_vec = current_vec + path[vec2int(current_vec)]
        if last_vec == vec(end.center):
            closest_to_end_vec = current_vec

    new_path_keys = [key_x for key_x in new_path.keys()]
    for x in range(len(new_path_keys)):
        if new_path_keys[x] in path:
            path[new_path_keys[x]] = new_path[new_path_keys[x]]
    
    return path, cost, graph








    









def main_loop(DISPSURF, node_distance, obstacle_rects, start_pos, goal_pos):

##    global FPSCLOCK, DISPSURF, CURRENT_TIME
##    pygame.init()
##    FPSCLOCK = pygame.time.Clock()
##    DISPSURF = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))
##    DISPSURF.fill(BGCOLOR)

    computing = False
    compute_time = 0
    generate_nodes = True
    mouse = {'x_pos': 0, 'y_pos': 0}
    obstacle_creator = {'start': None, 'end': None}
    start = {'x_pos': 0, 'y_pos': 0}
    goal = {'x_pos': 0, 'y_pos': 0}
    start_color = (0, 255, 255)
    goal_color = (255, 0, 0)
    start_drawn = False
    goal_drawn = False
    connections_made_start = False
    connections_made_goal = False
    path_created = False
    change_in_obstacles = False

    Start = SpecialNode(start_color, start_pos[0], start_pos[1], node_distance)
    Goal = SpecialNode(goal_color, goal_pos[0], goal_pos[1], node_distance)


    list_of_nodes, tested_nodes, graph, node_distance = generate_graph_and_map(obstacle_rects, node_distance)
    generating_nodes = True

    graph = create_node_map(node_distance)
    graph.cull_nodes_omni(obstacle_rects)
    Start.locate_neighbors(graph, obstacle_rects)
    Start.evaluate_connections(obstacle_rects)
    Goal.locate_neighbors(graph, obstacle_rects)
    Goal.evaluate_connections(obstacle_rects)

    closest_node_start = Start.closest_node['node']
    closest_node_start = graph.retrieve_node(closest_node_start)
    closest_node_goal = Goal.closest_node['node']
    closest_node_goal = graph.retrieve_node(closest_node_goal)

    path, cost, graph = a_star_search(graph, closest_node_start, closest_node_goal, obstacle_rects, tested_nodes)

    path_info = {'graph': graph, 'path': path, 'start': Start, 'goal': Goal, 'closest_node_start': closest_node_start, 'closest_node_goal': closest_node_goal, 'tested_nodes': tested_nodes}

    return path_info


if __name__ == "__main__":
    main_loop()






        
