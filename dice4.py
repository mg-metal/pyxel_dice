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
    def __init__(self):
        self.init()
    
    def init(self):
        self.x = 0
        self.y = 0
        self.vx = 0
        self.vy = 0
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
        self.vx = -1.0 + random.random() * 2
        self.vy = -4.0 * random.random() - 2.0
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
        self.x += self.vx
        self.y += self.vy
        self.vy += 0.25
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
        self.dice = [Die() for i in range(max_dice)]
        
    def reset(self):
        self.active_count = 0
        for die in self.dice:
            die.init()

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
                x = random.randint(60, 80)
                y = 70
                die.prepare_to_roll(x, y, random.randint(5, 20), random.randint(45, 60))

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
            self.dice.throw(8)
        
        # 更新
        self.dice.update()
        

    def draw(self):
        pyxel.cls(0)
        self.dice.draw() 

App()