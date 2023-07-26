import bs4
from bs4 import BeautifulSoup

with open("./html/ashigaru.html") as fp:
    soup = BeautifulSoup(fp, 'html.parser')

# print(soup)

soup.find_all('a')


def get_unit_information(soup: bs4.element.Tag, info_dict):
    """
    The function assumes you receive a Tag from the html after
    soup.find_all('section', class_="pi-item pi-group pi-border-color") in the main soup
    
    The information we need is:
    ERA, CIV, types
    """

    info_dict

    # 
    # test_f.find_all('div', class_="pi-data-value pi-font").find_all("a") in the main soup
    #  test_f.css.select("data-source")
    # 

