import psycopg2
import logging
from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
from decouple import config


def create_app():
    """
    Main function to create application
    """
    app = Flask(__name__)
    CORS(app)

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
        header('Content-type: application/json')
        
        pg_conn = psycopg2.connect(
            dbname=db_name, user=db_user, password=db_password, host=db_host)
        pg_cur = pg_conn.cursor()

        pg_cur.execute("""
        SELECT player
        FROM player_stats;
        """)

        players = pg_cur.fetchall()
        players = [list(player) for player in players]

        pg_cur.close()
        pg_conn.close()

        return render_template("players.html", players=players)

    @app.route("/submit", methods=['POST'])
    def submit():
        """
        Endpoint for user to submit a specific player and receive some stats as well as their player comparison
        """
        metrics = ['img, player, position, height, weight, college, draft_yr, pick, drafted_by, min_pg, pts_pg, trb_pg, ast_pg, player_comp, pred_yrs']

        pg_conn = psycopg2.connect(
            dbname=db_name, user=db_user, password=db_password, host=db_host)
        pg_cur = pg_conn.cursor()

        player = request.values['player_name']
        
        pg_cur.execute("""
        SELECT img, player, position, height, weight, college, draft_yr, pick, drafted_by, min_pg, pts_pg, trb_pg, ast_pg, player_comp, predictions
        FROM player_stats
        WHERE player = %s;
        """, (player,))

        submission = pg_cur.fetchall()
        submission = [list(elem) for elem in submission]

        #submission_dict = dict(zip(metrics, submission))

        comparison_player = submission[0][-2]

        pg_cur.execute(""" 
        SELECT img, player, position, height, weight, college, draft_yr, pick, drafted_by, min_pg, pts_pg, trb_pg, ast_pg
        FROM player_stats
        WHERE player = %s;
        """, (comparison_player,))

        comparison = pg_cur.fetchall()
        comparison = [list(elem) for elem in comparison]

        pg_cur.close()
        pg_conn.close()

        return render_template("submit.html", submission=submission, comparison=comparison)

    return app