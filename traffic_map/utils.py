def clean_table(table):
    pd.set_option('future.no_silent_downcasting', True)
    newtable = table
    nan_value = float("NaN")
    df = newtable.df
    df.replace("", nan_value, inplace=True)
    df.dropna(thresh=10, axis=1, inplace=True) # axis = 1 means 'columns'
    df.dropna(thresh=10, axis=0, inplace=True) # axis = 0 means rows (i.e. 'index')
    df.replace("\\(cid\\:\\d+\\)", nan_value, inplace=True, regex=True)
    newtable.df = df
    if (len(df) > 0):
        return(newtable)
    else:
        return(None)

# function to locate and fix problematic cells
# e.g., 4 digits, 2 sets of repeating - 1313 should be 13
def fix_nums(string):
    if len(string) > 3 and len(string) % 2 == 0:
        slen2 = round(len(string)/2)
        return(re.sub('(\d{'+str(slen2)+',})\\1+', '\\1', string=string))
    else:
        return(string)

# this chunk will crawl the Oak Park website searching for PDFs of past traffic meetings

from datetime import date, timedelta
import requests

# Function to give a date range
def daterange(start_date: date, end_date: date):
    days = int((end_date - start_date).days)
    for n in range(days):
        yield start_date + timedelta(n)

# Function to check if a url exists
def check_url_exists(url: str):
    return requests.head(url, allow_redirects=True, timeout=10).status_code == 200



# Function to clean tables (remove NAs, etc)
def clean_table(tab):    
    tab.df.replace("", "NaN", inplace=True)
    tab.df.dropna(thresh=10, axis=1, inplace=True) # axis = 1 means 'columns'
    tab.df.dropna(thresh=10, axis=0, inplace=True) # axis = 0 means rows (i.e. 'index')
    tab.df.replace("\\(cid\\:\\d+\\)", "NaN", inplace=True, regex=True)
    if (len(tab.df) == 0):
        return
    else:
        return tab

