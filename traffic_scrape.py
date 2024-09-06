# Idea for traffic analysis
# Download traffic calming petition status

# Here is another possible place to scrape/download traffic data
# https://idot.public.ms2soft.com/tcds/tsearch.asp?loc=Idot&mod=

# Setup
import sys
import os
import numpy as np
import pandas as pd
import camelot
import seaborn as sns

import urllib.request
import time
import requests
import re # regex
#import tabula # conda install tabula-py
import httplib2 # pip install httplib2
from PyPDF2 import PdfReader
#from bs4 import BeautifulSoup
from datetime import date, timedelta

# Where to put the project output
OUTDIR = '/Users/chad/Desktop/traffic_pdfs/'
PDF_DIR = os.path.join(OUTDIR + "pdfs")

# Create a path to put downloaded PDFs in
os.mkdir(OUTDIR + "/pdfs")

# Function to give a date range
def daterange(start_date: date, end_date: date):
	days = int((end_date - start_date).days)
	for n in range(days):
		yield start_date + timedelta(n)


# Set start and end dates for crawling web
start_date = date(2019, 1, 1)
end_date = date(2024, 8, 12)

# Function to check if a url exists
def check_url_exists(url: str):
	return requests.head(url, allow_redirects=True).status_code == 200

# Crawl Oak Park website looking for PDF files on specific dates
urls = []
for target_date in daterange(start_date, end_date):
	date_fmt = target_date.strftime("%Y-%m-%d")
	print(date_fmt)
	url = 'https://www.oak-park.us/sites/default/files/meeting-resources/' + date_fmt + '-transportation-commission-agenda_0.pdf'
	if check_url_exists(url):
		print('Found a record on ' + date_fmt)
		urls.append(url)

# Save output to TXT file
with open(OUTDIR + "/urls.txt", "w") as outfile:
	outfile.write("\n".join(urls))

# For every line in the file
for url in urls:
	name = url.rsplit('/', 1)[-1]
	filename = os.path.join(OUTDIR + "pdfs", name)
	if not os.path.isfile(filename):
		urllib.request.urlretrieve(url, filename)

# Load all data frames in PDF

import glob

pdf_files = glob.glob("%s/*.pdf" % PDF_DIR)

alldat = []

reader = PdfReader(pdf_files[39])
print(len(reader.pages))
page = reader.pages[40]
text = page.extract_text()
text

# TODO write a loop that filters and keeps only pages with data tables



# for help- help(re)

# Extract metadata about the table
# re.findall('Date Start: (.+)', text)
# re.findall('Date End: (.+)', text)
# re.findall('NB|SB', text)

# Extract the data table
# df = tabula.read_pdf(pdf_files[1], pages=33, multiple_tables=False, lattice=False, stream=False, pandas_options={'header':None})

# help(camelot.read_pdf)

# NB dir() gives you info about what you can do with an object! great for learning.

nan_value = float("NaN")

# f=pdf_files[1]

pd.set_option('future.no_silent_downcasting', True)

def clean_table(tab):
	df=tab.df
	df.replace("", nan_value, inplace=True)
	df.dropna(thresh=10, axis=1, inplace=True) # axis = 1 means 'columns'
	df.dropna(thresh=10, axis=0, inplace=True) # axis = 0 means rows or index
	df.replace("\\(cid\\:\\d+\\)", nan_value, inplace=True, regex=True)
	return(df)

#def scrape_table(pdf):

# TODO write function that gets metadata for a given page (e.g., street name, start/end dates, etc)

#pdf=pdf_files[1]

import matplotlib.pyplot as plt

allTables = []



pdf=pdf_files[1]

for pdf in pdf_files:
	print('Processing ' + pdf + '...')
	inTables = camelot.read_pdf(pdf, pages='all', flavor='stream', strip_text='\n')
	outTables = [table for table in inTables if len(table.rows) * len(table.cols) > 240] # Only keep tables with certain number of cells (>240)
	cleanTables = [clean_table(table) for table in outTables]
	allTables.append([x for x in cleanTables if x is not None])

df = allTables[0][2]

df.head(5)

type(df)

help(sns.heatmap)

df = df.iloc[2:26, 1:17]

np.array(df)

#sns.heatmap(df)


xaxis=df[1]
yaxis=df[2]
plt.plot(xaxis,yaxis)
plt.show()


c = ax.pcolormesh(x, y, z, cmap='RdBu', vmin=z_min, vmax=z_max)



re.findall('\n[0-9\\/\\:]+[0-9\\s]{16,16}', text)

# REGEX structure I'm looking for in a row of data-
# new line - time 12:00 - space - number (w or w/o space) x 16
# \\:(\\s)?\\d{2,2} 

re.findall('\n.*?[\:|\/]\d{2,2}[0-9\\s]+', text)

# re.findall('\n.*?[\\:|\\/|PM]\\s*\\d\\s*\\d\\s*?(\\d*\\s*){16,16}', text)

# re.findall('\\n.*?[\\:|\\/|PM]\\s*\\d\\s*\\d\\s*[\\d\\s*]{16,16}', text) # working?

# maybe working?
text2="\n0 0 0 0 3 0 0 0 0 0 0 0 0 0 0 0 3\n0 0 0 3 10 1 0 0 0 0 0 0 0 0 0 0 14\n00000000000000000 \n1 2 3 14444 3 2 3 4 5 4 3 2 1 2 3 4 5"
tmp = re.findall('\\n((\\d){16,16}|(\\d*\\s*){16,16})', text2) # this is working to get the digits. still need to work at finding the prefix time/date in a row..


text2 = "\n02/02/02 0 0 0 0 33 0 0 0 0 0 0 0 0 0 0 0 33\n0 1:00 0 0 0 3 10 1 0 0 0 0 0 0 0 0 0 0 14\n12 PM 00000000000000000\n13:00 1 2 3 14444 3 2 3 4 5 4 3 2 1 2 3 4 5\n"
tmp = re.findall('\n.*?(PM\\s*|[:|/]\\s*\\d\\s*\\d\\s*)((\\d){17,17}|(\\d*\\s*){17,17})(?=\n)', text2) # WORKS!
tmp[1][0]
# To access first in each list element
# Option 1: list comprehension(?)
[item[1] for item in tmp]
# Option 2: numpy
np.array(tmp)[:,1]

# SHIT - row 8 of table on p. 41 of 2024-04-08 PDF screws things up-
# 2122 1 02720000 2 8
# There's no way to know that the '1 0' should be a '10'

re.findall('Start\\sDate:\\s*([0-9/]+)', text)
re.findall('End\\sDate:\\s*([0-9/]+)', text)

tmp = re.findall('\n.*?([A|P]\\s*M\\s*|[:|/]\\s*\\d\\s*\\d\\s*)((\\d){17,17}|(\\d*\\s*){17,17})(?=\n)', text)  # WORKS better

type(tmp) # this says it's a list


# re.findall('\\n((\\d){16,16}|(\\d*\\s*){16,16})', text2)


# Convert into array



# 



# re.findall('\\n\\d+\\/\\d+\\/\\d+\\s*(\\d\\s*)+', text)
# re.findall('\\n\\d+[\\:|\\/|PM]\\s*\\d\\s*\\d\\s*[\\d\\s*]{16,16}', text)

#help(re)
# re.findall('\\n.*?[\\:|\\/|PM]\\s*\\d\\s*\\d\\s*(\\d+\\s*).*?$', text)
# re.match('\\n.*?[\\:|\\/|PM]\\s*\\d\\s*\\d\\s*(\\d+\\s*).*?\\n', text)
# re.fullmatch('\\n.*?[\\:|\\/|PM]\\s*\\d\\s*\\d\\s*(\\d+\\s*).*?$', text)

# NB: I should probably make this customizable where user can input a search pattern



# IDEAS

# Idea 1
# ^((\d){16,16}|(\d*\s*){16,16})
# this seems to get close to picking the numbers I want (problem data rows with only single digit number have no spaces, but rows with a least 1 double-digit number have spaces between all numbers I think.. )
# I think regex is first searching the \d and then the \d*\s*


import pdftotext  # first 1) brew install poppler, 2) pip install pdftotext

with open(pdf_files[1], 'rb') as file:
	pdftotext_string = pdftotext.PDF(file)

pdftotext_string[31]

pdftotext_lines = ("\n\n".join(pdftotext_string).splitlines())
pdftotext_lines = [ln for ln in pdftotext_lines if ln]
pdftotext_lines


import pdfplumber
pdf = pdfplumber.open(pdf_files[1])
page = pdf.pages[31]
page.extract_table(vertical_strategy="text")


# Is there a way to search loosely for a 24 x 16 matrix?? (24 hours, 16 speed classes)

# Concatenate!
pd.concat(dfs2[4:16])

# Set columns based on what's in PDF (search for metadata)
# data[4].columns = ['time', ]

# Plot?
data[4][0]  # this looks at column 5 in data set 5

#data[4].plot(x='0', y='1')

# Save to CSV

#tables_json = [table.to_json(orient='records') for table in tables]
#print(tables_json)

# Extract table
# TIME

r.headers.get('content-type') # is a PDf

with requests.Sesssion() as s:
	try:
		webpage_response = s.get(myurl)


# Convert PDF to text
reader = PdfReader('pdffile.pdf')
page = reader.pages[0]
extracted_text = page.extract_text()

print(extracted_text)

# Output text


# Do REgex stuff to find table of interest




# Save as cleaned CSV



# Merge multiple CSV files




# Do stats..



# Scrape PDFs for data on speed

# Get attributes of blocks (from google maps?)

# Do logistic regression to predict traffic volume/speed/etc. from predictors (proximity to busy street, account for proximity to other blocks in study.. ) - unit would be a block.

# Create novel insights for Oak Park.

