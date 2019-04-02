from bs4 import BeautifulSoup
from requests import get
from requests.exceptions import RequestException
from contextlib import closing
import re
import sqlite3
import os.path
import py_sql
import sys
import numpy as np
import pandas as pd
import time
from tqdm import tqdm


fh = open("logs2.txt", "a")


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
    try:
        content_type = resp.headers['Content-Type'].lower()
    except:
        return False
    return (resp.status_code == 200
            and content_type is not None
            and content_type.find('html') > -1)


def log_error(e):
    """
    It is always a good idea to log errors.
    This function just prints them, but you can
    make it do anything.
    """
    # print(e)
    fh.write(e)
    fh.write("\n")


def get_user_info(parsed_html, user_id, conn, c):
    """Takes in html from beautiful soup, finds the gender and state"""
    s = str(parsed_html)
    st = s.strip()
    if "Error" in st:
        # print("Non-existent player")
        fh.write("Non-existent player")
        fh.write("\n")
        return -3
    state_index = s.rfind("State")
    gender_index = st.index("Gender")
    try:
        s = st[state_index + 21: state_index + 23]
        g = st[gender_index + 22: gender_index + 23]
        values = (int(user_id), g, s)
        # print(values)
        fh.write(str(values))
        fh.write("\n")
    except:
        # print("Couldn't find gender or state")
        fh.write("Couldn't find gender or state")
        fh.write("\n")
        return -2
    try:
        c.execute("INSERT INTO users VALUES (?, ?, ?)", values)
        conn.commit()
        # print("Inserted user into database table")
        fh.write("Inserted user into database table")
        fh.write("\n")
    except:
        # print("Couldn't insert users into table")
        fh.write("Couldn't insert users into table")
        fh.write("\n")
        return -1
    return 0


def rating_helper(rating_string):
    """Gets the before and after rating for one instance with simple processing"""
    rating_split = rating_string.split("=>")
    first, second = rating_split[0].strip(), rating_split[1].strip()
    return first, second


def get_event_ratings(parsed_html, user_id, conn, c):
    """Takes in the html from beautiful soup and gets the tournament event id, dates, and ratings"""
    event_insert_error = False
    if "Error" in str(parsed_html):
        return -1
    table = parsed_html.find('table', {'valign': 'top', 'width': '960', 'cellspacing': '0', 'cellpadding': '4', 'border': '1'})
    if table:
        dates = table.find_all("td", {'width': '120'})
        tournaments = table.find_all("td", {'width': '350'})
        ratings = table.find_all("td", {'width': '160'})
        rating_i = 0
        for d, t in zip(dates, tournaments):
            try:
                d_s = d.getText()
                parsed_date = d_s[:10]
                parsed_event_id = d_s[10:]
                t_text = t.getText()
                # Matches anything that starts with ( and ends with ), .* says there can be zero or more of any characters
                match = re.search("\(.*\)", t_text)
                start, end = match.span()
                section = t_text[end:]
                state = t_text[start + 1:end - 1]
                tournament_name = t_text[:start - 1]
                reg_ratings = ratings[rating_i].getText()
                quick_ratings = ratings[rating_i + 1].getText()
                blitz_ratings = ratings[rating_i + 2].getText()
                rating_i += 3
                reg_rating_before, reg_rating_after, quick_rating_before, quick_rating_after, blitz_rating_before, \
                    blitz_rating_after = None, None, None, None, None, None
                if "=>" in reg_ratings:
                    reg_rating_before, reg_rating_after = rating_helper(reg_ratings)
                if "=>" in quick_ratings:
                    quick_rating_before, quick_rating_after = rating_helper(quick_ratings)
                if "=>" in blitz_ratings:
                    blitz_rating_before, blitz_rating_after = rating_helper(blitz_ratings)
                int_type = lambda a: int(a) if a else a
                values = (int_type(parsed_event_id.strip()), int_type(user_id), parsed_date, tournament_name, reg_rating_before, reg_rating_after,
                                quick_rating_after, quick_rating_after, blitz_rating_before, blitz_rating_after, section,
                                state)
            except:
                # print("Failed getting info for a tournament")
                fh.write("Failed getting info for a tournament")
                fh.write("\n")
                continue
            try:
                c.execute('INSERT INTO user_events VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)', values)
                conn.commit()
            except:
                event_insert_error = True
                # print("Couldn't insert events into table")
                fh.write("Couldn't insert events into table")
                fh.write("\n")
                break
        # print("Inserted events into table")
        fh.write("Inserted events into table")
        fh.write("\n")
        if not event_insert_error:
            return 0
        else:
            return -3
    else:
        # print("No events")
        fh.write("No events")
        fh.write("\n")
        return -2


def main():
    # Re create the database
    py_sql.main()

    base_dir = os.path.dirname(os.path.abspath(__file__))
    db_name = 'testDB2.db'
    db_path = os.path.join(base_dir, db_name)
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    lowest_id = 12435021
    highest_id = 12939951
    num_sample = highest_id - lowest_id
    #num_sample = 10
    # bayesian better than random better than grid search
    id_space = list(range(lowest_id, highest_id + 1))
    # uids_chosen = []
    # uids_users = []
    # uids_events = []
    uids = np.random.choice(id_space, size=num_sample, replace=False)
    # uids_chosen.append(uids)
    uid_count = 0
    start = time.time()
    for uid in tqdm(uids):
        if uid_count > num_sample:
            break
        uid = str(uid)
        # uid = "12735671"
        # uid = str(1243502) + str(i)
        # uid = str(12436954)
        # uid = "12641216"
        page = "http://www.uschess.org/msa/MbrDtlMain.php?" + uid
        # print("\n", "page: ", page)
        fh.write("page: " + page)
        fh.write("\n")
        # rating_page = "http://www.uschess.org/msa/MbrDtlTnmtHst.php?" + uid
        raw_html = simple_get(page)
        try:
            html = BeautifulSoup(raw_html, 'html.parser')
        except:
            fh.write("Broken link")
            fh.write("\n")
            continue
        # print("Getting user")
        fh.write("Getting user")
        fh.write("\n")
        user_r = get_user_info(html, uid, conn, c)
        # uids_users.append(user_r)
        count = 1
        event_return = 0
        # print("Getting events")
        fh.write("Getting events")
        fh.write("\n")
        # uid_event_list = []
        while event_return == 0:
            # if count > 5:
            #     break
            rating_page = "http://www.uschess.org/msa/MbrDtlTnmtHst.php?" + uid + "." + str(count)
            # rating_page = "http://www.uschess.org/msa/MbrDtlTnmtHst.php?12641216" + "." + str(count)
            raw_html = simple_get(rating_page)
            try:
                html = BeautifulSoup(raw_html, 'html.parser')
            except:
                fh.write("Broken event")
                fh.write("\n")
                event_return = -1
                break
            event_return = get_event_ratings(html, uid, conn, c)
            if event_return == 0:
                count += 1
            else:
                break
            # uid_event_list.append(event_return)
        uid_count += 1
        # uids_events.append(uid_event_list)
    conn.close()
    end = time.time()
    # print("Took this many seconds: ", end - start)
    fh.write("Took this many seconds: " + str(round(end - start)))
    fh.write("\n")
    # results_df = pd.DataFrame()
    # results_df['uids'] = uids_chosen
    # results_df['uid_users'] = uids_users
    # results_df['events'] = uids_events
    # results_df.to_csv("results/scraping_results.csv")
    fh.write("Finished!")
    fh.close()


if __name__ == "__main__":
    main()
