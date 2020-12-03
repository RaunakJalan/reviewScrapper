from bs4 import BeautifulSoup as bs
import requests
from urllib.request import urlopen as uReq

class reviewScrapper:
    def __init__(self, product):
        self.product = product
        self.baseUrl = 'https://www.flipkart.com'
        self.url = self.baseUrl + "/search?q=" + self.product

        uClient = uReq(self.url)
        self.flipkartPage = uClient.read()
        uClient.close()

    def reviewScrap(self):

        # req_data = requests.get(self.url)
        flipkartHtml = bs(self.flipkartPage, 'html.parser')
        
        checkError = flipkartHtml.findAll("div", {"class": "_3uTeW4"})
        if len(checkError) > 0 and checkError[0].text == "Sorry, no results found!":
            return [{'Product': self.product, 'Name': '-', 'Rating': '-', 'CommentHead': '-', 'Comment': 'No review found!'}]

        bigboxes = flipkartHtml.findAll("div", {"class": "_2pi5LC col-12-12"})
        del bigboxes[0:3]
        box = bigboxes[0]

        self.url = self.baseUrl + box.div.div.div.a['href']
        prodRes = requests.get(self.url)
        prodRes = bs(prodRes.content, 'html.parser')
        # print(review_soup)

        # rating_list = []
        # review_header_list = []
        # detailed_review_list = []
        # user_list = []
        # likes_dislikes_list = []

        pages_total = prodRes.find('div', {'class': '_3UAT2v _16PBlm'})

        review_link = str(pages_total.find_parent().get('href'))
        self.url = self.baseUrl + review_link
        c = 0
        reviews_list = []
        while True:
            c = c + 1
            # print(self.url)
            # print('*'*100)
            req_data = requests.get(self.url)
            review_soup = bs(req_data.content, 'html.parser')

            all_reviews = review_soup.find_all('div', {'class': 'col _2wzgFH K0kLPL'})
            # print(all_reviews)
            for review in all_reviews:
                rating = review.find('div', {'class': '_3LWZlK _1BLPMq'})
                if rating is None:
                    rating = review.find('div', {'class': '_3LWZlK _1rdVr6 _1BLPMq'})
                if rating is None:
                    rating = review.find('div', {'class': '_3LWZlK _32lA32 _1BLPMq'})
                rating = rating.text
                review_header = review.find('p', {'class': '_2-N8zT'}).text
                detailed_review = review.find('div', {'class': 't-ZTKy'}).text
                user = review.find('p', {'class': '_2sc7ZR _2V5EHH'}).text
                # likes_dislikes = review.find_all('span', {'class': '_3c3Px5'})
                # likes_dislikes = [e.get_text() for e in likes_dislikes]

                # rating_list.append(rating)
                # review_header_list.append(review_header)
                # detailed_review_list.append(detailed_review)
                # user_list.append(user)
                # likes_dislikes_list.append(page_like_dis)

                finalDict = {'Product': self.product, 'Name': user, 'Rating': rating, 'CommentHead': review_header, 'Comment': detailed_review}
                reviews_list.append(finalDict)

            review_links = review_soup.find_all('a', {'class': '_1LKTO3'})
            if len(review_links) == 1:
                if review_links[0].get_text() == "Previous":
                    break
                else:
                    url = self.baseUrl + str(review_links[0].get('href'))
            elif len(review_links) > 1:
                url = self.baseUrl + str(review_links[1].get('href'))
            else:
                break
            if c == 10:
                break

        return reviews_list

        # print(rating_list)
        # print('*'*50)
        # print(review_header_list)
        # print('*'*50)
        # print(detailed_review_list)
        # print('*'*50)
        # print(user_list)
        # print('*'*50)
        # print(likes_dislikes_list)
        # print('*'*50)


# prod = reviewScrapper("iphone")
# print(prod.reviewScrap())
