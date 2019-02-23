from bs4 import BeautifulSoup
from requests import get
from requests.exceptions import RequestException
from contextlib import closing
import random


def simple_get(url):
    """
    Attempts to get the content at `url` by making an HTTP GET request.
    If the content-type of response is some kind of HTML/XML, return the
    text content, otherwise return None.
    """
    try:
        with closing(get(url, stream=True)) as resp:
            if is_good_response(resp):
                return resp.content
            else:
                return None

    except RequestException as e:
        log_error('Error during requests to {0} : {1}'.format(url, str(e)))
        return None


def is_good_response(resp):
    """
    Returns True if the response seems to be HTML, False otherwise.
    """
    content_type = resp.headers['Content-Type'].lower()
    return (resp.status_code == 200
            and content_type is not None
            and content_type.find('html') > -1)


def log_error(e):
    """
    It is always a good idea to log errors.
    This function just prints them, but you can
    make it do anything.
    """
    print(e)


if __name__ == "__main__":
    '''TODO: Store the data in a database, try google colab'''
    for i in range(5, 9):
        page = "http://www.uschess.org/msa/MbrDtlMain.php?1243502" + str(i)
        rating_page = "http://www.uschess.org/msa/MbrDtlTnmtHst.php?12641216"
        # Pages then go http://www.uschess.org/msa/MbrDtlTnmtHst.php?12641216.2
        # http://www.uschess.org/msa/MbrDtlTnmtHst.php?12641216.3
        # http://www.uschess.org/msa/MbrDtlTnmtHst.php?12641216.11
        # and so forth
        # Event data, event name, reg rtg before / after
        # What do tournament results look like
        raw_html = simple_get(page)
        html = BeautifulSoup(raw_html, 'html.parser')
        table = html.find('table', {'valign': 'top', 'width': '960', 'cellspacing': '0', 'cellpadding': '4', 'border': '1'})
        dates = table.find_all("td", {'width': '120'})
        tournaments = table.find_all("td", {'width': '350'})
        ratings = table.find_all("td", {'width': '160'})
        s = str(html)
        st = s.strip()
        if "Error" in st:
            print("Non-existent player")
            continue
        state_index = st.index("State")
        gender_index = st.index("Gender")
        state = st[state_index + 21: state_index + 23]
        gender = st[gender_index + 22: gender_index + 23]
        print(state)
        print(gender)
