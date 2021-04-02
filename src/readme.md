# *package:* ssted

## Description:
stochastic spatial-temporal evolution dynamics (ssted) network toolset

## Packages List:
- app
- browser

## Modules List:
- launch
- tester


## Packages Summary:
- **app:**
    + description: ssted network toolset
    + suggestions: implement CLI user interface into this package

- **browser:**
    + description: browser frontend for ssted
    + suggestions: deploy as a web app   

## Modules Summary:
 - **launcher:**
    + requires: eel, app.controllers
    + description: Launcher for Browser verison of ssted toolset 
    + suggestions: none 

 - **tester:**
    + requires: app.controllers
    + description: Developer Tester module to issue headless requests to endpoints
    + suggestions: refactor into a CLI client to ssted toolset


