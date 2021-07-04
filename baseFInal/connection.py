import urllib.parse as up
import psycopg2
def connect():
    up.uses_netloc.append("postgres")
    url = up.urlparse("postgres://qlpjsqya:1mne0cb8GcdxyhjTQoiCt3GYNvzOCk31@batyr.db.elephantsql.com/qlpjsqya")
    conn = psycopg2.connect(database=url.path[1:],
    user=url.username,
    password=url.password,
    host=url.hostname,
    port=url.port
    )
    cur = conn.cursor()
    return cur