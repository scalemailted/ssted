# *package:* Analyzer

## Description:
This package contains all python scripts used to perform analysis on a Spatial Temporal Network

## Modules List:
- analysis_nx
- analysis_teneto
- network_measures 

## Modules Summary:
- **analysis_nx:**
    + requires: networkX
    + description: converts network from ssted to networkx & executes networkX's network measures. 
    + suggestions: decompose script such that: conversion logic in serializer & nx measures here

- **analysis_teneto:**
    + requires: tenento
    + description: converts network from ssted to teneto & executes teneto's network measures. 
    + suggestions: decompose script such that: conversion logic in serializer & teneto measures here

 - **network_measures:**
    + requires: numpy
    + description: defintions for common st-network measures  
    + suggestions: cluttered codebase, remove commented code & class/functions that are depreciated.











