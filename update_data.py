import os
from xml.dom import minidom
import requests

def main():
    if_file_exists_delete("sitemap_xml_files/for-sale-by-agent.xml")
    if_file_exists_delete("sitemap_xml_files/for-sale-by-owner.xml")
    if_file_exists_delete("sitemap_xml_files/auction.xml")

    if_file_exists_delete("sitemap_text_files/for-sale-by-agent.txt")
    if_file_exists_delete("sitemap_text_files/for-sale-by-owner_sitemaps.txt")
    if_file_exists_delete("sitemap_text_files/auction_sitemaps.txt")

    if_file_exists_delete("for-sale-by-agent_zpids.txt")
    if_file_exists_delete("for-sale-by-owner_zpids.txt")
    if_file_exists_delete("auction_zpids.txt")

    process_directory("sitemap_xml_files")
    process_directory("sitemap_text_files")

    root_urls = {
        "for-sale-by-agent": "https://www.zillow.com/xml/indexes/us/hdp/for-sale-by-agent.xml.gz",
        "for-sale-by-owner": "https://www.zillow.com/xml/indexes/us/hdp/for-sale-by-owner.xml.gz",
        "auction": "https://www.zillow.com/xml/indexes/us/hdp/auction.xml.gz"
    }

    for root_url in root_urls.values():
        response = requests.get(root_url, allow_redirects=True)
        output_file = os.path.join("sitemap_xml_files", root_url[42:-3])
        with open(output_file, 'wb') as file:
            file.write(response.content)

    xml_files = {
        "for-sale-by-agent": "sitemap_xml_files/for-sale-by-agent.xml",
        "for-sale-by-owner": "sitemap_xml_files/for-sale-by-owner.xml",
        "auction": "sitemap_xml_files/auction.xml"
    }

    for category, file_name in xml_files.items():
        sitemap_urls = get_all_sitemap_urls(file_name)
        for sitemap_url in sitemap_urls:
            urls = get_urls_from_sitemap(sitemap_url)
            zpids = [get_all_zpid(url) for url in urls]
            output_file = f"{category}_zpids.txt"
            write_zpids_to_file(zpids, output_file)

def get_all_sitemap_urls(file_name):
    dom = minidom.parse(file_name)
    loc_elements = dom.getElementsByTagName("loc")
    sitemap_urls = [loc.firstChild.data for loc in loc_elements]
    return sitemap_urls

def get_urls_from_sitemap(sitemap_url):
    response = requests.get(sitemap_url)
    dom = minidom.parseString(response.content)
    loc_elements = dom.getElementsByTagName("loc")
    urls = [loc.firstChild.data for loc in loc_elements]
    return urls

def get_all_zpid(url):
    split_url = url.split("/")
    zpid_line = split_url[5]
    split_zpid_line = zpid_line.split("_")
    return split_zpid_line[0]

def write_zpids_to_file(zpids, file_name):
    with open(file_name, 'w') as file:
        for zpid in zpids:
            file.write(f"{zpid}\n")

def if_file_exists_delete(file_name):
    if (os.path.exists(file_name)):
        os.remove(file_name)

def process_directory(directory_name):
    if os.path.exists(directory_name):
        os.removedirs(directory_name)
        os.makedirs(directory_name)

if __name__ == "__main__":
    main()