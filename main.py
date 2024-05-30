import requests
from bs4 import BeautifulSoup
import pandas as pd
import time
from tqdm import tqdm
from concurrent.futures import ThreadPoolExecutor, as_completed

# Base URL of the webpage
base_url = "https://mediadive.dsmz.de"


# Function to extract data from a single page
def extract_data_from_page(url, page, retries=5):
    params = {"p": page}
    for attempt in range(retries):
        try:
            response = requests.get(url, params=params)
            response.raise_for_status()
            soup = BeautifulSoup(response.content, 'html.parser')

            data = []
            table_rows = soup.find_all('tr')[1:]  # Skip the header row
            for row in table_rows:
                columns = row.find_all('td')
                row_data = [page]  # Add the page number

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
                growth_media = [a.get_text(strip=True) for a in columns[3].find_all('a')]
                growth_media_links = [base_url + a['href'] for a in columns[3].find_all('a')]
                row_data.append(growth_media)
                row_data.append(growth_media_links)

                # External links
                external_links = [a['href'] for a in columns[4].find_all('a')]
                row_data.append(external_links)

                data.append(row_data)

            return data
        except (requests.exceptions.RequestException, ConnectionResetError) as e:
            print(f"Error fetching page {page}: {e}. Retrying {attempt + 1}/{retries}...")
            time.sleep(5)  # Wait before retrying
    return []


# Main scraping process
all_data = []
num_pages = 2312  # Adjust the number of pages you want to scrape

max_workers = 96 # Adjust based on the MacBook M3 Pro capabilities

with ThreadPoolExecutor(max_workers=max_workers) as executor:
    future_to_page = {executor.submit(extract_data_from_page, base_url + "/strains", page): page for page in
                      range(1, num_pages + 1)}

    for future in tqdm(as_completed(future_to_page), total=num_pages, desc="Extracting data from pages"):
        page_data = future.result()
        all_data.extend(page_data)

# Sort the data based on the page number to maintain the order
all_data.sort(key=lambda x: x[0])

# Create a DataFrame from the extracted data
columns = ["Page", "Organism Group", "Name", "Name Link", "Taxonomy Link", "Growth media", "Growth Media Links",
           "External Links"]
df = pd.DataFrame(all_data, columns=columns)
df.drop(columns=["Page"], inplace=True)  # Remove the page column if not needed
df.to_csv('initial_dsmz_data.csv', index=False)

# Load the initial data
df = pd.read_csv('initial_dsmz_data.csv')


# Functions for extracting detailed data
def fetch_html_structure(url, retries=5):
    for attempt in range(retries):
        try:
            response = requests.get(url)
            response.raise_for_status()
            soup = BeautifulSoup(response.content, 'html.parser')
            return soup
        except (requests.exceptions.RequestException, ConnectionResetError) as e:
            print(f"Error fetching HTML content from {url}: {e}. Retrying {attempt + 1}/{retries}...")
            time.sleep(5)  # Wait before retrying
    return None


def extract_key_data(soup):
    if not soup:
        return None

    title = soup.find('title').text.strip() if soup.find('title') else 'N/A'
    strain_name = soup.find('h2').text.strip() if soup.find('h2') else 'N/A'
    synonyms = []
    paragraphs = soup.find_all('p')
    for p in paragraphs:
        bold_text = p.find('b', string='Synonyms:')
        if bold_text:
            for content in p.contents:
                if content.name == 'a':
                    synonyms.append(content.get_text(strip=True))
                    synonyms.append('href: ' + content.get('href'))
                elif isinstance(content, str) and content.strip():
                    synonyms.extend(content.split(', '))
            break

    media_details = []
    media_boxes = soup.find_all('div', class_='box')
    for box in media_boxes:
        media_title = box.find('h3', class_='title').text.strip() if box.find('h3', 'title') else 'N/A'
        media_link = box.find('a', class_='link colorless')['href'] if box.find('a', 'link colorless') else 'N/A'
        growth_observed = 'Yes' if box.find('i', class_='ph ph-lg ph-check text-success') else 'No'
        growth_conditions = box.find('span', class_='badge danger').text.strip() if box.find('span',
                                                                                             'badge danger') else 'N/A'

        media_details.append({
            'media_title': media_title,
            'media_link': media_link,
            'growth_observed': growth_observed,
            'growth_conditions': growth_conditions
        })

    return {
        'title': title,
        'strain_name': strain_name,
        'synonyms': synonyms,
        'media_details': media_details
    }


def extract_strain_details(row):
    url = row['Name Link']
    soup = fetch_html_structure(url)
    return extract_key_data(soup)


# Extract detailed information for each strain
detailed_data = []
num_strains = df.shape[0]

with ThreadPoolExecutor(max_workers=max_workers) as executor:
    future_to_index = {executor.submit(extract_strain_details, row): index for index, row in df.iterrows()}

    for future in tqdm(as_completed(future_to_index), total=num_strains, desc="Extracting strain details"):
        index = future_to_index[future]
        strain_details = future.result()
        if strain_details:
            detailed_data.append({
                "Name": df.loc[index, 'Name'],
                "Synonyms": ', '.join(strain_details['synonyms']),
                "Growth Conditions": strain_details['media_details']
            })

# Create a detailed DataFrame
df_detailed = pd.DataFrame(detailed_data)
df_detailed.to_csv('detailed_dsmz_data.csv', index=False)

# Merge the initial and detailed DataFrames
merged_df = df.merge(df_detailed, on='Name', how='left', sort=False)
merged_df.to_csv('merged_dsmz_strains.csv', index=False)

print("Merged data saved to merged_dsmz_strains.csv")