from django.shortcuts import render
from django.http import HttpResponse
import psycopg2


def get_db_connection():
    return psycopg2.connect(
        dbname="djangotraining",
        user="djangouser",
        password="secret",
        host="127.0.0.1",
        port="5432"
    )


def init(request):
    try:
        conn = get_db_connection()
        cur = conn.cursor()

        cur.execute("""
            CREATE TABLE IF NOT EXISTS ex02_movies (
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


def populate(request):
    movies_list = [
        {"ep": 1, "tit": "The Phantom Menace", "dir": "George Lucas", "prod": "Rick McCallum", "date": "1999-05-19"},
        {"ep": 2, "tit": "Attack of the Clones ", "dir": "George Lucas", "prod": "Rick McCallum", "date": "2002-05-16"},
        {"ep": 3, "tit": "Revenge of the Sith", "dir": "George Lucas", "prod": "Rick McCallum", "date": "2005-05-19"},
        {"ep": 4, "tit": "A New Hope", "dir": "George Lucas", "prod": "Gary Kurtz, Rick McCallum", "date": "1977-05-25"},
        {"ep": 5, "tit": "The Empire Strikes Back", "dir": "Irvin Kershner", "prod": "Gary Kurtz, Rick McCallum", "date": "1980-05-17"},
        {"ep": 6, "tit": "Return of the Jedi", "dir": "Richard Marquand", "prod": "Howard G. Kazanjian, George Lucas, Rick McCallum", "date": "1983-05-25"},
        {"ep": 7, "tit": "The Force Awakens", "dir": "J. J. Abrams", "prod": "Kathleen Kennedy, J. J. Abrams, Bryan Burk", "date": "2015-12-11"},
    ]

    try:
        conn = get_db_connection()
        cur = conn.cursor()
        responses = []

        for movie in movies_list:
            try:
                cur.execute("""
                    INSERT INTO ex02_movies (episode_nb, title, director, producer, release_date)
                    VALUES (%s, %s, %s, %s, %s);
                """, (movie['ep'], movie['tit'], movie['dir'], movie['prod'], movie['date']))

                conn.commit()
                responses.append("OK")

            except Exception as e:
                conn.rollback()
                responses.append(f"Error: {e}")

        cur.close()
        conn.close()

        return HttpResponse("<br>".join(responses))

    except Exception as e:
        return HttpResponse(f"Error connecting to database: {e}")


def display(request):
    try:
        conn = get_db_connection()
        cur = conn.cursor()

        cur.execute("SELECT * FROM ex02_movies;")
        movies_data = cur.fetchall()

        cur.close()
        conn.close()

        if len(movies_data) == 0:
            return HttpResponse("No data available")

        return render(request, 'ex02/display.html', {'movies': movies_data})

    except Exception:
        return HttpResponse("No data available")
