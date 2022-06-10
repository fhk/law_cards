"""
We want to study law and need to know what various words mean
in that context. Lets pick a random subset of terms from 
https://www.law.cornell.edu/wex/all

We can then turn these into print outs to put all over the house!

That way perhaps we will absorb them!

Step one: Scrapte the data
Step two: Make flash cards https://github.com/peterhuszar/flash_card_generator
Step three: Put them on the wall
"""
import time

import pandas as pd
import numpy as np
from bs4 import BeautifulSoup
import requests

BASE_URL = "https://www.law.cornell.edu"

possible_first_chars = {
    '1': 1, '3': 4, '4': 2, '7': 1, '9': 1,
    'A': 435, 'B': 195, 'C': 687, 'D': 365, 'E': 259,
    'F': 265, 'G': 123, 'H': 111, 'I': 333, 'J': 99,
    'K': 20, 'L': 214, 'M': 254, 'N': 165, 'O': 116,
    'P': 506, 'Q': 49, 'R': 293, 'S': 468, 'T': 231,
    'U': 120, 'V': 76, 'W': 118, 'Y': 10, 'Z': 7
}

def main():
    how_many = 10
    # we want to make sure we get all the ones with less than
    # or equal to 10 and randomly sample the others.
    fill_more_frequent = how_many - sum(v for v in possible_first_chars.values() if v <= 10)
    
    base_choices = [c for c, v in possible_first_chars.items() if v <= 10]

    resulting_cards = []

    for c in base_choices:
        r = requests.get(BASE_URL + '/wex/all/' + c)
        soup = BeautifulSoup(r.content, "html.parser")
        for section in soup.find_all('span', {"class": "field-content"}):
            for a in section.find_all('a', href=True):
                time.sleep(0.1)
                c_r = requests.get(BASE_URL + a['href'])
                c_soup = BeautifulSoup(c_r.content, "html.parser")
                header = c_soup.find('h1', {'class': 'title'}).text
                meaning = c_soup.find('div', {'class': 'field-item even'}).text
                resulting_cards.append([header, meaning])
   
    pd.DataFrame(resulting_cards).to_excel('text.xlsx', index=False, header=False)
    if fill_more_frequent:
        remaining_choices_possible = sum(v for v in possible_first_chars.values() if v > 10)


if __name__ == '__main__':
    main()