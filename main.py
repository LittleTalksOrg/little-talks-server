import os

def send_messages(request):
    if request.method == 'GET':
        return "<script>window.location.href='https://github.com/LittleTalksOrg/little-talks-server'</script>"
    else:
        if request.form['msg']!='':
            insert_msg(request)
        
        return get_msgs(request)

def insert_msg(request):
    conn = get_db_conn()
    cursor = conn.cursor()
    try:
        cursor.execute(get_insert_msg_query().format(os.environ['MSG_TABLE'], request.form['nickname'],request.form['msg'],request.form['lat'],request.form['lng'],request.remote_addr))
        conn.commit()
        conn.close()
    except:
        create_database()
        insert_msg(request)
    conn.close()

def get_msgs(request):

    LOCATION_PRECISION = 0.005
    WHITE = '\033[1;0m'
    LIGHT_WHITE = '\033[1;2m'
    GREEN = '\033[1;32m'
    DARKGREEN = '\033[1;31m'

    conn = get_db_conn()
    cursor = conn.cursor()
    try:
        min_lat = float(request.form['lat'])-LOCATION_PRECISION
        max_lat = float(request.form['lat'])+LOCATION_PRECISION
        min_lng = float(request.form['lng'])-LOCATION_PRECISION
        max_lng = float(request.form['lng'])+LOCATION_PRECISION
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
            """.format(os.environ['MSG_TABLE'], min_lat,max_lat,min_lng,max_lng)
        cursor.execute(query)
    except:
        conn.close()
        create_database()
        return get_msgs(request)

    returnString = ""
    test = cursor.fetchall()
    for linha in test:
        returnString = DARKGREEN + "(" + str(linha[5]) + ") " + linha[1] + " said: #" + str(linha[0]) + " " + GREEN + linha[2] + WHITE +"\n" + returnString 
    conn.close()
    return LIGHT_WHITE+"You are at "+request.form['lat']+","+request.form['lng']+" as "+request.form['nickname']+"\n"+WHITE+returnString

def get_db_conn():
    if os.environ['DB'] =='psql':
        import psycopg2
        PS_DATABASE = os.environ['PS_DATABASE']
        PS_USER = os.environ['PS_USER']
        PS_PASSWORD = os.environ['PS_PASSWORD']
        PS_HOST = os.environ['PS_HOST']
        PS_PORT = os.environ['PS_PORT']
        
        return psycopg2.connect(database = PS_DATABASE, user = PS_USER, password = PS_PASSWORD, host = PS_HOST, port = PS_PORT)
    else:
        import sqlite3
        return sqlite3.connect('msgs.db')

def create_database():
    conn = get_db_conn()
    cursor = conn.cursor() 
    # criando a tabela (schema)
    cursor.execute(get_create_table_msg_query())
    conn.commit()
    conn.close()
    print('Tabela criada com sucesso.')
    return 'ok'

def get_insert_msg_query():
    if os.environ['DB'] =='psql':
        return """
        INSERT INTO {} (nickname, msg, lat, lng, ip_address, created_at) 
        VALUES ('{}', '{}', {}, {}, '{}', NOW())
        """
    else: #sqlite
        return """
        INSERT INTO {} (nickname, msg, lat, lng, ip_address, created_at) 
        VALUES ('{}', '{}', {}, {}, '{}', strftime('%Y-%m-%d %H-%M-%S','now'))
        """

def get_create_table_msg_query():
    if os.environ['DB'] =='psql':
        return """
                CREATE TABLE IF NOT EXISTS {} (
                        id  SERIAL,
                        nickname TEXT NOT NULL,
                        msg TEXT NOT NULL,
                        lat REAL NULL,
                        lng REAL NULL,
                        created_at TIMESTAMP NULL,
                        ip_address TEXT NULL
                );
                """.format(os.environ['MSG_TABLE'])
    else: #sqlite
        return """
                CREATE TABLE IF NOT EXISTS {} (
                        id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
                        nickname TEXT NOT NULL,
                        msg TEXT NOT NULL,
                        lat REAL NULL,
                        lng REAL NULL,
                        created_at DATETIME NULL,
                        ip_address TEXT NULL
                );
                """.format(os.environ['MSG_TABLE'])