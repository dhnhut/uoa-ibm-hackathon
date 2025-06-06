import os
import re
import json
from pathlib import Path
from parsers import terms, acronyms_and_abbreviations, category_9

import pymupdf # imports the pymupdf library

def clean_unrelated_text(text):
  pagination_regex = r'(New Zealand Strategic Goods List November 2024 \nPage\s\d+)'
  cleaned_text=re.sub(pagination_regex, '', text, flags=re.MULTILINE)
  return cleaned_text

def extract_text_from_pdf(pdf_path):
  with  pymupdf.open(pdf_path) as doc: # open a document
    text = ''

    for page in doc: # iterate the document pages
      text += clean_unrelated_text(page.get_text())

  return text

def write_text_to_file(text, file_path):
  with open(file_path, "w") as file:
    file.write(text)
 

parts = [
  {
    "name": "terms",
    "parser": terms,
    "file": "_1_terms_14_32",
    "pages": [13, 31]
  },
  {
    "name": "acronyms_and_abbreviations",
    "parser": acronyms_and_abbreviations,
    "file": "_2_acronyms_and_abbreviations_33_36",
    "pages": [32, 35]
  },
  {
    "name": "category_9",
    "parser": category_9,
    "file": "_3_category_9_aerospace_and_propulsion_286_308",
    "pages": [285, 307]
  },
  # {
  #   "name": "category_9_sensitive",
  #   "parser": category_9.sensitive_parser,
  #   "file": "4_category_9_sensitive_list_of_dual_use_318_321",
  #   "pages": [319, 320]
  # },
  # {
  #   "name": "category_9_very_sensitive",
  #   "parser": category_9.very_sensitive_parser,
  #   "file": "5_category_9_very_sensitive_list_of_dual_use_327_327",
  #   "pages": [326, 326]
  # }
]

def extract_data():
  dir_path = os.path.dirname(os.path.realpath(__file__))
  Path(f"{dir_path}/parsed").mkdir(parents=True, exist_ok=True)
  with  pymupdf.open(f'{dir_path}/documents/NZ-Strategic-Goods-List-November.pdf') as doc: # open a document
    for part in parts:
      file_path = f'{dir_path}/parsed/{part['file']}'

      with pymupdf.open() as part_doc: # new empty PDF
        pdf_path = f"{file_path}.pdf"
        part_doc.insert_pdf(doc, from_page=part['pages'][0], to_page=part['pages'][1])
        part_doc.save(pdf_path)

      raw_text = extract_text_from_pdf(pdf_path)
      write_text_to_file(raw_text, f'{file_path}.raw.txt')
      
      parsed_json = part['parser'].to_json(raw_text)
      json_text = json.dumps(parsed_json, indent=2, ensure_ascii=False)
      write_text_to_file(json_text, f'{file_path}.json')
      
      parsed_txt = part['parser'].to_txt(parsed_json)
      write_text_to_file(parsed_txt, f'{file_path}.txt')

extract_data()