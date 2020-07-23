import random
from tkinter import *
from tkinter.ttk import Radiobutton
import tkinter.scrolledtext as st
from tkinter import messagebox as mb

'''Селекции'''


# Случайная
def Random_selection(first_population):
    # список для новой популяции
    second_population = []
    for i in first_population:
        # случайно выбираем новую хромосому
        second_population.append(random.choice(first_population))
    return second_population


# Инбридинг
def Inbreeding_selection(first_population, size):
    # список для новой популяции
    second_population = []
    t = 0
    while t < size:
        # выбираем 2 случайные хромосомы
        i = random.randint(0, len(first_population) - 1)
        j = random.randint(0, len(first_population) - 1)
        # если расстояние не больше 2, добавляем их среднее значение
        if 0 < abs(i - j) <= 2:
            second_population.append(int(round((first_population[i] + first_population[j]) / 2)))
            t += 1
    return second_population


'''Кроссинговер'''


# Стандартный одноточечный кроссинговер
def Single_point_crossover(first_population, size):
    # список для новой популяции
    second_population = []
    for k in range(size):
        # место "разреза"
        сut = random.randint(0, 4)
        i = random.randint(0, size - 1)
        j = random.randint(0, size - 1)
        while j == i:
            j = random.randint(0, size - 1)
        # берем 2 РАЗНЫЕ хромосомы
        a = str(first_population[i])
        b = str(first_population[j])
        tmp1 = a[сut + 1:size]
        tmp2 = b[сut + 1:size]
        # меняем гены с места разреза местами и 2-ух хромосом
        a.replace(tmp1, tmp2)
        b.replace(tmp2, tmp1)
        # если подходят обе и есть еще 2 места, то добавляем их
        if 9 <= int(a) <= 14 and 9 <= int(b) <= 14 and k != size - 1:
            second_population.append(int(a))
            second_population.append(int(b))
            k += 1
        # если подходит одна, добавляем ее
        elif int(a) < 9 or int(a) > 14:
            second_population.append(int(b))
        elif int(b) < 9 or int(b) > 14 or k == size - 1:
            second_population.append(int(a))
        else:
            k -= 1
    return second_population


# Упорядоченный одноточечный кроссинговер
def Ordered_single_point_crossover(first_population, size):
    # список для новой популяции
    second_population = []
    for k in range(size):
        # место "разреза"
        сut = random.randint(0, 4)
        i = random.randint(0, size - 1)
        j = random.randint(0, size - 1)
        while i == j:
            j = random.randint(0, size - 1)
        # берем 2 РАЗНЫЕ хромосомы
        a = bin(first_population[i])
        b = bin(first_population[j])
        # сортируем гены после среза
        key = lambda c: (c.lower(), c.islower())
        tmp1 = ''.join(sorted(str(a)[сut + 1:size], key=key))
        tmp2 = ''.join(sorted(str(b)[сut + 1:size], key=key))
        # меняем гены с места разреза местами и 2-ух хромосом
        str(a).replace(tmp1, tmp2)
        str(b).replace(tmp2, tmp1)
        # если подходят обе, то добавляем их
        if 9 <= int(a, 2) <= 14 and 9 <= int(b, 2) <= 14 and k != size - 1:
            second_population.append(int(a, 2))
            second_population.append(int(b, 2))
            k += 1
        # если подходит одна, добавляем ее
        elif int(a, 2) < 9 or int(a, 2) > 14:
            second_population.append(int(b, 2))
        elif int(b, 2) < 9 or int(b, 2) > 14 or k == size - 1:
            second_population.append(int(a, 2))
        else:
            k -= 1
    return second_population


# Циклический
def Cyclical_crossover(first_population, size):
    # список для новой популяции
    second_population = []
    for k in range(size):
        # новый ген
        i = random.randint(0, size - 1)
        j = random.randint(0, size - 1)
        while i == j:
            j = random.randint(0, size - 1)
        # берем 2 РАЗНЫЕ хромосомы
        a = str(bin(first_population[i]))
        b = str(bin(first_population[j]))
        # заполняем первую часть новой хромосомы
        # если гены 1-ого потомка(позиции) одинаковые
        # то просто переносим первые 2 гена 2-ого
        if int(a[2]) == int(a[3]):
            new_gene1 = a[:2] + b[2:4]
        else:
            # если у 1-ой хромосомы 2 1-ых гена-'10',
            # то переносим 2 1-ых гена из 2-ого
            # в обратном порядке
            if int(a[2]) > int(a[3]):
                new_gene1 = a[:2] + b[3:1:-1]
            # иначе(01) в прямом из 2-ого
            else:
                new_gene1 = a[:2] + b[2:4]
        # с точностью наоборот для 2-ого
        if int(b[4]) == int(b[5]):
            new_gene1 += a[4:]
        else:
            if int(b[4]) > int(a[5]):
                new_gene1 += a[5:3:-1]
            else:
                new_gene1 += a[4:]
        # для 2-ой новой хромосомы аналогично
        if int(b[2]) == int(b[3]):
            new_gene2 = b[:2] + a[2:4]
        else:
            if int(b[2]) > int(b[3]):
                new_gene2 = b[:2] + a[3:1:-1]
            else:
                new_gene2 = b[:2] + a[2:4]
        if int(a[4]) == int(a[5]):
            new_gene2 += b[4:]
        else:
            if int(a[4]) > int(a[5]):
                new_gene2 += b[5:3:-1]
            else:
                new_gene2 += b[4:]
        # если он находятся в [9-14], добавляем
        if 9 <= int(new_gene1, 2) <= 14 and 9 <= int(new_gene2, 2) <= 14 and k != size - 1:
            second_population.append(int(new_gene1, 2))
            second_population.append(int(new_gene2, 2))
            k += 1
        # если подходит одна, добавляем ее
        elif int(new_gene1, 2) < 9 or int(new_gene1, 2) > 14 or (k == size - 1 and 9 <= int(new_gene2, 2) <= 14):
            second_population.append(int(new_gene2, 2))
        elif int(new_gene2, 2) < 9 or int(new_gene2, 2) > 14 or (k == size - 1 and 9 <= int(new_gene1, 2) <= 14):
            second_population.append(int(new_gene1, 2))
        else:
            k -= 1
    return second_population


# Оператор кроссинговера на основе «Золотого сечения».
def Crossover_based_on_golden_section(first_population, size):
    # список для новой популяции
    second_population = []
    for k in range(int(size / 2)):
        i = random.randint(0, size - 1)
        j = random.randint(0, size - 1)
        while i == j:
            j = random.randint(0, size - 1)
        # берем 2 РАЗНЫЕ хромосомы
        a = str(bin(first_population[i]))
        b = str(bin(first_population[j]))
        # берем нужные промежутки
        l1 = int(0.618 * 4) + 1
        l2 = int((4 - 0.618 * 4) * 0.618 * 4) + 2
        # получаем новые хромосомы
        new_gene1 = int(a[:l1] + b[l1:l2] + a[l2:], 2)
        new_gene2 = int(b[:l1] + a[l1:l2] + b[l2:], 2)
        # если они находятся в [9-14], добавляем
        if 9 <= new_gene1 <= 14 and 9 <= new_gene2 <= 14 and k != size - 1:
            second_population.append(new_gene1)
            second_population.append(new_gene2)
            k += 1
        # если подходит одна, добавляем ее
        elif new_gene1 < 9 or new_gene1 > 14 or (k == size - 1 and 9 <= new_gene2 <= 14):
            second_population.append(new_gene2)
        elif new_gene2 < 9 or new_gene2 > 14 or (k == size - 1 and 9 <= new_gene1 <= 14):
            second_population.append(new_gene1)
        else:
            k -= 1
    return second_population


'''Операторы мутации и инверсии'''


# Обмена на основе «Золотого сечения»
def Exchange_based_on_golden_section(first_population, number):
    # место разреза как 0.618 * n, где 'n' - длинна хромосомы
    cut = int(0.618 * 4) + 1
    b = True
    while b:
        a = str(bin(first_population[number]))
        # гены, стоящие после cut-ого номера, инвертируются
        c = int("0b" + a[2:cut + 2] + a[:cut + 1:-1], 2)
        # если не удовлетворяет, то изменяем места среза
        if 9 <= c <= 14:
            b = False
            first_population[number] = c
        cut += 1
    return first_population


# Инверсия
def Inversion_mutation(first_population, number, cut):
    b = True
    while b:
        a = str(bin(first_population[number]))
        # гены, стоящие после cut-ого номера, инвертируются
        c = int("0b" + a[2:cut + 2] + a[:cut + 1:-1], 2)
        # если не удовлетворяет, то изменяем места среза
        if 9 <= c <= 14:
            b = False
            first_population[number] = c
        cut += 1
    return first_population


'''Оператор отбора'''


# Элитный отбор
def Elite_selection(first_population, size):
    # сортируем список по убыванию
    first_population.sort()
    first_population.reverse()
    # список для новой популяции
    second_population = []
    for i in range(size):
        # добавляем хромосомы в новую популяцию с новым размером
        second_population.append(first_population[i])
    return second_population


'''Допольнительные функции'''


# получение списка хромосом для вывода
def toString(population):
    string = ""
    for i in population:
        string += str(bin(int(i)))[2:] + "\n"
    return string


# формирование новой популяции по двум
def New_population(first_population, second_population):
    # список для новой популяции
    third_population = []
    for i in range(len(first_population)):
        third_population.append(first_population[i])
    for i in range(len(second_population)):
        third_population.append(second_population[i])
    return third_population


# получение значения функции по данному числу
def Function(x):
    return x * x + 0.1 * x - 23


# функция выполнения алгоритма
def main_function():
    text_area.delete(1.0, END)
    answer_text.delete(0, END)
    output_str = ''
    # проверка ввода:
    # верный формат ввода чисел
    error = False
    if not population_size.get().isdigit() or not population_size.get():
        error = True
        output_str += "Введите размер популяции цифрами!!!\n"
    if int(crossover_probability.get()) != 0 and int(population_size.get()) == 1:
        error = True
        output_str += "Для популяции размера 1 вероятность кроссинговера должна быть 0%!!!\n"
    if not number_of_generations.get().isdigit() or not number_of_generations.get():
        error = True
        output_str += "Введите количество генераций цифрами!!!\n"
    # выбраны все радиокнопки
    if not initial_population_strategy_select.get():
        error = True
        output_str += "Выберите стратегию создания начальной популяции!!!\n"
    if not type_of_selection_select.get():
        error = True
        output_str += "Выберите вид селекции!!!\n"
    if int(type_of_selection_select.get()) == 2 and int(population_size.get()) == 1:
        error = True
        output_str += "Для популяции размера 1 Инбридинг невозможен!!!\n"
    if not сrossover_operator_select.get() and (int(crossover_probability.get()) != 0 and int(population_size.get()) != 1):
        error = True
        output_str += "Выберите оператор кроссинговера!!!\n"
    if not mutation_and_inversion_operators_select.get() and mutation_probability.get() != 0:
        error = True
        output_str += "Выберите оператор мутации и инверсии!!!\n"
    # если есть ошибки, выдается окно с их перечисление
    if error:
        answer = mb.showerror(title="Ошибка", message=output_str)
    # иначе выполняется алгоритм
    else:
        separator = "++++++++++++++++++++++++++++++++++++++++++++++++++"
        output_str = separator
        population = []
        # Cтратегия создания начальной популяции
        # определение стратегии создания начальной популяции
        if initial_population_strategy_select.get() == 1:
            output_str += "Стратегия одеяла: \n"
            for i in range(int(population_size.get())):
                a = int(6 / (int(population_size.get()) * 2) + 6 * i / int(population_size.get()) + 9)
                population.append(a)
        else:
            output_str += "Стратегия дробовика: \n"
            for i in range(int(population_size.get())):
                a = random.randint(9, 14)
                population.append(a)
        size_of_new_generation = int(population_size.get())
        output_str += toString(population)
        # генерации согласно условиям
        for count in range(int(number_of_generations.get())):
            output_str += separator + "\n" + str((count + 1)) + "-Я ГЕНЕРАЦИЯ \n" + separator + "\n"
            # Вид селекции
            # определение вида селекции
            if type_of_selection_select.get() == 1:
                output_str += "Случайная: \n"
                new_population = Random_selection(population)
            else:
                output_str += "Инбридинг:\n"
                new_population = Inbreeding_selection(population, size_of_new_generation)
            output_str += "Отобранные хромосомы:\n" + toString(new_population) + separator
            # Оператор кроссинговера
            # генерируем случайное число от 0 до 100
            # если оно меньше вороятноти, то выполняем
            if random.randint(0, 100) < crossover_probability.get():
                # определение оператора кроссинговера
                if сrossover_operator_select.get() == 1:
                    output_str += "Стандартный Одноточечный: \n"
                    new_population = Single_point_crossover(new_population, size_of_new_generation)
                elif сrossover_operator_select.get() == 2:
                    output_str += "Упорядочивающий одноточечный: \n"
                    new_population = Ordered_single_point_crossover(new_population, size_of_new_generation)
                elif сrossover_operator_select.get() == 3:
                    output_str += "Циклический: \n"
                    new_population = Cyclical_crossover(new_population, size_of_new_generation)
                elif сrossover_operator_select.get() == 4:
                    output_str += "Оператор кроссинговера на основе «Золотого сечения»: \n"
                    new_population = Crossover_based_on_golden_section(new_population, size_of_new_generation)
            output_str += "Популяция после кроссинговера: \n" + toString(new_population) + separator
            # Операторы мутации и инверсии
            # генерируем случайное число от 0 до 100
            # если оно меньше вороятноти, то выполняем
            if random.randint(0, 100) < mutation_probability.get():
                # выбираем хромосому, которая будет мутировать
                сhromosome = random.randint(0, len(new_population) - 1)
                # выбираем номер гена, который будет мутировать
                gene_number = random.randint(0, 2)
                # определение оператора мутации и инверсии
                if mutation_and_inversion_operators_select.get() == 1:
                    output_str += "Мутация на осонове на основе «Золотого сечения».:\n"
                    choice = str(bin(new_population[сhromosome]))
                    new_population = Exchange_based_on_golden_section(new_population, сhromosome)
                else:
                    output_str += "\n" + "Инверсия:\n"
                    new_population = Inversion_mutation(new_population, сhromosome, gene_number)
                output_str += separator + "\n" + "Выбраная хромосома до мутации: " + str(
                    bin(new_population[сhromosome]))[
                                                                                     2:] + "\n"
                output_str += "Номер мутированного гена: " + str(gene_number + 1) + "\n"
                output_str += "Выбраная хромосома после мутации: " + str(bin(new_population[сhromosome]))[
                                                                     2:] + "\n" + separator
            final_population = New_population(population, new_population)
            output_str += "Популяция после мутации: \n" + toString(final_population) + separator
            population = Elite_selection(final_population, int(population_size.get()))
            output_str += "Популяция после отбора: \n" + toString(population)
        text_area.insert(1.0, output_str)
        answer_text.insert(0, str(Function(population[0])))


# формирование окна
if __name__ == '__main__':
    window = Tk()
    window.title("ХИЖНИЙ ЕВГЕНИЙ, 21 ГРУППА, ВАРИАНТ №26")
    window.geometry('910x600')
    # Размер популяции
    label_for_population_size = Label(window, text="Размер популяции:", fg="white",
                                                         background="black")
    population_size = Entry(window, width=10)
    population_size.insert(0, 10)
    # Количество генераций
    label_for_number_of_generations = Label(window, text="Количество генераций:", fg="white", background="black")
    number_of_generations = Entry(window, width=10)
    number_of_generations.insert(0, 50)
    # Вероятность кроссинговера
    label_for_crossover_probability = Label(window, text="Вероятность кроссинговера:", fg="white", background="black")
    crossover_probability = Scale(window, orient=HORIZONTAL, length=300, from_=0, to=100, tickinterval=10, resolution=1)
    crossover_probability.set(70)
    # Вероятность мутации
    label_for_mutation_probability = Label(window, text="Вероятность мутации:", fg="white", background="black")
    mutation_probability = Scale(window, orient=HORIZONTAL, length=300, from_=0, to=100, tickinterval=10, resolution=1)
    mutation_probability.set(20)
    # Стратегия создания начальной популяции
    initial_population_strategy_select = IntVar()
    label_for_initial_population_strategy_select = Label(window, text="Стратегия создания начальной популяции:",
                                                         fg="white", background="black")
    blanket = Radiobutton(window, text='Одеяло', value=1, variable=initial_population_strategy_select)
    shotgun = Radiobutton(window, text='Дробовик', value=2, variable=initial_population_strategy_select)
    # Вид селекции
    type_of_selection_select = IntVar()
    label_for_type_of_selection_select = Label(window, text="Вид селекции:", fg="white", background="black")
    random_selection = Radiobutton(window, text='Случайная', value=1, variable=type_of_selection_select)
    inbreeding_selection = Radiobutton(window, text='Инбридинг', value=2, variable=type_of_selection_select)
    # Оператор кроссинговера
    сrossover_operator_select = IntVar()
    label_for_сrossover_operator_select = Label(window, text="Оператор кроссинговера:", fg="white", background="black")
    standard_single_point = Radiobutton(window, text='Стандартный одноточечный', value=1,
                                        variable=сrossover_operator_select)
    sequencing_single_point = Radiobutton(window, text='Упорядочивающий одноточечный', value=2,
                                          variable=сrossover_operator_select)
    cyclical = Radiobutton(window, text='Циклический', value=3, variable=сrossover_operator_select)
    crossover_based_on_the_golden_section = Radiobutton(window,
                                                        text='Оператор кроссинговера на основе «Золотого сечения»',
                                                        value=4, variable=сrossover_operator_select)
    # Операторы мутации и инверсии
    mutation_and_inversion_operators_select = IntVar()
    label_for_mutation_and_inversion_operators_select = Label(window, text="Операторы мутации и инверсии", fg="white",
                                                              background="black")
    exchange_based_on_golden_section = Radiobutton(window, text='Обмена на основе «Золотого сечения».', value=1,
                                                   variable=mutation_and_inversion_operators_select)
    inversion = Radiobutton(window, text='Инверсия', value=2, variable=mutation_and_inversion_operators_select)
    # кнопка для начала выполнения
    star = Button(window, text='Начать выполнение', command=main_function)
    # функция, промежуток
    label_for_text_area = Label(window, text="max f(x) = х^2 + 0,1*х − 23\n [9−14]", fg="white", background="black")
    # поле вывода результатов работы генетического алгоритма
    text_area = st.ScrolledText(window, font=("Times New Roman", 15,), width=55)
    # поле вывода значения функции
    label_for_answer_text = Label(window, text="Ответ", fg="white", background="black")
    answer_text = Entry(width=10)

    # размещение всех элементов в окне
    label_for_population_size.grid(column=0, row=0)
    population_size.grid(column=0, row=1)

    label_for_number_of_generations.grid(column=0, row=2)
    number_of_generations.grid(column=0, row=3)

    label_for_crossover_probability.grid(column=0, row=4)
    crossover_probability.grid(column=0, row=5)

    label_for_mutation_probability.grid(column=0, row=6)
    mutation_probability.grid(column=0, row=7)

    label_for_initial_population_strategy_select.grid(column=0, row=8)
    shotgun.grid(column=0, row=10)
    blanket.grid(column=0, row=9)

    label_for_type_of_selection_select.grid(column=0, row=11)
    random_selection.grid(column=0, row=12)
    inbreeding_selection.grid(column=0, row=13)

    label_for_сrossover_operator_select.grid(column=0, row=14)
    standard_single_point.grid(column=0, row=15)
    sequencing_single_point.grid(column=0, row=16)
    cyclical.grid(column=0, row=17)
    crossover_based_on_the_golden_section.grid(column=0, row=18)

    label_for_mutation_and_inversion_operators_select.grid(column=0, row=19)
    exchange_based_on_golden_section.grid(column=0, row=20)
    inversion.grid(column=0, row=21)

    star.grid(column=0, row=22)

    label_for_text_area.grid(column=1, columnspan=2, row=0, rowspan=2)
    text_area.grid(column=1, columnspan=2, rowspan=20, row=2)

    label_for_answer_text.grid(column=1, row=22, sticky=E)
    answer_text.grid(column=2, row=22, sticky=W)

    window.mainloop()
