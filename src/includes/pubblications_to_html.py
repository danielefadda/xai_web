#!/usr/bin/env python
# coding: utf-8

import pandas as pd
from IPython.display import HTML
import math

#Convert numbers to words
import inflect
p = inflect.engine()
p.number_to_words(99)

import urllib.request
from urllib.error import HTTPError
import sys


# Import google spreadsheet
sheet_id = '1VaF5jAauYYYKo1WH40kLlsQ0-azIX5eMZoFYv5JrVr0'
sheet_names = ['papers','dataset','algorithms','masterThesis','phdThesis']


# Function to convert text to pug file
def write_html(string,filename='filename',path='src/includes/',extension='pug'):
    Html_file= open(f"{path}{filename}.{extension}","w")
    Html_file.write(string)
    Html_file.close()

### PAPERS
# Import Papers
sheet_name= sheet_names[0]
url = f'https://docs.google.com/spreadsheets/d/{sheet_id}/gviz/tq?tqx=out:csv&sheet={sheet_name}'

papers = pd.read_csv(url,header=0)
papers.columns
# Visualization order of the papers (featured before then year of publication)
papers=papers.sort_values(by=['featured','Year of publication'], ascending = False).reset_index(drop=True)


### Create Pug version for papers

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

    pubYearString = row['Year of publication']
    pubblicationYear =  '.' if pubYearString!=pubYearString else str(int(pubYearString))
    title=row['Title of the scientific publication'].strip('.')

    container=row['container']
    if not isinstance(container, str):
        container=''
    else:
        container=f' - {container}'
    journal=row['Title of the journal or equivalent']
    if not isinstance(journal, str):
        journal=''
    else:
        journal=f'. In {journal}'

    DOI=row['DOI']
    doiLink=row['doi link']
    image= row['image file']

    if isinstance(DOI, str):
        #Doi to bibtex
        BASE_URL = 'http://dx.doi.org/'
        url = BASE_URL + DOI
        req = urllib.request.Request(url)
        req.add_header('Accept', 'application/x-bibtex')
        try:
            with urllib.request.urlopen(req) as f:
                bibtex = f.read().decode()
                bibtex=bibtex.replace('\t','                    ')
                bibtex=bibtex[:-1] + "                }"
        except HTTPError as e:
            if e.code == 404:
                bibtex='BibTex not found'
            else:
                bibtex='BibTex not found.'# Service unavaillable
    else:
        bibtex='BibTex not found'

    #Create buttons IF:
        #More information
    if (isinstance(abstract, str) or (bibtex not in['BibTex not found','BibTex not found.']) ):
        if not (isinstance(abstract, str)):
            abstract= 'ABSTRACT NOT FOUND'

        abstractButton= f'''p.my-1
            a.btn-mini.px-2.btn-secondary.small(href='#' data-toggle='collapse' data-target='#collapse-{p.number_to_words(i)}' aria-expanded='true' aria-controls='collapseAbs') More information'''
    else:
        abstractButton=''

        #External link
    if (isinstance(doiLink, str)):
        externalButton= f'''p.my-1
            a.btn-mini.px-2.btn-secondary.small(href='{doiLink}', target="_blank") External Link'''
    else:
        externalButton= ''

    ##### string composition for pug file:
    ptOne=f'''.row.mt-4.justify-content-center
    .col-lg-1.text-right
        h4 {i+1}.'''

    # summary image?
    if row['summary image']=='YES':
        ptTwo=f'''
    .col-lg-2.pl-0
        img(src='assets/images/pubblications/{image} ' alt="immagine" style='width:100%;' data-toggle='modal' data-target='#modal-{p.number_to_words(i)}' type='button').mr-3
        #modal-{p.number_to_words(i)}.modal.fade(tabindex='-1' role='dialog' aria-labelledby='#modal-{p.number_to_words(i)}-Title' aria-hidden='true')
            .modal-dialog.modal-lg.modal-dialog-centered(role='document')
                .modal-content
                    .modal-header
                        p.small {title}
                        button.close(type='button' data-dismiss='modal' aria-label='Close')
                            span(aria-hidden='true') &times;
                    .modal-body
                        img(src='assets/images/pubblications/{image} ' alt="immagine" )
    .col-lg-6.bg-yellow.p-3'''
    else:
        ptTwo=f'''
    .col-lg-8.bg-yellow.p-3'''

    ptThree=f'''
        #accordion-{p.number_to_words(i)}.accordion
        | #[strong {title}]
        br
        | #[em {authors}] ({pubblicationYear}){container}{journal}
        #collapse-{p.number_to_words(i)}.collapse(aria-labelledby='heading-{p.number_to_words(i)}' data-parent='#accordion-{p.number_to_words(i)}')
            div.bg-yellow
                hr
                p.small #[strong Abstract]
                p.small {abstract}
            p.small.pt-2 #[strong BibTex]
            p.small.
                {bibtex}
    .col-lg-2.pl-3
        {abstractButton}
        {externalButton}
        {rlString}
'''

    card= ptOne+ptTwo+ptThree
    if row['visible on website'] == 'YES':
        cards+=card

### save pug file:
write_html(cards, filename='paper-cards')


### THESIS

sheet_name= sheet_names[3]
url = f'https://docs.google.com/spreadsheets/d/{sheet_id}/gviz/tq?tqx=out:csv&sheet={sheet_name}'
masterThesis = pd.read_csv(url)
masterThesis.columns

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


# ### Algorithms made by XAI group
#
# sheet_name= sheet_names[2]
# url = f'https://docs.google.com/spreadsheets/d/{sheet_id}/gviz/tq?tqx=out:csv&sheet={sheet_name}'
#
#
# algo = pd.read_csv(url)
# algo.columns
#
# bulletsAlgo='<ul>'
#
# for i, row in algo.iterrows():
#     author= row['Authors']
#     title= row['Title']
#     title = '' if title!=title else title
#
#     description= row['Brief Description']
#     description = '' if description!=description else ' - '+description.strip('.')+', '
#
#     githubLink=row['github link']
#
#     bullet=f"<li><strong>{title}</strong> {description} [ {author} ] </li>"
#     bulletsAlgo+=bullet
# bulletsAlgo+='</ul>'
# display(HTML(bulletsAlgo))




