from django.shortcuts import render
import os
from django.conf import settings
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
            CREATE TABLE IF NOT EXISTS ex08_planets (
                id SERIAL PRIMARY KEY,
                name VARCHAR(64) UNIQUE NOT NULL,
                climate VARCHAR,
                diameter INTEGER,
                orbital_period INTEGER,
                population BIGINT,
                rotation_period INTEGER,
                surface_water REAL,
                terrain VARCHAR(128)
            );
        """)

        cur.execute("""
            CREATE TABLE IF NOT EXISTS ex08_people (
                id SERIAL PRIMARY KEY,
                name VARCHAR(64) UNIQUE NOT NULL,
                birth_year VARCHAR(32),
                gender VARCHAR(32),
                eye_color VARCHAR(32),
                hair_color VARCHAR(32),
                height INTEGER,
                mass REAL,
                homeworld VARCHAR(64) REFERENCES ex08_planets(name)
            );
        """)

        conn.commit()
        cur.close()
        conn.close()
        return HttpResponse("OK")
    except Exception as e:
        return HttpResponse(f"Error: {e}")


def populate(request):
    planets_file = os.path.join(settings.BASE_DIR, 'd05', 'planets.csv')
    people_file = os.path.join(settings.BASE_DIR, 'd05', 'people.csv')

    try:
        conn = get_db_connection()
        cur = conn.cursor()
        responses = []

        try:
            with open(planets_file, 'r') as f:
                planets_columns = ('name', 'climate', 'diameter', 'orbital_period', 'population', 'rotation_period', 'surface_water', 'terrain')
                cur.copy_from(f, 'ex08_planets', sep='\t', null='NULL', columns=planets_columns)
                conn.commit()
                responses.append("OK")

        except Exception as e:
            conn.rollback()
            responses.append(f"Planets error: {e}")

        try:
            with open(people_file, 'r') as f:
                people_columns = ('name', 'birth_year', 'gender', 'eye_color', 'hair_color', 'height', 'mass', 'homeworld')
                cur.copy_from(f, 'ex08_people', sep='\t', null='NULL', columns=people_columns)
                conn.commit()
                responses.append("OK")

        except Exception as e:
            conn.rollback()
            responses.append(f"People error: {e}")

        cur.close()
        conn.close()
        return HttpResponse("<br>".join(responses))

    except Exception as e:
        return HttpResponse(f"Connection error: {e}")


def display(request):
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        sql_query = """
            SELECT ex08_people.name, ex08_planets.name, ex08_planets.climate
            FROM ex08_people
            JOIN ex08_planets ON ex08_people.homeworld = ex08_planets.name
            WHERE ex08_planets.climate ILIKE '%windy%'
            ORDER BY ex08_people.name ASC;
        """

        cur.execute(sql_query)
        data = cur.fetchall()

        cur.close()
        conn.close()

        if len(data) == 0:
            return HttpResponse("No data available")

        return render(request, 'ex08/display.html', {'data': data})

    except Exception:
        return HttpResponse("No data available")
