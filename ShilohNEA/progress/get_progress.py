import sqlite3
import logging

logging.basicConfig(
    filename='get_progress_debug.log',
    level=logging.DEBUG,
    format='%(asctime)s %(levelname)s:%(message)s'
)

def get_user_progress(username):
    """
    Returns a list of (username, topic, score) for the given username.
    Logs errors and actions for debugging and NEA evidence.
    """
    try:
        con = sqlite3.connect('user_data.db')
        cur = con.cursor()
        cur.execute("""
            SELECT userdata.username, progress.topic, progress.score
            FROM userdata
            JOIN progress ON userdata.id = progress.user_id
            WHERE userdata.username = ?
        """, (username,))
        result = cur.fetchall()
        logging.info(f'Fetched progress for username={username}')
        return result
    except Exception as e:
        logging.error(f'Error in get_user_progress: {e}')
        return []
    finally:
        try:
            con.close()
        except:
            pass



