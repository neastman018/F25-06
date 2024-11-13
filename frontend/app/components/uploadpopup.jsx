import React, { useEffect, useState } from "react";
import ClearIcon from '@mui/icons-material/Clear';
import UploadIcon from '@mui/icons-material/Upload';
import Typography from '@mui/material/Typography';
import Button from '@mui/material/Button'; 
import Box from '@mui/material/Box'; 
import CircularProgress from '@mui/material/CircularProgress';
import { useLogs } from '../hooks/get_logs';


export default function DragNDrop({onFilesSelected, width, height}) {
  const [files, setFiles] = useState([]);
  const [submittedFiles, setSubmittedFiles] = useState([]);
  
  const { data: acknowledged_files, isLoading, isError } = useLogs(submittedFiles);

    const handleFileChange = (event) => {
        // Changes the state of files to match those elected
        const selectedFiles = event.target.files;
        if (selectedFiles && selectedFiles.length > 0) {
        const newFiles = Array.from(selectedFiles);
        setFiles((prevFiles) => [...prevFiles, ...newFiles]);
        }
    };


    const handleDrop = (event) => {
        // Changes the dropped files to match all those selected
        event.preventDefault();
        const droppedFiles = event.dataTransfer.files;
        if (droppedFiles.length > 0) {
        const newFiles = Array.from(droppedFiles);
        setFiles((prevFiles) => [...prevFiles, ...newFiles]);
        }
    };

    const handleRemoveFile = (index) => {
        setFiles((prevFiles) => prevFiles.filter((_, i) => i !== index));
    };

    // This method uploads the submitted files but cannot clear them
    const handleUpload = (event) => {
        console.log('Files:', files.length)
        console.log("Submitted Files a:", submittedFiles.length)

        let firstIteration = true; // Want to make submitted files just the first file during the first iteration

        for (const file of files) {
            if (file.type === "application/json") {
                console.log('Parsing JSON File');
                const reader = new FileReader();
                reader.onload = (e) => {
                    try {
                        const json = JSON.parse(e.target.result); // Parse the JSON data
                        
                        if (firstIteration) {
                            // On first iteration, replace the state entirely
                            setSubmittedFiles([json]);
                            firstIteration = false; // After the first iteration, set flag to false
                        } else {
                            // On subsequent iterations, append the parsed JSON data
                            setSubmittedFiles((prevData) => [...prevData, json]);
                        }
                    } catch (error) {
                        console.error("Error parsing JSON:", error);
                    }
                };
                reader.readAsText(file); // Read file as text
            } else {
                console.error("Please upload a valid JSON file");
            }
        }
        setFiles([]) // This Clears the files selected
    };
        
    useEffect(() => {
        onFilesSelected(files);
    }, [files, onFilesSelected]);

    return (
        <Box sx={{
            width: width,
            height: height,
            backgroundColor: 'white',
            borderRadius: '6px',
            display: 'flex', // Flexbox for centering
            flexDirection: 'column', // Ensure items are in a column
            justifyContent: 'center', // Center content vertically
            alignItems: 'center', // Center content horizontally
            textAlign: 'center', // Center text inside the box
            zindex: 1300 
            }}>
            <Box
                className={`document-uploader ${
                    files.length > 0 ? "upload-box active" : "upload-box"
                }`}
                onDrop={handleDrop}
                onDragOver={(event) => event.preventDefault()}
            >
                
                {files.length > 0 ? (
                    <Button variant="contained" onClick={handleUpload} sx={{ textTransform: 'none', flexDirection: 'column', boxShadow: '4'}}>
                    <UploadIcon />
                    Upload
                </Button>
                ):(
                    <Button variant="contained" disabled sx={{ textTransform: 'none', flexDirection: 'column', boxShadow: '4'}}>
                    <UploadIcon />
                    Upload
                    </Button>
                )}
                <Typography sx={{fontSize:'16px', fontWeight:'bold', paddingTop:3}}>
                        Drag and Drop Your Simulation Files Here: 
                </Typography>
                <Typography sx={{fontSize:'16px', fontWeight:'bold', paddingTop:3}}>
                    Make Sure you close the popup before switching to another tab!
                </Typography>
                {isLoading ? (
                    <CircularProgress />
                ) : isError ? (
                    <Typography color="error">Error Sending Logs</Typography>
                ) : acknowledged_files?.files_uploaded && files.length != 0? (
                    <Typography color="success">Files Uploaded</Typography>
                ) :  files.length == 0 ?(
                    <Typography>Only Json Files Accepted</Typography>
                ) : null}
                <input
                    type="file"
                    hidden
                    id="browse"
                    onChange={handleFileChange}
                    accept=".json"
                    multiple
                />
                <label htmlFor="browse">
                    <Box sx={{p:1}}>
                    <Button variant="contained" component="span">
                        Browse Files
                    </Button>

                    </Box>
                </label>
            

                {files.length > 0 && (
                    <div className="file-list">
                        <div className="file-list__container">
                            {files.map((file, index) => (
                                <div className="file-item" key={index}>
                                    <div className="file-info">
                                        <p>{file.name}</p>
                                        {/* <p>{file.type}</p> */}
                                    </div>
                                    <div className="file-actions">
                                        <ClearIcon onClick={() => handleRemoveFile(index)} />
                                    </div>
                                </div>
                            ))}
                        </div>
                    </div>
                )}
            </Box>
        </Box>
    );
    };

