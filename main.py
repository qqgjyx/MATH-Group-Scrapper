import requests
from bs4 import BeautifulSoup
import pandas as pd
import time
from tqdm import tqdm
from concurrent.futures import ProcessPoolExecutor, as_completed

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
        growth_media_tag = columns[3].find('a')
        growth_media_links = [base_url + a['href'] for a in columns[3].find_all('a')]
        row_data.append(growth_media_links)

        # External links
        external_links = [a['href'] for a in columns[4].find_all('a')]
        row_data.append(external_links)

        data.append(row_data)

    return data


# Function to fetch and print the HTML structure of a given URL
def fetch_html_structure(url):
    try:
        response = requests.get(url)
        response.raise_for_status()
        soup = BeautifulSoup(response.content, 'html.parser')
        return soup
    except requests.exceptions.RequestException as e:
        print(f"Error fetching HTML content from {url}: {e}")
        return None


# Function to extract key data from the HTML structure
def extract_key_data(soup):
    if not soup:
        return None

    # Extracting the title
    title = soup.find('title').text.strip() if soup.find('title') else 'N/A'

    # Extracting the strain name
    strain_name = soup.find('h2').text.strip() if soup.find('h2') else 'N/A'

    # Extracting the synonyms
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

    # Extracting growth media details
    media_details = []
    media_boxes = soup.find_all('div', class_='box')

    for box in media_boxes:
        media_title = box.find('h3', class_='title').text.strip() if box.find('h3', 'title') else 'N/A'
        media_link = box.find('a', class_='link colorless')['href'] if box.find('a', 'link colorless') else 'N/A'

        # Corrected logic to check for growth observation
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


# Function to extract detailed strain information
def extract_strain_details(url):
    soup = fetch_html_structure(url)
    return extract_key_data(soup)


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


# Main scraping process
def scrape_page_data(page):
    try:
        # Extract data from the current page
        page_data = extract_data_from_page(base_url + "/strains", page)
        return page_data
    except (requests.exceptions.RequestException, ConnectionResetError) as e:
        print(f"Error fetching data from page {page}: {e}. Skipping this page...")
        return []


# Function to extract detailed information for each strain and medium
def extract_strain_and_media_details(row):
    strain_details = extract_strain_details(row['Name Link'])
    detailed_data = []
    if strain_details:
        for medium_link in row['Growth Media Links']:
            medium_details = extract_medium_details(medium_link)
            detailed_data.append({
                "Organism Group": row['Organism Group'],
                "Name": row['Name'],
                "Synonyms": ', '.join(strain_details['synonyms']),
                "Growth Conditions": strain_details['media_details'],
                "Medium Name": medium_details['Medium Name'],
                "Components": medium_details['Components']
            })
    return detailed_data


def main():
    all_data = []

    # Scrape data from the first 20 pages using multiprocessing
    with ProcessPoolExecutor() as executor:
        futures = [executor.submit(scrape_page_data, page) for page in range(1, 21)]
        for future in tqdm(as_completed(futures), total=20, desc="Scraping pages"):
            all_data.extend(future.result())

    # Create a DataFrame from the extracted data
    columns = ["Organism Group", "Name", "Name Link", "Taxonomy Link", "Growth Media Links", "External Links"]
    df = pd.DataFrame(all_data, columns=columns)

    # Extract detailed information for each strain and medium
    detailed_data = []
    with ProcessPoolExecutor() as executor:
        futures = [executor.submit(extract_strain_and_media_details, row) for index, row in df.iterrows()]
        for future in tqdm(as_completed(futures), total=df.shape[0], desc="Extracting strain and media details"):
            detailed_data.extend(future.result())

    # Create a detailed DataFrame
    df_detailed = pd.DataFrame(detailed_data)

    # Save the detailed DataFrame to a CSV file
    df_detailed.to_csv('dsmz_detailed_strains.csv', index=False)

    print("Detailed data scraped and saved to dsmz_detailed_strains.csv")


if __name__ == "__main__":
    main()
