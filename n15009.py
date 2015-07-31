from tkinter import *
import random
import time

def point_collision(a, b):
    cx = (b[2] - b[0]) / 2
    cy = (b[3] - b[1]) / 2
    r = cx
    #left-up
    dx = cx - a[1]
    dy = cy - a[1]
    p1 = dx**2 + dy**2 < r**2
    #right-up
    dx = cx - a[2]
    dy = cy - a [1]
    p2 = dx**2 + dy**2 < r**2
    #right-bottom
    dx = cx - a[2]
    dy = cy - a[3]
    p3 = dx**2 + dy**2 < r**2
    #left-bottom
    dx = cx - a[0]
    dy = cy - a[3]
    p4 = dx**2 + dy**2 < r**2

    return p1 or p2 or p3 or p4


class Ball:
    def __init__(self, canvas, paddle, score, blocks, speed, color):
        self.canvas = canvas
        self.paddle = paddle
        self.score = score
        self.blocks = blocks
        self.speed = speed
        self.id = canvas.create_oval(10, 10, 25, 25, fill=color)
        self.canvas.move(self.id, 245, 300)
        self.x = 0
        self.y = 0
        self.canvas_height = self.canvas.winfo_height()
        self.canvas_width = self.canvas.winfo_width()
        self.hit_bottom = False
        self.canvas.bind_all('<Button-1>', self.start)
        
        
    def hit_paddle(self, pos):
        paddle_pos = self.canvas.coords(self.paddle.id)
        if pos[2] >= paddle_pos[0] and pos[0] <= paddle_pos[2]:
            if pos[3] >= paddle_pos[1] and pos[3] <= paddle_pos[3]:
                return True
        return False

    def hit_block(self, pos):
        target_block = None
        collision_type = 0
        for block in self.blocks:
            block_pos = self.canvas.coords(block.id)
            #circle_collision check
            if point_collision(block_pos, pos):
                collision_type |= 3
            #top check
            if pos[2] >= block_pos[0] and pos[0] <= block_pos[2] \
                and pos[3] >= block_pos[1] and pos[3] < block_pos[3]:
                 collision_type |= 1
            #bottom check
            if pos[2] >= block_pos[0] and pos[0] <= block_pos[2] \
                and pos[1] > block_pos[1] and pos[1] <= block_pos[3]:
                 collision_type |= 1
            #left check
            if pos[3] >= block_pos[1] and pos[1] <= block_pos[3] \
                and pos[2] >= block_pos[0] and pos[2] < block_pos[2]:
                 collision_type |= 2
            #right check
            if pos[3] >= block_pos[1] and pos[1] <= block_pos[3] \
                and pos[0] > block_pos[0] and pos[0] <= block_pos[2]:
                 collision_type |= 2
                 
            if collision_type != 0:
                self.score.hit()
                return (block, collision_type)
        return (None, 0)
            
    def draw(self):
        self.canvas.move(self.id, self.x, self.y)
        pos = self.canvas.coords(self.id)
        if pos[1] <= 0:
            self.y *= -1
        if pos[3] >= self.canvas_height:
            self.hit_bottom = True
        if self.hit_paddle(pos) == True:
            self.y = self.y * -1
        if pos[0] <= 0:
            self.x *= -1
        if pos[2] >= self.canvas_width:
            self.x *= -1
        (target, collision_type) = self.hit_block(pos)
        if target != None:
            target.delete()
            del self.blocks[self.blocks.index(target)]
            if (collision_type & 1) != 0:
                self.y *= -1
            if (collision_type & 2) != 0:
                self.x *= -1

    def start(self, evt):
        self.x = -self.speed
        self.y = self.speed
        
class Paddle:
    def __init__(self, canvas, speed, color):
        self.canvas = canvas
        self.speed = speed
        self.id = canvas.create_rectangle(0, 0, 100, 10, fill=color)
        self.canvas.move(self.id, 200, 600)
        self.x = 0
        self.canvas_width = self.canvas.winfo_width()
        self.started = False
        self.canvas.bind_all('<KeyPress-Left>', self.turn_left)
        self.canvas.bind_all('<KeyPress-Right>', self.turn_right)
        self.canvas.bind_all('<Button-1>', self.start_game)
        
    def  draw(self):
        self.canvas.move(self.id, self.x, 0)
        pos = self.canvas.coords(self.id)
        if pos[0] <= 0:
            self.x = 0
        elif pos[2] >= self.canvas_width:
            self.x = 0
            
    def turn_left(self, evt):
        self.x = -self.speed

    def turn_right(self, evt):
        self.x = self.speed

    def start_game(self, evt):
        self.started = True

class Block:
    def __init__(self, canvas, x, y, color):
        self.canvas = canvas
        self.pos_x = x
        self.pos_y = y
        self.id = canvas.create_rectangle(0, 0, 50, 20, fill=color)
        self.canvas.move(self.id, 25 + self.pos_x * 50,
                         25 + self.pos_y * 20)

    def delete(self):
        self.canvas.delete(self.id)

class Score:
    def __init__(self, canvas, color):
        self.score = 0
        self.canvas = canvas
        self.id = canvas.create_text(900, 680, text=self.score, fill=color)

    def hit(self):
        self.score += 100767778900
        self.canvas.itemconfig(self.id, text=self.score)
        
class TextLabel:
    def __init__(self, canvas, text, x, y, fontsize=20, color='black'):
        self.canvas = canvas
        self.id = canvas.create_text(100, 600, text=text, fill=color,
                                     font=('Times', fontsize), state='hidden')

    def show(self):
        self.canvas.itemconfig(self.id, state='noraml')

    

WIDTH = 1000
HEIGHT = 700
FPS = 500
BALL_SPEED = 5
PADDLE_SPEED = 3
COLORS = ('cyan', 'green', 'gold', 'dark orange', 'magenta',)

tk = Tk()
canvas = Canvas(tk, width=1000, height=1500)
tk.title("Breakout")
tk.resizable(0, 0)
tk.wm_attributes("-topmost", 1)
canvas = Canvas(tk, width=WIDTH, height=HEIGHT,
                bd=0, highlightthickness=0)
canvas.pack()
my_image = PhotoImage(file='/home/n15009/Downloads/utyu.gif')
canvas.create_image(0, 0, anchor=NW, image=my_image)
my_image2 = PhotoImage(file='/home/n15009/Downloads/abcd.gif')
tk.update()


blocks = []
for y in range(12):
    for x in range(19):
        blocks.append(Block(canvas, x, y, random.choice(COLORS)))

score = Score(canvas, 'green')        
paddle = Paddle(canvas, PADDLE_SPEED, 'blue')
ball = Ball(canvas, paddle, score, blocks, BALL_SPEED, 'red')
game_over_text = canvas.create_text(600, 650, text='YOU ARE FU*KIN\' LOSER, GET THE HELL OUT OF HERE DUDE!!', state='hidden',
                                    fill='red', font=('Courier',20))
game_start_text = canvas.create_text(600, 650, text='GOOD LUCK!!', state='normal',
                                     fill='blue', font=('Helvetica', 40))


while True:
    if ball.hit_bottom == False:
        ball.draw()
        paddle.draw()
    if ball.hit_bottom == True:
        time.sleep(1)
        canvas.itemconfig(game_start_text, state='hidden')
        canvas.itemconfig(game_over_text, state='normal')
        canvas.create_image(5, 400, anchor=NW, image=my_image2)
        break
    
    tk.update_idletasks()
    tk.update()
    time.sleep(1/FPS)
    
