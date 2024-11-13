'use client'
import * as React from 'react';
import {Box, Grid, Typography} from '@mui/material';


export default function AboutPrimeVision() {
    <Box component="main" sx={{ p: 10, paddingTop: 20 }}>
    <Grid container spacing={4}>
    <Grid item xs={12} md={5} sx={{display: 'flex', flexDirection: 'column', justifyContent: 'center' }}>
        <Typography variant="h4">
        About Prime Vision
        </Typography>
        <Typography variant="body1">
        Prime Vision a global leader in computer vision integration and robotics for logistics and fulfillment. They operate fleets of autonomous package sorting robots to automate warehouses across the nation and abroad.
        </Typography>
    </Grid>
    <Grid item xs={12} md={7}>
        <Box
        component="img"
        sx={{
            height: 400,
            width: '100%',
            maxHeight: { xs: 233, md: 400 },
            maxWidth: { xs: 350, md: '100%' },
        }}
        alt="Prime Vision Robots"
        src="autographic.png"
        />
    </Grid>
    </Grid>
    </Box>
};