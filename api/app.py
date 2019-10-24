import psycopg2
from flask import Flask, request, jsonify
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
        return "Go to /players or /firstname_lastname (ex. /Larry_Bird)"

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

        return jsonify(players)

    @app.route('/<name>', methods=['GET', 'POST'])
    def request(name):
        """
        Endpoint for user to submit a specific player and receive some stats as well as their player comparison
        """

        player = name.replace('_', ' ')

        pg_conn = psycopg2.connect(
            dbname=db_name, user=db_user, password=db_password, host=db_host)
        pg_cur = pg_conn.cursor()

        pg_cur.execute("""
        SELECT img, player, position, height, weight, college, draft_yr, pick, drafted_by, min_pg, pts_pg, trb_pg, ast_pg, player_comp, predictions
        FROM player_stats
        WHERE player = %s;
        """, (player,))

        submission = pg_cur.fetchall()[0]
        comparison_player = submission[-2]

        metrics = ['img', 'player', 'position', 'height', 'weight', 'college', 'draft_yr',
                   'pick', 'drafted_by', 'min_pg', 'pts_pg', 'trb_pg', 'ast_pg', 'player_comp', 'pred_yrs']
        submission_dict = dict(zip(metrics, submission))

        pg_cur.execute(""" 
        SELECT img, player, position, height, weight, college, draft_yr, pick, drafted_by, min_pg, pts_pg, trb_pg, ast_pg
        FROM player_stats
        WHERE player = %s;
        """, (comparison_player,))

        comp_metrics = ['img', 'player', 'position', 'height', 'weight', 'college',
                        'draft_yr', 'pick', 'drafted_by', 'min_pg', 'pts_pg', 'trb_pg', 'ast_pg']
        comparison = pg_cur.fetchall()[0]
        comparison_dict = dict(zip(comp_metrics, comparison))

        pg_cur.close()
        pg_conn.close()

        return jsonify(submission_dict, comparison_dict)

    return app
