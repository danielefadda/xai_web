# XAI Website

- To update publication list run: `defaultPY` command from gulpfile.js
- To update the website without running publication python script run: `default` command from gulpfile.js
- To build the website run `build`

---

- Use the file `header.pug` to update main menu.
- To update events create an object into the file `src\includes\_config.pug` in the `news` list. For example:
```
 news = [
    {
        image: 'assets/images/blog/dubaiExpo.png',
        title: 'Expo Dubai: High-Level Forum on EU Vision for TrustworthyAI',
        link: 'news_dubaiExpo.html', 
        category: 'Forum',
        content: "Event organised by EU Commission to bring European AI Excellence & Trust approaches to the world",
        date: '15-16 March 2022 13:30 – 15:00 CET'
    },
    {...}
]
```
`link: 'news_dubaiExpo.html'` è una pagina html con template news e path `news_*.html`

- To add people to the *people page* `src\includes\_config.pug` in the `people` list. For example:
 
```
 people = [
                {
                    'firstName': 'Fosca',
                    'lastName': 'Giannotti',
                    'role': 'Principal Investigator',
                    'affiliation': 'Scuola Normale',
                    'type':'pl'
                },{
                    'firstName': 'Riccardo',
                    'lastName': 'Guidotti',
                    'role': 'Assitant Professor',
                    'affiliation': 'University of Pisa',
                    'type': 'core',
                    'researchLine': '1 ▪ 3 ▪ 4 ▪ 5',
                    'researchLeader':'1'
                }, {
                    'firstName': 'Mattia',
                    'lastName': 'Setzu',
                    'role': 'Phd Student',
                    'affiliation': 'University of Pisa',
                    'type': 'team',
                    'researchLine': '1 ▪ 2'
                },
    {...}
]
```
