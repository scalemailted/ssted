# Generator:

## Description:
This package contains all python scripts used to randomly generate a Spatial-Temporal Network

## Modules List:
- burstiness
- gaussian
- generator_utils
- geometric (directory)
- power_law
- uniform

## Packages List:
- geometric


## Modules Summary:
 - **burstiness:**
    + requires: numpy, matplotlib
    + description: randomly generate an event on an edge in ssted network  
    + suggestions: group into package with other network ditributions: edge generators, event generators, node generators. This script needs refactoring! __Check what depeneds on this package__

 - **gaussian:**
    + requires: numpy, generator.generator_utils, models.network 
    + description: randomly generate nodal degrees exhibiting a gaussian distrubtion   
    + suggestions: group into package with other nodal degree ditributions: powerlaw, uniform, 

- **generator_utils:**
    + requires: models.network, networkx
    + description: utility methods to generate & evolve a ssted network given a list of nodal degrees  
    + suggestions: Remove networkx dependency, compute own positional data instead!

- **power_law:**
    + requires: numpy, generator.generator_utils, models.network
    + description: randomly generate nodal degrees exhibiting a powerlaw distrubtion   
    + suggestions: group into package with other nodal degree ditributions: uniform, gaussian

- **uniform:**
    + requires: numpy, generator.generator_utils, models.network
    + description: randomly generate nodal degrees exhibiting a uniform distrubtion   
    + suggestions: group into package with other nodal degree ditributions: powerlaw, gaussian

## Packages Summary:
- **geometric:**
    + description: randomly generates spatial temporal graphs based on spatial parameters   
    + suggestions: Refactor this into a smaller module











