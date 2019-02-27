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


class UserEvents:
    """Dimensions table"""
    def __init__(self, event_id, user_id, date, event_name, reg_before, reg_after, quick_before, quick_after,
                 blitz_before, blitz_after):
        self.event_id = event_id
        self.user_id = user_id
        self.date = date
        self.event_name = event_name
        self.reg_before = reg_before
        self.reg_after = reg_after
        self.quick_before = quick_before
        self.quick_after = quick_after
        self.blitz_before = blitz_before
        self.blitz_after = blitz_after


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


def get_user_info(parsed_html, user_id, users_list):
    """Takes in html from beautiful soup, finds the gender and state, and returns a user object"""
    s = str(parsed_html)
    st = s.strip()
    if "Error" in st:
        print("Non-existent player")
        return -1
    state_index = st.index("State")
    gender_index = st.index("Gender")
    s = st[state_index + 21: state_index + 23]
    g = st[gender_index + 22: gender_index + 23]
    users_list.append(User(user_id, g, s))
    return 0


def get_event_ratings(parsed_html, user_events_list):
    """Takes in the html from beautiful soup and gets the tournament event id, dates, and ratings"""
    table = parsed_html.find('table', {'valign': 'top', 'width': '960', 'cellspacing': '0', 'cellpadding': '4', 'border': '1'})
    if table:
        dates = table.find_all("td", {'width': '120'})
        tournaments = table.find_all("td", {'width': '350'})
        ratings = table.find_all("td", {'width': '160'})
        for d, t in zip(dates, tournaments):
            d_s = str(d)
            parsed_date = d_s[16:26]
            parsed_eventID = d_s[38:-14]
            t_text = t.getText()
    else:
        return -1


if __name__ == "__main__":
    user_df = pd.DataFrame()
    user_events_df = pd.DataFrame()
    user_events = []
    users = []
    '''TODO: Store the data in a database, try google colab, just analyze tournament results between players, predict chess player that will
    win a tournament, getText before indexing'''
    for i in range(1, 2):
        uid = str(1243502) + str(i)
        page = "http://www.uschess.org/msa/MbrDtlMain.php?" + uid
        rating_page = "http://www.uschess.org/msa/MbrDtlTnmtHst.php?" + uid
        rating_page = "http://www.uschess.org/msa/MbrDtlTnmtHst.php?12641216"
        # Pages then go http://www.uschess.org/msa/MbrDtlTnmtHst.php?12641216.2
        # http://www.uschess.org/msa/MbrDtlTnmtHst.php?12641216.3
        # http://www.uschess.org/msa/MbrDtlTnmtHst.php?12641216.11
        # and so forth
        raw_html = simple_get(page)
        html = BeautifulSoup(raw_html, 'html.parser')
        get_user_info(html, uid, users)
        """TODO: create event class, and use the correct page for getting"""
        raw_html = simple_get(rating_page)
        html = BeautifulSoup(raw_html, 'html.parser')
        get_event_ratings(html, user_events)
