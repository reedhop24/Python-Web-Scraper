import requests
import re
from bs4 import BeautifulSoup

def monster_Scraper(url):
    page = requests.get(url)
    soup = BeautifulSoup(page.content, 'html.parser')
    results = soup.find(id='ResultsContainer')
    job_elems = results.find_all('section', class_='card-content')
    jobs = []
    for job_elem in job_elems:
        title_elem = job_elem.find('h2', class_='title')
        company_elem = job_elem.find('div', class_='company')
        location_elem = job_elem.find('div', class_='location')
        if None in (title_elem, company_elem, location_elem):
            continue
        jobs.append({
            'Title': title_elem.text.strip(),
            'Company': company_elem.text.strip(),
            'Location': location_elem.text.strip()
        })
    return jobs

def indeed_scraper(url, city, state):
    page = requests.get(url)
    soup = BeautifulSoup(page.content, 'html.parser')
    results = soup.find(id='resultsCol')
    job_elems = results.find_all('div', class_='jobsearch-SerpJobCard')
    jobs = []
    for job_elem in job_elems:
        title_elem = job_elem.find('h2', class_='title')
        company_elem = job_elem.find('div', class_='sjcl')
        inner_div = company_elem.find('div')
        company_span = inner_div.find('span', class_='company')
        updated_title = re.sub('new', '', title_elem.text.strip())
        location_elem = company_elem.find('div', class_='location accessible-contrast-color-location')
        if (None in (title_elem, company_elem, inner_div, company_span, updated_title, location_elem)):
            continue
        if (location_elem == None):
            jobs.append({
                'Title': updated_title,
                'Company': company_span.text.strip(),
                'Location': city + state
            })
        else:
            jobs.append({
                'Title': updated_title,
                'Company': company_span.text.strip(),
                'Location': location_elem.text.strip()
            })
    return jobs

def findJobs():
    print('This web scraper helps you search across multiple Job Boards. Rather than \nspend countless hours scanning for the right job in the right location\nuse this simple tool.')
    all_jobs = []

    job_title = input('Job Title: ')
    formatted_job_monster = '-'.join(job_title.split())
    formatted_job_indeed = '+'.join(job_title.split())

    city = input('City: ')
    formatted_city_monster = '-'.join(city.split())
    formatted_city_indeed = '+'.join(city.split())

    state = input('State (Letter Abbreviation): ')

    URL_Monster = 'https://www.monster.com/jobs/search/?q='+ formatted_job_monster +'&where=' + formatted_city_monster + '__2C-' + state
    URL_Indeed = 'https://www.indeed.com/jobs?q=' + formatted_job_indeed +'&l=' + formatted_city_indeed + '%2C+' + state

    all_jobs.append(indeed_scraper(URL_Indeed, city, state))
    all_jobs.append(monster_Scraper(URL_Monster))

    print(all_jobs)

findJobs()