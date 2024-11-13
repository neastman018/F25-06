import pymongo
import pandas as pd
import os
import json
import glob
import numpy as np
from colorama import Fore, Back, Style
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import pymongo.errors
import seaborn as sb
import base64
from io import BytesIO
from datetime import datetime
from random import random
algorithms = ['A*', 'D*', 'RandomTree', 'A* with ML', 'D* with ML', 'RandomTree with ML']
floor_plans = ['floor plan 1', 'floor plan 2', 'floor plan 3', 'floor plan 4', 'floor plan 5']


"""
Class for to deal with the Mongo Database
This class is responsible for:
    -committing and upload logs to the database
    -grabbing data from the database
    -graphing data from the database
"""


class Mongo:
    """
    Inializes the Mongo class
        - Connects to database
    """
    def __init__(self):
        self.label_size = 14
        self.title_size = 20
        self.graph_height = 6
        self.graph_width = 12

        print(f"{Fore.CYAN}Attempting to connect to the database...{Style.RESET_ALL}")

        try:
            uri = os.environ.get('MONGO_URI', 'mongodb://mongoAdmin:m0ng0passw0rd@mongo:27017')
            if uri is not None:
                print(f"{Fore.CYAN}Found Mongo URI in the environment: {uri}{Style.RESET_ALL}")
                self.client = pymongo.MongoClient(uri)
                self.db = self.client.get_database('MDE')
                self.simStats = self.db['simulationStatistics']
                print(f"{Fore.GREEN}Connected to the database{Style.RESET_ALL}")

                # Create a default MDE database
                # self.db = self.client.get_database('MDE')
                # self.simStats = self.db['simulationStatistics']

            else: 
                print(f"{Fore.RED}Could not find Mongo URI in the environment{Style.RESET_ALL}")
                raise Exception("Cound not find Mongo URI in the environment")
        except Exception as e:
            print(f"{Fore.RED}Error connecting to the database: {e}{Style.RESET_ALL}")
            raise Exception(f"Error connecting to the database: {e}")


    """
    Function to change the commit variable to true for all the JSON files in the data folder
    """
    def commit_logs(self):
        data_folder = 'app/data'

        # Get all JSON files in the data folder
        file_pattern = os.path.join(data_folder, '*.json')
        json_files = glob.glob(file_pattern)

        for filename in json_files:
            try:
                # Get the data from the JSON file
                with open(filename) as file:
                    data = json.load(file)

                # Change the commit variable to true
                data['commit'] = True

                # Write the updated data back to the JSON file
                with open(filename, 'w') as file:
                    json.dump(data, file)

                print(f"{Fore.RED}Commit variable changed to true for {filename}{Style.RESET_ALL}")

            except FileNotFoundError:
                print(f"{Fore.RED}The file {filename} does not exist{Style.RESET_ALL}")

            except json.JSONDecodeError:
                print(f"{Fore.RED}Error decoding JSON from the file {filename}{Style.RESET_ALL}")

            except OSError as e:
                print(f"{Fore.RED}OS error for {filename}: {e}{Style.RESET_ALL}")
    """
    Function to upload all committed logs to the Mongo Database
    """
    """
    Function to upload all committed logs to the Mongo Database
    @param log is a string that needs to be converted to json
    """
    def upload_logs(self, log)->bool:
        files_commited = 0
        # data = None
        # try:
        #     data = json.loads(log)
        # except json.JSONDecodeError as e:
        #     print(f"{Fore.RED}Error decoding log to JSON: {e}{Style.RESET_ALL}")
        #     return

        
        if isinstance(log, dict):
    # Proceed with uploading to MongoDB
            insert_result = self.simStats.insert_one(log)
        else:
            raise TypeError(f"Expected a dictionary but got {type(log)} instead")

        # Acknoledge f the data is inserted successfully
        if insert_result.acknowledged:
            print(f"{Fore.GREEN}Data has been inserted successfully{Style.RESET_ALL}")
            files_commited += 1
        else:
            print(f"{Fore.RED}Data insertion failed{Style.RESET_ALL}")
            return False
            
        print(f"{Fore.GREEN}Total files uploaded: {files_commited}{Style.RESET_ALL}")
        if files_commited > 0:
            return True

    # def upload_logs(self):
    #     files_commited = 0

    #     data_folder = 'app/data'
    #     cwd = os.getcwd()
    #     print(f"Uploading files from: {cwd + '/' + data_folder}")

    #     # Get all JSON files in the data folder
    #     file_pattern = os.path.join(data_folder, '*.json')
    #     json_files = glob.glob(file_pattern)

    #     for filename in json_files:

    #         try:
    #             # Get the data from the JSON file
    #             with open(filename) as file:
    #                 data = json.load(file)

    #             # Check if the commit variable is true
    #             if data.get('commit'):
    #                 try:
    #                     # Insert the data into the database
    #                     insert_result = self.simStats.insert_one(data)

    #                     # If the data is inserted successfully, remove the file
    #                     if insert_result.acknowledged:
    #                         print(f"{Fore.GREEN}Data from {filename} inserted successfully{Style.RESET_ALL}")
    #                         files_commited += 1
    #                         os.remove(filename)
    #                     else:
    #                         print(f"{Fore.RED}Data insertion failed for {filename}{Style.RESET_ALL}")
    #                 except pymongo.errors.PyMongoError as e:
    #                     print(f"{Fore.RED}Database error for {filename}: {e}{Style.RESET_ALL}")
    #                 except FileNotFoundError:
    #                     print(f"{Fore.RED}The file {filename} does not exist{Style.RESET_ALL}")
    #                 except json.JSONDecodeError:
    #                     print(f"{Fore.RED}Error decoding JSON from the file {filename}{Style.RESET_ALL}")
    #                 except OSError as e:
    #                     print(f"{Fore.RED}OS error for {filename}: {e}{Style.RESET_ALL}")           
    #         except pymongo.errors.PyMongoError as e:
    #             print(f"{Fore.RED}Database error for {filename}: {e}{Style.RESET_ALL}")
    #         except FileNotFoundError:
    #             print(f"{Fore.RED}The file {filename} does not exist{Style.RESET_ALL}")
    #         except json.JSONDecodeError:
    #             print(f"{Fore.RED}Error decoding JSON from the file {filename}{Style.RESET_ALL}")
    #         except OSError as e:
    #             print(f"{Fore.RED}OS error for {filename}: {e}{Style.RESET_ALL}")
    #     print(f"{Fore.GREEN}Total files uploaded: {files_commited}{Style.RESET_ALL}")

    """ Simple Method that usese the most basic commands to see if I am even connected to the database"""
    def basic_find(self):
        data = self.simStats.find()
        for doc in data:
            print(doc)
    
    """Clears all logs in the database"""
    def clear_logs(self, log=None):
        if log is None:
            try:
                result = self.simStats.delete_many({})
                print(f"{Fore.GREEN}Deleted {result.deleted_count} logs from the database{Style.RESET_ALL}")
            except pymongo.errors.PyMongoError as e:
                print(f"{Fore.RED}Error deleting logs from the database: {e}{Style.RESET_ALL}")
        else:
            try:
                result = self.simStats.delete_one(log)
                print(f"{Fore.GREEN}Deleted 1 log from the database{Style.RESET_ALL}")
            except pymongo.errors.PyMongoError as e:
                print(f"{Fore.RED}Error deleting log from the database: {e}{Style.RESET_ALL}")

    """
    Grabs all the values of a dependent variable based on an independent variable and 
    packages them into an array
    ind Example: {'algorithm': 'A*'}
    dep Example: {'avgTimePerPackage': 1}
    """
    def grab_data(self, ind:dict, dep:dict):
        # dep_term appends the name of the dependent variable to the string 'simulation results. to find in the database'
        dep_term = 'simulation results.' + list(dep.keys())[0]
        
        numbers = []
        
        key = list(ind.keys())[0]
        value = list(ind.values())[0]
        # need to change numpy int32 to int or mongo will not find any values
        if isinstance(value, np.int32) or isinstance(value, np.int64):
            value = int(value)
             
        data = self.simStats.find({key: value}, {dep_term: 1})
        for doc in data:
            numbers.append(doc['simulation results'][list(dep.keys())[0]])
        
        return numbers
   
    
    """
    Does the same thing as grab_data but averages the data
    """
    def grab_avg_data(self, ind:dict, dep:dict):
        data = self.grab_data(ind, dep)
        return sum(data)/len(data)

    """
    Grabs each the independent variable values and dependent variable averages and makes a multi-dimensional array
    ind Example: 'algorithm'
    dep Example: 'avgTimePerPackage'
    """
    def grab_single_dependent(self, ind: str, dep: str):
        search_results = {ind: [], dep: []}

        # find the number of different values there is for the independent variablesi
        print(f"{Fore.GREEN}ind: {ind}{Style.RESET_ALL}")
        data = self.simStats.find({ind: {"$exists": True}})

        # Used for testing, commit out when sure it works properly
        # print(f"{Fore.GREEN}Printing Documents{Style.RESET_ALL}")
        # for doc in data:
        #     print(doc)
        #=========================================================
        #should all unique values of the independent variable, having problems with this line.
        variable_values = np.array(list(set([doc[ind] for doc in data])))   
        print(f"variable_values = {variable_values}") 

        for var in variable_values:
            print({ind: var}, {dep: 1})
            dep_value = self.grab_avg_data({ind: var}, {dep: 1}) # grab_avg_data is looking for var to be a string but it is an int
            search_results[ind].append(var)
            search_results[dep].append(round(dep_value,1))
        print(f"search_results = {search_results}")
        return search_results

    """
    Grabs each the independent variable values and multiple dependent variable averages and makes a multi-dimensional array
    ind Example: 'algorithm'
    deps Example: ['avgTimePerPackage', 'packagesHourRobots']
    """
    def grab_multiple_dependents(self, ind:str, deps:list):
      
        search_results = {ind: [], "data": [], "Legend": []}

        data = self.simStats.find({ind: {"$exists": True}})
        variable_values = np.array(list(set([doc[ind] for doc in data])))    
        for dep in deps:
            for var in variable_values:
                search_results[ind].append(var)
                search_results["data"].append(round(self.grab_avg_data({ind: var}, {dep: 1}),1))
                search_results["Legend"].append(dep)
         
        print(f"search_results = {search_results}")
        return search_results

    """ 
    Combines the two previous methods into one method based on user input 
    when uploading from the website the deps is always a list, therefore grab_multiple_dependents is always called
    """
    def grab_all_data(self, ind: str, deps):
        if isinstance(deps, str): #if dep is string (only happens during testing w/o frontend)
            print(f"Grabbing single dependent variable (str): {deps}")
            return self.grab_single_dependent(ind, deps)
        # elif isinstance(deps, list) and len(deps) == 1: #happens if frontend only selects 1 dependent variable
        #     print(f"Grabbing single dependent variables (list): {deps}")
        #     return self.grab_single_dependent(ind, deps)
        elif isinstance(deps, list): #happends if frontend selects multiple dependent variables
            print(f"Grabbing multiple dependent variables: {deps}")
            return self.grab_multiple_dependents(ind, deps)
        else: 
            print("Invalid dependent variable type")
            return []

    """
    Method to grab the data of a continuous variable from the database
    NOT CURRENTLY IN USE
    """
    def grab_cont_data(self, ind, dep):
        data = self.simStats.find({ind: {"$exists": True}})
        search_results = {ind: [], dep: []}
        for doc in data:
            search_results[ind].append(doc[ind])
            search_results[dep].append(doc['simulation results'][dep])
        
        return search_results    


    # Method to grab all the logs from the database
    def get_all_logs(self):
        try:
            data = self.simStats.find({})
            print(f"{Fore.GREEN}Retrieved logs from the database{Style.RESET_ALL}")
            for doc in data:
                print(type(doc))
            return data
        except pymongo.errors.PyMongoError as e:
            print(f"{Fore.RED}Error retrieving logs from the database: {e}{Style.RESET_ALL}")
            return []
        
    """
    Method to parse all documents and search for a string
    @param search_str: The string to search for in the documents
    """
   
    def search_logs(self, search_str):
        numFiles = 0
        files = []
        try:
            data = self.simStats.find({})
            for doc in data:
                if search_str in str(doc):
                    numFiles += 1
                    files.append(doc)

        except pymongo.errors.PyMongoError as e:
            print(f"{Fore.RED}Error retrieving logs from the database{Style.RESET_ALL}")
            return []
        if (numFiles == 0):
            print(f"{Fore.RED}No logs found containing the string '{search_str}'{Style.RESET_ALL}")
        print(f"{Fore.GREEN}Found {numFiles} logs containing the string '{search_str}'{Style.RESET_ALL}")
        return files
    
    def delete_log(self, log):
        try:
            result = self.simStats.delete_one(log)
            print(f"{Fore.GREEN}Deleted 1 log from the database{Style.RESET_ALL}")
        except pymongo.errors.PyMongoError as e:
            print(f"{Fore.RED}Error deleting log from the database: {e}{Style.RESET_ALL}")

#============================================================================================================================================================================================= 
# Graphing Methods
#=============================================================================================================================================================================================

    

    def bar_graph(self, ind, dep):
        dataset = pd.DataFrame(self.grab_all_data(ind, dep))

        fig = plt.figure(figsize=(self.graph_width, self.graph_height))
        if isinstance(dep, str):
            # Set Y-axis bounds
            max_y = dataset[dep].max()
            bound_y = max_y - (max_y % 5) + 5 # rounds max_y up to the nearest multiple of 5

            # Create a bar chart using seaborn
            sb.barplot(data=dataset, x=ind, y=dep, color="#861F41")

            plt.xlabel(ind, fontsize=self.label_size)
            plt.ylim(0, bound_y)
            plt.yticks(np.arange(0, bound_y + 1, bound_y / 10))
            plt.ylabel(dep, fontsize=self.label_size)
            plt.title(f"{dep} vs {ind}", fontsize=self.title_size)
            plt.show()
            # Save the plot to a BytesIO object
            plt.savefig(os.path.join('app/data', 'graph.png'))
            
            # Convert the graph to a PNG image and then encode it to base64
            buffer = BytesIO()
            plt.savefig(buffer, format="png")
            buffer.seek(0)
            image_png = buffer.getvalue()
            buffer.close()

            return base64.b64encode(image_png).decode('utf-8')
            
        if isinstance(dep, list):
            
            # Set Y-axis bounds
            #max_y = dataset[dep].max()
            #bound_y = np.ceil(max_y % 5) * 5 # rounds max_y up to the nearest multiple of 5

            # Create a bar chart using seaborn
            # y = data and hue = Legend are specificed in the grab_multiple_dependents method to put the dataset in the right format for seaborn
            sb.barplot(data=dataset, x=ind, y="data", hue="Legend", color="#861F41")

            plt.xlabel(ind)
            # plt.ylim(0, bound_y)
            # plt.yticks(np.arange(0, bound_y + 1, bound_y / 10))
            plt.ylabel("")
            # plt.title(f"{dep} vs {ind}")
            plt.show()
            
            # Save the plot to a BytesIO object
            plt.savefig(os.path.join('app/data', 'graph.png'))

            # Convert the graph to a PNG image and then encode it to base64
            buffer = BytesIO()
            plt.savefig(buffer, format="png")
            buffer.seek(0)
            image_png = buffer.getvalue()
            buffer.close()

            return base64.b64encode(image_png).decode('utf-8')


    def line_graph(self, ind, dep):
        dataset = pd.DataFrame(self.grab_all_data(ind, dep))
        fig = plt.figure(figsize=(self.graph_width,self.graph_height))
        if isinstance(dep, list):
            sb.scatterplot(data=dataset, x=ind, y="data", hue="Legend", color="#861F41")
            for i in range(len(dep)):
                sb.lineplot(data=dataset, x=ind, y="data", hue="Legend", color="#861F41", legend=False)
          
            plt.xlabel(ind)
            plt.ylabel(f"Average {dep}")
            plt.title(f"Average {dep} vs {ind}")
            plt.show()

            plt.savefig(os.path.join('app/data', 'graph.png'))

            # Convert the graph to a PNG image and then encode it to base64
            buffer = BytesIO()
            plt.savefig(buffer, format="png")
            buffer.seek(0)
            image_png = buffer.getvalue()
            buffer.close()
            return base64.b64encode(image_png).decode('utf-8')
    
        
        elif isinstance(dep, str):          
            # Calculate the average of dep for each unique value of ind
            unique_ind = sorted(dataset[ind].unique())
            print(unique_ind)
            avgValue = []
            for i in unique_ind:
                avgValue.append(dataset[dataset[ind] == i][dep].mean())

            #print(avgValue)
            sb.scatterplot(x=unique_ind, y=avgValue, color="#861F41")

            # Plot the average values as a line graph
            sb.lineplot(x=unique_ind, y=avgValue, color="#861F41")
            # Add labels and title to the graph
            plt.xlabel(ind, fontsize=self.label_size)
            plt.ylabel(f"Average {dep}", fontsize=self.label_size)
            plt.title(f"Average {dep} vs {ind}", fontsize=self.title_size)
            plt.show()

            plt.savefig(os.path.join('app/data', 'graph.png'))            
            # Convert the graph to a PNG image and then encode it to base64
            buffer = BytesIO()
            plt.savefig(buffer, format="png")
            buffer.seek(0)
            image_png = buffer.getvalue()
            buffer.close()

            return base64.b64encode(image_png).decode('utf-8')
    """
    Method that brings together the line graph and bar graph methods based on the independent variable selected
    Also want it 
    """
    def graph_data(self, ind, dep):
        # If dep is a list with a single value make it a string
        if isinstance(dep, list) and len(dep) == 1:
            print(f"dep (list) (early) = {dep}")
            dep = dep[0]
            print(f"dep (str) (early) = {dep}")
            

        if ind == "Algorithm" or ind == "Floor Plan":
            print("Making Bar Graph")
            return self.bar_graph(ind, dep)
        elif ind == "Number of Robots" or ind == "Regional Reroute Radius" or ind == "Number of Nodes" or ind == "Number of Obstacles":
            print("Making Line Graph")
            return self.line_graph(ind, dep)
            

if __name__ == "__main__":
    mongo = Mongo()

    #print(mongo.grab_data({'Algorithm': 'A*'}, {'Average_Time_per_Package': 1}))
    # print('=========================================================================')
    #print(mongo.grab_avg_data({'Algorithm': 'A*'}, {'Average_Time_per_Package': 1}))
    # print('=========================================================================')
    #data = mongo.grab_single_dependent('Number_of_Nodes','Average_Time_per_Package')
    # print('=========================================================================')
    #print(mongo.grab_all_data('Number_of_Nodes','Average_Time_per_Package'))
    # print('=========================================================================')
    #data = mongo.grab_cont_data('Number of Robots', 'Number of Paths Rerouted per Stop')
    






# with open(filename) as file:
#     data = json.load(file)

# # Insert to Database
# insert_result = simStats.insert_one(data)

# # If the data is inserted successfully, remove the file
# if insert_result.acknowledged:
#     print('Data inserted successfully')
#     os.remove(filename)
# else: print("Data insertion failed")

#result = simStats.insert_many(data)

 # Read the data from the database
# docs = simStats.find()
# for doc in docs:
#     print(doc)