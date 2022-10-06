import pandas as pd
import math


class DataAnalysis:

    def __init__(self):
        self.optimal_k = 3
        self.correct_guesses = []
        self.data = None
        self.factorize_dict = list()
        self.read_data()

    def read_data(self):
        data = pd.read_csv('big_data.csv',
                           encoding='UTF-8',
                           sep=',')
        del data["Имя"], data["Отметка времени"]
        to_enumerate = ["Во сколько встаешь", 'Высшая школа', 'Округ', 'Цвет глаз', "Чай или кофе"]
        for column in data.columns:
            self.factorize_dict.append(list(pd.factorize(data[column])[1]))
        for index, elem in enumerate(self.factorize_dict):
            self.factorize_dict[index] = [str(x) for x in elem]
        data[to_enumerate] = data[to_enumerate].apply(lambda x: pd.factorize(x)[0])
        self.data = data.apply(lambda x: [element / max(x) for element in x])

    def sort_neighbours_by_distance(self, entry):
        neighbours_distance = []
        for index, value in self.data.iterrows():
            if index != entry:
                coordinates_difference = [x - y for x in self.data.iloc[entry][:-1] for y in value[:-1]]
                distance = sum(math.sqrt(x ** 2) for x in coordinates_difference)
                neighbours_distance.append([distance, value[-1]])
        return sorted(neighbours_distance)

    def predict_by_k_neighbours(self, k, entry):
        closest_neighbours = self.sort_neighbours_by_distance(entry)[:k + 1]
        prediction = round(sum(x[1] for x in closest_neighbours) / (k+1))
        return prediction

    def find_optimal_k(self):
        for k in range(1, len(self.data) - 1):
            guesses = []
            for entry in range(1, len(self.data)):
                guesses.append(self.predict_by_k_neighbours(k, entry) == self.data.iloc[entry][-1])
            self.correct_guesses.append(sum(guesses))
        self.optimal_k = self.correct_guesses.index(max(self.correct_guesses))

    def predict_tea_or_coffee(self):
        entry = input('Введите через пробел высшую школу, Округ, Спорт(0/1), Цвет глаз, Время подъема, Курение(1/0)')
        entry_factorized = []
        for i, element in enumerate(entry.split()):
            entry_factorized.append(self.factorize_dict[i].index(str(element)) / len(self.factorize_dict[i]))
        entry_factorized.append(0)
        self.data.loc[len(self.data.index)] = entry_factorized
        bewerage = self.predict_by_k_neighbours(self.optimal_k, -1)
        return 'Чай' if bewerage == 0 else 'Кофе'
