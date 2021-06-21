import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler

class LinearRegression:

    def init(self):
        df = pd.read_csv('prepared-data.csv').drop(['Unnamed: 0'],axis=1)
        self.x = df.drop(columns=['price'])
        x = self.x
        y = df['price']
        theta = np.zeros(len(x.columns)+1)

        self.scaler = StandardScaler()
        
        x_scaled = self.scaler.fit_transform(x)
        x_scaled = pd.DataFrame(x_scaled, columns=['area', 'build_year', 'number_of_rooms', 'level', 'price_average'])


        x_scaled = pd.concat([pd.Series(1, index=df.index, name='00'), x_scaled], axis=1)


        x_train, x_test, y_train, y_test = train_test_split(x_scaled, y, test_size=0.3, random_state=48)


        iterations = 1200

        J, j, theta = self.decent(x_train, y_train, x_test, y_test, theta, 0.01, iterations)

        self.theta = theta
        print(theta)

        plt.plot(range(1, iterations +1), j, color ='blue')
        plt.rcParams["figure.figsize"] = (10,6)
        plt.grid()
        plt.xlabel("Number of iterations")
        plt.ylabel("cost (J)")
        plt.title("Convergence of gradient descent")
        plt.savefig('cost.png')

        pred = x_test.dot(theta)
        print((y_test - pred).abs().mean())

        mae = ((pred - y_test).abs()).sum() / len(y_test)

        print ('MAE: ' + str(mae))

        print(self.compute_cost(x_test, y_test, theta))

    def scale(self, x):
        return x / (x.max() - x.min())

    def scale_normalization(self, x):
        mu = np.mean(x, axis=0)
        sigma = np.std(x, axis=0, ddof=1)
        x_norm = (x - mu) / sigma
        return x_norm

    def hypothesis(self, theta, x):
        return theta*x

    def compute_cost(self, x, y, theta):
        y1 = self.hypothesis(theta, x)
        y1 = np.sum(y1, axis=1)
        return (1/2*y.size) * np.sum(np.square(y1 - y))

    def decent(self, x, y, x_test, y_test, theta, alpha, interations):
        J = []
        k = 0
        j = []
        j_test = []
        while (k < interations):
            y1 = self.hypothesis(theta, x)
            y1 = np.sum(y1, axis=1)
            for c in range(0, len(x.columns)):
                theta[c] = theta[c] - alpha*(sum((y1-y)*x.iloc[:,c])/len(x))
            j.append(self.compute_cost(x, y, theta))
            J.append(j[k])

            j_test.append(self.compute_cost(x_test, y_test, theta))

            if k > 0 and (j[k] > j[k-1] or j_test[k] > j_test[k-1]):
                print('Stop iterations at: ' + str(k))
                return J, j, theta

            k += 1

            
        return J, j, theta

    def predict(self, city_part, build_year, area, number_of_rooms, level):
        price_category_df = pd.read_csv('city-part-categories.csv')
        price_category = price_category_df.loc[price_category_df['city_part'] == city_part]['price_average'].values[0]

        predict_df = pd.DataFrame({
            'area': [float(area)],
            'build_year': int(build_year),
            'number_of_rooms': int(number_of_rooms),
            'level': int(level),
            'price_average': price_category
        })

        df_with_predict_df = self.x.append(predict_df, ignore_index=True)
        array_with_predict_df_scaled = self.scaler.fit_transform(df_with_predict_df)
        df_with_predict_df_scaled = pd.DataFrame(array_with_predict_df_scaled, columns=['area', 'build_year', 'number_of_rooms', 'level', 'price_average'])

        predict_scaled = df_with_predict_df_scaled.tail(1)

        predict_scaled_repeated = pd.concat([pd.Series(1, index=predict_scaled.index, name='00'), predict_scaled], axis=1)

        result = np.sum(self.hypothesis(self.theta, predict_scaled_repeated), axis=1)

        return round(result.values[0], 2)
