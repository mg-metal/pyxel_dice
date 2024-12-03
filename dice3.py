import pyxel
import random

pyxres_name = "sample1.pyxres"
dice_dict = [
    (8*0, 128),
    (8*1, 128),
    (8*2, 128),
    (8*3, 128),
    (8*4, 128),
    (8*5, 128)
]

class Die:
    def __init__(self, x=80, y=60):
        self.init(x, y)
    
    def init(self, x, y):
        self.x = x
        self.y = y
        self.face_value = 1
        self.active = False
        self.is_roll = False 
        self.fcnt = 0
        self.frames_until_throw = 0
        self.frames_end_roll = 0
    
    def get_value(self):
        return self.face_value
    
    def prepare_to_roll(self, x, y, frames_until_throw, frames_end_roll):
        self.active = True
        self.face_value = random.randint(1, 6)
        self.x = x
        self.y = y
        self.frames_until_throw = frames_until_throw
        self.frames_end_roll = frames_end_roll
        
    def update(self):
        self.fcnt += 1
        if self.fcnt > self.frames_until_throw:
            if self.is_roll:
                self.roll()
        elif self.fcnt == self.frames_until_throw:
            self.is_roll = True
        else:
            return

    def roll(self):
        if self.fcnt % 3 == 0:
            self.face_value = pyxel.rndi(1, 6)
        if self.fcnt >= self.frames_end_roll:
            self.is_roll = False       
    
    def draw(self):
        pyxel.blt(self.x, self.y, 0,
                  dice_dict[self.face_value-1][0],
                  dice_dict[self.face_value-1][1],
                  8, 8)

class DiceSet():
    def __init__(self, max_dice):
        self.total = 0
        self.active_count = 0
        self.dice = [Die(10+i*9, 10) for i in range(max_dice)]
        
    def reset(self):
        self.active_count = 0
        for die in self.dice:
            die.init(0, 0)

    def set_active_dice_count(self, count):
        self.reset()
        if 0 < count <= len(self.dice):
            self.active_count = count
            for i in range(count):
                self.dice[i].active = True 
        else:
            raise ValueError("roll時の要求数が不適切です")

    def throw(self, count):
        self.set_active_dice_count(count)
        for die in self.dice:
            if die.active:
                x = random.randint(30, 130)
                y = random.randint(30, 90)
                die.prepare_to_roll(x, y, random.randint(5, 20), random.randint(70, 90))

    def update(self):
        self.total = 0
        for die in self.dice:
            if die.active:
                die.update()
                self.total += die.get_value()
                
    def draw(self):
        pyxel.text(86, 54, str(self.total), 3)
        for die in self.dice:
            if die.active:
                die.draw()


class App:
    def __init__(self) -> None:
        pyxel.init(160, 120)
        pyxel.mouse(True)
        pyxel.load(pyxres_name)
        self.dice = DiceSet(8)
        pyxel.run(self.update, self.draw)

    def update(self):
        # 入力
        if pyxel.btnp(pyxel.MOUSE_BUTTON_LEFT):
            self.dice.throw(6)
        
        # 更新
        self.dice.update()
        

    def draw(self):
        pyxel.cls(0)
        self.dice.draw() 

App()