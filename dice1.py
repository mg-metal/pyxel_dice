import pyxel

pyxres_name = "sample1.pyxres"
dice_dict = [
    (8*0, 128),
    (8*1, 128),
    (8*2, 128),
    (8*3, 128),
    (8*4, 128),
    (8*5, 128)
]

class Dice:
    def __init__(self):
        self.init(80, 60)
    
    def init(self, x, y):
        self.x = x
        self.y = y
        self.face_value = 1
        self.visible = True
        self.is_roll = False 
        self.fcnt = 0
    
    def throw(self):
        self.is_roll = True
        
    def update(self):
        if self.is_roll:
            self.roll()

    def roll(self):
        self.fcnt += 1
        if self.fcnt % 3 == 0:
            self.face_value = pyxel.rndi(1, 6)
        if self.fcnt == 45:
            self.fcnt = 0
            self.is_roll = False       
    
    def draw(self):
        if self.visible:
            pyxel.blt(self.x, self.y, 0,
                      dice_dict[self.face_value-1][0],
                      dice_dict[self.face_value-1][1],
                      8, 8)

class App:
    def __init__(self) -> None:
        pyxel.init(160, 120)
        pyxel.mouse(True)
        pyxel.load(pyxres_name)
        self.dice = Dice()
        pyxel.run(self.update, self.draw)

    def update(self):
        # 入力
        if pyxel.btnp(pyxel.MOUSE_BUTTON_LEFT):
            self.dice.throw()
        
        # 更新
        self.dice.update()

    def draw(self):
        pyxel.cls(0)
        self.dice.draw()   

App()