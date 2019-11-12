import requests
import re
import json
from bs4 import BeautifulSoup

class CommentScraper:

    def __init__(self):
        # insert here the url of the commentary by espn site
        self.list_of_url = [
            "https://www.espn.com/soccer/commentary?gameId=541728",
            "https://www.espn.com/soccer/commentary?gameId=541726",
            "https://www.espn.com/soccer/commentary?gameId=541731",
            "https://www.espn.com/soccer/commentary?gameId=541748",
            "https://www.espn.com/soccer/commentary?gameId=541738",
            "https://www.espn.com/soccer/commentary?gameId=541736",
            "https://www.espn.com/soccer/commentary?gameId=541741"
        ]
        for url in self.list_of_url:
            response = requests.get(url)
            if response.status_code != 200:
                raise Exception('The site is not reachable')

    def extract_comments(self):
        comments_dict = {}
        comments_dict["witnesses"] = []
        id = 0
        for url in self.list_of_url:
            print("...Processing:", url)
            website = requests.get(url)
            soup = BeautifulSoup(website.text, "html.parser")
            container = soup.find('div', {"id": "match-commentary-1-tab-1"})
            for td in container.find_all('td', {"class":"game-details"}):
                comment_cleaned = self.clean_comment(td)
                comments_dict["witnesses"].append({'id': id, 'content':comment_cleaned})
                id+=1

        with open("comments.json", "w+") as out_file:
            json.dump(comments_dict, out_file, indent=4)

    def clean_comment(self, comment):
        comment_cleaned = re.sub("\t", "", re.sub("\n", "", comment.text))[4:-8]




        return  comment_cleaned



if __name__ == '__main__':
    scraper = CommentScraper()
    scraper.extract_comments()