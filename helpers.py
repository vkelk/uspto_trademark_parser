import requests
from urllib.parse import urlsplit


def download_html(url):
    print('Downloading %s' % url)
    html_content = None
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) "
                      "Chrome/56.0.2924.87 Safari/537.36",
        "Accept": "text/html,application/xhtml+xml,application/xml;q = 0.9, image / webp, * / *;q = 0.8"}
    try:
        r = requests.get(url, headers=headers, allow_redirects=True)
        if r.status_code != 200:
            print('[%s] Downloading %s' % r.status_code, url)
            print(r.headers)
            print(r.cookies)
        else:
            html_content = r.content
    except requests.exceptions.RequestException as err:
        print('Failed to open url %s' % url)
        html_content = None
    finally:
        if type(html_content) is bytes:
            return html_content.decode()
        else:
            return html_content


def get_host_from_url(url):
    base_url = "{0.scheme}://{0.netloc}/".format(urlsplit(url))
    return base_url

