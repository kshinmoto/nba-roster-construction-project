from flask import Flask, render_template
import sqlite3

import copy_comps_algo

app = Flask(__name__)

@app.route('/')
@app.route('/home')
def home_page():
    return render_template('home.html')

@app.route('/glossary')
def glossary_page():
    return render_template('glossary.html')

# create team web pages
@app.route('/atl')
def atl_page():
    # connect to our database
    conn = sqlite3.connect('concat_4.db')
    conn.row_factory = sqlite3.Row

    # get team roster stats for players of designated team
    cur = conn.cursor()
    cur.execute("select * from concat_1_def_full where Team_x = 'ATL'")
    bos = cur.fetchall()

    # get Four Factors stats for designated team
    cur.execute("select * from df_ff where Team = 'Atlanta'")
    df = cur.fetchall()

    # use function from copy_comps_algo to get suggested players
    upcoming_fa, future_fa, multiyear_fa, list_names, list_th = copy_comps_algo.suggest_players('Atlanta', 'ATL')

    # render web page and assign variables values for our web page
    return render_template("atl.html", BOS = bos, DF = df, weak_names = list_names, th_list = list_th,
                           up_row_data = list(upcoming_fa.values.tolist()),
                           fut_row_data = list(future_fa.values.tolist()),
                           my_row_data = list(multiyear_fa.values.tolist()))

# repeat for rest of team web pages
@app.route('/bos')
def bos_page():
    conn = sqlite3.connect('concat_4.db')
    conn.row_factory = sqlite3.Row

    cur = conn.cursor()
    cur.execute("select * from concat_1_def_full where Team_x = 'BOS'")
    bos = cur.fetchall()

    cur.execute("select * from df_ff where Team = 'Boston'")
    df = cur.fetchall()

    upcoming_fa, future_fa, multiyear_fa, list_names, list_th = copy_comps_algo.suggest_players('Boston', 'BOS')



    return render_template("bos.html", BOS = bos, DF = df, weak_names = list_names, th_list = list_th,
                           up_row_data = list(upcoming_fa.values.tolist()),
                           fut_row_data = list(future_fa.values.tolist()),
                           my_row_data = list(multiyear_fa.values.tolist()))

@app.route('/brk')
def brk_page():
    conn = sqlite3.connect('concat_4.db')
    conn.row_factory = sqlite3.Row

    cur = conn.cursor()
    cur.execute("select * from concat_1_def_full where Team_x = 'BRK'")
    bos = cur.fetchall()

    cur.execute("select * from df_ff where Team = 'Brooklyn'")
    df = cur.fetchall()

    upcoming_fa, future_fa, multiyear_fa, list_names, list_th = copy_comps_algo.suggest_players('Brooklyn', 'BRK')



    return render_template("brk.html", BOS = bos, DF = df, weak_names = list_names, th_list = list_th,
                           up_row_data = list(upcoming_fa.values.tolist()),
                           fut_row_data = list(future_fa.values.tolist()),
                           my_row_data = list(multiyear_fa.values.tolist()))


@app.route('/cho')
def cho_page():
    conn = sqlite3.connect('concat_4.db')
    conn.row_factory = sqlite3.Row

    cur = conn.cursor()
    cur.execute("select * from concat_1_def_full where Team_x = 'CHO'")
    bos = cur.fetchall()

    cur.execute("select * from df_ff where Team = 'Charlotte'")
    df = cur.fetchall()

    upcoming_fa, future_fa, multiyear_fa, list_names, list_th = copy_comps_algo.suggest_players('Charlotte', 'CHO')



    return render_template("cho.html", BOS = bos, DF = df, weak_names = list_names, th_list = list_th,
                           up_row_data = list(upcoming_fa.values.tolist()),
                           fut_row_data = list(future_fa.values.tolist()),
                           my_row_data = list(multiyear_fa.values.tolist()))

@app.route('/chi')
def chi_page():
    conn = sqlite3.connect('concat_4.db')
    conn.row_factory = sqlite3.Row

    cur = conn.cursor()
    cur.execute("select * from concat_1_def_full where Team_x = 'CHI'")
    bos = cur.fetchall()

    cur.execute("select * from df_ff where Team = 'Chicago'")
    df = cur.fetchall()

    upcoming_fa, future_fa, multiyear_fa, list_names, list_th = copy_comps_algo.suggest_players('Chicago', 'CHI')



    return render_template("chi.html", BOS = bos, DF = df, weak_names = list_names, th_list = list_th,
                           up_row_data = list(upcoming_fa.values.tolist()),
                           fut_row_data = list(future_fa.values.tolist()),
                           my_row_data = list(multiyear_fa.values.tolist()))

@app.route('/cle')
def cle_page():
    conn = sqlite3.connect('concat_4.db')
    conn.row_factory = sqlite3.Row

    cur = conn.cursor()
    cur.execute("select * from concat_1_def_full where Team_x = 'CLE'")
    bos = cur.fetchall()

    cur.execute("select * from df_ff where Team = 'Cleveland'")
    df = cur.fetchall()

    upcoming_fa, future_fa, multiyear_fa, list_names, list_th = copy_comps_algo.suggest_players('Cleveland', 'CLE')



    return render_template("cle.html", BOS = bos, DF = df, weak_names = list_names, th_list = list_th,
                           up_row_data = list(upcoming_fa.values.tolist()),
                           fut_row_data = list(future_fa.values.tolist()),
                           my_row_data = list(multiyear_fa.values.tolist()))

@app.route('/dal')
def dal_page():
    conn = sqlite3.connect('concat_4.db')
    conn.row_factory = sqlite3.Row

    cur = conn.cursor()
    cur.execute("select * from concat_1_def_full where Team_x = 'DAL'")
    bos = cur.fetchall()

    cur.execute("select * from df_ff where Team = 'Dallas'")
    df = cur.fetchall()

    upcoming_fa, future_fa, multiyear_fa, list_names, list_th = copy_comps_algo.suggest_players('Dallas', 'DAL')



    return render_template("dal.html", BOS = bos, DF = df, weak_names = list_names, th_list = list_th,
                           up_row_data = list(upcoming_fa.values.tolist()),
                           fut_row_data = list(future_fa.values.tolist()),
                           my_row_data = list(multiyear_fa.values.tolist()))

@app.route('/den')
def den_page():
    conn = sqlite3.connect('concat_4.db')
    conn.row_factory = sqlite3.Row

    cur = conn.cursor()
    cur.execute("select * from concat_1_def_full where Team_x = 'DEN'")
    bos = cur.fetchall()

    cur.execute("select * from df_ff where Team = 'Denver'")
    df = cur.fetchall()

    upcoming_fa, future_fa, multiyear_fa, list_names, list_th = copy_comps_algo.suggest_players('Denver', 'DEN')



    return render_template("den.html", BOS = bos, DF = df, weak_names = list_names, th_list = list_th,
                           up_row_data = list(upcoming_fa.values.tolist()),
                           fut_row_data = list(future_fa.values.tolist()),
                           my_row_data = list(multiyear_fa.values.tolist()))

@app.route('/det')
def det_page():
    conn = sqlite3.connect('concat_4.db')
    conn.row_factory = sqlite3.Row

    cur = conn.cursor()
    cur.execute("select * from concat_1_def_full where Team_x = 'DET'")
    bos = cur.fetchall()

    cur.execute("select * from df_ff where Team = 'Detroit'")
    df = cur.fetchall()

    upcoming_fa, future_fa, multiyear_fa, list_names, list_th = copy_comps_algo.suggest_players('Detroit', 'DET')



    return render_template("det.html", BOS = bos, DF = df, weak_names = list_names, th_list = list_th,
                           up_row_data = list(upcoming_fa.values.tolist()),
                           fut_row_data = list(future_fa.values.tolist()),
                           my_row_data = list(multiyear_fa.values.tolist()))

@app.route('/gsw')
def gsw_page():
    conn = sqlite3.connect('concat_4.db')
    conn.row_factory = sqlite3.Row

    cur = conn.cursor()
    cur.execute("select * from concat_1_def_full where Team_x = 'GSW'")
    bos = cur.fetchall()

    cur.execute("select * from df_ff where Team = 'Golden State'")
    df = cur.fetchall()

    upcoming_fa, future_fa, multiyear_fa, list_names, list_th = copy_comps_algo.suggest_players('Golden State', 'GSW')



    return render_template("gsw.html", BOS = bos, DF = df, weak_names = list_names, th_list = list_th,
                           up_row_data = list(upcoming_fa.values.tolist()),
                           fut_row_data = list(future_fa.values.tolist()),
                           my_row_data = list(multiyear_fa.values.tolist()))

@app.route('/hou')
def hou_page():
    conn = sqlite3.connect('concat_4.db')
    conn.row_factory = sqlite3.Row

    cur = conn.cursor()
    cur.execute("select * from concat_1_def_full where Team_x = 'HOU'")
    bos = cur.fetchall()

    cur.execute("select * from df_ff where Team = 'Houston'")
    df = cur.fetchall()

    upcoming_fa, future_fa, multiyear_fa, list_names, list_th = copy_comps_algo.suggest_players('Houston', 'HOU')



    return render_template("hou.html", BOS = bos, DF = df, weak_names = list_names, th_list = list_th,
                           up_row_data = list(upcoming_fa.values.tolist()),
                           fut_row_data = list(future_fa.values.tolist()),
                           my_row_data = list(multiyear_fa.values.tolist()))

@app.route('/ind')
def ind_page():
    conn = sqlite3.connect('concat_4.db')
    conn.row_factory = sqlite3.Row

    cur = conn.cursor()
    cur.execute("select * from concat_1_def_full where Team_x = 'IND'")
    bos = cur.fetchall()

    cur.execute("select * from df_ff where Team = 'Indiana'")
    df = cur.fetchall()

    upcoming_fa, future_fa, multiyear_fa, list_names, list_th = copy_comps_algo.suggest_players('Indiana', 'IND')



    return render_template("ind.html", BOS = bos, DF = df, weak_names = list_names, th_list = list_th,
                           up_row_data = list(upcoming_fa.values.tolist()),
                           fut_row_data = list(future_fa.values.tolist()),
                           my_row_data = list(multiyear_fa.values.tolist()))

@app.route('/lac')
def lac_page():
    conn = sqlite3.connect('concat_4.db')
    conn.row_factory = sqlite3.Row

    cur = conn.cursor()
    cur.execute("select * from concat_1_def_full where Team_x = 'LAC'")
    bos = cur.fetchall()

    cur.execute("select * from df_ff where Team = 'LA Clippers'")
    df = cur.fetchall()

    upcoming_fa, future_fa, multiyear_fa, list_names, list_th = copy_comps_algo.suggest_players('LA Clippers', 'LAC')



    return render_template("lac.html", BOS = bos, DF = df, weak_names = list_names, th_list = list_th,
                           up_row_data = list(upcoming_fa.values.tolist()),
                           fut_row_data = list(future_fa.values.tolist()),
                           my_row_data = list(multiyear_fa.values.tolist()))

@app.route('/lal')
def lal_page():
    conn = sqlite3.connect('concat_4.db')
    conn.row_factory = sqlite3.Row

    cur = conn.cursor()
    cur.execute("select * from concat_1_def_full where Team_x = 'LAL'")
    bos = cur.fetchall()

    cur.execute("select * from df_ff where Team = 'LA Lakers'")
    df = cur.fetchall()

    upcoming_fa, future_fa, multiyear_fa, list_names, list_th = copy_comps_algo.suggest_players('LA Lakers', 'LAL')



    return render_template("lal.html", BOS = bos, DF = df, weak_names = list_names, th_list = list_th,
                           up_row_data = list(upcoming_fa.values.tolist()),
                           fut_row_data = list(future_fa.values.tolist()),
                           my_row_data = list(multiyear_fa.values.tolist()))

@app.route('/mem')
def mem_page():
    conn = sqlite3.connect('concat_4.db')
    conn.row_factory = sqlite3.Row

    cur = conn.cursor()
    cur.execute("select * from concat_1_def_full where Team_x = 'MEM'")
    bos = cur.fetchall()

    cur.execute("select * from df_ff where Team = 'Memphis'")
    df = cur.fetchall()

    upcoming_fa, future_fa, multiyear_fa, list_names, list_th = copy_comps_algo.suggest_players('Memphis', 'MEM')



    return render_template("mem.html", BOS = bos, DF = df, weak_names = list_names, th_list = list_th,
                           up_row_data = list(upcoming_fa.values.tolist()),
                           fut_row_data = list(future_fa.values.tolist()),
                           my_row_data = list(multiyear_fa.values.tolist()))




