import scrape_insert
import read_sql


def test_users():
    users, events = read_sql.main()
    assert users == [(12436954, 'M', 'MD')]


def test_events():
    users, events = read_sql.main()
    assert events[0] == (201511206032, 12436954, '2015-11-20', 'DCCL WINTER CHESS LEAGUE 2', '1889', '1899', None, None, None, None, '2: AMATEUR', 'VA')