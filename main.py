import requests
from bs4 import BeautifulSoup
import pandas as pd
import time
from tqdm import tqdm

# Base URL of the webpage
base_url = "https://mediadive.dsmz.de"

# Function to extract data from a single page
def extract_data_from_page(url, page):
    params = {"p": page}
    response = requests.get(url, params=params)
    response.raise_for_status()
    soup = BeautifulSoup(response.content, 'html.parser')

    data = []
    table_rows = soup.find_all('tr')[1:]  # Skip the header row
    for row in table_rows:
        columns = row.find_all('td')
        row_data = []

        # Organism Group
        organism_group = columns[0].get_text(strip=True)
        row_data.append(organism_group)

        # Name and link
        name_tag = columns[1].find('a')
        name = name_tag.get_text(strip=True)
        name_link = base_url + name_tag['href']
        row_data.append(name)
        row_data.append(name_link)

        # Taxonomy link
        taxonomy_tag = columns[2].find('a')
        taxonomy_link = base_url + taxonomy_tag['href'] if taxonomy_tag else None
        row_data.append(taxonomy_link)

        # Growth Media links
        growth_media_links = [base_url + a['href'] for a in columns[3].find_all('a')]
        row_data.append(growth_media_links)

        # External links
        external_links = [a['href'] for a in columns[4].find_all('a')]
        row_data.append(external_links)

        data.append(row_data)

    return data, soup

# Function to extract detailed strain information
def extract_strain_details(url):
    retries = 3
    for i in range(retries):
        try:
            response = requests.get(url)
            response.raise_for_status()
            soup = BeautifulSoup(response.content, 'html.parser')

            details = {}
            # Extract synonyms and growth conditions
            details['Synonyms'] = soup.find('div', class_='synonyms').get_text(strip=True) if soup.find('div',
                                                                                                        class_='synonyms') else ""
            details['Growth Conditions'] = soup.find('div', class_='growth-conditions').get_text(
                strip=True) if soup.find('div', class_='growth-conditions') else ""
            return details
        except (requests.exceptions.RequestException, ConnectionResetError) as e:
            print(f"Error fetching strain details from {url}: {e}. Retrying ({i + 1}/{retries})...")
            time.sleep(5)
    return {"Synonyms": "", "Growth Conditions": ""}

# Function to extract medium information
def extract_medium_details(url):
    retries = 3
    for i in range(retries):
        try:
            response = requests.get(url)
            response.raise_for_status()
            soup = BeautifulSoup(response.content, 'html.parser')

            medium_details = {}
            # Extract medium name and components
            medium_details['Medium Name'] = soup.find('h1').get_text(strip=True)
            medium_details['Components'] = {
                item.find('span', class_='compound-name').get_text(strip=True): item.find('span',
                                                                                          class_='compound-amount').get_text(
                    strip=True) for item in soup.find_all('div', class_='compound')}
            return medium_details
        except (requests.exceptions.RequestException, ConnectionResetError) as e:
            print(f"Error fetching medium details from {url}: {e}. Retrying ({i + 1}/{retries})...")
            time.sleep(5)
    return {"Medium Name": "", "Components": {}}

all_data = []

# Scrape data from the first 5R pages
for page in range(1, 6):
    try:
        # Extract data from the current page
        page_data, soup = extract_data_from_page(base_url + "/strains", page)
        all_data.extend(page_data)

        # Print the current page number
        print(f"Processing page {page}")
    except (requests.exceptions.RequestException, ConnectionResetError) as e:
        print(f"Error fetching data from page {page}: {e}. Skipping this page...")
        time.sleep(5)
        continue

# Create a DataFrame from the extracted data
columns = ["Organism Group", "Name", "Name Link", "Taxonomy Link", "Growth Media Links", "External Links"]
df = pd.DataFrame(all_data, columns=columns)

# Extract detailed information for each strain and medium
detailed_data = []
for index, row in tqdm(df.iterrows(), total=df.shape[0], desc="Extracting strain details"):
    strain_details = extract_strain_details(row['Name Link'])
    for medium_link in tqdm(row['Growth Media Links'], desc=f"Extracting media for {row['Name']}", leave=False):
        medium_details = extract_medium_details(medium_link)
        detailed_data.append({
            "Organism Group": row['Organism Group'],
            "Name": row['Name'],
            "Synonyms": strain_details['Synonyms'],
            "Growth Conditions": strain_details['Growth Conditions'],
            "Medium Name": medium_details['Medium Name'],
            "Components": medium_details['Components']
        })
    # Save progress periodically
    if (index + 1) % 10 == 0:
        df_detailed = pd.DataFrame(detailed_data)
        df_detailed.to_csv('dsmz_detailed_strains_partial.csv', index=False)

# Create a detailed DataFrame
df_detailed = pd.DataFrame(detailed_data)

# Save the detailed DataFrame to a CSV file
df_detailed.to_csv('dsmz_detailed_strains.csv', index=False)

print("Detailed data scraped and saved to dsmz_detailed_strains.csv")