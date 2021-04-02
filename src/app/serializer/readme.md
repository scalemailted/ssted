# Serializer:

## Description:
This package contains all python scripts used to serialize a Spatial-Temporal Network

## Modules List:
- dat
- json
- network_writer

## Modules Summary:
- **dat:**
    + requires: networkx
    + description: reads dat filetype & deserializes into stted
    + suggestions: refactor & remove this dependency, only used by geometric ssteds. (artifact of origin build).

- **json:**
    + requires: networkx
    + description: writes json file from dat file
    + suggestions: refactor & remove this dependency, only used by geometric ssteds. (artifact of origin build).

- **network_writer:**
    + requires: models.network
    + description: converts ssted into a list of JSONs or JSON files 
    + suggestions: refactor script to only having writing logic











