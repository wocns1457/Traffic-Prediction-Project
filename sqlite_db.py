from mongo_db import MONGODB_SETUP
import sqlite3
import os

DB_FILENAME = "traffic.db"
CSV_FILENAME = "traffic.csv"
DB_FILEPATH = os.path.join(os.getcwd(), DB_FILENAME)
CSV_FILEPATH = os.path.join(os.getcwd(), 'reference\\',CSV_FILENAME)

def get_cursor(DB_FILEPATH):
    connection = sqlite3.connect(DB_FILEPATH)
    cursor = connection.cursor()
    
    return connection, cursor

def table_init():
    conn, cur = get_cursor(DB_FILEPATH)
    
    create_weather_table = """CREATE TABLE IF NOT EXISTS weather (
                        id INTEGER NOT NULL,
                        MSRDT DATETIME,
                        MSRSTE_NM VARCHAR(20),
                        pm10 FLOAT,
                        pm25 FLOAT,
                        O3 FLOAT,
                        NO2 FLOAT,
                        CO FLOAT,
                        SO2 FLOAT,
                        PRIMARY KEY (id)
                        );"""
                        
    create_vol_table = """CREATE TABLE IF NOT EXISTS vol (
                        id INTEGER NOT NULL,
                        ymd DATETIME,
                        spot_num VARCHAR(20),
                        spot_name VARCHAR(20),
                        vol FLOAT,
                        PRIMARY KEY (id)
                        );"""
                        
    cur.execute("DROP TABLE IF EXISTS weather;")   
    cur.execute("DROP TABLE IF EXISTS vol;")        
    cur.execute(create_weather_table)
    cur.execute(create_vol_table)
    
    conn.commit()
    

def add_weather(docs):
    conn, cur = get_cursor(DB_FILEPATH)
    cur.execute("SELECT * FROM weather;")
    data_all = cur.fetchall()

    try:
        id_num = data_all[-1][0] + 1
    except IndexError:
        id_num = 1
        
    print("Start input into database...")     
    for doc in docs:
        doc['MSRDT'] = doc['MSRDT'][:4]+'-'+doc['MSRDT'][4:6]+'-'+doc['MSRDT'][6:8]+' '+doc['MSRDT'][8:10]+':'+doc['MSRDT'][10:]
        
        inset_data = [doc['MSRDT'], doc['MSRSTE_NM'], doc['PM10'], doc['PM25'], 
                doc['O3'], doc['NO2'], doc['CO'], doc['SO2']]
        
        cur.execute("""INSERT INTO weather (id, MSRDT, MSRSTE_NM, pm10, pm25, O3, NO2, CO, SO2)
                        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?);""", ([id_num]+inset_data))
        id_num+=1

    conn.commit()
    print("Complete input into database!!!")


def add_vol(docs):
    conn, cur = get_cursor(DB_FILEPATH)
    cur.execute("SELECT * FROM vol;")
    data_all = cur.fetchall()
    
    aaa = {'A-15':'종로구', 'A-20':'용산구', 'A-16':'중구',
        'D-14':'은평구', 'C-07':'마포구', 'B-01':'도봉구',
        'D-13':'노원구', 'B-03':'광진구', 'B-05':'중랑구',
        'D-05':'동대문구', 'D-09':'성북구', 'B-17':'영등포구', 
        'D-31':'동작구', 'D-33':'관악구', 'B-24':'금천구',
        'D-21':'강서구', 'B-30':'양천구', 'D-26':'구로구',
        'D-35':'강남구', 'D-37':'서초구', 'D-46':'송파구',
        'C-22':'강동구'
        }
    
    try:
        id_num = data_all[-1][0] + 1
    except IndexError:
        id_num = 1
        
    print("Start input into database...")     
       
    for doc in docs:
        try:
            for value in doc['result']:
                value['ymd'] =value['ymd'][:4]+'-'+value['ymd'][4:6]+'-'+value['ymd'][6:8]+' '+value['ymd'][8:10]+':'+value['ymd'][10:]
                inset_data = [value['ymd'], doc['spot_num'], aaa[doc['spot_num']], value['vol']]
                cur.execute("""INSERT INTO vol (id, ymd, spot_num, spot_name, vol)
                        VALUES (?, ?, ?, ?, ?);""", ([id_num]+inset_data))
                id_num+=1
        except KeyError:
            pass
    conn.commit()
    print("Complete input into database!!!")
     
    return None


def to_csv(DB_FILEPATH, CSV_FILEPATH):
    import pandas as pd
    conn, cur = get_cursor(DB_FILEPATH)
    to_csv_query = """SELECT w.id , v.spot_name, v.ymd, w.pm10, w.pm25, w.O3, w.NO2, w.CO, w.SO2, v.vol 
                    from weather w 
                    join vol v  on (w.MSRSTE_NM == v.spot_name) and (w.MSRDT ==v.ymd);
                    """
    db_df = pd.read_sql_query(to_csv_query, conn)
    db_df.to_csv(CSV_FILEPATH, index=False, encoding='cp949')
    print('Complete DATABASE to CSV!!!')
    
mongo = MONGODB_SETUP(2021, 2, 1, 2021, 3, 1)

# table_init()
# vol_docs = mongo.get_vol()
# add_vol(vol_docs)
# weather_docs = mongo.get_weather()
# add_weather(weather_docs)
to_csv(DB_FILEPATH, CSV_FILEPATH)
print(DB_FILEPATH)
print(CSV_FILEPATH)