import numpy as np
import pandas as pd
import math
from sklearn.preprocessing import StandardScaler

class KNN:
    def init(self):
        self.df = pd.read_csv('prepared-data.csv').drop(['Unnamed: 0'],axis=1)
        self.df['target_category'] = self.df.apply(lambda row: self.determine_category(row.price), axis=1)
        self.df = self.df.drop(columns=['price'])

        k = round(math.sqrt(len(self.df)))
        if (k % 2 == 0):
            k += 1

        print('K = ' + str(k))

        self.k = k

    def predict(self, city_part, build_year, area, number_of_rooms, level, k=None):
        price_category_df = pd.read_csv('city-part-categories.csv')
        price_category = price_category_df.loc[price_category_df['city_part'] == city_part]['price_average'].values[0]

        predict_df = pd.DataFrame({
            'area': [float(area)],
            'build_year': int(build_year),
            'number_of_rooms': int(number_of_rooms),
            'level': int(level),
            'price_average': price_category
        })

        df_without_target = self.df.drop(columns=['target_category'])
        all = df_without_target.append(predict_df)
        scaler = StandardScaler()
        all_scaled = scaler.fit_transform(all)
        all_scaled = pd.DataFrame(all_scaled, columns=['area', 'build_year', 'number_of_rooms', 'level', 'price_average'])
        df_scaled = all_scaled[:-1]

        given_scaled_df = all_scaled.tail(1)
        repeated = pd.concat([given_scaled_df]*len(self.df), ignore_index=True)

        distances = self.euclidean_distance(df_scaled, repeated)

        df_with_distances = self.df.copy()

        df_with_distances['distances'] = distances


        df_result = df_with_distances.sort_values(by=['distances'])

        if k is None:
            chosen = df_result.head(self.k)
        else:
            chosen = df_result.head(k)
        

        return chosen['target_category'].value_counts().sort_values(ascending=False).keys()[0]

    def determine_category(self, value):
        if value <= 49999:
            return '0-49999'
        elif 50000 <= value <= 99999:
            return '50000-99999'
        elif 100000 <= value <= 149999:
            return '10000-149999'
        elif 150000 <= value <= 199999:
            return '150000-199999'
        else:
            return '200000-'

    def euclidean_distance(self, dataset, given):
        distance = 0
        for i in range(len(dataset.columns)):
            distance += pow(dataset.iloc[:,i] - given.iloc[:, i], 2)
        return np.sqrt(distance)

    def manhattan_distance(self, dataset, given):
        distance = 0
        for i in range(len(dataset.columns)):
            distance += np.abs(dataset.iloc[:,i] - given.iloc[:, i])
        return distance
