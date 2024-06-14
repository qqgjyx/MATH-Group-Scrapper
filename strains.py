# %%
import requests
from bs4 import BeautifulSoup
import pandas as pd
import time
from tqdm import tqdm
from concurrent.futures import ThreadPoolExecutor, as_completed
import re

# %%
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

                dsm_no = name.split(' ')[-1]
                row_data.append(dsm_no)

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
                external_links = [a['href'] for a in columns[4].find_all('a')] if columns[4].find('a') else None
                row_data.append(external_links)
                dsmz_catalogue = columns[4].find_all('a')[0]['href'] if "dsmz" in columns[4].find_all('a')[0][
                    'href'] else None
                bacdive_link = columns[4].find_all('a')[1]['href'] if len(columns[4].find_all('a')) > 1 and "bacdive" in \
                                                                      columns[4].find_all('a')[1]['href'] else None
                row_data.append(dsmz_catalogue)
                row_data.append(bacdive_link)

                data.append(row_data)

            return data
        except (requests.exceptions.RequestException, ConnectionResetError) as e:
            print(f"Error fetching page {page}: {e}. Retrying {attempt + 1}/{retries}...")
            time.sleep(1)  # Wait before retrying
    return []


# Main scraping process
all_data = []
num_pages = 2314  # Adjust the number of pages you want to scrape

max_workers = 256  # Adjust based on the MacBook M3 Pro capabilities

with ThreadPoolExecutor(max_workers=max_workers) as executor:
    future_to_page = {executor.submit(extract_data_from_page, base_url + "/strains", page): page for page in
                      range(1, num_pages + 1)}

    for future in tqdm(as_completed(future_to_page), total=num_pages, desc="Extracting data from pages"):
        page_data = future.result()
        all_data.extend(page_data)

# Sort the data based on the page number to maintain the order
all_data.sort(key=lambda x: x[0])

# Create a DataFrame from the extracted data
columns = ["Page", "Organism Group", "Name", "Name Link", "DSM No.", "Taxonomy Link", "Growth media",
           "Growth Media Links", "external links", "DSMZ Catalogue", "Bacdive Link"]
df = pd.DataFrame(all_data, columns=columns)
df.drop(columns=["Page"], inplace=True)  # Remove the page column if not needed

df


# %%
# Function to fetch HTML content and parse it with BeautifulSoup
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


# Function to extract key data from the parsed HTML content
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
                    synonyms.extend(content.strip().split(', '))
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


# Function to extract strain details from a row of the DataFrame
def extract_strain_details(row):
    url = row['Name Link']
    soup = fetch_html_structure(url)
    return extract_key_data(soup)


# Function to save detailed data incrementally
def save_detailed_data(detailed_data):
    df_detailed = pd.DataFrame(detailed_data)
    df_detailed.to_csv('detailed_dsmz_data.csv', index=False)


# Load the initial DataFrame (assuming it's loaded in variable df)
# df = pd.read_csv('initial_data.csv')  # Load your initial DataFrame here

# Initialize an empty list to hold detailed data
detailed_data = []
num_strains = df.shape[0]
max_workers = 10  # Adjust the number of workers as needed

# Extract detailed information for each strain with ThreadPoolExecutor
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
            # Save incrementally after each strain is processed
            save_detailed_data(detailed_data)

# # Sort the detailed data based on the Name to maintain order
# detailed_data.sort(key=lambda x: int(x['Name'].split(' ')[-1]))

# Create the final detailed DataFrame
df_detailed = pd.DataFrame(detailed_data)
merged_df = pd.merge(df, df_detailed, on="Name", how='left')

merged_df
# %%
link_data_temp = list


# Function to extract data from a single page
def extract_data_from_link(link, extractor_method, pbar, new_names, retries=5):
    for attempt in range(retries):
        try:
            response = requests.get(link)
            response.raise_for_status()
            soup = BeautifulSoup(response.content, 'html.parser')
            extractor = Extractor(link, soup, extractor_method)
            data = extractor.extract()
            if data is None:
                print('No soup for {}'.format(link))
                # pbar.set_description('Failed to extract data from {}'.format(link))
                data = [link]
                data.extend([None] * (len(new_names) - 1))
            pbar.update(1)
            return data
        except (requests.exceptions.RequestException, ConnectionResetError) as e:
            print(f"Error fetching link {link}: {e}. Retrying {attempt + 1}/{retries}...")
            time.sleep(1)  # Wait before retrying
    return [link].extend([None] * (len(new_names) - 1))


def scrape_link(old_df, on_old_name, extractor_method, new_names):
    global link_data_temp
    link_data_temp = []
    links = old_df[on_old_name].dropna().unique()

    with tqdm(total=len(links), desc=on_old_name + " link Progress") as pbar:
        with ThreadPoolExecutor(max_workers=max_workers) as executor:
            future_to_link = {executor.submit(extract_data_from_link, link, extractor_method, pbar, new_names): link for
                              link in links}
            for future in as_completed(future_to_link):
                data = future.result()
                link_data_temp.append(data)
        link_df = pd.DataFrame(link_data_temp, columns=new_names)
        merged_df = pd.merge(old_df, link_df, on=on_old_name, how='left')
    return merged_df


class Extractor:
    def __init__(self, link, soup, method):
        self.link = link
        self.soup = soup
        self.method = method

    def extract(self):
        return self.method(self.link, self.soup)


def dsmzlink_method(dsmzlink, soup):
    soup = soup.find('div', class_='product-detail') if soup.find('div', class_='product-detail') else None
    if soup is None:
        return None

    def get_field_value(soup, label):
        field = soup.find('div', class_='label', string=lambda x: x and label in x)
        if field:
            return '"' + field.find_next_sibling('div', class_='value').get_text(strip=True) + '"'
        return None

    name_value = get_field_value(soup, 'Name: ')
    sd_value = get_field_value(soup, 'Strain designation: ')

    dsm_field = soup.find('div', class_='label', string=lambda x: x and 'DSM No.: ' in x) if soup.find('div',
                                                                                                       class_='label',
                                                                                                       string=lambda
                                                                                                           x: x and 'DSM No.: ' in x) else None
    if dsm_field:
        dsm_value = dsm_field.find_next_sibling('div', class_='value').get_text(strip=True)
        type_strain = "yes" if "Type strain" in dsm_value else "no"
    else:
        type_strain = "No"

    def get_comp_value(soup, label):
        field = soup.select_one('div.label:-soup-contains("' + label + '")')
        if field:
            return field.find_next_sibling('div', class_='value')
        else:
            return None

    other_value = get_comp_value(soup, "Other collection no.")
    if other_value:
        other_value = '"' + other_value.get_text(strip=True) + '"'

    iso_value = get_field_value(soup, 'Isolated from: ')
    country_value = get_field_value(soup, 'Country: ')
    date_value = get_field_value(soup, 'Date of sampling: ')

    risk_tag = get_comp_value(soup, 'Risk group: ')
    if risk_tag:
        risk_value = '"' + risk_tag.get_text(strip=True) + '"'
    else:
        risk_value = None
    risk_group = risk_tag.get_text(strip=True).split(' ')[0].split('(')[0] if risk_tag else None
    class_by = risk_tag.find('a').get_text(strip=True) if risk_tag.find('a') else \
    risk_tag.get_text(strip=True).split(' ')[-1].replace(')', '')

    nagoya_value = get_field_value(soup, 'Nagoya Protocol Restrictions: ')
    history_value = get_field_value(soup, 'History: ')

    genbank_tag = get_comp_value(soup, 'Genbank accession numbers: ')
    if genbank_tag:
        genbank_value = '"' + genbank_tag.get_text(strip=True) + '"'
    else:
        genbank_value = None

    # Initialize the dictionary
    sequence_dict = {}
    # Extract information
    if genbank_tag:
        text_taw = genbank_tag.get_text(separator="|").split("|")
        text = [s for s in text_taw if ":" in s]
        links = genbank_tag.find_all('a')
        for i, part in enumerate(text):
            if ':' in part:
                key = part.strip()
                value = [links[i].text, links[i]['href']]
                sequence_dict[key] = value
    whole_genome_tag = sequence_dict.get("whole genome shotgun sequence:")
    if whole_genome_tag:
        whole_genome = whole_genome_tag[0]
        whole_genome_link = whole_genome_tag[1]
    else:
        whole_genome = None
        whole_genome_link = None
    sixteens_rrna_tag = sequence_dict.get("16S rRNA gene:")
    if sixteens_rrna_tag:
        sixteens_rrna = sixteens_rrna_tag[0]
        sixteens_rrna_link = sixteens_rrna_tag[1]
        if sixteens_rrna_link != '' and sixteens_rrna_link is not None:
            sixteens_rrna_link = sixteens_rrna_link + '.1?report=fasta'
    else:
        sixteens_rrna = None
        sixteens_rrna_link = None

    additional_tag = get_comp_value(soup, 'additional information: ')
    if additional_tag:
        additional_value = '"' + additional_tag.get_text(strip=True) + '"'
    else:
        additional_value = None

    literature_value = get_field_value(soup, "Literature: ")

    wink_tag = get_comp_value(soup, "Wink compendium: ")
    if wink_tag:
        wink_value = '"' + wink_tag.get_text(strip=True) + '"'
        wink_link = wink_tag.find('a')['href']
    else:
        wink_value = None
        wink_link = None

    supplied_tag = get_comp_value(soup, "Supplied as: ")
    supplied_dic = {}
    price_category = None
    if supplied_tag:
        supplied_value = '"' + supplied_tag.get_text(strip=True) + '"'
        table = supplied_tag.find('table')
        trs = table.find_all('tr')[2:]
        for tr in trs:
            td = tr.find_all('td')
            if len(td) == 4:
                delivery_form = td[0].get_text(strip=True)
                prices = td[-2].get_text(strip=True)
                supplied_dic[delivery_form] = prices
            if len(td) == 3:
                delivery_form = td[0].get_text(strip=True)
                prices = td[-1].get_text(strip=True)
                supplied_dic[delivery_form] = prices
            if len(td) == 1:
                price_category = td[0].find('b').get_text(strip=True) if td[0].find('b') else None
    else:
        supplied_value = None
        price_category = None
    freeze_dried = supplied_dic.get("Freeze Dried")
    active_culture = supplied_dic.get("Active culture on request")
    dna_price = supplied_dic.get("DNA")

    culture_tag = get_comp_value(soup, "Other cultures:")
    if culture_tag:
        culture_link = culture_tag.find('a')['href']
    else:
        culture_link = None

    return [dsmzlink, name_value, sd_value, type_strain, other_value, iso_value, country_value, date_value, risk_value,
            risk_group, class_by, nagoya_value, history_value, genbank_value, sequence_dict, whole_genome,
            whole_genome_link, sixteens_rrna, sixteens_rrna_link, additional_value, literature_value, wink_value,
            wink_link, supplied_value, supplied_dic, freeze_dried, active_culture, dna_price, price_category,
            culture_link]


merged_merged_df = scrape_link(merged_df, 'DSMZ Catalogue', dsmzlink_method,
                               ["DSMZ Catalogue", "Full Stain Name", "Strain Designation", "Type Strain",
                                "Other collection no./WDCM no.", "Isolated from", "Country", "Date of sampling",
                                "Risk group raw", "Risk group", "classification by", "Nagoya Protocol Restrictions",
                                "History", "Genbank accession raw", "Genbank dict", "whole genome shotgun sequence no.",
                                "whole genome shotgun sequence no. link", "16S rRNA gene no.", "16S rRNA gene no. link",
                                "Summary and additional information", "Literature", "Wink compendium",
                                "Wink compendium link", "Supplied as raw", "Supplied as dict", "Price of Freeze Dried",
                                "Price of Active culture on request", "Price of DNA", "Price Category", "Culture link"])

merged_merged_df


# %%
def bacdiv_method(bacdivlink, soup, retries=5):
    if soup is None:
        return None
    link_div = soup.find('td', class_="bold_valigntop width180_valigntop", string="Synonym") if soup.find('td',
                                                                                                          class_="bold_valigntop width180_valigntop",
                                                                                                          string="Synonym") else None
    if link_div:
        href = link_div.find_next_sibling('td').find('a')['href']
    else:
        return [bacdivlink, None]
    for attempt in range(retries):
        try:
            response = requests.get(href)
            response.raise_for_status()
            soup_2 = BeautifulSoup(response.content, 'html.parser')
            synonyms_full = soup_2.find('p').get_text(strip=True).split(':')[-1] if "Name" in soup_2.find('p').get_text(
                strip=True) else None
            return [bacdivlink, synonyms_full]
        except (requests.exceptions.RequestException, ConnectionResetError) as e:
            print(f"Error fetching link {href}: {e}. Retrying {attempt + 1}/{retries}...")
            time.sleep(1)  # Wait before retrying
    return [bacdivlink, href]


merged_merged_merged_df = scrape_link(merged_merged_df, 'Bacdive Link', bacdiv_method,
                                      ["Bacdive Link", "Synonyms Full"])

merged_merged_merged_df
# %%
merged_merged_merged_df.to_csv("strains.csv", index=False)
# %%
