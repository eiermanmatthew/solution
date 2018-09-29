from requests import get
from bs4 import BeautifulSoup
import json


url = 'http://127.0.0.1:5000'
response = get(url)
html_soup = BeautifulSoup(response.text, 'html.parser')

## Getting Pagination Info 
pagination_container = html_soup.find('ul', 'pagination pagination-sm')
pagination = pagination_container.find_all('a')
last_index = int(pagination[len(pagination)-2].text) ## index of last page
pagination_url = url + pagination[len(pagination)-2].get('href').split("=")[0] + "=" ## pagination url for all indexes

current_index = 1 ## first page index is current page
all_companies = [] 

## loop through each page from 1 - last index
while current_index <= last_index:
    print "Extracting data from page: "+ str(current_index)
    ## Get page data from current index
    if current_index > 1:
        response = get(pagination_url + str(current_index))
        html_soup = BeautifulSoup(response.text, 'html.parser')
    ## Getting company links to get detail
    table = html_soup.find('table', 'table table-hover')
    company_links = table.find_all('a')
    for link in company_links:
        new_company = {}
        ## getting company detail page
        company = get(url+link.get('href'))
        html_soup = BeautifulSoup(company.text, 'html.parser')
        ## getting table which contains all information of company
        company_table = html_soup.find('table', 'table table-hover')
        details = company_table.find_all("td")
        prev = ""
        for detail in details:
##            Since we have each detail like company name in 2 <td>s so we used prev variable to store value of <td> value
##            when we have value in prev we used that to set value of that index in new_company dict            
            if prev == "":
                prev = detail.text
                new_company[prev] = ""
            else:
                new_company[prev] = detail.text
                prev = ""
        all_companies.append(new_company)
    current_index = current_index+1

## storing all_companies data in json file
with open('edgar.json', 'w') as fout:
    json.dump(all_companies, fout,indent=2)
print "edgar.json file created successfully."
