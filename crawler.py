import os
import fitz  # PyMuPDF
import pandas as pd
import re

pdf_path = 'path/to/root/folder/of/all/pdfs'

def extract_text_from_pdf(pdf_path):
    """ This function reads the textual information in a pdf and extract them in raw format for further processing. 
    It divides the text into pages and the output is a list of all the page contents.
    """
    # Open the PDF file
    pdf_document = fitz.open(pdf_path)
    whole_text = []
    # Iterate through each page
    for page_num in range(len(pdf_document)):
        page = pdf_document.load_page(page_num)
        text = page.get_text("text")
        print(f"Page {page_num + 1}:\n{text}\n")
        whole_text.append(page)
    return whole_text
# Example usage


def append_data(pdf_text,filename):
    """ This function extracts chunks of data from the raw text that was extracted from the PDF and organizes them in a tabular format. 
    The patterns should be adjusted according to the pdfs'structure"""
    pattern = r'(?m)(?<!\d °)(?<!\d°)(?<!z\. )(?<!z\.)([A-Z]\. )(.*?)(?=(?<!\d°)(?<!z\. )(?<!z\.B)(?<!\d °)(?<!\d°)[A-G]\. |\Z)'
    count = 1
    cat_text = {}
    for page in pdf_text:
        text = page.get_text('text')
        ## removing unnecessary characters that are in my data, may need to skip this if your data is clean
        text = re.sub(r'[\n\xa0]','',text)
        result = re.findall(pattern,text)
        for item in result:
            ## again, regex patterns are specific to my data and can be changed.
            nummers = re.findall(r'Nr. *\S+',item[1])
            cat_text[count] = [nummers,item[1]]
            count+=1
            df = pd.DataFrame(cat_text).T
            df.to_csv(f'katalogue_mined_data/{filename}.csv',encoding='utf-8',sep=';')
    


def folder_crawler(root_folder):
    """ This function crawls a folder with all the PDF files that are to be crawled and mined. 
    Using the two other functions (extract_text_from_pdf, append_data) it crawls the files in the folder,
    reads the text and process it further to create csv files that structure the pdf data into columns of 
    product_numbers and product descriptions (can be modified based on requirements).

    """
    # Walk through the root folder and its subfolders
    for foldername, subfolders, filenames in os.walk(root_folder):
        for filename in filenames:
            if filename.lower().endswith('.pdf'):
                pdf_path = os.path.join(foldername, filename)
                print(f'Opening {pdf_path}')
                pdf_text = extract_text_from_pdf(pdf_path)
                append_data(pdf_text,filename)


folder_crawler(pdf_path)