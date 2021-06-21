import mysql.connector
import pandas as pd

mydb = mysql.connector.connect(
  host="localhost",
  user="mladen",
  password="password",
  database="crawler"
)

# my_cursor = mydb.cursor(dictionary=False, prepared=False)

def execute_a():
    sale = pd.read_sql("""
        SELECT COUNT(id) AS sale 
        FROM records 
        WHERE `type` = 'Prodaja'
    """, mydb)

    rent = pd.read_sql("""
        SELECT COUNT(id) AS rent 
        FROM records 
        WHERE `type` = 'Izdavanje'
    """, mydb)

    df = pd.DataFrame()
    df['prodaja'] = sale['sale']
    df['iznajmljivanje'] = rent['rent']
    df.to_csv('phase-2/a.csv')

def execute_b():
    df = pd.read_sql("""
        SELECT COUNT(id) AS broj_prodaje, city 
        FROM records 
        WHERE `type` = 'Prodaja' 
        GROUP BY city 
        ORDER BY broj_prodaje DESC
    """, mydb)
    df.to_csv('phase-2/b.csv')

def execute_c():
    registered_houses =  pd.read_sql("""
         SELECT COUNT(id) AS uknjizene_kuce 
         FROM records 
         WHERE registered = 1 
            AND offer_type = 'Kuće'
    """, mydb)

    unregistered_houses =  pd.read_sql("""
         SELECT COUNT(id) AS neuknjizene_kuce 
         FROM records 
         WHERE registered = 0 
            AND offer_type = 'Kuće'
    """, mydb)

    registered_apartments =  pd.read_sql("""
         SELECT COUNT(id) AS uknjizeni_stanovi 
         FROM records 
         WHERE registered = 1 
            AND offer_type = 'Stanovi'
    """, mydb)

    unregistered_apartments =  pd.read_sql("""
         SELECT COUNT(id) AS neuknjizeni_stanovi 
         FROM records 
         WHERE registered = 0 
            AND offer_type = 'Stanovi'
    """, mydb)

    df = pd.DataFrame()
    df['uknjizene_kuce'] = registered_houses['uknjizene_kuce']
    df['neuknjizene_kuce'] = unregistered_houses['neuknjizene_kuce']
    df['uknjizeni_stanovi'] = registered_apartments['uknjizeni_stanovi']
    df['neuknjizeni_stanovi'] = unregistered_apartments['neuknjizeni_stanovi']

    df.to_csv('phase-2/c.csv')

def execute_d():
    houses = pd.read_sql("""
        SELECT * FROM records WHERE offer_type = 'Kuće' AND `type` = 'Prodaja' ORDER BY price DESC LIMIT 30
    """, mydb)

    apartments = pd.read_sql("""
        SELECT * FROM records WHERE offer_type = 'Stanovi' AND `type` = 'Prodaja' ORDER BY price DESC LIMIT 30
    """, mydb)

    houses.to_csv('phase-2/d-houses.csv')
    apartments.to_csv('phase-2/d-apartments.csv')

def execute_e():
    houses = pd.read_sql("""
        SELECT * FROM records WHERE offer_type = 'Kuće' ORDER BY area DESC LIMIT 100
    """, mydb)

    apartments = pd.read_sql("""
        SELECT * FROM records WHERE offer_type = 'Stanovi' ORDER BY area DESC LIMIT 100
    """, mydb)

    houses.to_csv('phase-2/e-houses.csv')
    apartments.to_csv('phase-2/e-apartments.csv')

def execute_f():
    df = pd.read_sql("""
        SELECT * FROM records WHERE build_year = 2020 ORDER BY price DESC
    """, mydb)

    df.to_csv('phase-2/f.csv')

def execute_g():
    number_of_rooms = pd.read_sql("""
        SELECT * FROM records ORDER BY number_of_rooms DESC LIMIT 30
    """, mydb)

    area = pd.read_sql("""
        SELECT * FROM records WHERE offer_type = 'Stanovi' ORDER BY area DESC LIMIT 30
    """, mydb)

    area_field = pd.read_sql("""
        SELECT * FROM records WHERE offer_type = 'Kuće' ORDER BY area_field DESC LIMIT 30
    """, mydb)

    number_of_rooms.to_csv('phase-2/g-number-of-rooms.csv')
    area.to_csv('phase-2/g-area.csv')
    area_field.to_csv('phase-2/g-area-field.csv')


execute_g()

