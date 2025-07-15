📘 Data Analysis & Web Scraping Assignments
This repository contains two assignments that demonstrate skills in data engineering, data extraction, and web scraping using Python and R. Both projects reflect a practical application of real-world data processing and dynamic web content extraction.

📌 Assignment 1: JSON Flattening and Data Enrichment (DMCA Notices)
📂 Objective
Process a deeply nested JSON file containing DMCA takedown notices.

Flatten and enrich the data.

Generate analytical summaries using both Python and R.

🧠 Approach
1. Pre-analysis
Used JSONLint to understand and validate the structure.

Reorganized the JSON into a more readable format for inspection.

2. Flattening the JSON
Iterated through notices, works, and infringing URLs.

Extracted key metadata: notice ID, sender, principal name, work description.

Output: flattened_step1.csv.

3. Adding Domain and IP
Extracted domain from each infringing URL.

Resolved domain to IP using:

Python: socket.gethostbyname() with ThreadPoolExecutor.

R: nslookup() with parSapply() on a 4-core cluster.

Output: flattened_step3.csv.

4. Summarizations
Top 10 infringing domains.

Unique notices per sender.

Infringing URLs grouped by work description.

Additional metrics: most active senders/domains.

🛠️ Tech Stack
Languages: Python, R

Python Libraries: pandas, json, urllib.parse, socket, concurrent.futures

R Packages: jsonlite, dplyr, urltools, parallel

✅ Outcome
Successfully built a scalable and parallelized data pipeline.

Generated CSV summaries with clean code in both languages.

📌 Assignment 2: Web Scraping Journal Articles (SAGE)
📂 Objective
Scrape article metadata from the Journal of Marketing (SAGE) current issue page, including:

Title

Authors

First Published Date

DOI

Abstract

🧠 Approach
❌ Attempt 1: requests + BeautifulSoup
Could not retrieve article data due to JavaScript-rendered content.

✅ Final Solution: Selenium + BeautifulSoup
Controlled Chrome via Selenium to simulate browser behavior.

Accepted cookies and waited for JS execution.

Extracted and parsed article content using BeautifulSoup.

Saved data into a structured CSV.

🛠️ Tech Stack
Python 3.x

Selenium + ChromeDriver

BeautifulSoup (bs4)

pandas

requests (explored, not used in final solution)

✅ Outcome
Extracted full article metadata.

Saved output as assignment2_articles_final.csv.

Selenium proved reliable for dynamic web scraping.

📎 Deliverables
✅ Clean and well-documented Python & R scripts

✅ Output CSVs for both assignments

✅ Summary documents outlining approach and results

✅ Video explanation and 1-page report for Assignment 1 (if applicable)