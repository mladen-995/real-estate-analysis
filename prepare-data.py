import mysql.connector
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


mydb = mysql.connector.connect(
  host="localhost",
  user="mladen",
  password="password",
  database="crawler"
)

city_parts_df = pd.read_sql("""
    SELECT r.city_part, AVG(r.price) AS price_average 
    FROM records r
    WHERE r.city = "Beograd" 
        AND r.offer_type = "Stanovi" 
        AND `r`.`type` = "Prodaja" 
        AND r.city_part IN (SELECT cp.name FROM city_parts AS cp)
    GROUP BY r.city_part 
    ORDER BY price_average DESC
""", mydb)

city_parts_df.to_csv('city-part-categories.csv', index=False)

city_parts_average_price = city_parts_df[['price_average', 'city_part']]


df = pd.read_sql("""
  SELECT r.* 
  FROM records AS r
  WHERE r.offer_type = "Stanovi" 
    AND `r`.`type` = "Prodaja" 
    AND `r`.`level` >= 0 
    AND `r`.`level` < 100 
    AND r.area IS NOT NULL 
    AND r.area < 6000
    AND r.city_part IN (SELECT cp.name FROM city_parts AS cp)
    AND
      (r.build_year BETWEEN 1900 AND 2030
      OR r.build_year IS NULL)
""", mydb)

df = pd.merge(df, city_parts_average_price, on='city_part')

df['build_year'] = df['build_year'].replace(np.nan, df['build_year'].mean())
df['number_of_rooms'] = df['number_of_rooms'].replace(np.nan, df['number_of_rooms'].mean())
df['level'] = df['level'].replace(np.nan, df['level'].mean())

df.hist()
plt.show()

# prepared_df = df[['area', 'build_year', 'price', 'number_of_rooms', 'level', 'price_average']]

# prepared_df.to_csv('prepared-data.csv')
