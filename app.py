from flask import Flask, jsonify, request
import os
from dotenv import load_dotenv
load_dotenv()

app = Flask(__name__)

WHITE = '\033[1;0m'
LIGHT_WHITE = '\033[1;2m'
GREEN = '\033[1;32m'
DARKGREEN = '\033[1;31m'

MSG_TABLE = os.environ['MSG_TABLE']

@app.route('/')
def hello_world():
    return "<script>window.location.href='https://github.com/LittleTalksOrg/little-talks-server'</script>"

@app.route('/', methods=["POST"])
def send_messages():
    if request.form['msg']!='':
        insert_msg(request.form)
    
    return get_msgs()

def insert_msg(form):
    conn = get_db_conn()
    cursor = conn.cursor()
    try:
        cursor.execute("""
        INSERT INTO {} (nickname, msg, lat, lng) 
        VALUES ('{}', '{}', {}, {})
        """.format(MSG_TABLE, form['nickname'],form['msg'],form['lat'],form['lng']))
        conn.commit()
        conn.close()
    except:
        create_database()
        insert_msg(form)
    conn.close()

def get_msgs():
    conn = get_db_conn()
    cursor = conn.cursor()
    try:
        min_lat = float(request.form['lat'])-0.05
        max_lat = float(request.form['lat'])+0.05
        min_lng = float(request.form['lng'])-0.05
        max_lng = float(request.form['lng'])+0.05
    except:
        return "invalid latitude '{}' or longitud '{}'".format(request.form['lat'],request.form['lng']) 
    try:
        
        query = """
            SELECT * 
            FROM {} 
                WHERE 
                    lat >= {} 
                    AND lat <= {} 
                    AND lng >= {} 
                    AND lng <= {} 
                ORDER BY id DESC 
                LIMIT 25
            """.format(MSG_TABLE, min_lat,max_lat,min_lng,max_lng)
        print(query)
        cursor.execute(query)

    except:
        conn.close()
        create_database()
        return get_msgs()


    returnString = ""
    for linha in cursor.fetchall():
        returnString = DARKGREEN + linha[1] + " (" + str(linha[3]) + "," + str(linha[4]) + ") said: #" + str(linha[0]) + " " + GREEN + linha[2] + WHITE +"\n" + returnString 
    conn.close()
    return LIGHT_WHITE+"You are at "+request.form['lat']+","+request.form['lng']+" as "+request.form['nickname']+"\n"+WHITE+returnString

def create_database():
    conn = get_db_conn()
    cursor = conn.cursor() 
    # criando a tabela (schema)
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS {} (
            id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
            nickname TEXT NOT NULL,
            msg TEXT NOT NULL,
            lat REAL NULL,
            lng REAL NULL,
            created_at DATE NULL,
            ip_address STRING NULL
    );
    """.format(MSG_TABLE))
    conn.close()
    print('Tabela criada com sucesso.')
    return 'ok'

def get_db_conn():
    import sqlite3

    # conectando...
    conn = sqlite3.connect('msgs.db')
    # definindo um cursor
    return conn