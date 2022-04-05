#!/usr/bin/env python
# -*- coding: utf-8 -*-

import requests
from lxml import html
import datetime
import unicodecsv as csv

def parse_listing(keyword, place, pagination):
    """

    Function to process yellowpages.ca listing page
    : param keyword: search query
    : param place : place name City+2 character province abbreviation (Ex. Toronto+ON)

    """
    url = "https://yellowpages.ca/search/si/{2}/{0}/{1}".format(keyword, place, pagination)
    print("retrieving ", url)

    """ You might need to add headers dictionary here - please refer to the below"""

    """headers = {'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
				'Accept-Encoding':'gzip, deflate, br',
				'Accept-Language':'en-GB,en;q=0.9,en-US;q=0.8,ml;q=0.7',
				'Cache-Control':'max-age=0',
				'Connection':'keep-alive',
				'Host':'www.yellowpages.ca',
				'Upgrade-Insecure-Requests':'1',
				'User-Agent':'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.140 Safari/537.36'
			}"""

    # Adding retries
    for retry in range(10):
        try:
            response = requests.get(url) #Verify and headers are optional
            print(response.status_code)
            if response.status_code==200:
                parser = html.fromstring(response.text)

                #Making base link absolute
                base_url = "https://www.yellowpages.ca"
                parser.make_links_absolute(base_url)

                XPATH_LISTINGS = "//div[contains(@class, 'listing listing--bottomcta ') and contains(@data-pin-number, '-1')]" #listings ex pinned
                listings = parser.xpath(XPATH_LISTINGS)
                scraped_results = []

                for results in listings:
                    #Add additional fields as necessary
                    XPATH_BUSINESS_NAME = ".//a[contains(@class, 'listing__name--link')]//text()"
                    XPATH_BUSINESS_PAGE = ".//a[contains(@class, 'listing__name--link')]//@href"
                    XPATH_STREET = ".//div[contains(@class, 'listing__address')]//span[@itemprop='address']//span[@itemprop='streetAddress']//text()"
                    XPATH_LOCALITY = ".//div[contains(@class, 'listing__address')]//span[@itemprop='address']//span[@itemprop='addressLocality']//text()"
                    XPATH_REGION = ".//div[contains(@class, 'listing__address')]//span[@itemprop='address']//span[@itemprop='addressRegion']//text()"
                    XPATH_ZIP_CODE = ".//div[contains(@class, 'listing__address')]//span[@itemprop='address']//span[@itemprop='postalCode']//text()"
                    XPATH_WEBSITE = ".//div[contains(@class, 'listing__mlr__root')]//ul/li[3]//@href"
                    XPATH_TELEPHONE = ".//div[contains(@class, 'listing__mlr__root')]//ul/li[1]/ul/li//text()"

                    raw_business_name = results.xpath(XPATH_BUSINESS_NAME)
                    raw_business_page = results.xpath(XPATH_BUSINESS_PAGE)
                    raw_street = results.xpath(XPATH_STREET)
                    raw_locality = results.xpath(XPATH_LOCALITY)
                    raw_region = results.xpath(XPATH_REGION)
                    raw_zip_code = results.xpath(XPATH_ZIP_CODE)
                    raw_website = results.xpath(XPATH_WEBSITE)
                    raw_business_telephone = results.xpath(XPATH_TELEPHONE)

                    business_name = ''.join(raw_business_name).strip() if raw_business_name else None
                    business_page = ''.join(raw_business_page).strip() if raw_business_page else None
                    street = ''.join(raw_street).strip() if raw_street else None
                    website = ''.join(raw_website).strip() if raw_website else None
                    locality = ''.join(raw_locality).replace(',\xa0','').strip() if raw_locality else None
                    region = ''.join(raw_region).strip() if raw_region else None
                    zipcode = ''.join(raw_zip_code).strip() if raw_zip_code else None
                    telephone = ''.join(raw_business_telephone).strip() if raw_business_telephone else None

                    business_details = {
										'business_name': business_name,
                                        'telephone' : telephone,
										'street': street,
										'locality': locality,
										'region': region,
										'zipcode': zipcode,
                                        'website': website,
                                        'business_page': business_page,
                                        'search_category': keyword,
										'updated_at': datetime.datetime.now()
					}

                    scraped_results.append(business_details)

                return scraped_results

            elif response.status_code==404:
                print("Could not find a location matching", place)
                break
            else:
                print("Test failed to process page")
                return []

        except:
            print("Failed to process page")
            return []

if __name__=="__main__":
    #Check https://www.yellowpages.ca/ for exact link format
    #https://www.yellowpages.ca/search/si/1/keyword/place
    keyword = "plumbing" #Keyword based on search category
    place = "Toronto+ON" #Location based on the link usually City+Province
    scraped_data = []
    for pagination in range(1,15): #Page range to scrape
        scraped_data.extend(parse_listing(keyword, place, pagination))

    if scraped_data:
        print("Writing scraped data to %s-%s-pg%s-yellowpages-scraped-data.csv" % (keyword, place, pagination))
        with open('%s-%s-pg%s-yellowpages-scraped-data.csv' % (keyword, place, pagination), 'wb') as csvfile:
            fieldnames = scraped_data[0].keys()

            writer = csv.DictWriter(csvfile, fieldnames=fieldnames, quoting=csv.QUOTE_ALL)
            writer.writeheader()
            for data in scraped_data:
                writer.writerow(data)
