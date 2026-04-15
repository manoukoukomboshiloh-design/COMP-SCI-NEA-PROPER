
import logging

logging.basicConfig(
    filename='dashboard_debug.log',
    level=logging.DEBUG,
    format='%(asctime)s %(levelname)s:%(message)s'
)

def get_topic_averages(user_id):
    """
    Returns a list of (topic, average score) for the given user_id.
    Logs errors and actions for debugging and NEA evidence.
    """
    try:
        con = sqlite3.connect('user_data.db')
        cur = con.cursor()
        cur.execute("""
            SELECT topic, AVG(score)
            FROM progress
            WHERE user_id = ?
            GROUP BY topic
        """, (user_id,))
        results = cur.fetchall()
        logging.info(f'Fetched topic averages for user_id={user_id}')
        return results
    except Exception as e:
        logging.error(f'Error in get_topic_averages: {e}')
        return []
    finally:
        try:
            con.close()
        except:
            pass

def get_total_quizzes(user_id):
    """
    Returns the total number of quizzes taken by the user.
    Logs errors and actions for debugging and NEA evidence.
    """
    try:
        con = sqlite3.connect('user_data.db')
        cur = con.cursor()
        cur.execute("""
            SELECT COUNT(*)
            FROM progress
            WHERE user_id = ?
        """, (user_id,))
        result = cur.fetchone()[0]
        logging.info(f'Fetched total quizzes for user_id={user_id}')
        return result
    except Exception as e:
        logging.error(f'Error in get_total_quizzes: {e}')
        return 0
    finally:
        try:
            con.close()
        except:
            pass

def get_best_score(user_id):
    """
    Returns the best (maximum) score for the user.
    Logs errors and actions for debugging and NEA evidence.
    """
    try:
        con = sqlite3.connect('user_data.db')
        cur = con.cursor()
        cur.execute("""
            SELECT MAX(score)
            FROM progress
            WHERE user_id = ?
        """, (user_id,))
        result = cur.fetchone()[0]
        logging.info(f'Fetched best score for user_id={user_id}')
        return result
    except Exception as e:
        logging.error(f'Error in get_best_score: {e}')
        return 0
    finally:
        try:
            con.close()
        except:
            pass