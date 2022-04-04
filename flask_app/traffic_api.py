import psycopg2

def has_duplicates2(seq):
    seen = []
    unique_list = [x for x in seq if x not in seen and not seen.append(x)]
    return unique_list

def trans_pred(data, result, logs, conn, cur):
    if data  not in has_duplicates2(logs)[:-1]:    
        data = data+[result]
        create_traffic_table = """CREATE TABLE IF NOT EXISTS traffic(
                            id INTEGER NOT NULL,
                            spot_name VARCHAR(20),
                            hour FLOAT,
                            pm10 FLOAT,
                            pm25 FLOAT,
                            O3 FLOAT,
                            NO2 FLOAT,
                            CO FLOAT,
                            SO2 FLOAT,
                            prediction FLOAT,
                            PRIMARY KEY (id)
                            );"""
                    
        cur.execute(create_traffic_table)        
        conn.commit()
        
        cur.execute("SELECT * FROM traffic;")
        data_all = cur.fetchall()

        try:
            id_num = data_all[-1][0] + 1
        except IndexError:
            id_num = 1
        cur.execute("""INSERT INTO traffic (id, spot_name, pm10, pm25, O3, NO2, CO, SO2, hour, prediction)
                        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s);""", [id_num]+data)

        conn.commit()


def table_init():
        
    host = 'Insert host'
    user = 'Insert user'
    password = 'Insert password'
    database = 'Insert database'

    conn = psycopg2.connect(
        host=host,
        user=user,
        password=password,
        database=database
    )

    cur = conn.cursor()
    
    cur.execute("DROP TABLE IF EXISTS traffic;") 
    
    create_traffic_table = """CREATE TABLE IF NOT EXISTS traffic(
                        id INTEGER NOT NULL,
                        spot_name VARCHAR(20),
                        hour FLOAT,
                        pm10 FLOAT,
                        pm25 FLOAT,
                        O3 FLOAT,
                        NO2 FLOAT,
                        CO FLOAT,
                        SO2 FLOAT,
                        prediction FLOAT,
                        PRIMARY KEY (id)
                        );"""
    cur.execute(create_traffic_table) 
    conn.commit()
    
#table_init()
