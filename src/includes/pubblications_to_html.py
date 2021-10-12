#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
from IPython.display import HTML


# In[2]:


sheet_id = '1VaF5jAauYYYKo1WH40kLlsQ0-azIX5eMZoFYv5JrVr0'
sheet_names = ['papers','dataset','algorithms','masterThesis','phdThesis']


# In[3]:


def write_html(string,path='src/includes/', filename='filename',extension='pug'):
    Html_file= open(f"{path}{filename}.{extension}","w")
    Html_file.write(string)
    Html_file.close()


# ## Papers


sheet_name= sheet_names[0]
url = f'https://docs.google.com/spreadsheets/d/{sheet_id}/gviz/tq?tqx=out:csv&sheet={sheet_name}'


papers = pd.read_csv(url)


# ### Pug version

bullets=''
for i, row in papers.iloc[1:].iterrows():
    authors= row['Authors']
#     pubblicationYear = int(row['Year of publication'])
    pubYearString = row['Year of publication']
    pubblicationYear =  '.' if pubYearString!=pubYearString else str(int(pubYearString))

    title=row['Title of the scientific publication'].strip('.')

    journalString=row['Title of the journal or equivalent']
    journal='.' if journalString!=journalString else ', '+journalString.strip()+'.'
    DOI=row['DOI']

    bullet=f'''li
    div.mb-3
        a(href='https://doi.org/{DOI}', target="_blank")
            | {authors} ({pubblicationYear}). #[strong {title}]
'''
    if row['visible on website'] == 'YES':
        bullets+=bullet

write_html(bullets, filename='paper-list')


# ## Thesis

sheet_name= sheet_names[3]
url = f'https://docs.google.com/spreadsheets/d/{sheet_id}/gviz/tq?tqx=out:csv&sheet={sheet_name}'


masterThesis = pd.read_csv(url)


bulletsThesis=''
for i, row in masterThesis.iterrows():
    author= row['Author']
    title= row['Title']
    title = '' if title!=title else title

    status= row['Status [Ongoing] / [completed]']

    classification = row['Thesis ']
    year= row['Year']

    bullet=f'''li
    div.mb-3
        | {author} - #[strong {title}]. [{classification} - {year} - {status}]
'''
    if row['visible on website'] == 'YES':
        bulletsThesis+=bullet


write_html(bulletsThesis, filename='thesis-list')

