############################## STATIC DATA ##############################
# Distance-related question templates
DISTANCE_TEMPLATES = [
    "Which distance is the shortest?\nOptions: {option_str}\nRespond with the correct option letter in \\boxed{{option}}.",
    "Identify the longest distance between the points.\nChoices: {option_str}\nReply with the right option letter in \\boxed{{option}}.",
    "Among the given distances, which one is the longest?\nSelections: {option_str}\nAnswer with the correct option letter in \\boxed{{option}}.",
    "Which distance is shorter, {pair1} or {pair2}?\nOptions: {option_str}\nRespond with the correct option letter in \\boxed{{option}}.",
    "Compare the distances: {pair1} and {pair2}. Which one is longer?\nChoices: {option_str}\nReply with the correct option letter in \\boxed{{option}}."
]

# Direction-related question templates
DIRECTION_TEMPLATES = [
    "What is the direction from the {from_obj} point to the {to_obj} point?\nOptions: {option_str}\nRespond with the correct option letter in \\boxed{{option}}.",
    "From {from_obj} to {to_obj}, which direction is it?\nChoices: {option_str}\nReply with the correct option letter in \\boxed{{option}}.",
    "Determine the direction from {from_obj} to {to_obj}.\nSelections: {option_str}\nAnswer with the correct option letter in \\boxed{{option}}."
]

# Size-related question templates
SIZE_TEMPLATES = [
    "Which object is the largest?\nOptions: {option_str}\nRespond with the correct option letter in \\boxed{{option}}.",
    "Identify the largest object.\nChoices: {option_str}\nReply with the correct option letter in \\boxed{{option}}.",
    "Among the objects, which one is the largest?\nSelections: {option_str}\nAnswer with the correct option letter in \\boxed{{option}}.",
    "Which object is the smallest?\nOptions: {option_str}\nRespond with the correct option letter in \\boxed{{option}}.",
    "Identify the smallest object.\nChoices: {option_str}\nReply with the correct option letter in \\boxed{{option}}.",
    "Among the objects, which one is the smallest?\nSelections: {option_str}\nAnswer with the correct option letter in \\boxed{{option}}.",
    "Which object is smaller, {obj1} or {obj2}?\nOptions: {option_str}\nRespond with the correct option letter in \\boxed{{option}}.",
    "Compare the sizes: {obj1} and {obj2}. Which one is larger?\nChoices: {option_str}\nReply with the correct option letter in \\boxed{{option}}."
]

# Position-related question templates
POSITION_TEMPLATES = [
    "Where is the {obj} object located?\nOptions: {option_str}\nRespond with the correct option letter in \\boxed{{option}}.",
    "What is the position of the {obj} object?\nChoices: {option_str}\nReply with the correct option letter in \\boxed{{option}}.",
    "Identify the location of the {obj} object.\nSelections: {option_str}\nAnswer with the correct option letter in \\boxed{{option}}."
]

# Phrases for describing positions
POSITION_PHRASES = [
    "The {obj} object is at the {pos} of the image.",
    "You'll find the {obj} object at the {pos} of the image.",
    "The {obj} object is located at the {pos} of the image."
]

# Phrases for describing directions
DIRECTION_PHRASES = [
    "You can reach the {obj2} object by going {direction} from the {obj1} object.",
    "Starting at the {obj1} object, head {direction} to find the {obj2} object.",
    "From the {obj1} object, you can go {direction} to reach the {obj2} object."
]

# Phrases for introducing distance comparisons
DISTANCE_INTRO_PHRASES = [
    "Comparing distances:",
    "When looking at distances:",
    "Distance-wise:"
]

# Introductory phrases
INTRO_PHRASES = [
    "Here's a breakdown of the spatial relationships between the objects in the image:\n\n",
    "Let's describe the spatial relationships among the objects in the image:\n\n",
    "This is an analysis of how the objects are spatially related in the image:\n\n"
]

# Queries for asking about spatial relationships
QUERIES = [
    "Can you describe the spatial relationships between the objects in the 10 by 10 image?",
    "Please provide a description of the spatial relationships among the various objects in the 10 by 10 picture.",
    "I'd like a detailed description of the spatial relationships of the objects shown in the 10 by 10 image.",
    "Could you explain the spatial relationships between different objects in this 10 by 10 image?",
    "Give a comprehensive description of the spatial relationships of the objects within the 10 by 10 image."
]

DIRECTION_QUERIES = [
    "Can you describe the directional relationships between the objects in the image?",
    "Please provide a description of the directions among the various objects in the picture.",
    "I'd like a detailed description of the directional relationships of the objects shown in the image.",
    "Could you explain the directional relationships between different objects in this image?",
    "Give a comprehensive description of the directions of the objects within the image."
]

DISTANCE_QUERIES = [
    "Can you describe the distances between the objects in the 10 by 10 image?",
    "Please provide a description of the distances among the various objects in the 10 by 10 picture.",
    "I'd like a detailed description of the distances between the objects shown in the 10 by 10 image.",
    "Could you explain the distances between different objects in this 10 by 10 image?",
    "Give a comprehensive description of the distances of the objects within the 10 by 10 image."
]

POSITION_QUERIES = [
    "Can you describe the positions of the objects in the 10 by 10 image?",
    "I'd like a detailed description of the positions of the objects shown in the 10 by 10 image.",
    "Could you explain the positions of different objects in this 10 by 10 image?",
    "Give a comprehensive description of the positions of the objects within the 10 by 10 image."
]






# Templates for describing positions
POSITION_DESCRIPTION_TEMPLATES = [
    "The coordinate of the {object} object is ({x:.2f}, {y:.2f})."
]

# Templates for comparing distances
DISTANCE_COMPARISON_TEMPLATES = [
    "The distance from {obj1_from} to {obj1_to} is longer than the distance from {obj2_from} to {obj2_to}.",
    "The distance from {obj2_from} to {obj2_to} is longer than the distance from {obj1_from} to {obj1_to}.",
    "The distance from {obj1_from} to {obj1_to} is the same as the distance from {obj2_from} to {obj2_to}.",
    "The distance between the {obj1} and {obj2} objects is {distance:.2f}."
]




NEW_DIRECTION_QUERIES = [
    "What is the direction from the {from_obj} object to the {to_obj} object?",
    "From the {from_obj} object to the {to_obj} object, which direction should you move?",
    "Determine the direction from the {from_obj} object to the {to_obj} object."
]


NEW_DISTANCE_COMPARE_QUERIES = [
    "Which distance is the shortest? {all_pairs}",
    "Among the given distances, which one is the longest? {all_pairs}",
    "Which distance is shorter, {pair1} or {pair2}?",
    "Compare the distances: {pair1} and {pair2}. Which one is longer?"
]

NEW_DISTANCE_ABSOLUTE_QUERIES = [
    "The image is 10x10. What is the distance between the {obj1} and {obj2} objects?",
    "In a 10x10 image, what is the distance between the {obj1} and {obj2} objects?"
]

NEW_POSITION_RELATIVE_QUERIES = [
    "Which relative position is the {obj} located at?",
    "What is the position of the {obj}?",
    "Identify the location of the {obj}."
]

NEW_POSITION_ABSOLUTE_QUERIES = [
    "The image is 10x10. What is the absolute position of the {obj} object?",
    "In a 10x10 image, what is the coordinate of the {obj} object?"
]




############################## TSP DATA ##############################
TSP_QUESTION_TEMPLATES = [
    # "This image contains five colored objects: yellow, red, green, blue, and purple. Solve the Traveling Salesman Problem (TSP) by finding the shortest path that visits each object once. Return the order of colors in the optimal path as a Python list.",
    # "In this image, there are five colored objects: yellow, red, green, blue, and purple. Find the shortest path that visits each object exactly once to solve the Traveling Salesman Problem (TSP). Return the optimal sequence of colors as a Python list.",
    # "You have an image with five colored objects: yellow, red, green, blue, and purple. Your task is to solve the TSP by finding the shortest path that visits each object once. Return the colors in the order of the optimal path as a Python list.",
    # "This image shows five colored objects: yellow, red, green, blue, and purple. Solve the TSP by determining the shortest path that visits each object exactly once. Provide the order of colors in the optimal path as a Python list."
    # "This image has five colored objects: yellow, red, green, blue, and purple. Your task is to solve the Traveling Salesman Problem (TSP) by finding the shortest path that visits each object exactly once. Return the optimal order of the objects as a Python list of colors."
    
    # "The image shows five colored objects: yellow, red, green, blue, and purple. Based on the image, reason over the spatial relationships between the objects and find the shortest path that visits each object exactly once. Return the optimal order of the objects as a Python list of colors without using tools or code.",
    # "The image shows five colored objects: yellow, red, green, blue, and purple. Based on the image, reason over the spatial relationships between the objects and find the shortest path that starts at the yellow object and visits each object exactly once. Return the optimal order of the objects as a Python list of colors without using tools or code."

    """Given an image containing exactly {num_objects} objects:
{objects_string}

Task:
1. Analyze the spatial relationships between these objects.
2. Determine the shortest path that visits each object exactly once.
3. Return the optimal order as a Python list of objects.

Requirements:
- Use only the {num_objects} objects listed above.
- Do not include any additional text, tools, or code.
- Provide only the Python list as your answer.

Example output format: {objects}""",
    """Given an image containing exactly {num_objects} objects:
{objects_string}

Task:
1. Analyze the spatial relationships between these objects.
2. Find the shortest path that:
   a. Starts at the {start_color} object
   b. Visits each object exactly once
3. Return the optimal order as a Python list of objects.

Requirements:
- Use only the {num_objects} objects listed above.
- Do not include any additional text, tools, or code.
- Provide only the Python list as your answer.
- The list must start with {start_color}.

Example output format: {objects}"""
]


TSP_QUESTION_TEMPLATES_NOCODE = [
    # "This image contains five colored objects: yellow, red, green, blue, and purple. Solve the Traveling Salesman Problem (TSP) by finding the shortest path that visits each object once. Return the order of colors in the optimal path as a Python list.",
    # "In this image, there are five colored objects: yellow, red, green, blue, and purple. Find the shortest path that visits each object exactly once to solve the Traveling Salesman Problem (TSP). Return the optimal sequence of colors as a Python list.",
    # "You have an image with five colored objects: yellow, red, green, blue, and purple. Your task is to solve the TSP by finding the shortest path that visits each object once. Return the colors in the order of the optimal path as a Python list.",
    # "This image shows five colored objects: yellow, red, green, blue, and purple. Solve the TSP by determining the shortest path that visits each object exactly once. Provide the order of colors in the optimal path as a Python list."
    # "This image has five colored objects: yellow, red, green, blue, and purple. Your task is to solve the Traveling Salesman Problem (TSP) by finding the shortest path that visits each object exactly once. Return the optimal order of the objects as a Python list of colors."
    
    # "The image shows five colored objects: yellow, red, green, blue, and purple. Based on the image, reason over the spatial relationships between the objects and find the shortest path that visits each object exactly once. Return the optimal order of the objects as a Python list of colors without using tools or code.",
    # "The image shows five colored objects: yellow, red, green, blue, and purple. Based on the image, reason over the spatial relationships between the objects and find the shortest path that starts at the yellow object and visits each object exactly once. Return the optimal order of the objects as a Python list of colors without using tools or code."

    """Given an image containing exactly {num_objects} objects:
{objects_string}

Task:
1. Analyze the spatial relationships between these objects.
2. Determine the shortest path that visits each object exactly once.
3. Return the optimal order as a Python list of objects.

Requirements:
- Use only the {num_objects} objects listed above.
- Do not include any additional text, tools, **directly provide reasoning and don't write any code**.
- Provide only the Python list as your answer.

Example output format: {objects}""",
    """Given an image containing exactly {num_objects} objects:
{objects_string}

Task:
1. Analyze the spatial relationships between these objects.
2. Find the shortest path that:
   a. Starts at the {start_color} object
   b. Visits each object exactly once
3. Return the optimal order as a Python list of objects.

Requirements:
- Use only the {num_objects} objects listed above.
- Do not include any additional text, tools, **directly provide reasoning and don't write any code**.
- Provide only the Python list as your answer.
- The list must start with {start_color}.

Example output format: {objects}"""
]






############################## Shortest DATA ##############################

SHORTEST_QUESTION_TEMPLATES_26B = ["""The image shows a grid graph where each node is labeled (N1, N2, ... N{n}) and connected to neighboring nodes. Based on the image, find the shortest path from the start node (green) to the end node (red) without loops or backtracking. Don't use any tools, **don't write any code**. Directly return the solved shortest path in a list format. Example output format: ["Na", "Nb", "Nc"].
"""]



SHORTEST_QUESTION_TEMPLATES = [
    "The image displays a grid graph where each node is connected to its neighboring nodes to the up, down, left, and right. Base on the image, reason over the spatial relationships between the objects nodes and find a shortest path from the start node (green) to the end node (red) without using tools or code. Please return the sequence of movements as a Python list, where each movement is one of the following directions: ['up', 'down', 'left', 'right'].",
    
    """The image displays a grid graph where each node is labeled with text (N1, N2, ... N{n}) and connected to its neighboring nodes in the up, down, left, and right directions. 
    Based on the image, reason over the spatial relationships between the nodes and find the shortest path from the start node (green) to the end node (red) without using tools or code. 
Please follow these instructions to solve the path from the start node to the end node:
1. Let's think step by step.
2. Select the shortest path from the starting node to the end node without any loops or backtracking.
3. At each reasoning step, output the following details:
- Step number
- Current node and the end node
- The neighboring nodes of the current node, and their positions relative to the current node.
- Action decision: indicate which action to take (left, right, up, down) which node to arrive at.
4. After completing the reasoning, summarize the solved path as a list of node labels in a Python list format: [node1 text label, node2 text label, ...].""",

    """Given an image of a grid graph with the following properties:

1. Nodes:
   - Represented by coordinates (x, y) or labeled text (N1, N2, ..., N{n})
   - Connected to neighboring nodes in four directions:
     * Up:    (x, y+1)
     * Down:  (x, y-1)
     * Left:  (x-1, y)
     * Right: (x+1, y)

2. Special Nodes:
   - Start node: Green, located at coordinate {start_coord}, label: {start_label}
   - End node:   Red, located at coordinate {end_coord}, label: {end_label}
   
Please follow these instructions to solve the path from the start node to the end node:
1. Let's think step by step.
2. Select the shortest path from the starting node to the end node without any loops or backtracking.
3. At each reasoning step, output the following details:
- Step number
- Current node and the end node
- The neighboring nodes of the current node, and their positions relative to the current node.
- Action decision: indicate which action to take (left, right, up, down) which node to arrive at.
4. After completing the reasoning, summarize the solved path as a list of node labels in a Python list format: [node1 text label, node2 text label, ...].""",
"""The image shows a grid graph where each node is labeled (N1, N2, ... N{n}) and connected to neighboring nodes. Based on the image, find the shortest path from the start node (green) to the end node (red) without loops or backtracking.
return the solved shortest path in a Python list format. Example ourput format: ["Na", "Nb", "Nc"].
"""
]



############################## UP DATA ##############################

UP_QUESTION_TEMPLATES = [
    "Select the option that correctly describes the image. {options}\nRespond with the correct option letter in \\boxed{{option}}.",
    "Which option best describes the scene in the image? {options}\nReply with the right option letter in \\boxed{{option}}.",
    "Choose the most accurate caption for the image. {options}\nAnswer with the correct option letter in \\boxed{{option}}.",
    "Identify the correct description of the image. {options}\nRespond with the correct option letter in \\boxed{{option}}.",
    "Pick the correct option that matches the image. {options}\nReply with the correct option letter in \\boxed{{option}}."
]

UP_QUESTION_COT_TEMPLATES = [
    "Select the option that correctly describes the image. {options}\nLet's think step by step, reason through the spatial relationships of objects in the options, and respond with the correct option letter in \\boxed{{option}}.",
    "Which option best describes the scene in the image? {options}\nLet's think step by step, reason through the spatial relationships of objects in the options, and respond with the correct option letter in \\boxed{{option}}.",
    "Choose the most accurate caption for the image. {options}\nLet's think step by step, reason through the spatial relationships of objects in the options, and respond with the correct option letter in \\boxed{{option}}.",
    "Identify the correct description of the image. {options}\nLet's think step by step, reason through the spatial relationships of objects in the options, and respond with the correct option letter in \\boxed{{option}}.",
    "Pick the correct option that matches the image. {options}\nLet's think step by step, reason through the spatial relationships of objects in the options, and respond with the correct option letter in \\boxed{{option}}."
]





############################## COCO / VG DATA ##############################


COVG_QUESTION_TEMPLATES = [
    "Select the option that correctly describes the image. Options: A: {A}. B: {B}. \nRespond with the correct option letter in \\boxed{{option}}.",
    "Which option best describes the scene in the image? Selections: A: {A}. B: {B}. \nReply with the right option letter in \\boxed{{option}}.",
    "Choose the most accurate caption for the image. Options: A: {A}. B: {B}. \nAnswer with the correct option letter in \\boxed{{option}}.",
    "Identify the correct description of the image. Selections: A: {A}. B: {B}. \nRespond with the correct option letter in \\boxed{{option}}.",
    "Pick the correct option that matches the image. Options: A: {A}. B: {B}. \nReply with the correct option letter in \\boxed{{option}}."
]



COVG_QUESTION_TEMPLATES_LLAVA = [
    # "Select the option that correctly describes the image. Options: A: {A}. B: {B}. \nReply with 'A' or 'B'",
    # "Which option best describes the scene in the image? Selections: A: {A}. B: {B}. \nReply with 'A' or 'B'",
    # "Choose the most accurate caption for the image. Options: A: {A}. B: {B}. \nReply with 'A' or 'B'",
    # "Identify the correct description of the image. Selections: A: {A}. B: {B}. \nReply with 'A' or 'B'",
    # "Pick the correct option that matches the image. Options: A: {A}. B: {B}. \nReply with 'A' or 'B'"
    "Select the option that correctly describes the image. Options: A: {A}. B: {B}. \nRespond with the correct option letter in \\boxed{{option}}.",
    "Which option best describes the scene in the image? Selections: A: {A}. B: {B}. \nReply with the right option letter in \\boxed{{option}}.",
    "Choose the most accurate caption for the image. Options: A: {A}. B: {B}. \nAnswer with the correct option letter in \\boxed{{option}}.",
    "Identify the correct description of the image. Selections: A: {A}. B: {B}. \nRespond with the correct option letter in \\boxed{{option}}.",
    "Pick the correct option that matches the image. Options: A: {A}. B: {B}. \nReply with the correct option letter in \\boxed{{option}}."
]


############################## VROOMS DATA ##############################

VROOMS_QUESTION_TEMPLATES = [
    """Given a top-view image of an indoor scene, the graph represents the floor plan where:

- **Nodes** correspond to objects in the rooms.
- **Edges** represent the possible paths connecting these objects.

Your task is to navigate from the **{start_obj}** (node **{start_node}**) to the **{end_obj}** (node **{end_node}**) by moving along the edges that connect the nodes.

Please follow these instructions to solve the path from the start node to the end node:
1. Let's think step by step.
2. Select the shortest path from the starting node to the end node without any loops or backtracking.
3. At each reasoning step, output the following details:
- Step number
- Current node and the end node
- The neighboring nodes (connected through edges) of the current node, and their positions relative to the current node.
- Action decision: indicate which action to take and which node to arrive at.
4. After completing the reasoning, summarize the solved path as a list of node labels in a Python list format (e.g., ["N1", "N2", ...]).""",
    """Given a top-view image of an indoor scene, the graph represents the floor plan where:

- **Nodes** correspond to objects in the rooms.
- **Edges** represent the possible paths connecting these objects.

Network Description (Each item indicates an edge connecting two nodes): 
{network}

Your task is to navigate from the **{start_obj}** (node **{start_node}**) to the **{end_obj}** (node **{end_node}**) by moving along the edges that connect the nodes.

Please follow these instructions to solve the path from the start node to the end node:
1. Let's think step by step.
2. Select the shortest path from the starting node to the end node without any loops or backtracking.
3. At each reasoning step, output the following details:
- Step number
- Current node and the end node
- The neighboring nodes (connected through edges) of the current node, and their positions relative to the current node.
- Action decision: indicate which action to take and which node to arrive at.
4. After completing the reasoning, summarize the solved path as a list of node labels in a Python list format (e.g., ["N1", "N2", ...])."""
]