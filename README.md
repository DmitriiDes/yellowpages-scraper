# Yellow Pages Business Details Scraper - amended to work with yellowpages.ca as of Apr/2022

Yellowpages.ca Web Scraper written in Python and LXML to extract business details available based on a particular category and location.

If you would like to know more about original scraper you can check it out at the blog post 'How to Scrape Business Details from Yellow Pages using Python and LXML' - https://www.scrapehero.com/how-to-scrape-business-details-from-yellowpages-com-using-python-and-lxml/

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes.

### Fields to Extract

This yellow pages scraper can extract the fields below (it can be modified by you):

1. Business Name
2. Phone Number
3. Street name
4. Locality
5. Region
6. Zipcode
7. Website
8. Business Page
9. Category

### Prerequisites

For this web scraping tutorial using Python 3, we will need some packages for downloading and parsing the HTML. 
Below are the package requirements:

 - lxml
 - requests

### Installation

PIP to install the following packages in Python (https://pip.pypa.io/en/stable/installing/) 

Python Requests, to make requests and download the HTML content of the pages (http://docs.python-requests.org/en/master/user/install/)

Python LXML, for parsing the HTML Tree Structure using Xpaths (Learn how to install that here – http://lxml.de/installation.html)

## Running the scraper
Open the script in an edditor of your choice. Modify keyword, place, pagination according to your requirements. Save changes.

Due to specific for https://www.yellowpages.ca/ link construction first verify your parameters manually.

Example. for https://www.yellowpages.ca/search/si/1/plumbing/Toronto+ON
keyword = "plumbing"
place = "Toronto+ON"
pagination in range(1,15) - range will depend on how many pages you would like to scrape

## Sample Output

This will create a csv file:

[Sample Output](https://github.com/DmitriiDes/yellowpages-scraper/blob/master/plumbing-Toronto%2BON-pg14-yellowpages-scraped-data.csv)
 
 
