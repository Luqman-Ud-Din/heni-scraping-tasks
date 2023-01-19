# Heni Scraping Assessment

This codebase implements the tasks stated
in the file [JHA_Data_Engineer_Scraping_Assessment.html](JHA_Data_Engineer_Scraping_Assessment.html)

1. `Task 1. Parsing HTML` => [task1.py](task1.py)
1. `Task 2. Regex` => [task2.py](task2.py)
1. `Task 3. Web crawler` => [bearspace.py](artwork_scraper/artwork_scraper/spiders/bearspace.py) & [task3.py](task3.py)

   -- spider implementation => [bearspace.py](artwork_scraper/artwork_scraper/spiders/bearspace.py)

   -- loading of the scraped data in dataframe => [task3.py](task3.py)

   -- [artwork_data.json](artwork_data.json) contains scraped data in JSON format

1. `Task 4. Data` => [task4.py](task4.py)

## Tech Stack

1. python 3.10
1. scrapy 2.7.1

## How To Setup

1. You need install Python 3.10

   -- You can download Python from here: `https://www.python.org/downloads/`

2. Create a virtual environment

   -- Follow these guidelines: `https://docs.python.org/3/library/venv.html`

3. Activate the virtual environment and install the packages

   -- Execute the command: `pip install -r requirements.txt`
   
## How To Run The Spider
1. Open the terminal or cmd
1. `cd /path/to/artwork_scraper`
1. `scrapy crawl bearspace-crawl -o output.json`