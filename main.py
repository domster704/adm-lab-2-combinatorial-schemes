# Лабораторная работа №2: Исупов Григорий, Рид Екатерина
# Python 3.12.1
from __future__ import annotations

import functools
import random
from typing import Callable

type TaskDict = dict[int, list[Task]]


class CustomSolutions:
    """
    Класс, содержащий решение определенных задач в виде статических методов.
    """

    @staticmethod
    def findNumberAllFiveDigitNumbers(combinations_with_repetitions_rule: Callable) -> None:
        """
        Решение задачи: Найти количество всех пятизначных чисел?
        :param combinations_with_repetitions_rule - правило `размещение с повторениями`
        """
        first_possible_count_of_combinations: int = 9
        other_possible_count_of_combinations: int = 10
        answer: int = first_possible_count_of_combinations * combinations_with_repetitions_rule(
            other_possible_count_of_combinations, 4)
        print(f"Ответ: {answer}\n")

    @staticmethod
    def howManyDifferentPermutationsAreThere(permutation_rule: Callable) -> None:
        """
        Решение задачи: Сколько существует различных перестановок из букв слова m?
        :param permutation_rule - правило `перестановки с повторениями`
        """
        word = input(f"Введите слово m: ")
        letters_count: list[int] = [word.count(i) for i in set(word)]
        print(f"Ответ: {permutation_rule(*letters_count)}\n")


class CombinatorialSchemes(object):
    """
    Класс, содержащий комбинаторные схемы для решения задач.
    """

    def __sumRule(self, *operands: list[int]) -> int:
        """
        Правило суммы.
        :param operands - массив переменных, которые будут использованы для суммирования.
        :return результат суммирования.
        """
        return sum(operands)

    def __multiplyRule(self, *operands: list[int]) -> int:
        """
        Правило произведения.
        :param operands - массив переменных, которые будут использованы для произведения.
        :return результат произведения.
        """
        return functools.reduce(lambda x, y: x * y, operands, 1)

    def __placementsWithRepetitions(self, n: int, k: int) -> int:
        """
        Правило размещения с повторениями.
        :param n - количество элементов.
        :param k - количество выборок.
        :return количество возможных выборок.
        """
        return n ** k

    def __placementsWithoutRepetitions(self, n: int, k: int) -> int:
        """
        Правило размещения без повторений.
        :param n - количество элементов.
        :param k - количество выборок.
        :return количество возможных выборок.
        """
        if n < k:
            n, k = k, n
        res = n
        for i in range(n - 1, n - k, -1):
            res *= i
        return res

    def __combinationsWithRepetitions(self, n: int, k: int) -> float | int:
        """
        Правило сочетания с повторениями.
        :param n - количество элементов.
        :param k - количество выборок.
        :return количество возможных сочетаний.
        """
        return self.__combinationsWithoutRepetitions(n - 1, n + k - 1)

    def __combinationsWithoutRepetitions(self, n: int, k: int) -> float | int:
        """
        Правило сочетания без повторений.
        :param n - количество элементов.
        :param k - количество выборок.
        :return количество возможных сочетаний.
        """
        res = self.__placementsWithoutRepetitions(n, k) / self.__permutationsWithoutRepetitions(n)
        if int(res) == res:
            return int(res)
        return res

    def __permutationsWithRepetitions(self, *operands: list[int]) -> float | int:
        """
        Правило перестановок с повторениями.
        :param operands - массив переменных, которые будут использованы для подсчета.
        :return количество возможных перестановок.
        """

        res = self.__permutationsWithoutRepetitions(sum(operands))
        for i in operands:
            res /= self.__permutationsWithoutRepetitions(i)

        if int(res) == res:
            return int(res)
        return res

    def __permutationsWithoutRepetitions(self, n: int) -> int:
        """
        Правило перестановок без повторений.
        :param n - количество элементов.
        :return - количество возможных перестановок.
        """
        return self.__placementsWithoutRepetitions(n, n)

    def choseScheme(self, scheme_id: int) -> Callable:
        """
        Выбор нужной схемы по id.
        :param scheme_id - id схемы.
        :return - правило в виде callback функции.
        """
        match scheme_id:
            case 1:
                return self.__sumRule
            case 2:
                return self.__multiplyRule
            case 3:
                return self.__placementsWithRepetitions
            case 4:
                return self.__placementsWithoutRepetitions
            case 5:
                return self.__combinationsWithRepetitions
            case 6:
                return self.__combinationsWithoutRepetitions
            case 7:
                return self.__permutationsWithRepetitions
            case 8:
                return self.__permutationsWithoutRepetitions
            case _:
                return lambda: None


class Task(object):
    """
    Класс для описания задачи.
    """

    def __init__(self, scheme_id: int, variables_count: int, solution_custom: Callable = None):
        self.variables_count = variables_count  # количество переменных, необходимых для решения задачи
        self.scheme_id: int = scheme_id  # id схемы для правила
        self.description: str = ""  # описание задачи

        self.custom_solution: Callable = solution_custom  # пользовательский (нестандартный) вариант решения задачи

    def setDescription(self, description: str) -> Task:
        """
        Установка описания задачи.
        :param description - описание задачи.
        :return - объект этой же задачи (то есть возврат ссылки на себя).
        """

        self.description = description.strip()
        return self

    def solution(self) -> None:
        """
        Стандартное решение задачи посредством использования правила для вводимых переменных.
        """
        combinatorial_scheme = CombinatorialSchemes()
        callback_rule: Callable = combinatorial_scheme.choseScheme(self.scheme_id)
        print("-" * 30)
        print(self.description)
        print("-" * 30)

        # если пользовательский вариант решения задачи задан, то вызываем его.
        if self.custom_solution is not None:
            self.custom_solution(callback_rule)
            return

        inputted_variables: list[int] = []
        print("Введите переменные в том порядке, в котором они описаны в задаче")
        for i in range(self.variables_count):
            inputted_variables.append(int(input(f"Введите значение переменной {i + 1}: ")))

        print(f"Ответ: {callback_rule(*inputted_variables)}\n")


class NavigationBash(object):
    """
    Класс для взаимодействия с пользователем. Осуществляет ввод и вывод данных. Ввод данных осуществляется с помощью
    функции input().
    """

    def __init__(self, task_dictionary: TaskDict):
        self.task_dictionary = task_dictionary

    def __str__(self) -> str:
        """
        Вывод списка правил.
        :return - список правил в виде строки.
        """
        return ("########################################################\n"
                "1. Правила суммы\n"
                "2. Правила произведения\n"
                "3. Размещения с повторениями\n"
                "4. Размещения без повторений\n"
                "5. Сочетания с повторениями\n"
                "6. Сочетания без повторений\n"
                "7. Перестановки с повторениями\n"
                "8. Перестановки без повторений\n"
                "0. Выход\n"
                "########################################################\n")

    def input(self, prompt: int):
        """
        Ввод данных.
        :param prompt - id схемы правила.
        """
        random_task_by_scheme_id: Task = random.choice(
            list(self.task_dictionary[prompt]))  # задача выбирается случайным образом.
        random_task_by_scheme_id.solution()


if __name__ == '__main__':
    # Словарь с задачами, распределенными по схемам. Ключ - id схемы, значение - список задач.
    task_dictionary: TaskDict = {
        # Правило суммы
        1: [Task(1, 2).setDescription("В классе учится n мальчиков и m девочек. \n"
                                      "Сколькими способами можно назначить одного дежурного?"),
            Task(1, 3).setDescription("На полке стоят n томов Пушкина, m тома Лермонтова и k томов Гоголя. "
                                      "Сколькими способами можно выбрать с полки одну книгу?")],
        # Правило произведения
        2: [Task(2, 3).setDescription("В магазине есть n видов пиджаков, m видов брюк и k видов галстуков. Сколькими "
                                      "способами можно купить комплект из пиджака, брюк и галстука"),
            Task(2, 2).setDescription("Найти число маршрутов из пункта M в пункт N через пункт K. Из M в K ведут n "
                                      "дорог, из K в N — m дорог.")],
        # Размещения с повторениями
        3: [Task(3, 2, CustomSolutions.findNumberAllFiveDigitNumbers).setDescription("Найти количество всех "
                                                                                     "пятизначных чисел"),
            Task(3, 2).setDescription("Сколько n - значных чисел можно составить из k - цифр?")],
        # Размещения без повторений
        4: [Task(4, 2).setDescription("В хоккейном турнире участвуют n команд. Разыгрываются k видов медалей. "
                                      "Сколькими способами могут быть распределены медали?")],
        # Сочетания с повторениями
        5: [Task(5, 2).setDescription("n ребят собрали в саду m яблок. Сколькими способами они могут их "
                                      "разделить между собой?")],
        # Сочетания без повторений
        6: [Task(6, 2).setDescription("Необходимо выбрать в подарок n из m имеющихся различных книг. Сколькими "
                                      "способами можно это сделать?")],
        # Перестановки с повторениями
        7: [Task(7, 1, CustomSolutions.howManyDifferentPermutationsAreThere).setDescription("Сколько существует "
                                                                                            "различных перестановок "
                                                                                            "из букв слова m?")],
        # Перестановки без повторений
        8: [Task(8, 1).setDescription("Компания из n друзей вызвала такси-минивэн на семь пассажирских мест. "
                                      "Сколькими способами они могут разместиться внутри машины?")]
    }

    navigation_bash = NavigationBash(task_dictionary)
    chosen_scheme_id = -1
    # Главный цикл для ввода и вывода результатов пользовательского запроса.
    while True:
        print(navigation_bash.__str__())
        chosen_scheme_id = int(input("Введите номер схемы: "))
        if chosen_scheme_id == 0:
            break

        navigation_bash.input(chosen_scheme_id)
        input("Продолжить? (enter): ")
