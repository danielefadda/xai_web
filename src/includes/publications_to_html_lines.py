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
papers=papers.iloc[::-1] #reverse all
papers=papers.sort_values(by=['featured','Year of publication'], ascending = False).reset_index(drop=True)


### Create Pug version for papers inside each reasearch line

lines = [*range(1,6,1)]
for line in lines:
    cards=''
    paperi = papers[papers['Research line'].str.contains(str(line), case=False, na=False)]
    for i, row in paperi.iterrows():
        authors= row['Authors']
        abstract= row['abstract']
        idAlpha= row['Id di Riccardo']

        researchLine= row['Research line']
        if isinstance(researchLine, str):
            researchLine=researchLine.replace(",", "▪")
            rlString=f'''p.my-1
                    small Research Line #[strong {researchLine}]'''
        else:
            rlString=''

        pubYearString = row['Year of publication']
        publicationYear =  '.' if pubYearString!=pubYearString else str(int(pubYearString))
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
        imageSize= row['image size']
        if imageSize=='big':
            modalSize='.modal-lg'
        else:
            modalSize=''


        #Create buttons IF:
            #More information
        if (isinstance(abstract, str)  ):
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
        ptOne=f'''#{idAlpha}.row.mt-5.justify-content-center
    .col-lg-1.text-right
        h4 {i+1}.
        small [{idAlpha}]'''

        # summary image?
        if row['summary image']=='YES':
            ptTwo=f'''
    .col-lg-2.pl-0
        img(src='assets/images/publications/{image} ' alt="immagine" style='width:100%;' data-toggle='modal' data-target='#modal-{p.number_to_words(i)}' type='button').mr-3.border.border-secondary.bwc-image
        #modal-{p.number_to_words(i)}.modal.fade(tabindex='-1' role='dialog' aria-labelledby='#modal-{p.number_to_words(i)}-Title' aria-hidden='true')
            .modal-dialog{modalSize}.modal-dialog-centered(role='document')
                .modal-content
                    .modal-header
                        p.small {title}
                        button.close(type='button' data-dismiss='modal' aria-label='Close')
                            span(aria-hidden='true') &times;
                    .modal-body
                        img(src='assets/images/publications/{image} ' alt="immagine" )
    .col-lg-6.bg-yellow.p-3'''
        else:
            ptTwo=f'''
    .col-lg-8.bg-yellow.p-3'''

        ptThree=f'''
        #accordion-{p.number_to_words(i)}.accordion
        | #[strong {title}]
        br
        | #[em {authors}] ({publicationYear}){container}{journal}
        #collapse-{p.number_to_words(i)}.collapse(aria-labelledby='heading-{p.number_to_words(i)}' data-parent='#accordion-{p.number_to_words(i)}')
            div.bg-yellow
                hr
                p.small #[strong Abstract]
                p.small {abstract}
    .col-lg-2.pl-3
        {abstractButton}
        {externalButton}
        {rlString}
    '''

        card= ptOne+ptTwo+ptThree
        if row['visible on website'] == 'YES':
            cards+=card

    ### save pug file:
    write_html(cards, filename=f'paper-cards-{line}')
