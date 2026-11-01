from graphics import *
import keyboard
import math
import asyncio

WIN_HEIGHT, WIN_WIDTH = 750, 750
win = GraphWin("windowow", WIN_HEIGHT, WIN_WIDTH)
win.setBackground('black') 
FPS = 60
class GameObject:
    total_objects = 0
    def __init__(self, x, y, width = 0, height = 0):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        points_tl_br = (Point(x-width/2, y-height/2), Point(x+width/2, y+height/2))
        self.shape = Rectangle(points_tl_br[0], points_tl_br[1])
        self.shape.draw(win)
        GameObject.total_objects+=1
    def collides_with(self, other):
        self_xmin = self.x - self.width/2
        self_xmax = self.x + self.width / 2
        self_ymin = self.y - self.height / 2
        self_ymax = self.y + self.height / 2

        other_xmin = other.x - other.width / 2
        other_xmax = other.x + other.width / 2
        other_ymin = other.y - other.height / 2
        other_ymax = other.y + other.height / 2

        return (self_xmin < other_xmax and self_xmax > other_xmin and
                self_ymin < other_ymax and self_ymax > other_ymin)
    @staticmethod
    def is_out_of_bounds(x, y):
        if x > WIN_WIDTH or x < 0 or y > WIN_HEIGHT or y < 0:
            return True
        return False
class Bullet(GameObject):
    bullet_list = []
    def __init__(self, x, y, speed, direction, width,  height):
        super().__init__(x, y, width, height)
        self.shape.setFill("red")
        self.speed = speed
        self.direction = direction
        Bullet.bullet_list.append(self)

    def move(self):
        dx = self.speed * math.cos(self.direction)
        dy = self.speed * math.sin(self.direction)
        self.x += dx
        self.y += dy
        self.shape.move(dx, dy)


class Player(GameObject):
    def __init__(self, x, y, speed, width, height):
        super().__init__(x,y,width,height)
        self.shape.setFill("blue")
        self.speed = speed
    def movement(self):
        dx, dy = 0,0
        if keyboard.is_pressed('w'):
            dy-=self.speed
        if keyboard.is_pressed('a'):
            dx-=self.speed
        if keyboard.is_pressed('s'):
            dy+=self.speed
        if keyboard.is_pressed('d'):
            dx+=self.speed
        if dx!=0 or dy !=0:
            self.x += dx
            self.y += dy
            self.shape.move(dx, dy)

async def bulletGenerator():
    while True:
        Bullet(75, 375, 10, 0, 20, 20)
        await asyncio.sleep(1)

async def main_loop(player):
    Text1 = Text(Point(375, 50), "Basic Hitboxes and stuff")
    Text1.setFill("white")
    Text1.draw(win)

    while True:
        player.movement()
        for bullet in Bullet.bullet_list:
            bullet.move()

            if bullet.collides_with(player):
                print("player bullet collision")
                bullet.shape.undraw()
                Bullet.bullet_list.remove(bullet)
            elif GameObject.is_out_of_bounds(bullet.x, bullet.y):
                bullet.shape.undraw()
                Bullet.bullet_list.remove(bullet)
        await asyncio.sleep(1/FPS)

async def main():
    player = Player(375, 375, 8, 30, 30)
    await asyncio.gather(
        bulletGenerator(),
        main_loop(player)
    )
if __name__ == "__main__":
    asyncio.run(main())