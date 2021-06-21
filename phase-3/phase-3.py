from matplotlib.pyplot import title
import plotly.express as px
import mysql.connector
import pandas as pd

mydb = mysql.connector.connect(
  host="localhost",
  user="mladen",
  password="password",
  database="crawler"
)

def execute_a():
    df = pd.read_sql("""
        SELECT city_part, COUNT(id) AS total FROM records WHERE city = "Beograd" GROUP BY city_part ORDER BY total DESC LIMIT 10
    """, mydb)

    fig = px.bar(df, x='city_part', y='total', color='city_part', 
        labels={
            'city_part': 'Deo grada',
            'total': 'Broj oglasa'
        }, title="10 najzastupljenijih delova Beograda sa najvecim brojem nekretnina u ponudi")
    fig.write_html('phase-3/a.html', auto_open=True)

def execute_b():
    range_35 = pd.read_sql('SELECT COUNT(id) AS broj_stanova FROM records WHERE area <=35 AND offer_type = "Stanovi" AND `type` = "Prodaja"', mydb)
    range_35_50 = pd.read_sql('SELECT COUNT(id) AS broj_stanova FROM records WHERE area > 35 AND area <=50 AND offer_type = "Stanovi" AND `type` = "Prodaja"', mydb)
    range_50_65 = pd.read_sql('SELECT COUNT(id) AS broj_stanova FROM records WHERE area > 50 AND area <=65 AND offer_type = "Stanovi" AND `type` = "Prodaja"', mydb)
    range_65_80 = pd.read_sql('SELECT COUNT(id) AS broj_stanova FROM records WHERE area > 65 AND area <=80 AND offer_type = "Stanovi" AND `type` = "Prodaja"', mydb)
    range_80_95 = pd.read_sql('SELECT COUNT(id) AS broj_stanova FROM records WHERE area > 80 AND area <=95 AND offer_type = "Stanovi" AND `type` = "Prodaja"', mydb)
    range_95_110 = pd.read_sql('SELECT COUNT(id) AS broj_stanova FROM records WHERE area > 95 AND area <=110 AND offer_type = "Stanovi" AND `type` = "Prodaja"', mydb)
    range_110 = pd.read_sql('SELECT COUNT(id) AS broj_stanova FROM records WHERE area > 110 AND offer_type = "Stanovi" AND `type` = "Prodaja"', mydb)

    df = pd.DataFrame(
        [
            ['do 35', range_35['broj_stanova'][0]],
            ['35-50', range_35_50['broj_stanova'][0]],
            ['50-65', range_50_65['broj_stanova'][0]],
            ['65-80', range_65_80['broj_stanova'][0]],
            ['80-95', range_80_95['broj_stanova'][0]],
            ['95-110', range_95_110['broj_stanova'][0]],
            ['preko 110', range_110['broj_stanova'][0]],
        ],
        columns=['category', 'total']
    )

    fig = px.bar(df, x='category', y='total', color='category',
        labels={
                'category': 'Kategorija',
                'total': 'Broj stanova'
            }, title="Broj stanova za prodaju prema kvadraturi")
    fig.write_html('phase-3/b.html', auto_open=True)

def execute_c():
    range_1951_1960 = pd.read_sql('SELECT COUNT(id) AS total FROM records WHERE build_year BETWEEN 1951 AND 1960', mydb)
    range_1961_1970 = pd.read_sql('SELECT COUNT(id) AS total FROM records WHERE build_year BETWEEN 1961 AND 1970', mydb)
    range_1971_1980 = pd.read_sql('SELECT COUNT(id) AS total FROM records WHERE build_year BETWEEN 1971 AND 1980', mydb)
    range_1981_1990 = pd.read_sql('SELECT COUNT(id) AS total FROM records WHERE build_year BETWEEN 1981 AND 1990', mydb)
    range_1991_2000 = pd.read_sql('SELECT COUNT(id) AS total FROM records WHERE build_year BETWEEN 1991 AND 2000', mydb)
    range_2001_2010 = pd.read_sql('SELECT COUNT(id) AS total FROM records WHERE build_year BETWEEN 2001 AND 2010', mydb)
    range_2011_2020 = pd.read_sql('SELECT COUNT(id) AS total FROM records WHERE build_year BETWEEN 2011 AND 2020', mydb)

    df = pd.DataFrame(
        [
            ['1951-1960', range_1951_1960['total'][0]],
            ['1961-1970', range_1961_1970['total'][0]],
            ['1871-1980', range_1971_1980['total'][0]],
            ['1981-1990', range_1981_1990['total'][0]],
            ['1991-2000', range_1991_2000['total'][0]],
            ['2001-2010', range_2001_2010['total'][0]],
            ['2011-2020', range_2011_2020['total'][0]],
        ],
        columns=['category', 'total']
    )

    fig = px.bar(df, x='category', y='total', color='category',
        labels={
                'category': 'Kategorija',
                'total': 'Broj nekretnina'
            }, title="Broj izgradjenih nekretnina po dekadama")
    fig.write_html('phase-3/c.html', auto_open=True)

def execute_d():
    my_cursor = mydb.cursor(dictionary=False, prepared=False)

    my_cursor.execute('SELECT city, COUNT(id) AS total FROM records GROUP BY city ORDER BY total DESC LIMIT 5')
    top_cities = my_cursor.fetchall()

    for city in top_cities:
        my_cursor.execute('SELECT COUNT(id) FROM records WHERE type = "Izdavanje" AND city = %s', (city[0],))
        rent = int(my_cursor.fetchone()[0])

        my_cursor.execute('SELECT COUNT(id) FROM records WHERE type = "Prodaja" AND city = %s', (city[0],))
        sale = int(my_cursor.fetchone()[0])

        df = pd.DataFrame([
            ['Izdavanje', rent, str(round(rent/(rent+sale)*100)) + '%'],
            ['Prodaja', sale, str(round(sale/(rent+sale)*100)) + '%']
        ], columns=['Kategorija', 'Broj oglasa', 'Procenat'])

        fig = px.bar(df, x='Kategorija', y='Broj oglasa', color='Kategorija', hover_data=['Procenat'], title="Broj nekretnina za grad " + city[0])
        fig.write_html('phase-3/d/d-' + city[0] + '.html', auto_open=True)

def execute_e():
    my_cursor = mydb.cursor(dictionary=False, prepared=False)

    my_cursor.execute('SELECT COUNT(id) FROM records WHERE `type` = "Prodaja" AND price <= 49999')
    range_49999 = my_cursor.fetchone()[0]

    my_cursor.execute('SELECT COUNT(id) FROM records WHERE `type` = "Prodaja" AND price >= 50000 AND price <= 99999')
    range_50000_99999 = my_cursor.fetchone()[0]

    my_cursor.execute('SELECT COUNT(id) FROM records WHERE `type` = "Prodaja" AND price >= 100000 AND price <= 149999')
    range_100000_149999 = my_cursor.fetchone()[0]

    my_cursor.execute('SELECT COUNT(id) FROM records WHERE `type` = "Prodaja" AND price >= 150000 AND price <= 199999')
    range_150000_199999 = my_cursor.fetchone()[0]

    my_cursor.execute('SELECT COUNT(id) FROM records WHERE `type` = "Prodaja" AND price >= 200000')
    range_200000 = my_cursor.fetchone()[0]

    total = range_49999 + range_50000_99999 + range_100000_149999 + range_150000_199999 + range_200000;

    df = pd.DataFrame([
        ['do 49.999e', range_49999, str(round(range_49999/(total)*100)) + '%'],
        ['od 50.000e do 99.999e', range_50000_99999, str(round(range_50000_99999/(total)*100)) + '%'],
        ['od 100.000e do 149.999e', range_100000_149999, str(round(range_100000_149999/(total)*100)) + '%'],
        ['od 150.000e do do 199.999e', range_150000_199999, str(round(range_150000_199999/(total)*100)) + '%'],
        ['preko 200.000e', range_200000, str(round(range_200000/(total)*100)) + '%']
    ], columns=['Kategorija', 'Broj oglasa', 'Procenat'])

    fig = px.bar(df, x='Kategorija', y='Broj oglasa', color='Kategorija', hover_data=['Procenat'], title='Broj oglasa po cenovnom posegu')
    fig.write_html('phase-3/e.html', auto_open=True)


execute_c()