import requests 
from bs4 import BeautifulSoup

# The link could come via copy pasted from the URL bar
page_link = 'https://www.reddit.com/r/ProgrammerHumor/comments/rn05li/userfist_name/'

# Or from the "share" button (probably this is more common)
share_link = 'https://www.reddit.com/r/ProgrammerHumor/comments/rn05li/userfist_name/?utm_source=share&utm_medium=web2x&context=3'

page = requests.get(share_link)

soup = BeautifulSoup(page.content, 'html.parser')

image_tag_selector = '#t3_rn05li > div._1poyrkZ7g36PawDueRza-J._11R7M_VOgKO1RJyRSRErT3 > div.STit0dLageRsa2yR4te_b > div > div._3JgI-GOrkmyIeDeyzXdyUD._2CSlKHjH7lsjx0IpjORx14 > div > a > div > div > img'
image_tag = soup.select(image_tag_selector)

img_source = soup.select("a[href^=http]")
[i['href'] for i in img_source]


#share_link = 'https://i.redd.it/3yumipqkqb781.jpg'
#image_data = requests.get(share_link).content
#
#with open ('a.jpg', 'wb') as image_file:
#    image_file.write(image_data)
#
#
#def download_image(link):
#    pass