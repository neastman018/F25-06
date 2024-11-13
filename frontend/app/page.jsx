
'use client'
import Image from "next/image";
import styles from "./page.module.css";
import * as React from "react";
import {Box, Grid, Typography, Card} from "@mui/material";
import FlipCardLink from "./components/linkflipcard";


const components = [
  {
    title: "Prime Vision",
    description: `
        Click here to learn more about our customer by visiting their website.
        `,
    link: "https://primevision.com/",
  },
  {
    title: "Project Info",
    description: `
        Click here to learn more about the project.
        `,
    link: "./project",
  },
  {
    title: "Approach",
    description: `
        Click here to learn more about the approach we took to tackle the project.
        `,
    link: "./methodology",
  },
  {
    title: "Results",
    description: `
        Click here to learn more about the results of the project.
        `,
    link: "./results",
  },
  {
    title: "About Us",
    description: `
        Click here to learn more about our team.
        `,
    link: "./aboutus",
  },
]

export default function Home() {
  return (
    <main className={styles.main}>
      <Card
      sx={{
        backgroundColor: '#861F41', // Chicago maroon color hex code
        borderRadius: '16px', // Adjusts the corner rounding
        padding: '24px', // Adds padding to fit the text nicely
        paddingTop: '16px', // Adds padding to fit the text nicely
        paddingBottom: '16px', // Adds padding to fit the text nicely
        textAlign: 'center',
        color: 'white', // Changes the text color to white
        fontWeight: 'bold', // Makes the text bold
        margainBottom: '5px', // Adds space between the card and the next element
      }}
      >
      <Typography variant="h4">
      F24-06: State of the Art Robotic Motion Planning
      </Typography>
    </Card>
  
    <Image
        src="/VTLogo.png"
        alt="VT Logo"
        width={360}
        height={200}   
        style={{ marginTop: '0px' }} // Removes any extra margin on top of the image

    />
  
      
      <Box sx={{paddingTop: '5px' }}>
      <Grid container spacing={4}>
      {components.map((component, index) => (
        <FlipCardLink key={index} post={component}/>
      ))}
      </Grid>
      </Box>

    </main>
    );
}
