"""
Puzzle game created by REI_F. 
Features:
* Sprites customization
* Automatic animation when game over
* Optimized for Ubuntu run
Last version: 1.0
Released: 05/05/2026
"""

import tkinter as tk
from tkinter import ttk, messagebox
import random
import re
import math

from config import ASSETS as assets # TODO: Background sprites are not used because there is no background rendering implementation. This needs to be fixed
"""
Game field sprites: enabled - [0][i], disabled - [1][i], backgrounds - [2][i] (not used), auxiliary textures - [3][i]
"""

class Startscreen: 
    """Implementation of the game's start screen."""

    def __init__(self, master, assets):
        """
        A constructor method for initializing the parameters of a class object and creating the startscreen window.
         
        During the work, there are the window name, resolution, and scaling parameters will be set, 
        as well as created and placed interface elements, such as a combo box for selecting the game field resolution and START and FINISH buttons.
        Parameters: 
            assets: a list of paths to game sprites, required for subsequent transfer to the Game child class
            master : the source of the created window, which will be transferred to the Game master child class

        return: Nothing
        rtype: None
        """

        self.master = master
        self.assets = assets
        self.master.title("Light \'em up!")
        self.master.geometry("300x300")
        self.master.resizable(False, False)

        size = ["4", "5", "6", "7", "8", "9", "10"] # Возможные варианты разрешения игрового поля: от 4х4 до 10х10
        self.cmb = ttk.Combobox(master, values=size, state="readonly") # Комбобокс - обьект-список с неизменяемыми вариантами выбора
        self.cmb.set("Gameboard size") 
        self.cmb.pack(pady=20) 

        start = tk.Button(master, text="START", width=10, height=2, command=self.board_size_calc) # Кнопка старта - при нажатии вызывает функцию (1)
        start.place(x=40, y=50)

        finish = tk.Button(master, text="FINISH", width=10, height=2, command=self.finish) # Кнопка выхода из игры - вызывает функцию (2) после клика
        finish.place(x=180, y=50)

        self.master.mainloop() # запуск цикла обработки событий окна - необходимо для взаимодействия
    
    def board_size_calc(self): # (1) - функция расчета величины окна
        """
        Calculating the resolution of the game field using the value selected by the user on the start screen.
        If no value is selected, 4 is automatically set as the lowest value.

        rtype: None
        """

        try:
            self.size = int(self.cmb.get()) # Размер поля выбран из списка
        except:
            self.size = 4 # Если не выбран - автоматически выбирается наименьший
        self.window = 630
        while self.window % self.size != 0:
            self.window += 1
        self.start()

    def start(self): # функция начала игры
        """
        Destroying the startscreen window, creating the game window, and launching the game. 
        Activated when the START button is clicked
        """

        self.master.destroy() # уничтожаем стартскрин
        root = tk.Tk() # создание нового окна - обьекта класса Tk
        Game(root, self.size, self.window, self.assets)

    def finish(self): # функция выхода из игры
        """
        Destroying the startscreen window.
        Activated when the FINISH button is clicked
        """

        self.master.destroy()

class Game: # Реализация игрового окна
    """Implementation of the gameboard."""

    def __init__(self, master, blockCnt, winSize, assets):
        """
        A constructor method for initializing the parameters of a class object and creating the gameboard window.
         
        During the work, there are the window name, resolution, and scaling parameters will be set, 
        as well as created and placed interface elements, such as a combo box for selecting the game field resolution and START and FINISH buttons.
        Parameters (were transferred from the Startscreen parent class): 
        master : the source of the created window
        blocknt: expansion of the gameboard
        winSize: expansion of the whole game window
        assets: a list of paths to game sprites, required for subsequent

        return: Nothing
        rtype: None
        """

        self.master = master
        self.blockcnt = blockCnt # кол-во блоков, выбранное на стартскрине
        self.winsize = winSize # разрешение окна
        self.asset_list = assets
        
        self.PID = None # PID - The ID of the current process,
                        # is required for correct checking of self.rungame
                        # and processing of functions that depend on this status
        self.rungame = True # rungame - current game status: in progress (True) or completed (False)
        
        self.arr_cell = []
        """
        arr_cell - "code-status" list
        DEFINITION:
        code-status - block sprite ID, depending on its type (linear/angular) and current rotation

        STRUCTURE:
        [0] - block rt code status, 
        [1] - block code status in Hamiltonian traversal, 
        [2] - block position in H/T
        """

        self.master.title('Light \'em up!')
        wd, hg = winSize + 80, winSize + 150
        self.master.geometry(f'{wd}x{hg}')
        self.master.resizable(False, False)
        
        self.blocksize = winSize // blockCnt
        """
        Calculation of the game field block sprite resolution,
        depending on the selected field size, the sprites will be scaled
        """

        global_board = tk.Frame(self.master)
        """
        Splitting the game field window into frames:
        GLOBAL_BOARD - The main frame occupies the entire window,
        is necessary for the subsequent placement of the gameboard components
        UI_FRAME - the interface frame, it will be placed at the top of the window
        GAME_BOARD - the gameboard field frame, it will take up the rest of the window
        """

        global_board.pack(fill=tk.BOTH, expand=True)

        self.UI_frame = tk.Frame(global_board)
        self.UI_frame.pack(fill='x', padx=10)

        self.game_board = tk.Frame(global_board)
        self.game_board.pack(pady=10)

        self.labyrinth() # построение лабиринта
        self.remix() # перемешивание труб

        self.draw() # отрисовка поля

        self.time_var = tk.StringVar()
        self.time_var.set("TIMER: 0")
        self.timer = 0
        self.timer_v2() # запуск таймера

        self.master.update() # обновление всего окна
        self.master.mainloop()

    def timer_v2(self):
        """
        timer_v2 - creating an interface and starting a timer

        The interface frame is also divided into two frames: 
        one for the timer and one for the buttons.
        Local variables:
        rem_time - The time allocated to the player for solving the puzzle 
        depends on the number of blocks selected on the game board.
        """

        self.rem_time = 2 * self.blockcnt + 1
        
        left_frame = tk.Frame(self.UI_frame)
        left_frame.pack(side="left", fill="both", expand=True)
    
        timer = tk.Label(left_frame, textvariable=self.time_var, font=("Arial", 12)) 
        timer.pack()
    
        self.progress = ttk.Progressbar(left_frame, orient="horizontal", length=self.rem_time, value=self.rem_time, mode="determinate")
        self.progress.pack(pady=5, fill='x')
    
        right_frame = tk.Frame(self.UI_frame)
        right_frame.pack(side="right", padx=10)
    
        btn_accept = tk.Button(right_frame, text='New Game', width=10, height=3, command=self.new_game)
        btn_accept.pack(side="left", padx=5, pady=10)
    
        btn_quit = tk.Button(right_frame, text='Quit', width=10, height=3, command=self.quit)
        btn_quit.pack(side="left", padx=5, pady=10)
        
        self.update_timer()

    def update_timer(self):
        """
        Updating the timer value and animating the progress bar

        if self.rungame is False, it will not start.
        Every 1000 ms, it updates the timer value by reducing the self.rem_time by one with each iteration
        """

        if not self.rungame:
            return
        
        if self.rem_time > 0:
            self.time_var.set("TIMER: " + str(self.rem_time))
            self.progress['value'] = self.rem_time - 1
            self.rem_time -= 1
            self.PID = self.master.after(1000, self.update_timer)
        else:
            self.stop_timer()
            self.game_over()
    
    def stop_timer(self):
        """
        Checking self.PID and self.progress 
        and stopping the progressbar correctly
        """
        if self.PID:
            try:
                self.master.after_cancel(self.PID)
                self.PID = None
            except:
                pass
        if hasattr(self, 'progress') and self.progress:
            try:
                self.progress.stop()
            except:
                pass
    
    def draw(self): 
        """
        Layer-by-layer rendering of gameboard blocks and binding the button fucntion after click
        The structure of the sprite block of the gameboard:
        Frame object -> Canvas object -> background sprite -> pipe sprite
        """

        self.squares = [] # список отрисованных клеток
        block_size = self.blocksize

        for i in range(self.blockcnt):
            row = []
            for j in range(self.blockcnt):
                frame = tk.Frame(self.game_board, height=block_size, width=block_size) # создание фрейма для игрового обьекта - блока
                frame.grid(row=i, column=j, padx=1, pady=1) # размещение
                frame.grid_propagate(False) # фрейм игнорирует размеры дочерних эл-тов и сохраняет заданные размеры

                block = tk.Canvas(frame, height=block_size, width=block_size) # создание шаблона для блока в созданном фрейме
                block.pack(fill=tk.BOTH, expand=True) # размещение шаблона по всей площади фрейма

                block.row = i # сохранение индексов строки и столбца текущего блока в матрице посещений 
                block.column = j

                try: # отрисовка фона блока
                    bg = tk.PhotoImage(file=self.asset_list[3][0])
                    block.bg = bg 
                    block.create_image(block_size//2, block_size//2, image=bg)
                except Exception as e: # при ошибке загрузки спрайта - рисуем заглушку
                    print(f"Background download failed: {e}")
                    block.create_rectangle(0, 0, block_size, block_size, fill="lightgray")

                # определение типа трубы на блоке
                idb = i * self.blockcnt + j
                type = self.arr_cell[idb][0]

                try: # отрисовка спрайта трубы
                    sprite = tk.PhotoImage(file=self.asset_list[1][type-1])
                    block.sprite = sprite
                    block.create_image(block_size//2, block_size//2, image=sprite, tags="sprite")
                except Exception as e:
                    print(f"Sprite download failed: {e}")
                
                block.bind("<Button-1>", self.click) # бинд блока под выполнение функции обработки клика при нажатии на блок
                row.append(block)
            self.squares.append(row)
        self.game_board.update()
        
    def click(self, event):
        """Transition function required for correct handling of widget clicks"""

        canvas = event.widget
        self.rotate(canvas.row, canvas.column)

    def rotate(self, x, y):
        """Rotating the pipe sprite in the block after click"""

        idb = x * self.blockcnt + y
        type = self.arr_cell[idb][0]

        rot_map = {1:2, 2:1, 3:4, 4:5, 5:6, 6:3}
        rt_type = rot_map[type]
        
        self.arr_cell[idb][0] = rt_type
        self.block_update(x, y, 'update')
        self.highlight()
    
    def block_update(self, x, y, mode):
        """
        Block sprite update: removing the previous object and drawing a new sprite in one of the modes
        Update modes:
        UPDATE - Drawing a new sprite after interacting with a block
        HIGHLIGHT - highlighting a sprite after connecting it to another highlighted one
        ENDGAME - Replacing the block sprite with the "correct" version from the Hamilton traversal, 
        which is needed for animating the field after a time over
        """

        block = self.squares[x][y]
        block.delete("sprite")
        idb = x * self.blockcnt + y

        match mode:
            case 'update':
                type = self.arr_cell[idb][0]
                sprite_index = self.asset_list[1]
            case 'highlight':
                type = self.arr_cell[idb][0]
                sprite_index = self.asset_list[0]
            case 'endgame':
                type = self.arr_cell[idb][1]
                if type in [3,4,5,6]:
                    type = {3:4, 4:5, 5:6, 6:3}.get(type, type)
                sprite_index = self.asset_list[0]
        try:
            sprite = tk.PhotoImage(file=sprite_index[type-1])
            block.sprite = sprite
            block.create_image(self.blocksize//2, self.blocksize//2, image=sprite, tags="sprite")
        except Exception as e:
            print(f"Sprite download failed: {e}")

    def highlight(self):
        """Implementation of lighting for the game field blocks when connected correctly"""

        for i in range(self.blockcnt):
            for j in range(self.blockcnt):
                self.block_update(i, j, 'update')
        
        vis_lst = [False] * (self.blockcnt * self.blockcnt)
        path = []
        self.build_path(0, vis_lst, path)

        for i in path:
            x = i // self.blockcnt
            y = i % self.blockcnt
            self.block_update(x, y, 'highlight')

        if len(path) == self.blockcnt * self.blockcnt:
            self.win()

    def build_path(self, index, vis_list, path_list):
        """Converting the coordinates of the vertices of a Hamiltonian graph into blocks of a game board"""

        def connect_check(inp, out, dir):
            con_vars = {1: {'lt', 'rt'}, 2: {'up', 'dn'},
                        3: {'up', 'lt'}, 4: {'dn', 'lt'},
                        5: {'dn', 'rt'}, 6: {'up', 'rt'}}
            opps = {'up': 'dn', 'dn': 'up', 'rt': 'lt', 'lt': 'rt'}
            return (dir in con_vars[inp] and opps[dir] in con_vars[out])
        
        vis_list[index] = True
        path_list.append(index)

        block_type = self.arr_cell[index][0]
        x, y = divmod(index, self.blockcnt)
        dirs = [
            ('up', x > 0, -self.blockcnt),
            ('dn', x < self.blockcnt - 1, self.blockcnt), 
            ('lt', y > 0, -1), 
            ('rt', y < self.blockcnt - 1, 1)
        ]

        for dir, coord, delta in dirs:
            if coord:
                nextblock = index + delta
                if not vis_list[nextblock]:
                    if connect_check(block_type, self.arr_cell[nextblock][0], dir):
                        self.build_path(nextblock, vis_list, path_list)
                        return
        
    def show(self):
        """Locking the game board and preparing the puzzle solution animation"""

        self.gameboard_lock()

        self.save = []
        for i in range(self.blockcnt):
            for j in range(self.blockcnt):
                idb = i * self.blockcnt + j
                self.save.append(self.arr_cell[idb][0])
        
        self.animate(0)
    
    def animate(self, step):
        """Animation of the puzzle solution and display of the timeout message"""

        size = self.blockcnt **2
        if step < size:
            i = step // self.blockcnt
            j = step % self.blockcnt
            idb = step
            self.arr_cell[idb][0] = self.arr_cell[idb][1]
            self.block_update(i, j, 'endgame')
            self.master.after(50, lambda: self.animate(step+1)) # lambda - анонимная функция, вызываемая через 50 мс после предыдущего вызовыа
        else:
            self.rungame = False
            result = tk.messagebox.askyesno("Time Over!", "Would you like to start the new game?")
            if result:
                self.new_game()
            else:
                self.quit()
    
    def labyrinth(self): 
        """
        Converting vertex coordinates to specific types of game board blocks.
        Intermediate function between hamilton_gen() and build_path()
        """

        sz, i = self.blockcnt, 0
        path = self.hamilton_gen() # Получение сгенерированного пути
                                   # По пути строим матрицу пути
        while i < sz*sz: # Проход по всем клеткам поля
            self.arr_cell.append([0,0,0])
            i+=1
        for i, (x, y) in enumerate(path[:-1]): # Цикл по шагам пути с расстановкой плиток
            xy = x * sz + y
            if i == 0: # Стартовый блок - всегда линейная труба
                if path[i+1][0] > 0: # Вертикальная труба
                    self.arr_cell[xy][0] = self.arr_cell[xy][1] = 2
                else: # Горизонтальная труба
                    self.arr_cell[xy][0] = self.arr_cell[xy][1] = 1
            else:   # Промежуточные блоки по положению соседних
                dx1 = path[i-1][0] - path[i][0] # x предыдущего
                dx2 = path[i][0] - path[i+1][0] # x следующего
                dy1 = path[i-1][1] - path[i][1] # y предыдущего
                dy2 = path[i][1] - path[i+1][1] # y следующего
                if abs(dx1 + dx2) == 2:
                    self.arr_cell[xy][0] = self.arr_cell[xy][1] = 2
                if abs(dy1 + dy2) == 2:
                    self.arr_cell[xy][0] = self.arr_cell[xy][1] = 1   
                if (dx1 == -1 and dy2 == -1) or (dx2 == 1 and dy1 == 1):
                    self.arr_cell[xy][0] = self.arr_cell[xy][1] = 5   
                if (dx1 == -1 and dy2 == 1) or (dx2 == 1 and dy1 == -1):
                    self.arr_cell[xy][0] = self.arr_cell[xy][1] = 6      
                if (dx1 == 1 and dy2 == -1) or (dx2 == -1 and dy1 == 1):
                    self.arr_cell[xy][0] = self.arr_cell[xy][1] = 4   
                if (dx1 == 1 and dy2 == 1) or (dx2 == -1 and dy1 == -1):
                    self.arr_cell[xy][0] = self.arr_cell[xy][1] = 3 
        dx1 = path[sz*sz-2][0] - path[sz*sz-1][0] #Конечная линия
        if dx1 != 0:
            self.arr_cell[path[sz*sz-1][0]*sz+path[sz*sz-1][1]][0] = self.arr_cell[path[sz*sz-1][0]*sz+path[sz*sz-1][1]][1] = 2
        else:
            self.arr_cell[path[sz*sz-1][0]*sz+path[sz*sz-1][1]][0] = self.arr_cell[path[sz*sz-1][0]*sz+path[sz*sz-1][1]][1] = 1 
        return            
    
    def remix(self):
        """Shuffling the game field blocks in a pseudo-random order"""

        su=[3,4,5,6]
        sv=[1,2]
        for cell in self.arr_cell:
            if cell[0] in su:
                cell[0]= random.choice(su)
            if cell[0] in sv:
                cell[0]= random.choice(sv)
        return
    
    def hamilton_gen(self):
        """Building a Hamilton path as an array of coordinates"""

        def vars(x, y, vis_list): # обработка возможного хода
            ans = []
            ways = [(0, 1), (1, 0), (0, -1), (-1, 0)] 
            for mx, my in ways:
                px, py = x + mx, y + my
                if (0 <= px < sz) and (0 <= py < sz) and not vis_list[px][py]:
                    ans.append((px, py))
            return ans
        
        sz = self.blockcnt
        for _ in range(1000000):
            vis = [[False for i in range(sz)] for k in range(sz)] # матрица всех клеток на поле - до начала обхода False
            path = [] # путь - в конце кол-во эл-тов должно быть равно sz**2
            x, y = 0, 0  # Начальные коорд.
            for _ in range(sz * sz): #проход по всем эл-там матрицы block_cnt порядка
                vis[x][y] = True # отметка текущей клетки как посещённой
                path.append((x, y)) # добавление пройденной клетки в путь
                var = vars(x, y, vis) # проверка возможности следующего хода
                if not var and len(path) < sz * sz: # not var => не осталось возможных ходов, но не все клетки пройдены
                    break
                if var: # если ходы остались - выбор хода
                    if sz<=7: 
                        x, y = random.choice(var) # для маленьких полей - рандом, разнообразие маршрутов и допустимая случайность
                    else:
                        x = var[0][0] # для больших - жадный отбор, оптимизация поиска
                        y = var[0][1]
            if len(path) == sz * sz: # все клетки пройдены
                return path
        return None
    
    def quit(self):
        """Ending the game, stopping the timer and destroying the gameboard window"""

        self.rungame = False
        self.stop_timer()
        try:
            self.master.destroy()
        except:
            pass

    def gameboard_lock(self):
        """Locking the game board before the puzzle solution animation"""

        for i in range(self.blockcnt):
            for j in range(self.blockcnt):
                try:
                    self.squares[i][j].unbind("<Button-1>")
                except:
                    pass
    
    def win(self):
        """Ending the game with the game field locked, the timer stopped, and a message about winning"""

        if not self.rungame:
            return
        
        self.rungame = False
        self.stop_timer()
        self.gameboard_lock()
        
        result = tk.messagebox.askyesno("You win!", "Congradulations! Wanna start again?")
        if result:
            self.new_game()
        else:
            self.quit()
    
    def new_game(self):
        """Ending the current game session, stopping the timer, destroying the game board window, and starting a new game"""

        self.rungame = False
        self.stop_timer()
        try:
            self.master.destroy()
        except:
            pass

        root = tk.Tk()
        Startscreen(root, self.asset_list)

    def game_over(self):
        """A transition function that ends the game when defeated and triggers the defeat scenario"""
        
        if not self.rungame:
            return
        
        self.show()

# __name__ - служебная переменная, хранящая имя модуля
if __name__ == "__main__": # проверка ручного запуска модуля
    root = tk.Tk() # создание коренного обьекта - пустого окна стартскрина
    app = Startscreen(root, assets)
    root.mainloop() # запуск цикла обработки взаимодействий с окном