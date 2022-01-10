#!/usr/bin/env python
# coding: utf-8

# In[274]:


import pandas as pd
from IPython.display import HTML
import math


# In[275]:


import inflect
p = inflect.engine()
p.number_to_words(99)


# In[276]:


sheet_id = '1VaF5jAauYYYKo1WH40kLlsQ0-azIX5eMZoFYv5JrVr0'
sheet_names = ['papers','dataset','algorithms','masterThesis','phdThesis']


# In[277]:


def write_html(string,filename='filename',extension='pug'):
    Html_file= open(f"{filename}.{extension}","w")
    Html_file.write(string)
    Html_file.close()


# ## Papers

# In[278]:


sheet_name= sheet_names[0]
url = f'https://docs.google.com/spreadsheets/d/{sheet_id}/gviz/tq?tqx=out:csv&sheet={sheet_name}'


# In[279]:


papers = pd.read_csv(url,header=0)
papers.columns


# In[280]:


bullets='<ul>'
for i, row in papers.iterrows():
    authors= row['Authors']
#     pubblicationYear = int(row['Year of publication'])
    pubYearString = row['Year of publication']
    pubblicationYear =  '.' if pubYearString!=pubYearString else ' - '+str(int(pubYearString))+' -'
    title=row['Title of the scientific publication'].strip('.')
    
    journalString=row['Title of the journal or equivalent']
    journal='.' if journalString!=journalString else ', '+journalString.strip()+'.'
    DOI=row['DOI']
    
    bullet=f"<li><strong><a href='https://doi.org/{DOI}' target='_blank'>{title}</a></strong>{pubblicationYear} {authors} {journal}</li>"
    if row['visible on website'] == 'YES':
        bullets+=bullet
bullets+='</ul>'
#display(HTML(bullets))


# ### Pug version

# In[281]:


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
# display(HTML(bullets))


# In[282]:


write_html(bullets, filename='paper-list')


# In[283]:


cards=''
for i, row in papers.iterrows():
    authors= row['Authors']
    abstract= row['abstract']
    researchLine= row['Research line']
    
    if isinstance(researchLine, str):
        researchLine=researchLine.replace(",", "▪")
        rlString=f'''p.my-1
                small Research Line #[strong {researchLine}]'''
    else:
        rlString=''

    if isinstance(abstract, str):
        abstractButton= f'''p.my-1
            a.btn-mini.px-2.btn-secondary.small(href='#' data-toggle='collapse' data-target='#collapse-{p.number_to_words(i)}' aria-expanded='true' aria-controls='collapseAbs') Abstract'''
    else:
        abstractButton=''
#     pubblicationYear = int(row['Year of publication'])
    pubYearString = row['Year of publication']
    pubblicationYear =  '.' if pubYearString!=pubYearString else str(int(pubYearString))
    
    title=row['Title of the scientific publication'].strip('.')
    
    journalString=row['Title of the journal or equivalent']
    journal='.' if journalString!=journalString else ', '+journalString.strip()+'.'
    DOI=row['DOI']
    
    ptOne=f'''.row.mt-4.justify-content-center
    .col-lg-1.text-right
        h4 {i}.'''
    # summary image?
    if row['summary image']=='YES':
        ptTwo=f'''
    .col-lg-2.pl-0
        img(src='assets/images/pubblications/pubblication_demo_img.jpg ' alt="immagine" style='width:100%;').mr-3
    .col-lg-6.bg-yellow.p-3'''
    else:
        ptTwo=f'''
    .col-lg-8.bg-yellow.p-3'''

    ptThree=f'''
        #accordion-{p.number_to_words(i)}.accordion
        | #[strong {title}] 
        br
        | #[em {authors}] ({pubblicationYear}) - {journalString}
        #collapse-{p.number_to_words(i)}.collapse(aria-labelledby='heading-{p.number_to_words(i)}' data-parent='#accordion-{p.number_to_words(i)}')
            div.bg-yellow
                hr
                p.small ABSTRACT: {abstract}
    .col-lg-2.pl-3
        p.my-1
            a.btn-mini.px-2.btn-secondary.small(href='https://doi.org/{DOI}', target="_blank") Resource Link
        p.mb-1.mt-0
            a.btn-mini.px-2.btn-secondary.small(href="about.html") BibTeX
        {abstractButton}
        {rlString}
'''
    
    card= ptOne+ptTwo+ptThree
    if row['visible on website'] == 'YES':
        cards+=card
    
# display(HTML(bullets))


# In[284]:


write_html(cards, filename='paper-cards')


# ## Thesis

# In[135]:


sheet_name= sheet_names[3]
url = f'https://docs.google.com/spreadsheets/d/{sheet_id}/gviz/tq?tqx=out:csv&sheet={sheet_name}'


# In[16]:


masterThesis = pd.read_csv(url)
masterThesis.columns


# In[17]:


bulletsThesis='<ul>'

for i, row in masterThesis.iterrows():
    author= row['Author']
    title= row['Title']
    title = '' if title!=title else title
    
    status= row['Status [Ongoing] / [completed]']
    
    classification = row['Thesis ']
    year= row['Year']
    bullet=f"<li>{author}, <strong>{title}</strong> [{classification} - {year} - {status}]</li>"
    if row['visible on website'] == 'YES':
        bulletsThesis+=bullet
bulletsThesis+='</ul>'
#display(HTML(bulletsThesis))


# #### Pug version

# In[18]:


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
    
#     bullet=f"<li>{author}, <strong>{title}</strong> [{classification} - {year} - {status}]</li>"
#display(HTML(bulletsThesis))


# In[19]:


write_html(bulletsThesis, filename='thesis-list')


# # Algorithms made by XAI group 

# In[20]:


sheet_name= sheet_names[2]
url = f'https://docs.google.com/spreadsheets/d/{sheet_id}/gviz/tq?tqx=out:csv&sheet={sheet_name}'


# In[21]:


algo = pd.read_csv(url)
algo.columns


# In[22]:


bulletsAlgo='<ul>'

for i, row in algo.iterrows():
    author= row['Authors']
    title= row['Title']
    title = '' if title!=title else title
    
    description= row['Brief Description']
    description = '' if description!=description else ' - '+description.strip('.')+', '
    
    githubLink=row['github link']
    
    bullet=f"<li><strong>{title}</strong> {description} [ {author} ] </li>"
    bulletsAlgo+=bullet
bulletsAlgo+='</ul>'
#display(HTML(bulletsAlgo))


# In[ ]:




