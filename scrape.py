from bs4 import BeautifulSoup
from requests import get
from requests.exceptions import RequestException
from contextlib import closing
import random
import pandas as pd


class User:
    """Dimension table"""
    def __init__(self, user_id, gender, state):
        self.user_id = user_id
        self.gender = gender
        self.state = state


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


def get_user_info(parsed_html, user_id):
    """Takes in html from beautiful soup, finds the gender and state, and returns a user object"""
    s = str(parsed_html)
    st = s.strip()
    if "Error" in st:
        print("Non-existent player")
        return -1, -1
    state_index = st.index("State")
    gender_index = st.index("Gender")
    s = st[state_index + 21: state_index + 23]
    g = st[gender_index + 22: gender_index + 23]
    return User(user_id, g, s)


def get_event_ratings(parsed_html):
    """Takes in the html from beautiful soup and gets the tournament event id, dates, and ratings"""
    table = parsed_html.find('table', {'valign': 'top', 'width': '960', 'cellspacing': '0', 'cellpadding': '4', 'border': '1'})
    dates = table.find_all("td", {'width': '120'})
    tournaments = table.find_all("td", {'width': '350'})
    ratings = table.find_all("td", {'width': '160'})
    return dates, tournaments, ratings


if __name__ == "__main__":
    user_df = pd.DataFrame()
    user_events_df = pd.DataFrame()
    '''TODO: Store the data in a database, try google colab'''
    for i in range(1, 2):
        uid = str(1243502) + str(i)
        page = "http://www.uschess.org/msa/MbrDtlMain.php?" + uid
        rating_page = "http://www.uschess.org/msa/MbrDtlTnmtHst.php?12641216"
        # Pages then go http://www.uschess.org/msa/MbrDtlTnmtHst.php?12641216.2
        # http://www.uschess.org/msa/MbrDtlTnmtHst.php?12641216.3
        # http://www.uschess.org/msa/MbrDtlTnmtHst.php?12641216.11
        # and so forth
        # Event data, event name, reg rtg before / after
        # What do tournament results look like
        raw_html = simple_get(page)
        html = BeautifulSoup(raw_html, 'html.parser')
        user = get_user_info(html, uid)
        """TODO: create event class, and use the correct page for getting"""
        #d, t, r = get_event_ratings(html)
