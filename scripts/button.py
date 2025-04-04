import pygame

def text_objects(text, font, color):
    textSurface = font.render(text, True, color)
    return textSurface, textSurface.get_rect()

class Button:
    button_count_per_column = {}
    def __init__(self, msg, w, h, x, column_name, buttons_y_start, height_step, ic, ac, text_color, text_size, game_display, action, args):
        if isinstance(Button.button_count_per_column.get(column_name, None), int):
            Button.button_count_per_column[column_name] += 1
        else:
            Button.button_count_per_column[column_name] = 0
        self.msg = msg
        self.x = x
        self.y = buttons_y_start + (Button.button_count_per_column[column_name] * height_step)
        self.w = w
        self.h = h
        self.ic = ic
        self.ac = ac
        self.text_color = text_color
        self.text_size = text_size
        self.game_display = game_display 
        self.action = action
        self.args = args
        self.was_clicked = False


    def is_hovered(self):
        mouse = pygame.mouse.get_pos()
        return self.x+self.w > mouse[0] > self.x and self.y+self.h > mouse[1] > self.y
    
    def is_clicked(self):
        click = pygame.mouse.get_pressed()
        return click[0] == 1


    def draw(self):
        if self.is_hovered():
            pygame.draw.rect(self.game_display, self.ac,(self.x, self.y, self.w, self.h))
            if self.is_clicked():
                if not self.was_clicked:
                    self.was_clicked = True
                    self.action(*self.args)
            else:
                self.was_clicked = False
            
        else:
            pygame.draw.rect(self.game_display, self.ic,(self.x, self.y, self.w, self.h))
        # text_size = display_width // 33
        text_size = self.text_size
        smallText = pygame.font.Font("fonts/Segoe UI Symbol.ttf", text_size)
        textSurf, textRect = text_objects(self.msg, smallText, self.text_color)
        textRect.center = ( (self.x+(self.w/2)), (self.y+(self.h/2)) )
        self.game_display.blit(textSurf, textRect)        