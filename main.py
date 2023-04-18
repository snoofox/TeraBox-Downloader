from urllib.parse import urlparse, parse_qs
import requests
import re


def extract_domain_and_surl(url):
    """
    Extracts the domain name and 'surl' value from a given URL.

    Args:
        url (str): The URL to extract domain name and 'surl' value from.

    Returns:
        tuple: A tuple containing the domain name and 'surl' value as (domain_name, surl_value).
    """

    return urlparse(url).netloc, parse_qs(urlparse(url).query).get('surl', [''])[0]


def parseCookieFile(cookiefile):
    """
    Parse cookies from a file in Netscape format.

    Args:
        cookiefile (str): Path to the cookies file.

    Returns:
        dict: A dictionary containing cookies as key-value pairs.
    """

    cookies = {}
    with open(cookiefile, 'r') as fp:
        for line in fp:
            if not line.startswith('#'):
                line_fields = line.strip().split('\t')
                # Make sure the line has at least 7 fields, as per Netscape format
                if len(line_fields) >= 7:
                    # Extract the cookie name and value
                    cookie_name = line_fields[5]
                    cookie_value = line_fields[6]
                    cookies[cookie_name] = cookie_value
    return cookies


def download(url: str) -> str:
    """
    Downloads data from a given URL and returns the result.

    Args:
        url (str): The URL to download data from.

    Returns:
        str: The downloaded data.
    """

    axios = requests.Session()

    # Load cookies from 'cookies.txt'
    cookies = parseCookieFile('cookies.txt')
    axios.cookies.update(cookies)

    response = axios.get(url)
    domain, key = extract_domain_and_surl(response.url)

    headers = {
        'Accept': 'application/json, text/plain, */*',
        'Accept-Language': 'en-US,en;q=0.5',
        'Accept-Encoding': 'gzip, deflate, br',
        'Referer': f'https://{domain}/sharing/link?surl={key}',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.82 Safari/537.36'
    }

    response = axios.get(
        f'https://www.terabox.com/share/list?app_id=250528&shorturl={key}&root=1', headers=headers)

    try:
        result = response.json()['list'][0]['dlink']
    except KeyError:
        print("Failed to get download link")
    else:
        return result


# Example usage
dlink = download('https://teraboxapp.com/s/1ZqumlUbwrc32c40geaQsVg')
print(dlink)
