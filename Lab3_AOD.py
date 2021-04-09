from tkinter import Button, Label, DISABLED, Tk, Entry, Scrollbar, Listbox, Y, RIGHT, StringVar, END
from tkinter import messagebox as mb
import matplotlib.pyplot as plt
import networkx as nx

# Список связности для графа
graph = {'A': ['B', 'C', 'D'],
         'B': ['A', 'D', 'E'],
         'C': ['A', 'F'],
         'D': ['A', 'B'],
         'E': ['B'],
         'F': ['C', 'A']}

graph_main = {}  # Пустой словарь для списка связности графа


def iteractive_dfs(graph, start, path=None):  # Функция обхода графа в глубину
    if path is None:
        path = []
    q = [start]
    while q:
        v = q.pop()
        if v not in path:
            path = path + [v]
            q += graph[v]
    return path


class main_class:
    # Функция инициализации
    def __init__(self, window):
        self.window = window
        self.label1 = Label(window, wraplength=700, text='Перенумеруйте вершины графа в порядке обхода в глубину и '
                                                         'вычислите среднюю плотность графа как частное от деления '
                                                         'количества его ребер на число вершин. Можно ли оба эти '
                                                         'действия выполнить за один обход графа?')
        self.label_create = Label(window, text='Введите название вершины:')
        self.m = StringVar()
        self.text_box = Entry(textvariable=self.m)
        scrollbar = Scrollbar(window)
        scrollbar.pack(side=RIGHT, fill=Y)
        self.add = Button(window, text='Добавить вершину', command=self.add)
        self.choice = Label(window, text='Укажите вершины, смежные к данной:')
        self.listbox = Listbox(yscrollcommand=scrollbar.set, selectmode='multiple', width=40)
        self.listbox.insert(0, "A")
        scrollbar.config(command=self.listbox.yview)
        self.edg_vert = Button(window, text="Дабавить смежные вершины", command=self.edg_vert)
        self.button = Button(window, text="Создать граф", command=self.plot)
        self.button2 = Button(window, text='Найти среднюю плотность графа', command=self.task)
        self.button3 = Button(window, text='Обход в глубину', command=self.depth)
        self.button4 = Button(window, text='Показать обход в глубину', command=self.show_changed_nodes)
        self.label1.pack()
        self.label_create.pack()
        self.text_box.pack()
        self.add.pack()
        self.choice.pack()
        self.listbox.pack()
        self.edg_vert.pack()
        self.button.pack()
        self.button2.pack()
        self.button3.pack()

    # Функция добавления вершин в граф
    def add(self):
        if self.m.get() != 0:
            self.vertex = self.m.get()
            self.listbox.insert(END, self.m.get())
            self.text_box.delete(0, END)

    def switch(self, graph):  # Функция для создания спиская смежности
        for key in graph:  # для каждого ключа в словаре
            for i in graph:
                for q in range(0, len(graph[i])):  # Каждое значение каждого ключа
                    if graph[i][q] == key:  # сравнивается с названием ключа
                        pic = graph[
                            key]  # если совпадает, то для начала то значение что уже есть записывается в переменную
                        if i not in pic:
                            pic += i
                            graph.update({key: pic})  # Ключ графа обновляется

    # Функция добавления смыжных вершин в список смежности графа, представленный в виде словаря
    def edg_vert(self):
        key_exists = 'A' in graph_main
        if key_exists:
            self.select = self.listbox.curselection()
            reslist = list()
            for i in self.select:
                entr = self.listbox.get(i)
                reslist.append(entr)
            graph_main.update({self.vertex: reslist})
            show_graph = Label(window)
            self.switch(graph_main)
            show_graph.config(text=graph_main)
            show_graph.pack()
        else:
            graph_main.update({'A': [self.vertex]})

    def count_edges(self, graph):  # Функция подсчета количества ребер у графа
        p = 0  # Переменная для подсчета ребер
        w = 'A'  # Вершины, которые мы уже обошли
        for key in graph:
            if key == 'A':  # Подсчитываем количество ребер от вершины А
                for q in range(0, len(graph['A'])):
                    p += 1
            else:
                for r in range(0, len(graph[key])):
                    if graph[key][r] not in w: # Если такое ребро рвньше не встречалось
                        p += 1  # Добавляем его
                        w += key
        return p

    def task(self):  # Функция нахождения средней плотности графа
        self.label2 = Label(window)
        if len(g.nodes) == 0 or len(g.edges()) == 0:
            self.label2.config(state=DISABLED)
            mb.showerror("Ошибка", "Граф не создан")
        else:
            avgVol = self.count_edges(graph_main) / len(graph_main)  # средняя плотность графа
            self.label2['text'] = ('Средняя плотность графа: ' + str(self.count_edges(graph_main)) +
                                   ' / ' + str(len(graph_main)) + ' = ' + str(avgVol))
            self.label2.pack()
            self.button2.config(state=DISABLED)

    def depth(self):  # Вывод обхода графа на окно
        self.label3 = Label(window)
        if len(g.nodes) == 0 or len(g.edges()) == 0:
            self.label3.config(state=DISABLED)
            mb.showerror("Ошибка", "Граф не создан")
        else:
            obhod = iteractive_dfs(graph_main, 'A')
            self.label3['text'] = ('Обход в глубину: ' + str(obhod))
            self.label3.pack()
            self.button3.config(state=DISABLED)
            self.button.config(state=DISABLED)
            self.button4.pack()

    def show_changed_nodes(self):  # Функция создания анимации обхода графа
        path = iteractive_dfs(graph_main, 'A')  # список, содержащий значения в порядке обхода
        dict = {}  # Создаем пустой словарь
        a = 1
        for i in path:  # Присваиваем цифры буквам
            dict.update({i: a})
            a += 1
        nx.relabel_nodes(g, dict, copy=False)
        nx.draw_networkx(g)
        plt.title(dict)
        plt.show()

    def plot(self):  # Функция создания графа
        for key in graph_main:  # Создаем вершины
            g.add_node(key)
            for key2 in graph_main[key]:
                # Для каждой связи в матрице создаем ребро
                g.add_edge(key, key2)
        plt.axis('off')  # Убираем оси
        nx.draw_networkx(g)  # Рисуем граф
        plt.show()


# При помощи библиотеки nx создаем граф
g = nx.Graph()
window = Tk()
window.title("Лабораторная работа 3")
start = main_class(window)
window.mainloop()
