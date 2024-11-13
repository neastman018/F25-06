from fastapi import FastAPI, WebSocket, WebSocketDisconnect, File, UploadFile
from fastapi.responses import HTMLResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import time
from .mongo import Mongo
from colorama import Fore, Style, init
from io import BytesIO
from datetime import datetime
import ast
from fastapi.responses import JSONResponse
import json

app = FastAPI()
mongo = Mongo()

init(autoreset=True)
print(f"{Fore.GREEN}Mongo Should have upload logs{Style.RESET_ALL}")


origins = [
    "http://localhost:3000",
    "localhost:3000"
]

class VariableModel(BaseModel):
    independent: str
    dependent: list[str]

class LogModel(BaseModel):
    files: list[dict]
    files_uploaded: bool = False

class SearchModel(BaseModel):
    search: str
    deleteFile: int = -1


app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)


class ConnectionManager:
    def __init__(self):
        self.active_connections: list[WebSocket] = []
    
    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)

    async def send_personal_message(self, message: str, websocket: WebSocket):
        await websocket.send_text(message)
    
    #broadcasts to everyone awaiting messages
    async def broadcast(self, message: str):
        for connection in self.active_connections:
            await connection.send_text(message)

    
manager = ConnectionManager()

@app.get("/", tags=["todos"])
async def get_variables(variables: VariableModel) -> dict:
    return {  
        "independent": variables.independent,
        "dependent": variables.dependent  
        }

@app.post("/", tags=["root"])
async def reads(variables: VariableModel):
    print(f" ind:{variables.independent} dep:{variables.dependent}")

    graph_base64 = mongo.graph_data(variables.independent, variables.dependent)
    time.sleep(0.5)

    to_return = {
        "encoded_graph": graph_base64,
        "independent": variables.independent,
        "dependent": variables.dependent
    }
    return JSONResponse(content=to_return)



@app.get("/logs", tags=["todos"])
async def get_variables(variables: LogModel):
    return {
        "files": variables.files,
        "tosubmit": variables.tosubmit
    }

@app.post("/logs", tags=["root"])   
async def read(variables: LogModel):
    print("_---------------------------------------")
    uploaded = False
    for log in variables.files:
        data_string = str(log)  
        data_dict = ast.literal_eval(data_string)
        print(f"Data type of data_dict: {type(data_dict)}")
        with open("log.json", "w") as json_file:
            json.dump(data_dict, json_file, indent=4)
        with open("log.json", "r") as json_file:
            data = json.load(json_file)
            uploaded = mongo.upload_logs(data)
    time.sleep(2)
    variables.files = []
    print("-------------Clear Files-------------")
    # variables.files_uploaded = True
    


    to_return = {
        "files": None,
        "files_uploaded": uploaded,
    }

    return JSONResponse(content=to_return)
    
@app.get("/search", tags=["todos"])
async def get_variables(variables: SearchModel):
    return {  
        "search": variables.search
        }

@app.post("/search", tags=["root"])
async def reads(variables: SearchModel):

    if variables.deleteFile is type(None):
        print("No value found for delete")
    else: print(f"Deleting Files at index {variables.deleteFile}")

    print(f" Search:{variables.search}")
    files_to_return = mongo.search_logs(variables.search)
    print(f"Number of Files Returned: {len(files_to_return)}")

    if 0 <= variables.deleteFile < len(files_to_return):
        mongo.delete_log(files_to_return[variables.deleteFile])
        del files_to_return[variables.deleteFile]

    if variables.deleteFile == -10:
        mongo.clear_logs()
        print("Deleting All Files")
        
    file_names = [file["Simulation Name"] for file in files_to_return]
    # Assuming files_to_return contains MongoDB documents
    json_files = [json.dumps({**file, "_id": str(file["_id"])}) for file in files_to_return]
    print(f"Number of Json Files Returned: {len(files_to_return)}")
    
    to_return = {
        "file_names": file_names,
        "json_files": json_files
    }

    return JSONResponse(content=to_return)
    