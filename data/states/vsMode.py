
import pygame as pg
from Tkinter import *
from .. import ball as ball_
from .. import paddle
from .. import tools
import random

class VsMode(tools.States):
    def __init__(self, screen_rect, difficulty): 
        tools.States.__init__(self)
        self.screen_rect = screen_rect
        self.score_text, self.score_rect = self.make_text("SCOREBOARD_PLACEHOLDER",
            (255,255,255), (screen_rect.centerx,100), 50)
        self.pause_text, self.pause_rect = self.make_text("PAUSED",
            (255,255,255), screen_rect.center, 50)
            
        self.cover = pg.Surface((screen_rect.width, screen_rect.height))
        self.cover.fill(0)
        self.cover.set_alpha(200)
        
        #game specific content
        self.bg_color = (1,1,1)
        self.pause = False
        self.score = [0,0]
                
        paddle_width = 10
        paddle_height = 100
        paddle_y = self.screen_rect.centery - (paddle_height // 2)
        padding = 25 #padding from wall
        midle = 200
        pad_right = screen_rect.width - paddle_width - padding
        pad_midle = screen_rect.width    
        self.ball = ball_.Ball(self.screen_rect, 10,10, (255,0,255))
        self.paddle_left = paddle.Paddle(padding,paddle_y, paddle_width,paddle_height, (150,150,150))
        self.paddle_middle = paddle.Paddle(padding+midle,paddle_y, paddle_width,paddle_height, (150,150,150))
        self.paddle_right = paddle.Paddle(pad_right,paddle_y, paddle_width,paddle_height, (150,150,150))
        
    def reset(self):
        self.pause = False
        self.score = [0,0]
        self.ball.set_ball()
    
    def get_event(self, event, keys):
        if event.type == pg.QUIT:
            self.quit = True
        elif event.type == pg.KEYDOWN:
            if event.key == self.controller_dict['back']:
                #self.button_sound.sound.play()
                self.done = True
                self.next = 'MENU'
                self.reset()
            elif event.key == self.controller_dict['pause']:
                self.pause = not self.pause
        elif event.type == self.background_music.track_end:
            self.background_music.track = (self.background_music.track+1) % len(self.background_music.tracks)
            pg.mixer.music.load(self.background_music.tracks[self.background_music.track]) 
            pg.mixer.music.play()
                    
    def movement(self, keys):
        if keys[pg.K_w]:
            self.paddle_left.move(0, -1)
        if keys[pg.K_s]:
            self.paddle_left.move(0, 1)
            
        #temp fix for keys until prefecting key bindings
        #if keys[self.controller_dict['up']]:
        if keys[pg.K_UP]:
            self.paddle_right.move(0, -1)
        #if keys[self.controller_dict['down']]:
        if keys[pg.K_DOWN]:
            self.paddle_right.move(0, 1)
        
    def update(self, now, keys):
        if not self.pause:
            self.score_text, self.score_rect = self.make_text('{}:{}'.format(self.score[0], self.score[1]),
                (255,255,255), (self.screen_rect.centerx,25), 50)
            self.paddle_left.update(self.screen_rect)
            self.paddle_middle.update(self.screen_rect)
            self.paddle_right.update(self.screen_rect)
            hit_side = self.ball.update(self.paddle_left.rect, self.paddle_right.rect,self.paddle_middle.rect)
            if hit_side:
                self.adjust_score(hit_side)
            self.movement(keys)
        else:
            self.pause_text, self.pause_rect = self.make_text("PAUSED",
                (255,255,255), self.screen_rect.center, 50)
        pg.mouse.set_visible(False)

    def render(self, screen):
        screen.fill(self.bg_color)
        screen.blit(self.score_text, self.score_rect)
        self.ball.render(screen)
        self.paddle_left.render(screen)
        self.paddle_middle.render(screen)
        self.paddle_right.render(screen)
        if self.pause:
            screen.blit(self.cover,(0,0))
            screen.blit(self.pause_text, self.pause_rect)
        
    def adjust_score(self, hit_side):
       
        
        if hit_side == -1:
            self.score[1] += 1
        elif hit_side == 1:
            self.score[0] += 1

        if self.score[0] == 5 or self.score[1] == 5:
            self.root = Tk()
            self.root.title('Game over!')
            self.root.geometry('300x100+1000+500')
            self.root.minsize(500,100)
            self.root.maxsize(500,100)

            if self.score[0] == 5:
                self.lbl1 = Label(self.root, text="Left Win!")
                self.lbl1.pack()
                self.lbl1.config(justify = CENTER)
                self.lbl1.config(font = ('consolas', 25, 'bold'))
                self.lbl1.config(foreground = 'red')
                self.root.mainloop()
                self.done = True
                self.next = 'MENU'
                self.reset()
            
            elif self.score[1] == 5:
                self.lbl2 = Label(self.root, text="Right Win!")
                self.lbl2.pack()
                self.lbl2.config(justify = CENTER)
                self.lbl2.config(font = ('consolas', 25, 'bold'))
                self.lbl2.config(foreground = 'green')
                self.root.mainloop()
                self.done = True
                self.next = 'MENU'
                self.reset()
            
    def cleanup(self):
        pg.mixer.music.stop()
        self.background_music.setup(self.background_music_volume)
        
    def entry(self):
        pg.mixer.music.play()
