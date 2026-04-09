from django.http import HttpResponse
import psycopg2


def init(request):
    try:
        conn = psycopg2.connect(
            dbname="djangotraining",
            user="djangouser",
            password="secret",
            host="127.0.0.1",
            port="5432"
        )

        cur = conn.cursor()

        cur.execute("""
            CREATE TABLE IF NOT EXISTS ex00_movies (
                episode_nb INT PRIMARY KEY,
                title VARCHAR(64) UNIQUE NOT NULL,
                opening_crawl TEXT,
                director VARCHAR(32) NOT NULL,
                producer VARCHAR(128) NOT NULL,
                release_date DATE NOT NULL
            ); 
        """)

        conn.commit()
        cur.close()
        conn.close()

        return HttpResponse("OK")

    except Exception as e:
        return HttpResponse(f"Error: {e}")
