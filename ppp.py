#!/usr/bin/python3
"""
Financeable Evaluation of Paycheck Protection Program (PPP)
Loans on the Balance Sheet of the Lenders
"""

import os
import requests
import pandas as pd
from bs4 import BeautifulSoup

def check_if_dir_exists(dir_path):
    if not os.path.exists(dir_path):
        os.mkdir(dir_path)

def download_file(file_path, response_ppp):
    with open(file_path, "wb") as f:
        f.write(response_ppp.content)

def find_links_to_xlsx_and_csv_files(soup):
    # Find all the links to xlsx and csv files
    links = soup.find_all("a", href=lambda href: href.endswith(".xlsx") or href.endswith(".csv"))
    return links

def download_file_if_new(output_dir, soup):
    links = find_links_to_xlsx_and_csv_files(soup)
    # Download each file
    for link in links:
        file_name = link["href"].split("/")[-1]
        file_path = os.path.join(output_dir, file_name)
        # Check if the file already exists
        if not os.path.exists(file_path):
            response_ppp = requests.get(link["href"])
            with open(file_path, "wb") as f:
                f.write(response_ppp.content)
        else:
            print(f"File {file_path} already exists, skipping download.")

def get_naics(output_dir):
    url = "https://www.census.gov/naics/2022NAICS/2022_NAICS_Structure.xlsx"
    response = requests.get(url)

    #xlsx_file_path = os.path.join(output_dir, "2022_NAICS_Structure.xlsx")
    #csv_file_path = os.path.join(output_dir, "2022_NAICS_Structure.csv")
    filename = os.path.basename(url)
    #filename_no_ext = os.path.splitext(filename)
    filename_no_ext = os.path.splitext(filename)[0]

    xlsx_file_path = os.path.join(output_dir, filename)
    csv_file_path = os.path.join(output_dir, filename_no_ext + ".csv")

    if not os.path.exists(xlsx_file_path):
        with open(xlsx_file_path, "wb") as f:
            f.write(response.content)

        df = pd.read_excel(xlsx_file_path)
        df.to_csv(csv_file_path, index=False)
    else:
        print(f"File {xlsx_file_path} already exists. Skipping download.")


def tickers(x):
    # Morgan Stanley and Goldman Sachs did not appear in the lenders.
    # We discuss reasons why in our report conclusions.
    if "JPMorgan Chase Bank" in x:
        return "JPM"
    return "Other"

def etl_ppp(output_dir):
    """
    Keep a select list of the PPP variables and combine the 13 source files. Make some ETLs.
    """
    keep_cols_ppp = [
        "LoanNumber",
        "NAICSCode",
        "OriginatingLender",
        "DateApproved",
        "SBAOfficeCode",
        "ProcessingMethod",
        "BorrowerName",
        "LoanStatusDate",
        "LoanStatus",
        "Term",
        "ServicingLenderName",
        "ForgivenessAmount",
        "ForgivenessDate",
    ]

    # Create a list of the paths to the CSV files that start with "public_"
    # and end with ".csv" in the output_dir directory.
    csv_files = [
        os.path.join(output_dir, f) for f in os.listdir(output_dir) if f.startswith("public_")
        and f.endswith(".csv")
    ]

    # The axis=0 argument tells the pd.concat() function to concatenate
    # the DataFrames along the axis=0, which is the row axis.
    # This means that the DataFrames will be stacked on top of each other,
    # with the rows of each DataFrame being appended to the rows of the previous DataFrame.
    if not os.path.exists(os.path.join(output_dir, "Finaldf.csv")):
        Newdf = pd.concat([pd.read_csv(f, usecols=keep_cols_ppp) for f in csv_files], axis=0)

        finaldf = Newdf.copy()
        finaldf['OriginatingLender'] = finaldf['OriginatingLender'].astype(str)
        finaldf['OriginatingLenderSymbol'] = finaldf['OriginatingLender'].apply(tickers)

        del Newdf
        finaldf.to_csv(os.path.join(output_dir, "Finaldf.csv"))
#    else:
#        finaldf = pd.read_csv(os.path.join(outdir, "Finaldf.csv"))

    return finaldf

def 


def main():
    # Set the URL of the SBA PPP FOIA dataset
    url_ppp = "https://data.sba.gov/dataset/ppp-foia"
    # Set the directory to write the downloaded files to
    output_dir = "/mnt/c/Users/topre/Downloads/ppp-foia/"
    # Create a directory to store the downloaded files
    check_if_dir_exists(output_dir)
    # Get the HTML response from the URL
    response_ppp = requests.get(url_ppp)
    # Create a Beautiful Soup object from the HTML response
    soup = BeautifulSoup(response_ppp.content, "html.parser")
    # Download PPP FOIA CSV files if new
    download_file_if_new(output_dir, soup)
    # Get NAICS files if new
    get_naics(output_dir)
    # Combine the PPP FOIA CSV files if new
    etl_ppp(output_dir)

if __name__ == "__main__":
    main()
