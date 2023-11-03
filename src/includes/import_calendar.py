from __future__ import print_function

import datetime
import os.path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

import inflect
p = inflect.engine()


def write_html(string,filename='filename',path='src/includes/',extension='pug'):
    Html_file= open(f"{path}{filename}.{extension}","w")
    Html_file.write(string)
    Html_file.close()
    
month_dict = {'01': 'Jan',
              '02': 'Feb',
              '03': 'Mar',
              '04': 'Apr',
              '05': 'May',
              '06': 'Jun',
              '07': 'Jul',
              '08': 'Aug',
              '09': 'Sep',
              '10': 'Oct',
              '11': 'Nov',
              '12': 'Dec'}
    
    
# If modifying these scopes, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/calendar.readonly']

"""Shows basic usage of the Google Calendar API.
Prints the start and name of the next 10 events on the user's calendar.
"""
creds = None
# The file token.json stores the user's access and refresh tokens, and is
# created automatically when the authorization flow completes for the first
# time.
if os.path.exists('src/includes/.credentials/credentials.json'):
    creds = Credentials.from_authorized_user_file('src/includes/.credentials/credentials.json', SCOPES)
# If there are no (valid) credentials available, let the user log in.
if not creds or not creds.valid:
    if creds and creds.expired and creds.refresh_token:
        creds.refresh(Request())
    else:
        flow = InstalledAppFlow.from_client_secrets_file(
            'src/includes/.credentials/credentials.json', SCOPES)
        creds = flow.run_local_server(port=0)
    # Save the credentials for the next run
    with open('src/includes/.credentials/credentials.json', 'w') as token:
        token.write(creds.to_json())

try:
    service = build('calendar', 'v3', credentials=creds)
    xai_id = '8881f4je38oo4rbj8qs2cr05lo@group.calendar.google.com'
    # Call the Calendar API
    now = datetime.datetime.utcnow().isoformat() + 'Z'  # 'Z' indicates UTC time
    xai_bday = '2019-01-01T11:30:00+02:00'
    events_result = service.events().list(calendarId=xai_id, timeMin=xai_bday,
                                          maxResults=100, singleEvents=True,
                                          orderBy='startTime').execute()
    events = events_result.get('items', [])

    if not events:
        print('No upcoming events found.')
    
    # Prints the start and name of the next 10 events
    seminars = []
    for i, event in enumerate(events):
        seminar = {}
        id = event['id']
        imported_event = service.events().get(calendarId=xai_id, eventId=id).execute()

        if '[SM]' in imported_event['summary']:
            start = imported_event['start'].get('dateTime', imported_event['start'].get('date'))
            seminar['date'] = {}
            seminar['date']['day'] = start.split('T')[0].split('-')[2]
            seminar['date']['month'] = start.split('T')[0].split('-')[1]
            seminar['date']['year'] = start.split('T')[0].split('-')[0]
            seminar['date']['hour'] = start.split('T')[1]
            seminar['complete_date'] = start
            seminar['summary'] = imported_event['summary'].replace('[SM]', '').strip()
            if 'location' in imported_event:
                seminar['location'] = imported_event['location']
            if 'description' in imported_event:
                seminar['description'] = imported_event['description']

            seminars.append(seminar)

            # if i == 7:
            #     break

except HttpError as error:
    print('An error occurred: %s' % error)

def create_cards(seminars):
    seminar_cards = ''
    for i, row in enumerate(seminars):
        abstract = row['summary']
        day = row['date']['day']
        month = month_dict[row['date']['month']]
        year = row['date']['year']
        hour = int(row['date']['hour'].split(':')[0])
        minutes = row['date']['hour'].split(':')[1]
        title = row['summary'].strip('.')
        if 'location' in row:
            location = f'''br
            | #[em  {row['location']}]'''
        else:
            location = ''
    
        # image = row['image file']
        # imageSize = row['image size']
    
        #Create buttons IF:
        #More information
        if 'description' in row:
            descrtiption = row['description']
            # remove the text between the first string '##' and the second '##' from row['description']
            if '##' in descrtiption:
                presenter = f'''br
            br
            | {descrtiption.split('##')[1]}'''
                descrtiption = descrtiption.split('##')[0] + descrtiption.split('##')[2]
            else:
                presenter = ''
                descrtiption = row['description']
            descrtiptionButton = f'''p.my-1
                a.btn-mini.px-2.btn-secondary.small(href='#' data-toggle='collapse' data-target='#collapse-{p.number_to_words(i)}' aria-expanded='true' aria-controls='collapseAbs') Complete description'''
        else:
            descrtiption = 'ABSTRACT NOT FOUND'
            descrtiptionButton = ''
            presenter= ''
    
        ##### string composition for pug file:
        ptOne = f'''#{month + '-' + day}.row.mt-5.justify-content-center
        .col-lg-2.text-right
            h4 {month + ' ' + day + ', ' + year}
            small h. {hour}:{minutes}'''
            
        ptTwo = f'''
        .col-lg-7.bg-yellow.p-3
            #accordion-{p.number_to_words(i)}.accordion
            | #[strong {title}]
            {presenter}
            {location}
            #collapse-{p.number_to_words(i)}.collapse(aria-labelledby='heading-{p.number_to_words(i)}' data-parent='#accordion-{p.number_to_words(i)}')
                div.bg-yellow
                    hr         
                    .
                        {descrtiption}
        .col-lg-2.pl-3
            {descrtiptionButton}
'''
        
        seminar_card = ptOne + ptTwo 
        seminar_cards += seminar_card
    return seminar_cards

all_seminar_cards = create_cards(seminars[::-1])
### save pug file:
write_html(all_seminar_cards, filename='seminars-cards', path='src/includes/', extension='pug')

home_seminar_cards = create_cards(seminars[::-1][:5])
write_html(home_seminar_cards, filename='seminars-cards-home', path='src/includes/', extension='pug')

