import React, { useState } from 'react';
import { CopyToClipboard } from 'react-copy-to-clipboard';
import { Button, Box, Typography } from '@mui/material';
import { Light as SyntaxHighlighter } from 'react-syntax-highlighter';
// Import the Python language syntax
import python from 'react-syntax-highlighter/dist/esm/languages/hljs/python';
// Import a light theme (e.g., `github` light theme)
import { atomOneLight } from 'react-syntax-highlighter/dist/esm/styles/hljs';

// Register the Python language
SyntaxHighlighter.registerLanguage('python', python);

export default function SimPopUp({ code }) {
  const [isCopied, setIsCopied] = useState(false);

  const handleCopy = () => {
    setIsCopied(true);
    setTimeout(() => setIsCopied(false), 1500); // Reset after 1.5 seconds
  };

  return (
    <Box sx={{ 
      boxShadow: 3, 
      backgroundColor: '#f5f5f5', 
      paddingBottom: '10px',
      borderBottomLeftRadius: "5px",
      borderBottomRightRadius: "5px",
      zindex: 1300 }}>
      {/* Top gray bar with Copy button and language */}
      <Box sx={{
        backgroundColor: '#D3D3D3',
        width: "100%",
        height: "40px",
        borderTopLeftRadius: "5px",
        borderTopRightRadius: "5px",
        display: "flex",
        justifyContent: "space-between", // Spreads copy button and language
        alignItems: "center",
        paddingRight: "10px",
        paddingLeft: "10px"
      }}>
        <Typography variant="body2" sx={{ fontWeight: 'bold', color: '#000000' }}>
          Python
        </Typography>
        <CopyToClipboard text={code} onCopy={handleCopy}>
          <Button variant="text" sx={{
            fontWeight: "bold", color: "#000000", textTransform: "none" // Keeps "Copy" not all caps
          }}>
            {isCopied ? "Copied!" : "Copy"}
          </Button>
        </CopyToClipboard>


      </Box>

      {/* Syntax Highlighter */}
      <Typography>
        {code}
      </Typography>
    </Box>
  )};