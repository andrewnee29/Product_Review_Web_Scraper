import requests
from bs4 import BeautifulSoup
import pandas as pd

custom_headers = { #attempts to get to second page of reviews
    "Accept-language": "en-GB,en;q=0.9",
    "Cache-Control": "max-age=0",
    "Connection": "keep-alive",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7", 
    "Accept-Encoding": "gzip, deflate, br, zstd", 
    "Priority": "u=0, i", 
    "Sec-Ch-Ua": "\"Not/A)Brand\";v=\"8\", \"Chromium\";v=\"126\", \"Brave\";v=\"126\"", 
    "Sec-Ch-Ua-Mobile": "?0", 
    "Sec-Ch-Ua-Platform": "\"Windows\"", 
    "Sec-Fetch-Dest": "document", 
    "Sec-Fetch-Mode": "navigate", 
    "Sec-Fetch-Site": "cross-site", 
    "Sec-Fetch-User": "?1", 
    "Sec-Gpc": "1", 
    "Referer": "https://www.google.com/",
    "Upgrade-Insecure-Requests": "1",
    "X-Amzn-Trace-Id": "Root=1-66873cfb-1c52835e3a210000551a0459",
    "User-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.1 Safari/605.1.15",
}
def get_soup(url):
    response = requests.get(url, headers=custom_headers)

    if response.status_code != 200:
        print("Error in getting webpage")
        exit(-1)

    soup = BeautifulSoup(response.text, "html.parser")
    return soup

def get_reviews(soup):
    review_elements = soup.select("div.review")

    scraped_reviews = []

    for review in review_elements:
        r_author_element = review.select_one("span.a-profile-name")
        r_author = r_author_element.text if r_author_element else None

        r_rating_element = review.select_one("i.review-rating")
        r_rating = r_rating_element.text.replace("out of 5 stars", "") if r_rating_element else None

        r_title_element = review.select_one("a.review-title")
        r_title_span_element = r_title_element.select_one("span:not([class])") if r_title_element else None
        r_title = r_title_span_element.text if r_title_span_element else None

        r_content_element = review.select_one("span.review-text-content")
        r_content = r_content_element.text if r_content_element else None

        r_date_element = review.select_one("span.review-date")
        r_date = r_date_element.text if r_date_element else None
        
        r_help_element = review.select_one("span.cr-vote-text")
        r_help = r_help_element.text.replace("people found this helpful", "") if r_help_element else None

        r_verified_element = review.select_one("span.a-size-mini")
        r_verified = r_verified_element.text if r_verified_element else None
        
        r_product_element = review.select_one('h1.a-size-large.a-text-ellipsis')
        r_product = r_product_element.text if r_product_element else None


        r_image_element = review.select_one("img.review-image-tile")
        r_image = r_image_element.attrs["src"] if r_image_element else None

        r = {
            "author": r_author,
            "rating": r_rating,
            "title": r_title,
            "content": r_content, #i don't know why the content isn't printing, it was working before
            "date": r_date,
            "helpful": r_help,
            "verified": r_verified,
            "product": r_product, #issues finding suitable classes that work for product name
            "image_url": r_image
        }

        scraped_reviews.append(r)

    return scraped_reviews

def main():
    search_url = "https://www.amazon.com/A315-24P-R7VH-Display-Quad-Core-Processor-Graphics/product-reviews/B0BS4BP8FB"
    all_data = []
    
    pages = 20
    for page in range(1, pages + 1): #iterating through pages
        url = f"{search_url}/ref=cm_cr_arp_d_paging_btm_next_2?ie=UTF8&reviewerType=all_reviews&pageNumber={page}"
        soup = get_soup(url)
        data = get_reviews(soup)
        all_data.append(data)
        df = pd.DataFrame([r for d in all_data for r in d])

    df.to_csv("amz.csv")

if __name__ == '__main__':
    main()