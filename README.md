# Team 7

Language Technology and Web Applications  
Fall Semester 2024

Code for team project

# Lang. Tech. Web Apps Project

Project for language technology web apps

## Goal Summary:

- Extract Information from learning resources
- Structure Information for categorical overview
- (Interactive) Visualization

## Planned Data Pipeline:

### Front-End File Upload

Upload Files on webpage
Group Files into same "project", corresponds to uni-module
Send Files to API backend

### Back-End Pipeline

in Python: Extract information from pdf
  OCR, Pdf text extraction
  Use file structure for basic categorization
  
Use python NLP modules to process and structure text information
  Topic Modelling, GenSim

Store structured/mapped data

### Database

Raw Text Files
Extracted and Segmented Text
Extracted and Structured Information

Relations between Text and Structured Information

### Front-End Visualization

Selection of "project"

visualize processed information
  Mindmap / Graph Structure
  
Interaction:
  Windows, Zoom, Selection
  Display Text/Source from Mindmap Node

## Tech Used:

### Python Modules

GenSim
Bokeh
Pdf Text Extraction

### Stack

Flask
PostgreSQL
JS Frontend
  Svelte if necessary?


---

URL of website: http://172.23.66.241:52091
(only accessible inside UZH network)

Database Connection URI: postgres://postgres:f0dbcdddbf78ef64f9e3d9e0febb9cc7@172.23.66.241:59172/team_project_7_db
