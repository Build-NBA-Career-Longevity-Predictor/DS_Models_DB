import psycopg2
from flask import Flask, render_template, request
from decouple import config


def create_app():
    """
    Main function to create application
    """
    app = Flask(__name__)

    db_host = config('DB_HOST')
    db_name = config('DB_NAME')
    db_user = config('DB_USER')
    db_password = config('DB_PASSWORD')

    @app.route("/")
    def home_page():
        """
        Application home page
        """
        return render_template("index.html")

    @app.route("/players")
    def players():
        """
        Endpoint to get all players in database
        """
        pg_conn = psycopg2.connect(
            dbname=db_name, user=db_user, password=db_password, host=db_host)
        pg_cur = pg_conn.cursor()

        pg_cur.execute("""
        SELECT player
        FROM player_stats;
        """)

        players = pg_cur.fetchall()

        pg_cur.close()
        pg_conn.close()

        return render_template("players.html", players=players)

    @app.route("/submit", methods=['POST'])
    def submit():
        """
        Endpoint for user to submit a specific player and receive some stats as well as their player comparison
        """
        pg_conn = psycopg2.connect(
            dbname=db_name, user=db_user, password=db_password, host=db_host)
        pg_cur = pg_conn.cursor()

        player = request.values['player_name']

        pg_cur.execute("""
        SELECT player, position, height, weight, college, draft_yr, pick, fg_pct, fg3_pct, ft_pct, orb_pg, drb_pg, steals_pg, player_comp
        FROM player_stats
        WHERE player = %s;
        """, (player,))

        submission = pg_cur.fetchall()

        pg_cur.close()
        pg_conn.close()

        return render_template("submit.html", submission=submission)

    return app
