import requests

url = 'https://ageofempires.fandom.com/wiki/Ashigaru_Musketeer'
r = requests.get(url)
# print(r.text)

with open('./html/ashigaru.html', 'w') as f:
    f.write(r.text)