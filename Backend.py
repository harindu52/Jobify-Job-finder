import json
from Reader import get_job_name
import requests
from bs4 import BeautifulSoup
import pandas as pd


def get_job_data(name):
    u = f"https://lk.linkedin.com/jobs/{get_job_name(name)}-jobs?countryRedirected=1&position=1&pageNum=0"
    linkedin_url1 = (
        "https://lk.linkedin.com/jobs/search?keywords=Data%20science&location=Colombo%2C%20Western%20Province"
        "%2C%20Sri%20Lanka&geoId=105665594&trk=public_jobs_jobs-search-bar_search-submit&position=1&pageNum=0")
    linkedin_url = u
    job_list = []
    try:
        # Send a GET request to the LinkedIn profile URL
        response = requests.get(linkedin_url)
        # print(response.text)

        # Check if the request was successful (status code 200)
        if response.status_code == 200:
            # Parse the HTML content of the LinkedIn profile page
            ind = 0

            linkedin_soup = BeautifulSoup(response.text, 'html.parser')
            jobs = linkedin_soup.find('ul', class_="jobs-search__results-list")

            for li in jobs.find_all('li'):
                # Extract the name and job information
                job = li.find("h3", class_="base-search-card__title")
                job_link = li.find("a", class_="base-card__full-link absolute top-0 right-0 bottom-0 left-0 p-0 "
                                               "z-[2]")["href"]
                company = li.find("a", class_="hidden-nested-link")
                company_link = company["href"]
                image = li.find("img", class_="artdeco-entity-image")['data-delayed-url']

                print(job.text.strip())
                print(company.text.strip())
                print(job_link)
                print(company_link)
                print(image)

                try:
                    response_job = requests.get(job_link)
                    print(response_job.status_code)

                    if response_job.status_code == 200:
                        job_soup = BeautifulSoup(response_job.text, 'html.parser')

                        job_detail = job_soup.find("div", class_="description__text description__text--rich")
                        for strong in job_detail.find_all("strong"):
                            el = strong.get_text()
                            print(el)

                except Exception as e:
                    print(f"An error occurred:......... {str(e)}")
                data = {
                    "id": ind,
                    "Job": job.text.strip(),
                    "Job_link": job_link,
                    "Company": company.text.strip(),
                    "Company_link": company_link,
                    "Job_detail": job_detail.text.strip(),
                    "Image": image
                }
                ind += 1
                job_list.append(data)
        else:
            print("Failed to retrieve the LinkedIn profile page.")

    except Exception as e:
        print(f"An error occurred: {str(e)}")

    with open("jobdata.json", "w") as final:
        json.dump(job_list, final)

    return job_list
