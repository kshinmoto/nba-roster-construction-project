# Comps-490, Data Analytics Web-App for NBA Roster Construction

## Description
The goal of this project is to create a web-app that uses data analytics to identify NBA teams' strengths and weaknesses, and suggest possible roster changes to improve those teams' roster constructions. This process is done by observing a team's league ranking in the [Four Factors](https://squared2020.com/2017/09/05/introduction-to-olivers-four-factors/) model, identifying players on their team potentially contributing to Four Factor deficiencies, and then suggesting players of a similar role from around the league who could positively impact the team's weaknesses in the Four Factors.

## Final Product Example
![top page](https://user-images.githubusercontent.com/60911325/145886322-5a3070e8-2814-4a37-ad34-589365f7847a.png)
![team roster web](https://user-images.githubusercontent.com/60911325/145885852-6f4bc05d-4174-470c-86d5-0fb177a553ae.png)
![Screenshot (25)](https://user-images.githubusercontent.com/60911325/145885571-fe9d8649-0bbe-438b-bbd2-135241267470.png)

## Requirements/Installation
Highlighted words link to installation guides for the designated applications/language. Installation guides aren't listed in readme for puposes of the organization and length of the readme.

### IDE and Applications:

- [Python](https://www.digitalocean.com/community/tutorial_series/how-to-install-and-set-up-a-local-programming-environment-for-python-3) (version 3.8.5 is used)
- Python IDE (project used [Spyder](https://docs.spyder-ide.org/current/installation.html) 4.1.5 and [PyCharm](https://www.jetbrains.com/help/pycharm/installation-guide.html) 2021.2.2)
- Ability to create and edit html files (project made and edited html 5 files in PyCharm IDE)
- [DB Browser for SQLite](https://sqlitebrowser.org/dl/) (version 3.12.2)
- Web Browser ([Google Chrome](https://chromeenterprise.google/browser/download/?utm_source=adwords&utm_medium=cpc&utm_campaign=2021-H2-chromebrowser-paidmed-paiddisplay-other-chromebrowserent&utm_term=downloadnow%23chrome-browser-download&utm_content=GCEJ&brand=GCEJ&gclid=CjwKCAiA-9uNBhBTEiwAN3IlNNLX4ywfEwf_bDGfA4QKs2jXSWsQbb-d-a8Ww0rzrvg96dRUELWk3xoCiYkQAvD_BwE&gclsrc=aw.ds#windows-tab) Version 96.0.4664.93)

### Python Packages:
The instructions to installing a python package onto your computer can be found [here](https://packaging.python.org/en/latest/tutorials/installing-packages/). The following Python packages were all used at some point during the project. The numbers following the packages represents the version used of the package.

- Pandas 1.1.3
- Numpy 1.19.2
- Sklearn 0.23.3
- from sklearn.preprocessing import StandardScaler
- from sklearn.decomposition import PCA
- from sklearn.cluster import KMeans
- from sklearn.metrics import silhouette_score
- import matplotlib.pyplot as plt (matplotlib 3.3.2)
- import unidecode
- import requests 2.24.0
- from bs4 import BeautifulSoup (bs4 4.9.3)
- from flask import Flask, render_template (flask 1.1.2)
- import sqlite3

## Running the Project

### Backend
We will start the project with the backend process of making our web-app. The objective of our backend is to use web-scraping to get the NBA player stats we need, and then use those stats to get the player recommendations we want our web-app to show. The first thing we need to do is make a folder/repository on our computer that will hold our project files. This is important for allowing our web-app to run properly. 

#### Backend Python File Order
- kmeans_nba.py
- basketballref_scrape.py
- clean_up.py
- copy_comps_algo.py

The first file we will need to run is the **kmeans_nba.py** file. The objective of this file is to use machine learning and kmeans clustering to categorize NBA players into roles. The roles will later be used in our process of suggesting players. When running this program there are a few important things we will need for the program to work correctly. First, we make sure that we have the python packages needed for the file (packages are shown in the py file and installation and versions are listed above). Second, this file uses web-scraping to collect stats from the [NBA stats site](https://www.nba.com/stats/), which means we will need internet connection. And last, an important piece of the program is intializing the headers at the beginning of the file. The headers are what allows us to access the stats on the NBA stats pages, so without the headers we will not be able to scrape any of the stats we need.

![headers](https://user-images.githubusercontent.com/60911325/145907537-fff9af1a-33bb-4927-86f7-58ef0d371905.png)

The next file we will be running is the **basketballref_scrape.py** file. This file is in charge of scraping all the necessary information that we will forming our tables in our web-app with, as well as attaching the player roles to each player that we created in the kmeans_nba.py file. The stats are scraped from [basketball-reference.com](https://www.basketball-reference.com/), [Cleaning the Glass](https://cleaningtheglass.com/) and the NBA stats site. This file uses web-scraping like the previous file, so you will need internet access to do the web-scraping, as well as the headers mentioned previously when scraping information from the NBA stats site. Feel free to build off of the web-scraping functions and scrape other stats you find relevant to the project. Another important part of this file that users looking to reproduce the product should know is that the file uses csv files to read in the player role information. This means you will need to change the code so that the pathway matches where your csv file holding player roles is located in your computer. 

![csv files](https://user-images.githubusercontent.com/60911325/145913844-1c34a9c5-9d2e-4454-bd6e-e2053ab16be1.png)

The third file we will run is the **clean_up.py** file. This file is in charge of adding player percentiles rank to every stat of our players based on their percentile ranking for the stat when compared to other players in the same role. Just like the previous file, the clean_up.py file also reads in csv files so make sure to change the pathways to your file path on your computer. After running the file we will have a csv file with all the current players in the NBA and their stats, along with percentile ranks for the players that were assigned a role. Once we finish making the csv of finalized percentiles and the player stats, we can then move on to our program in charge of player suggestions.

The last python file for our backend is the **copy_comps_algo.py** file. This file creates our three tables of suggested players based on their contract lengths, while also recording the stat headers related to the team's Four Factors weaknesses as well as the players on the team roster designated as potential players contributing to the areas of weakness. This file follows our trend of reading in csv files, so be sure to correct the file paths to the right file paths for your computer. With these four files set up, we should have the backend almost ready to go. Next is just creating our SQL database through DB Browser that will be used in the web-app. 

#### DB Browser
DB Browser is a program that allows us to make and edit a SQL database using the csv files that have our saved dataframes of player and Four Factor stats. The two csv files that we will be importing into our DB Browser are the concat_1_def_full.csv and df_ff.csv files. The concat_1_def_full.csv file holds all the player information along with their roles, stat percentiles, and salary information, while the df_ff.csv file holds the Four Factors stats and league rankings for every NBA team. When making this database make sure that it is **located in the same repository as the rest of our files for the project.**

![db browser](https://user-images.githubusercontent.com/60911325/145916352-69574743-3176-4ab7-aea1-1366a16029af.png)
Screenshot of how to import csv file

![db tables](https://user-images.githubusercontent.com/60911325/145916343-7d383202-d4f5-46ed-9541-6d2a5df0e2d2.png)

Screenshot of our database tables


### Frontend

