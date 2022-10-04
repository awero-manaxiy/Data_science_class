from k_nearest_neighbours import DataAnalysis


if __name__ == '__main__':
    entry = input('Введите 0, если хотите найти оптимальное число соседей;\n'
                  ' 1, если хотите предсказать чай или кофе пьёт человек\n'
                  '(в случае, если до этого не считали оптимальное k, k=3)\n')
    analysis = DataAnalysis()
    if entry == '0':
        analysis.find_optimal_k()
        success_rate = 100 * round(analysis.correct_guesses[analysis.optimal_k] / len(analysis.data), 3)
        print(f'оптимальное k = {analysis.optimal_k + 1}, успешно предсказано {success_rate}%')
        print(analysis.predict_tea_or_coffee())
    else:
        print(analysis.predict_tea_or_coffee())
