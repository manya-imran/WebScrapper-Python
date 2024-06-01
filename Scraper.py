import os
from requests_html import HTMLSession
from requests.exceptions import RequestException

# clear console cls for windows and clear for linux
def clear_console():
    os.system('cls' if os.name == 'nt' else 'clear')

# get query to scrape for
def get_user_input():
    query = input('Enter Your Query: ')
    limit = int(input('Enter No. Of URLs To Scrape: '))
    return query, limit

# scrape google search results
def scrape_google_search(query, limit):
    # start a http session
    session = HTMLSession()

    # headers for a web request
    headers = {
        'authority': 'www.google.com',
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8',
        'accept-language': 'en-US,en;q=0.5',
        'sec-fetch-dest': 'document',
        'sec-fetch-mode': 'navigate',
        'sec-fetch-site': 'none',
        'sec-fetch-user': '?1',
        'sec-gpc': '1',
        'upgrade-insecure-requests': '1',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36',
    }

    params = {
        'q': query,
        'num': limit,
    }

    # try-except block to handle exceptions
    try:
        # send a get request to google search
        response = session.get('https://www.google.com/search', headers=headers, params=params)
        # check if the response is successful if not 404 or other exceptions
        response.raise_for_status()

        if 'did not match any documents' in response.text:
            print('No Results Found')
            return []
        elif 'Our systems have detected unusual traffic from your computer' in response.text:
            print('Captcha Triggered! Use VPN or Try After Sometime.')
            return []

        # find all anchor tags in the response
        links = response.html.find('a')
        result_urls = []
        for link in links:
            # get the href attribute of the anchor tag
            url = link.attrs.get('href')
            if url and 'http' in url and not 'google' in url:
                result_urls.append(url)
                if len(result_urls) >= limit:
                    break

        return result_urls
    # handle exceptions
    except RequestException as e:
        print(f'An error occurred: {e}')
        return []

# write urls to a file
def write_urls_to_file(urls, filename='Results.txt'):
    with open(filename, 'w') as file:
        for url in urls:
            file.write(url + '\n')

# main function
def main():
    clear_console()
    query, limit = get_user_input()
    urls = scrape_google_search(query, limit)
    if urls:
        write_urls_to_file(urls)
        print(f'Successfully scraped {len(urls)} URLs')
    else:
        print('No URLs were scraped.')

if __name__ == "__main__":
    main()
