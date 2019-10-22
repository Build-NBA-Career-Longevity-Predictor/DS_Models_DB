import psycopg2
from flask import Flask, render_template


def create_app():
    """
    Main function to create application
    """
    app = Flask(__name__)
    app.config["FLASK_ENV"] = "development"

    db_host = 'ec2-54-235-180-123.compute-1.amazonaws.com'
    db_name = 'd9j38jtaim5u92'
    db_user = 'ticqhtmsxabnow'
    db_password = 'a3be20dbc652d427ca174fc64781b6bd33cd6bce42e3158ac3b2a9e642f0f383'

    @app.route("/")
    def home_page():
        pg_conn = psycopg2.connect(dbname=db_name, user=db_user, password=db_password, host=db_host)
        pg_cur = pg_conn.cursor()
        
        pg_cur.execute("""
        SELECT *
        FROM player_stats
        LIMIT 1;
        """)

        data = pg_cur.fetchall()

        pg_cur.close()
        pg_conn.close()

        return render_template("index.html", data=data)
    
    @app.route("/players")
    def players():
        """
        Endpoint to get all players in database
        """
        pg_conn = psycopg2.connect(dbname=db_name, user=db_user, password=db_password, host=db_host)
        pg_cur = pg_conn.cursor()

        pg_cur.execute("""
        SELECT player
        FROM player_stats;
        """)

        players = pg_cur.fetchall()

        pg_cur.close()
        pg_conn.close()

        return render_template("players.html", players=players)
    return app