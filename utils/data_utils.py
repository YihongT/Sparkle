import matplotlib.pyplot as plt
import numpy as np
import random
import json
import copy
import math
from matplotlib.patches import Circle, Rectangle
from itertools import combinations
from scipy.spatial import distance
from itertools import combinations
from scipy.spatial.distance import euclidean
from prompts.data import DISTANCE_TEMPLATES, DIRECTION_TEMPLATES, SIZE_TEMPLATES, POSITION_TEMPLATES, POSITION_PHRASES, DIRECTION_PHRASES, DISTANCE_INTRO_PHRASES, INTRO_PHRASES, QUERIES, DISTANCE_COMPARISON_TEMPLATES, POSITION_DESCRIPTION_TEMPLATES
from prompts.data import NEW_POSITION_RELATIVE_QUERIES, NEW_DISTANCE_ABSOLUTE_QUERIES, NEW_DISTANCE_COMPARE_QUERIES, NEW_DIRECTION_QUERIES, NEW_POSITION_ABSOLUTE_QUERIES, DIRECTION_QUERIES, DISTANCE_QUERIES, POSITION_QUERIES


class SpatialRelationshipMCQGenerator:
    def __init__(self, data, num_directions=8):
        self.data = data
        self.num_directions = num_directions
        
        # Define direction options based on the number of directions
        if self.num_directions == 8:
            self.direction_options = ["top left", "top", "top right", "left", "right", "down left", "down", "down right"]
        elif self.num_directions == 4:
            self.direction_options = ["top left", "top right", "down left", "down right"]
        else:
            raise ValueError("num_directions must be either 4 or 8")

        # Map direction options to letters A, B, C, etc.
        self.direction_dict = {option: chr(65 + i) for i, option in enumerate(self.direction_options)}

        self.position_options = ["top left", "top", "top right", "left", "center", "right", "down left", "down", "down right"]
        self.position_dict = {option: chr(65 + i) for i, option in enumerate(self.position_options)}

        self.distance_templates = DISTANCE_TEMPLATES
        self.direction_templates = DIRECTION_TEMPLATES
        self.size_templates = SIZE_TEMPLATES
        self.position_templates = POSITION_TEMPLATES

    def get_direction_option_str(self):
        return ', '.join([f'{self.direction_dict[option]}. {option}' for option in self.direction_options])

    def get_position_option_str(self):
        return ', '.join([f'{self.position_dict[option]}. {option}' for option in self.position_options])

    def generate_distance_question(self):
        distances = self.data['distances']
        max_distance_pair = max(distances, key=distances.get)
        min_distance_pair = min(distances, key=distances.get)
        pair1, pair2 = random.sample(list(distances.keys()), 2)
        option_str = ', '.join([f'{chr(65 + i)}. {pair.replace("_", " to ")}' for i, pair in enumerate(distances.keys())])
        selected_template = random.choice(self.distance_templates)
        
        if "shorter" in selected_template:
            question = selected_template.format(pair1=pair1.replace("_", " to "), pair2=pair2.replace("_", " to "), option_str=option_str)
            correct_answer = chr(65 + list(distances.keys()).index(pair1 if distances[pair1] < distances[pair2] else pair2))
        elif "longer" in selected_template:
            question = selected_template.format(pair1=pair1.replace("_", " to "), pair2=pair2.replace("_", " to "), option_str=option_str)
            correct_answer = chr(65 + list(distances.keys()).index(pair1 if distances[pair1] > distances[pair2] else pair2))
        elif "shortest" in selected_template:
            question = selected_template.format(option_str=option_str)
            correct_answer = chr(65 + list(distances.keys()).index(min_distance_pair))
        else:  # For "longest" templates
            question = selected_template.format(option_str=option_str)
            correct_answer = chr(65 + list(distances.keys()).index(max_distance_pair))
        
        return question, correct_answer

    def generate_direction_question(self):
        directions = self.data['directions']
        direction_pair = random.choice(list(directions.keys()))
        from_obj, to_obj = direction_pair.split('_')
        correct_direction = directions[direction_pair]
        option_str = self.get_direction_option_str()
        selected_template = random.choice(self.direction_templates)
        question = selected_template.format(from_obj=from_obj, to_obj=to_obj, option_str=option_str)
        correct_answer = self.direction_dict[correct_direction]
        return question, correct_answer

    def generate_size_question(self):
        sizes = self.data['radius']
        max_size = max(sizes.values())
        min_size = min(sizes.values())
        max_size_obj = [k for k, v in sizes.items() if v == max_size]
        min_size_obj = [k for k, v in sizes.items() if v == min_size]

        selected_option = random.choice(["largest", "smallest", "larger", "smaller"])

        if selected_option == "largest" and len(max_size_obj) > 1:
            selected_option = "larger"
        elif selected_option == "smallest" and len(min_size_obj) > 1:
            selected_option = "smaller"

        if selected_option == "largest" and len(max_size_obj) == 1:
            option_str = ', '.join([f'{chr(65 + i)}. {obj}' for i, obj in enumerate(sizes.keys())])
            selected_template = random.choice([t for t in self.size_templates if "largest" in t])
            question = selected_template.format(option_str=option_str)
            correct_answer = chr(65 + list(sizes.keys()).index(max_size_obj[0]))
        elif selected_option == "smallest" and len(min_size_obj) == 1:
            option_str = ', '.join([f'{chr(65 + i)}. {obj}' for i, obj in enumerate(sizes.keys())])
            selected_template = random.choice([t for t in self.size_templates if "smallest" in t])
            question = selected_template.format(option_str=option_str)
            correct_answer = chr(65 + list(sizes.keys()).index(min_size_obj[0]))
        elif selected_option == "larger":
            obj1, obj2 = random.sample(sizes.keys(), 2)
            option_str = ', '.join([f'{chr(65)}. {obj1}', f'{chr(66)}. {obj2}', f'{chr(67)}. Both are the same size'])
            selected_template = random.choice([t for t in self.size_templates if "larger" in t])
            question = selected_template.format(obj1=obj1, obj2=obj2, option_str=option_str)
            # Determine the correct answer
            if sizes[obj1] == sizes[obj2]:
                correct_answer = 'C'
            elif sizes[obj1] > sizes[obj2]:
                correct_answer = 'A'
            else:
                correct_answer = 'B'
        elif selected_option == "smaller":
            obj1, obj2 = random.sample(sizes.keys(), 2)
            option_str = ', '.join([f'{chr(65)}. {obj1}', f'{chr(66)}. {obj2}', f'{chr(67)}. Both are the same size'])
            selected_template = random.choice([t for t in self.size_templates if "smaller" in t])
            question = selected_template.format(obj1=obj1, obj2=obj2, option_str=option_str)
            # Determine the correct answer
            if sizes[obj1] == sizes[obj2]:
                correct_answer = 'C'
            elif sizes[obj1] < sizes[obj2]:
                correct_answer = 'A'
            else:
                correct_answer = 'B'
        else:
            raise ValueError("Invalid size comparison")

        return question, correct_answer

    def generate_position_question(self):
        positions = self.data['positions']
        position_obj = random.choice(list(positions.keys()))
        correct_position = positions[position_obj]
        option_str = self.get_position_option_str()
        selected_template = random.choice(self.position_templates)
        question = selected_template.format(obj=position_obj, option_str=option_str)
        correct_answer = self.position_dict[correct_position]
        return question, correct_answer

    
    
def describe_spatial_relationships_new(data, abs=True):
    query_list, resp_list = [], []
    
    points = data['points']
    distances = data['distances']
    directions = data['directions']
    positions = data['positions']
        
    def desc_distances(distances):
        # Lists to store the final queries and responses
        absolute_queries = []
        absolute_responses = []
        relative_queries = []
        relative_responses = []

        # Extract all the distance pairs and sort them by distance
        all_pairs = list(distances.keys())
        sorted_distances = sorted(distances.items(), key=lambda x: x[1])  # Sort by distance value
        
        # Generate absolute queries (what is the distance between X and Y?)
        for pair in all_pairs:
            # Sample a template for each pair from the absolute templates
            template = random.choice(NEW_DISTANCE_ABSOLUTE_QUERIES)
            obj1, obj2 = pair.split('_')
            formatted_query = template.format(obj1=obj1, obj2=obj2)
            
            absolute_queries.append(formatted_query)
            absolute_responses.append(str(round(distances[pair], 2)))
        
        # Generate compare (relative) queries
        for template in NEW_DISTANCE_COMPARE_QUERIES:
            sampled_template = random.choice(NEW_DISTANCE_COMPARE_QUERIES)
            if "{all_pairs}" in sampled_template:
                # Replace {all_pairs} with the distance pairs list
                formatted_query = sampled_template.format(all_pairs=', '.join(all_pairs).replace("_", " and "))
                relative_queries.append(formatted_query)
                
                # Answer for shortest/longest queries
                if "shortest" in sampled_template:
                    shortest_pair = sorted_distances[0][0]
                    relative_responses.append(shortest_pair.replace("_", " and "))
                elif "longest" in sampled_template:
                    longest_pair = sorted_distances[-1][0]
                    relative_responses.append(longest_pair.replace("_", " and "))
            
            elif "{pair1}" in sampled_template and "{pair2}" in sampled_template:
                # Randomly select two pairs for comparison
                pair1, pair2 = random.sample(all_pairs, 2)
                formatted_query = sampled_template.format(pair1=pair1.replace("_", " and "), pair2=pair2.replace("_", " and "))
                relative_queries.append(formatted_query)
                
                # Answer for pairwise comparison queries
                if "shorter" in sampled_template:
                    shorter_pair = pair1 if distances[pair1] < distances[pair2] else pair2
                    relative_responses.append(shorter_pair.replace("_", " and "))
                elif "longer" in sampled_template:
                    longer_pair = pair1 if distances[pair1] > distances[pair2] else pair2
                    relative_responses.append(longer_pair.replace("_", " and "))
        
        return absolute_queries, absolute_responses, relative_queries, relative_responses
    
    
    for obj_pair, direction in directions.items():
        obj1, obj2 = obj_pair.split('_')
        query_list.append(random.choice(NEW_DIRECTION_QUERIES).format(from_obj=obj1, to_obj=obj2))
        resp_list.append(direction)
    
    direction_query_list = copy.deepcopy(query_list)
    direction_resp_list = copy.deepcopy(resp_list)
    
    absolute_queries, absolute_responses, relative_queries, relative_responses = desc_distances(distances)
    distance_query_list = copy.deepcopy(relative_queries)
    distance_resp_list = copy.deepcopy(relative_responses)
    
    query_list += relative_queries
    resp_list += relative_responses
    
    position_query_list = []
    position_resp_list = []
    for obj, pos in positions.items():
        query_list.append(random.choice(NEW_POSITION_RELATIVE_QUERIES).format(obj=obj))
        resp_list.append(pos)
        position_query_list.append(random.choice(NEW_POSITION_RELATIVE_QUERIES).format(obj=obj))
        position_resp_list.append(pos)
    
    if abs:
        query_list += absolute_queries
        resp_list += absolute_responses
        
        distance_query_list += absolute_queries
        distance_resp_list += absolute_responses
            
        for obj, pos in points.items():
            query_list.append(random.choice(NEW_POSITION_ABSOLUTE_QUERIES).format(obj=obj))
            resp_list.append(f"({round(pos[0], 2)}, {round(pos[1], 2)})")
            position_query_list.append(query_list[-1])
            position_resp_list.append(f"({round(pos[0], 2)}, {round(pos[1], 2)})")
        
            
    
    return query_list, resp_list, direction_query_list, direction_resp_list, distance_query_list, distance_resp_list, position_query_list, position_resp_list
    

def describe_spatial_relationships(data, abs=True):
    points = data['points']
    distances = data['distances']
    directions = data['directions']
    # sizes = data['radius']
    positions = data['positions']
    
    def describe_positions(points):
        desc_positions = []
        for object, point in points.items():
            desc_positions.append(
                POSITION_DESCRIPTION_TEMPLATES[0].format(object=object, x=point[0], y=point[1])
            )
        return desc_positions

    def compare_distances(distances, abs=True):
        dist_keys = list(distances.keys())
        comparisons = []
        for i in range(len(dist_keys)):
            for j in range(i + 1, len(dist_keys)):
                d1_key = dist_keys[i]
                d2_key = dist_keys[j]
                d1_value = distances[d1_key]
                d2_value = distances[d2_key]
                obj1_from, obj1_to = d1_key.split('_')
                obj2_from, obj2_to = d2_key.split('_')

                if d1_value > d2_value:
                    comparisons.append(
                        DISTANCE_COMPARISON_TEMPLATES[0].format(
                            obj1_from=obj1_from, obj1_to=obj1_to, obj2_from=obj2_from, obj2_to=obj2_to
                        )
                    )
                elif d1_value < d2_value:
                    comparisons.append(
                        DISTANCE_COMPARISON_TEMPLATES[1].format(
                            obj1_from=obj1_from, obj1_to=obj1_to, obj2_from=obj2_from, obj2_to=obj2_to
                        )
                    )
                else:
                    comparisons.append(
                        DISTANCE_COMPARISON_TEMPLATES[2].format(
                            obj1_from=obj1_from, obj1_to=obj1_to, obj2_from=obj2_from, obj2_to=obj2_to
                        )
                    )
        if abs:
            for key, value in distances.items():
                obj1, obj2 = key.split('_')
                comparisons.append(
                    DISTANCE_COMPARISON_TEMPLATES[3].format(
                        obj1=obj1, obj2=obj2, distance=value
                    )
                )
        
        return comparisons

    distance_descriptions = compare_distances(distances, abs=abs)
    position_descriptions = describe_positions(points)

    if abs:
        sections = [
            ("Positions", lambda: [random.choice(POSITION_PHRASES).format(obj=obj, pos=pos) for obj, pos in positions.items()] + position_descriptions),
            ("Directions", lambda: [random.choice(DIRECTION_PHRASES).format(obj1=obj1, obj2=obj2, direction=direction) for (obj_pair, direction) in directions.items() for obj1, obj2 in [obj_pair.split('_')]]),
            ("Distances", lambda: [random.choice(DISTANCE_INTRO_PHRASES)] + distance_descriptions)
        ]
    else:
        sections = [
            ("Positions", lambda: [random.choice(POSITION_PHRASES).format(obj=obj, pos=pos) for obj, pos in positions.items()]),
            ("Directions", lambda: [random.choice(DIRECTION_PHRASES).format(obj1=obj1, obj2=obj2, direction=direction) for (obj_pair, direction) in directions.items() for obj1, obj2 in [obj_pair.split('_')]]),
            ("Distances", lambda: [random.choice(DISTANCE_INTRO_PHRASES)] + distance_descriptions)
        ]
        
        
    random.shuffle(sections)

    description = random.choice(INTRO_PHRASES)
    direction_description = copy.deepcopy(description)
    distance_description = copy.deepcopy(description)
    position_description = copy.deepcopy(description)
    
    for title, content_func in sections:
        if title not in ["Sizes", "Distances"]:
            description += f"{title}:\n"
        description += "\n".join(content_func()) + "\n\n"
        
        if title == "Directions":
            direction_description += f"{title}:\n"
            direction_description += "\n".join(content_func()) + "\n\n"
        
        if title == "Distances":
            distance_description += f"{title}:\n"
            distance_description += "\n".join(content_func()) + "\n\n"
            
        if title == "Positions":
            position_description += f"{title}:\n"
            position_description += "\n".join(content_func()) + "\n\n"

    query = random.choice(QUERIES)
    direction_query = random.choice(DIRECTION_QUERIES)
    distance_query = random.choice(DISTANCE_QUERIES)
    position_query = random.choice(POSITION_QUERIES)
    
    return query, description, direction_query, direction_description, distance_query, distance_description, position_query, position_description







def calculate_position(point):
    x, y = point
    if not (0 <= x <= 1 and 0 <= y <= 1):
        raise ValueError("Coordinates must be within the range [0, 1].")

    if x < 0.4:
        if y < 0.4:
            return "down left"
        elif y < 0.6:
            return "left"
        else:
            return "top left"
    elif x < 0.6:
        if y < 0.4:
            return "down"
        elif y < 0.6:
            return "center"
        else:
            return "top"
    else:
        if y < 0.4:
            return "down right"
        elif y < 0.6:
            return "right"
        else:
            return "top right"
        

def solve_open_tsp_dynamic_programming(distance_matrix, start_idx=None):
    num_points = len(distance_matrix)
    if num_points == 0:
        return [], 0.0
    if num_points == 1:
        return [0], 0.0

    full_mask = (1 << num_points) - 1
    dp = {}
    parent = {}

    if start_idx is None:
        for idx in range(num_points):
            state = (1 << idx, idx)
            dp[state] = 0.0
            parent[state] = None
    else:
        state = (1 << start_idx, start_idx)
        dp[state] = 0.0
        parent[state] = None

    for mask in range(full_mask + 1):
        for last in range(num_points):
            state = (mask, last)
            if state not in dp:
                continue
            current_cost = dp[state]
            for nxt in range(num_points):
                if mask & (1 << nxt):
                    continue
                next_mask = mask | (1 << nxt)
                next_state = (next_mask, nxt)
                next_cost = current_cost + distance_matrix[last][nxt]
                if next_state not in dp or next_cost < dp[next_state]:
                    dp[next_state] = next_cost
                    parent[next_state] = state

    end_state = min(
        ((full_mask, last) for last in range(num_points) if (full_mask, last) in dp),
        key=lambda state: dp[state]
    )

    permutation = []
    state = end_state
    while state is not None:
        permutation.append(state[1])
        state = parent[state]
    permutation.reverse()

    return permutation, dp[end_state]


def calculate_direction(point1, point2, num_direction=8, primary_span=22.5):
    x1, y1 = point1
    x2, y2 = point2
    
    dx = x2 - x1
    dy = y2 - y1
    angle = math.degrees(math.atan2(dy, dx))
    
    if num_direction == 8:
        half_primary_span = primary_span / 2
        diagonal_span = 90 - primary_span
        
        if -half_primary_span <= angle < half_primary_span:
            return "right"
        elif half_primary_span <= angle < half_primary_span + diagonal_span:
            return "top right"
        elif -half_primary_span + 90 <= angle < half_primary_span + 90:
            return "top"
        elif half_primary_span + 90 <= angle < half_primary_span + 90 + diagonal_span:
            return "top left"
        elif 180 - half_primary_span <= angle < 180 or -180 <= angle < -180 + half_primary_span:
            return "left"
        elif -180 + half_primary_span <= angle < -180 + half_primary_span + diagonal_span:
            return "down left"
        elif -90 - half_primary_span <= angle < -90 + half_primary_span:
            return "down"
        elif -90 + half_primary_span <= angle < -half_primary_span:
            return "down right"

    elif num_direction == 4:
        # if -45 <= angle < 45:
        #     return "top right"
        # elif 45 <= angle < 135:
        #     return "top left"
        # elif -135 <= angle < -45:
        #     return "down right"
        # else:
        #     return "down left"
        
        diagonal_span = 90  # 360 degrees / 4 directions
        
        if 0 <= angle < diagonal_span:
            return "top right"
        elif diagonal_span <= angle < 180:
            return "top left"
        elif -180 <= angle < -diagonal_span:
            return "down left"
        elif -diagonal_span <= angle < 0:
            return "down right"

    else:
        raise ValueError("num_direction must be either 4 or 8")
        
def generate_coordinates(radius, num_points=3):
    points = []
    while len(points) < num_points:
        x, y = np.random.uniform(radius, 1-radius, 2)
        new_point = np.array([x, y])
        if all(distance.euclidean(new_point, np.array(p)) >= 2*radius for p in points):
            points.append([x, y])
    return points


# def add_noise_points(points, radius, num_noise_points, noise_colors):
#     used_colors = []
#     while len(points) < 3 + num_noise_points:
#         x, y = np.random.uniform(radius, 1-radius, 2)
#         new_point = np.array([x, y])
#         if all(distance.euclidean(new_point, np.array(p)) >= 2*radius for p in points):
#             points.append([x, y])
#             used_colors.append(noise_colors[len(used_colors) % len(noise_colors)])
#     return points, used_colors


def calculate_distances_and_save(points, colors, filename='distances.json'):
    distances = {}
    for (i, point1), (j, point2) in combinations(enumerate(points), 2):
        dist = distance.euclidean(point1, point2)
        key = f"{colors[i]}_{colors[j]}"
        distances[key] = dist
    
    return distances


def calculate_directions_and_save(points, colors, num_direction=9):

    directions = {}
    for (i, point1), (j, point2) in combinations(enumerate(points), 2):
        direction = calculate_direction(point1, point2, num_direction)
        key = f"{colors[i]}_{colors[j]}"
        directions[key] = direction
    
    return directions

def get_direction_value_dict(num_direction=9):
    
    if num_direction == 4:
        value_to_key_dict = {
            "top left": "A", "top right": "B",
            "down left": "C", "down right": "D"
        }
    else:  # num_direction == 9
        value_to_key_dict = {
            "top left": "A", "top center": "B", "top right": "C",
            "middle left": "D", "middle center": "E", "middle right": "F",
            "down left": "G", "down center": "H", "down right": "I"
        }

    return value_to_key_dict


def add_noise_points(points, radii, num_noise_points, noise_colors, distance_threshold):
    used_colors = []
    num_basic_points = len(points)
    while len(points) < num_basic_points + num_noise_points:
        # radius = np.random.choice([25, 50, 75])
        radius = 50
        while True:
            x, y = np.random.uniform(radius/1000, 1-radius/1000, 2)
            new_point = np.array([x, y])
            no_overlap = True
            for p, r in zip(points, radii):
                if distance.euclidean(new_point, np.array(p)) < (radius + r + distance_threshold*1000)/1000:
                    no_overlap = False
                    break
            if no_overlap:
                points.append([x, y])
                radii.append(radius)
                used_colors.append(noise_colors[len(used_colors) % len(noise_colors)])
                break
    return points, radii, used_colors



def draw_points_with_numbers(base_dir, num_basic_points=3, num_noise_points=0, dpi=200, index=0, type='train', distance_threshold=0.2, run_type='static', fontsize=25, fontcolor='black', object_color='lightgray'):
    fig, ax = plt.subplots(figsize=(8, 8))
    fig.patch.set_alpha(0)
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.set_aspect('equal')

    # Generating basic points with random radii
    points = []
    radii = []
    texts = []
    while len(points) < num_basic_points:
        radius = 50
        while True:
            x, y = np.random.uniform(radius/1000, 1-radius/1000, 2)
            new_point = np.array([x, y])
            no_overlap = True
            for p, r in zip(points, radii):
                if distance.euclidean(new_point, np.array(p)) < (radius + r + distance_threshold*1000)/1000:
                    no_overlap = False
                    break
            if no_overlap:
                points.append([x, y])
                radii.append(radius)
                break

    if num_noise_points > 0:
        points, radii, _ = add_noise_points(points, radii, num_noise_points, [object_color], distance_threshold)

    texts = [f"N{i+1}" for i in range(len(points))]
    random.shuffle(texts)

    for i, (point, radius) in enumerate(zip(points, radii)):
        x, y = point
        circle = Circle((x, y), radius/1000, color=object_color)
        ax.add_patch(circle)
        ax.text(x, y, texts[i], fontsize=fontsize, color=fontcolor, ha='center', va='center')

    plt.axis('off')
    plt.savefig(f'{base_dir}/{type}_{index}.png', dpi=dpi, transparent=True, bbox_inches='tight', pad_inches=0)
    plt.close()
    
    return points[:num_basic_points], texts[:num_basic_points], radii[:num_basic_points]


def draw_points_with_noise(base_dir, num_basic_points=3, num_noise_points=0, dpi=200, index=0, type='train', distance_threshold=0.2, run_type='static'):
    fig, ax = plt.subplots(figsize=(8, 8))
    fig.patch.set_alpha(0)
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.set_aspect('equal')

    if run_type == 'static':
        if type == 'train':
            main_colors = ['yellow', 'red', 'green', 'brown']
        else:
            main_colors = ['blue', 'purple', 'black', 'orange']
            
    elif run_type == 'tsp':
        main_colors = ['yellow', 'red', 'green', 'blue', 'purple', 'black', 'brown']
        
    else:
        raise ValueError("Invalid run type")

    noise_colors = [
        'gray', 'olive'
    ]
    
    # Generating basic points with random radii
    points = []
    radii = []
    while len(points) < num_basic_points:
        # radius = np.random.choice([25, 50, 75]) we don't consider radius anymore
        radius = 50
        while True:
            # print(f'radius: {radius}')
            # print(f'points: {points}')
            x, y = np.random.uniform(radius/1000, 1-radius/1000, 2)
            new_point = np.array([x, y])
            no_overlap = True
            for p, r in zip(points, radii):
                # print(f'dis: {distance.euclidean(new_point, np.array(p))}')
                # print(f'r: {(radius + r + distance_threshold*1000)/1000}')
                if distance.euclidean(new_point, np.array(p)) < (radius + r + distance_threshold*1000)/1000:
                    # print(f'overlapped!!')
                    no_overlap = False
                    break
            if no_overlap:
                points.append([x, y])
                radii.append(radius)
                break

    if num_noise_points > 0:
        points, radii, noise_point_colors = add_noise_points(points, radii, num_noise_points, noise_colors, distance_threshold)
    else:
        noise_point_colors = []

    all_colors = main_colors[:num_basic_points] + noise_point_colors
    
    for i, (point, radius) in enumerate(zip(points, radii)):
        x, y = point
        circle = Circle((x, y), radius/1000, color=all_colors[i], alpha=0.6)
        ax.add_patch(circle)
        ax.plot(x, y, 'o', color=all_colors[i], markersize=radius/10)

    plt.axis('off')
    plt.savefig(f'{base_dir}/{type}_{index}.png', dpi=dpi, transparent=True, bbox_inches='tight', pad_inches=0)
    plt.close()
    
    return points[:num_basic_points], all_colors[:num_basic_points], radii[:num_basic_points]




    
def plot_circle_grid(n, start_pos, end_pos, args, text_grid=None, start_color='green', end_color='red', grid_color='lightgray', edge_color='lightgray', text_color='black', text_size=15, circle_radius=0.2, rect_width=0.03, dpi=200, save_path=None):
    fig, ax = plt.subplots(figsize=(8, 8))
    fig.patch.set_alpha(0)
    
    # Set the limits and configure the grid
    plt.xlim(0, 1)
    plt.ylim(0, 1)
    plt.gca().set_aspect('equal', adjustable='box')
    plt.xticks([])  # Hide grid ticks
    plt.yticks([])  # Hide grid ticks
    plt.axis('off')  # Remove the outer frame
    
    if args.textgrid and text_grid is not None:        
            
        # Plot the grid of circles and add text to each
        for i in range(n):
            for j in range(n):
                x, y = (i + 0.5) / n, (j + 0.5) / n
                circle = Circle((x, y), circle_radius / n, color=grid_color)
                ax.add_patch(circle)
                # Add text to the center of each circle
                ax.text(x, y, text_grid[i][j], color=text_color, fontsize=text_size, ha='center', va='center')
    
    # Draw rectangles to connect circles
    for i in range(n):
        for j in range(n):
            if i < n - 1:  # Rectangle to the right
                x, y = (i + 0.5) / n, (j + 0.5) / n
                rect = Rectangle((x, y - rect_width / 2 / n), 1 / n, rect_width / n, color=edge_color)
                ax.add_patch(rect)
            if j < n - 1:  # Rectangle upwards
                x, y = (i + 0.5) / n, (j + 0.5) / n
                rect = Rectangle((x - rect_width / 2 / n, y), rect_width / n, 1 / n, color=edge_color)
                ax.add_patch(rect)
    
    # Plot the grid of circles
    for i in range(n):
        for j in range(n):
            x, y = (i + 0.5) / n, (j + 0.5) / n
            circle = Circle((x, y), circle_radius / n, color=grid_color)
            ax.add_patch(circle)
    
    # Plot start position
    x, y = (start_pos[0] + 0.5) / n, (start_pos[1] + 0.5) / n
    ax.add_patch(plt.Circle((x, y), circle_radius / n, color=start_color))

    # Plot end position
    x, y = (end_pos[0] + 0.5) / n, (end_pos[1] + 0.5) / n
    ax.add_patch(plt.Circle((x, y), circle_radius / n, color=end_color))
    
    # Save or show the plot
    if save_path:
        plt.savefig(save_path, dpi=dpi, transparent=True, bbox_inches='tight', pad_inches=0)
    else:
        plt.show()

    plt.close()


def generate_hop_pairs(n, m, k):
    # n: Grid size
    # m: Number of pairs to generate
    # k: Required distance in hops
    
    def distance(p1, p2):
        # Manhattan distance for grid points
        return abs(p1[0] - p2[0]) + abs(p1[1] - p2[1])
    
    def is_valid_pair(start, end, k):
        return distance(start, end) >= k
    
    pairs = []
    attempts = 0
    max_attempts = 10000  # To avoid infinite loop
    
    while len(pairs) < m and attempts < max_attempts:
        start = [random.randint(0, n-1), random.randint(0, n-1)]
        end = [random.randint(0, n-1), random.randint(0, n-1)]
        
        if is_valid_pair(start, end, k) and (start, end) not in pairs and (end, start) not in pairs:
            pairs.append([start, end])
        
        attempts += 1
    
    if len(pairs) < m:
        print(f"Could only generate {len(pairs)} pairs after {max_attempts} attempts.")
    
    return pairs


def generate_static_data_worker(args, index, data_type):
    if data_type == 'train':
        data_dir = f'{args.data_dir}/{args.train_folder}'
    else:
        data_dir = f'{args.data_dir}/{args.test_folder}'
    img_path = f"{data_dir}/imgs/{data_type}_{index}.png"

    if data_type == 'train':
        # args.num_noise_points = 0
        if args.textobj:
            points, colors, radius = draw_points_with_numbers(data_dir + '/imgs', args.num_basic_points, 0, index=index, type=data_type, fontsize=25, fontcolor='black', object_color=args.obj_color)
        else:
            points, colors, radius = draw_points_with_noise(data_dir + '/imgs', args.num_basic_points, 0, index=index, type=data_type)
    else:
        if args.textobj:
            points, colors, radius = draw_points_with_numbers(data_dir + '/imgs', args.num_basic_points, args.num_noise_points, index=index, type=data_type, fontsize=25, fontcolor='black', object_color=args.obj_color)
        else:
            points, colors, radius = draw_points_with_noise(data_dir + '/imgs', args.num_basic_points, args.num_noise_points, index=index, type=data_type)

    distances = calculate_distances_and_save(points, colors)
    directions = calculate_directions_and_save(points, colors, args.num_direction)
    positions = {}
    for i, point in enumerate(points):
        positions[colors[i]] = calculate_position(point)

    radius = {color: r for color, r in zip(colors, radius)}
    
    image_width = args.img_width # suppose the image is 10x10    
    distances = {key: value * image_width for key, value in distances.items()}
    points = {color: [point[0].item() * image_width, point[1].item() * image_width] for color, point in zip(colors, points)}

    return {
        'index': index,
        'img_path': img_path,
        'distances': distances,
        'directions': directions,
        'radius': radius,
        'points': points,
        'positions': positions
    }
    
    

def generate_tsp_data_worker(args, index, data_type):
    if data_type == 'train':
        data_dir = f'{args.data_dir}/{args.train_folder}'
    else:
        data_dir = f'{args.data_dir}/{args.test_folder}'
    img_path = f"{data_dir}/imgs/{data_type}_{index}.png"

    if args.textobj:
        points, colors, radius = draw_points_with_numbers(data_dir + '/imgs', args.num_basic_points, 0, index=index, type=data_type, fontsize=25, fontcolor='black', object_color=args.obj_color)
    else:
        points, colors, radius = draw_points_with_noise(data_dir + '/imgs', args.num_basic_points, 0, index=index, type=data_type, run_type='tsp')
    
    # Calculate the distance matrix
    num_points = len(points)
    distance_matrix = np.zeros((num_points, num_points))

    for i in range(num_points):
        for j in range(num_points):
            if i != j:
                distance_matrix[i][j] = euclidean(points[i], points[j])

    if args.tsp_type == 'fixstart':
        start_idx = random.randrange(num_points)
        permutation, distance = solve_open_tsp_dynamic_programming(distance_matrix, start_idx=start_idx)
    elif args.tsp_type == 'free':
        permutation, distance = solve_open_tsp_dynamic_programming(distance_matrix)
    else:
        raise ValueError("Invalid tsp_type")
    
    return {
        'index': index,
        'img_path': img_path,
        'points': points,
        'colors': colors,
        'permutation': permutation,
        'distance': distance
    }
    


def generate_shortest_data_worker(args, index, data_type, start_end):
    if data_type == 'train':
        data_dir = f'{args.data_dir}/{args.train_folder}'
    else:
        data_dir = f'{args.data_dir}/{args.test_folder}'
    img_path = f"{data_dir}/imgs/{data_type}_{index}.png"
    
    start = start_end[0]
    end = start_end[1]
    
    if args.textgrid:
        text_grid = [[f"N{i*args.ngrid+j+1}" for j in range(args.ngrid)] for i in range(args.ngrid)]  # Generating some example text like N1, N2, ..., N25
        start_text_label = text_grid[start[0]][start[1]]
        end_text_label = text_grid[end[0]][end[1]]
    else:
        text_grid = None
        start_text_label = None
        end_text_label = None
    
    plot_circle_grid(args.ngrid, start, end, args, grid_color=args.obj_color, edge_color=args.obj_color, text_color=args.font_color, text_grid=text_grid, save_path=img_path)
    gt_shortest_path_length = abs(start[0] - end[0]) + abs(start[1] - end[1])
    
    return {
        'index': index,
        'img_path': img_path,
        'start': start,
        'end': end,
        'start_text_label': start_text_label,
        'end_text_label': end_text_label,
        'gt_shortest_path_length': gt_shortest_path_length
    }
    



