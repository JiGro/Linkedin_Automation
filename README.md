# LinkedIn Automations Repository

![Logo of the Project](https://cdn.pixabay.com/photo/2017/08/22/11/55/linked-in-2668692_1280.png)

This repository is supposed to include automations revolving around LinkedIn. In a first approach companies within a certain location where scraped and then enriched with their LinkedIn company specific information. A potential use case would be sales lead generation.

## Getting Started
These instructions will get you a copy of the project up and running on your local machine for development and testing purposes.

### Installing
1. Make sure you have Python installed on your system (version 3.6 or later).

2. Clone the repository to your local machine
```
git clone https://github.com/JiGro/Linkedin_Automation.git
```

3. Install the required packages
```
pip install -r requirements.txt
```

4. Set Username, password & scrape url
```
email = ""
pw = ""
...
url = f"https://www.linkedin.com/search/results/companies/?companyHqGeo=%5B%2290000828%22%5D&companySize=%5B%22B%22%2C%22C%22%2C%22D%22%2C%22E%22%5D&keywords={letter}*&origin=FACETED_SEARCH&sid=fCx"
```

5. Run the code using the following command:
```
python company_scraper.py
```

## Authors
- **Jimmy (JiGro)** - *Initial work* - [My Github Profile](https://github.com/JiGro)