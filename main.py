import pyglet
from pyglet import shapes
import random


class PlatformPlayer(shapes.Rectangle):
    def __init__(self, x, y, w, h, c, window_width, window_height):
        self.d1 = 1
        self.d2 = 1
        self.pc = 0
        super().__init__(x, y, w, h, c)
        self.window_width = window_width
        self.window_height = window_height

    def uptD(self):
        self.x += 5

    def uptA(self):
        self.x -= 5


class PlatformBot(shapes.Rectangle):
    def __init__(self, x, y, w, h, c, window_width, window_height):
        self.d1 = 1
        self.d2 = 1
        self.bc = 0
        super().__init__(x, y, w, h, c)
        self.window_width = window_width
        self.window_height = window_height

    def upt(self, ball_x):
        if self.x <= 0:
            self.x = 0
        if self.x >= 650:
            self.x = 650
        if self.x + self.width / 2 < ball_x:
            self.x += 3.3
        if self.x + self.width / 2 > ball_x:
            self.x -= 3.3


class Ball(shapes.Circle):
    def __init__(self, x, y, r, color, window_width, window_height, player, bot):
        self.f = True
        self.dx = 1
        self.dy = 1
        self.player = player
        self.bot = bot
        super().__init__(x=x, y=y, radius=r, color=color)
        self.window_width = window_width
        self.window_height = window_height

    def upt(self):
        ball_t = self.y + self.radius
        ball_d = self.y - self.radius
        ball_r = self.x - self.radius
        ball_l = self.x + self.radius
        player_t = self.player.y + self.player.height
        player_r = self.player.x + self.player.width
        player_l = self.player.x
        bot_d = self.bot.y
        bot_r = self.bot.x + self.bot.width
        bot_l = self.bot.x

        if (ball_d <= player_t) and ball_r <= player_r and ball_l >= player_l:
            self.dy = random.randint(1, 2)

        if (ball_t >= bot_d) and ball_r <= bot_r and ball_l >= bot_l:
            self.dy = random.randint(-2, -1)

        if ball_d < player_t and self.f:
            self.bot.bc += 1
            self.f = False

        if ball_t > bot_d and self.f:
            self.player.pc += 1
            self.f = False

        if ball_t < bot_d and ball_d > player_t:
            self.f = True

        if self.y >= 750:
            self.dy = -1
        elif self.y <= 50:
            self.dy = 1
        if self.x >= 750:
            self.dx = random.randint(-2, -1)
        elif self.x <= 50:
            self.dx = random.randint(1, 2)
        self.y += 6 * self.dy
        self.x += 4 * self.dx


class Text:
    def __init__(self, text, x, y, player, bot, font_name='Comic Sans MS', font_size=20, color=(50, 255, 50, 255)):
        self.player = player
        self.bot = bot
        self.label = pyglet.text.Label(
            text,
            font_name=font_name,
            font_size=font_size,
            x=x,
            y=y,
            anchor_x='center',
            anchor_y='center',
            color=color  # RGBA (0..255)
        )

    def upt(self):
        self.label.text = f'{self.player.pc}:{self.bot.bc}'

    def draw(self):
        self.label.draw()
class GameOverText():
    def __init__(self, text, x, y, font_name='Comic Sans MS', font_size=40, color=(200, 0, 0, 255)):
        self.label = pyglet.text.Label(
            text,
            font_name=font_name,
            font_size=font_size,
            x=x,
            y=y,
            anchor_x='center',
            anchor_y='center',
            color=color  # RGBA (0..255)
        )

    def draw(self):
        self.label.draw()
class GameOver(shapes.Rectangle):
    def __init__(self, w, h):
        self.visisble = False
        super().__init__(0, 0, w, h, (0,0,0))

    def upt(self, pl, bot):
        if pl >= 3:
            self.visisble = True
        if bot >= 3:
            self.visisble = True
        if bot < 3 and pl < 3:
            self.visisble = False
class GameWindow(pyglet.window.Window):
    WIDTH = 800
    HEIGTH = 800

    def __init__(self):
        super().__init__(self.WIDTH, self.HEIGTH, "xpowl")
        self.q = PlatformPlayer(self.WIDTH // 2, 0, 150, 50, (255, 0, 0), self.width, self.height)
        self.w = PlatformBot(self.WIDTH//2, self.HEIGTH - 50, 150, 50, (0, 0, 255) , self.width, self.height)
        self.e = Ball(self.WIDTH // 2, self.HEIGTH // 2, 50, (255, 255, 255), self.width, self.height, self.q, self.w)
        self.text = Text("0:0", x=self.width // 2, y=self.height // 2, player = self.q, bot = self.w)
        self.s = GameOver(self.WIDTH, self.HEIGTH)
        self.stext1 = GameOverText("Game Over", x=self.WIDTH// 2, y=self.HEIGTH // 2)
        self.stext2 = GameOverText("Press R to restart", x=self.WIDTH // 2 , y=self.HEIGTH // 2 - 150)
        self.push_handlers(self.on_draw)
        self.keys = pyglet.window.key.KeyStateHandler()
        self.push_handlers(self.keys)
        pyglet.clock.schedule_interval(self.update, 1 / 80.0)

    def update(self, dt):
        if self.keys[pyglet.window.key.D] and self.q.x < 650:
            self.q.uptD()
        if self.keys[pyglet.window.key.A] and self.q.x > 0:
            self.q.uptA()
        self.e.upt()
        self.w.upt(self.e.x)
        self.text.upt()
        self.s.upt(self.q.pc, self.w.bc)
        if self.s.visisble:
            if self.keys[pyglet.window.key.R]:
                self.q.pc = 0
                self.w.bc = 0
                self.s.visisble = False

    def on_draw(self):
        if self.s.visisble == False:
            self.clear()
            self.q.draw()
            self.w.draw()
            self.e.draw()
            self.text.draw()
        elif self.s.visisble == True:
            self.s.draw()
            self.stext1.draw()
            self.stext2.draw()
    def run(self):
        pyglet.app.run()


def main():
    window = GameWindow()
    window.run()


if __name__ == "__main__":
    main()
