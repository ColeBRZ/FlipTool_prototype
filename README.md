# FlipTool_prototype

This is an idea for a software I have had since 2023. There are many software tools that help you flip houses or calculate certain things during the process. I am aiming to automate as much of this flipping process as I can and will be scaling this application. Currently it is just python code, however, in a future version I would like to add a user interface. I made a previous version of this application in Django with a UI, however, I do not see a website being what I want this app to perform on. What I am currently looking at is a PyQt5 GUI for a desktop application. Anyways, enough background information on the project.

The primary goal of this current bit of software is to web scrape data from zillows robots.txt site in which they provide sitemaps for web scraping all of their URL's. 

I used MySQL databasing and workbench to store and analyze the data I extracted.  

update_data.py & database_connection.py must be executed before data_extractor.py is executed. 

This is a prototype and the current generator function for processing the data into the database is a rough rendition. For a future iteration, I would like to delete prior file data so that the current program will work just fine with picking up where it left off. Currently, it does not pick up where you left off. You will have to delete the all zpid's in the .txt files that were already recorded in the database manually to start from where you left off. 

Currently, data_extractor.py does a good job of identifying possible flip homes by iteself. However, the program was made to extract "training" data for a machine learning model that would identify these houses more accurately. Given its success in finding many flip homes already, I thought it would be a good idea to post to Github. In addition to this, the program can used for whatever you would like, from analyzing market trends to training your models. So feel free to use and modify the code. 
