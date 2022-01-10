import habanero
from habanero import Crossref
from pprint import pprint
from collections import Counter # for easy counting
import ast # for string to dictionary conversion
import pandas as pd # for data manipulation
import numpy as np # for array manipulation

cr = Crossref() # create a crossref object

# query for the term "permafrost"
permafrost = cr.works(query = "xai")
doi = '10.3390/e23081064'

paper=cr.works(ids = doi)
pprint(paper)



