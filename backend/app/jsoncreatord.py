import json
import os
from datetime import datetime
import json
import os
from datetime import datetime
import random

num_files = 50
algorithms = ['A*', 'D*', 'RandomTree', 'A* with ML', 'D* with ML', 'RandomTree with ML']
floor_plans = ['floor plan 1', 'floor plan 2', 'floor plan 3', 'floor plan 4', 'floor plan 5']



# Data to be written to the JSON file
for i in range(num_files):
    print(i)
    data = {
        # Keys cannot have spaces or it will throw a conversion error when trying to query from Mongo
        "Simulation Name": str(i) + "_Test Simulation ",
        # "Simulation Conducted": datetime.now().strftime("%Y-%m-%d %H:%M:%S") + '_' + str(i),
        "Simulation Conducted": "Test Simulations",
        "Algorithm": random.choice(algorithms),
        "Floor Plan": random.choice(floor_plans),
        "Number of Robots": random.randint(1, 20),
        "Number of Nodes": random.randint(1, 500),
        "Regional Reroute Radius": random.randint(1, 5),
        "simulation results": {
            "Packages/Hour/Robot": random.randint(1, 20),
            "Average Time per Package": random.randint(30, 1000),
            "Emergency Stops per Obstacle": random.randint(1, 20),
            "Average Nodes per Path": random.randint(1, 20),
            "Average Length of Path": random.randint(1, 100),
            "Number of Paths Rerouted per Stop": random.randint(1, 10),
            "Calculation Time": random.randint(1, 1000),
        },
        "commit": False
    }

    # Specify the directory and filename
    directory = 'backend/app/data'
    filename = datetime.now().strftime("%Y-%m-%d_%H_%M_%S") + '_num' + str(i) + '_data.json'

    # Create the directory if it doesn't exist
    os.makedirs(directory, exist_ok=True)

    # Full path to the file
    filepath = os.path.join(directory, filename)

    # Write the data to a JSON file
    with open(filepath, 'w') as json_file:
        json.dump(data, json_file, indent=4)

    print(f"Data has been written to {filename}")


