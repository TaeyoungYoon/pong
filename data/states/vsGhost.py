
from Tkinter import *
from . import vsMode
from .. import ball as ball_
import random
import pygame as pg

class VsGhost(vsMode.VsMode):
    def __init__(self, screen_rect, difficulty):
        vsMode.VsMode.__init__(self, screen_rect, difficulty)
        self.fake_balls = []
        
    def add_fake_ball(self):
        color = (random.randint(0,255), random.randint(0,255), random.randint(0,255))
        speed = random.randint(3,10)
        ball = ball_.Ball(self.screen_rect, 10,10, color, menu=True, speed=speed)
        self.fake_balls.append(ball)
        
    def adjust_score(self, hit_side):
        
        if hit_side == -1:
            self.add_fake_ball()
            self.score[1] += 1
        elif hit_side == 1:
            self.add_fake_ball()
            self.score[0] += 1

        if self.score[0] == 15 or self.score[1] == 15:
            self.root = Tk()
            self.root.title('Game over!')
            self.root.geometry('300x100+1000+500')
            self.root.minsize(500,100)
            self.root.maxsize(500,100)

            if self.score[0] == 15:
                self.lbl1 = Label(self.root, text="Left Win!")
                self.lbl1.pack()
                self.lbl1.config(justify = CENTER)
                self.lbl1.config(font = ('consolas', 25, 'bold'))
                self.lbl1.config(foreground = 'red')
                self.root.mainloop()
                self.done = True
                self.next = 'MENU'
                self.reset()
            
            elif self.score[1] == 15:
                self.lbl2 = Label(self.root, text="Right Win!")
                self.lbl2.pack()
                self.lbl2.config(justify = CENTER)
                self.lbl2.config(font = ('consolas', 25, 'bold'))
                self.lbl2.config(foreground = 'green')
                self.root.mainloop()
                self.done = True
                self.next = 'MENU'
                self.reset()
            
            
    def render(self, screen):
        screen.fill(self.bg_color)
        screen.blit(self.score_text, self.score_rect)
        self.ball.render(screen)
        for ball in self.fake_balls:
            ball.render(screen)
        self.paddle_left.render(screen)
        self.paddle_middle.render(screen)
        self.paddle_right.render(screen)
        if self.pause:
            screen.blit(self.cover,(0,0))
            screen.blit(self.pause_text, self.pause_rect)
            
    def update(self, now, keys):
        if not self.pause:
            self.score_text, self.score_rect = self.make_text('{}:{}'.format(self.score[0], self.score[1]),
                (255,255,255), (self.screen_rect.centerx,25), 50)
            self.paddle_left.update(self.screen_rect)
            self.paddle_middle.update(self.screen_rect)
            self.paddle_right.update(self.screen_rect)
            hit_side = self.ball.update(self.paddle_left.rect, self.paddle_right.rect,self.paddle_middle.rect)
            for ball in self.fake_balls:
                ball.update(self.bogus_rect, self.bogus_rect,self.bogus_rect)
            if hit_side:
                self.adjust_score(hit_side)
            self.movement(keys)
        else:
            self.pause_text, self.pause_rect = self.make_text("PAUSED",
                (255,255,255), self.screen_rect.center, 50)
        pg.mouse.set_visible(False)
        
    def cleanup(self):
        pg.mixer.music.stop()
        self.background_music.setup(self.background_music_volume)
        self.fake_balls = []
        
