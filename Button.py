from pygame.draw import rect
from pygame.font import SysFont


class Button():
    def __init__(self, x, y, width, height, text='', color=(255, 255, 255)):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.text = text
        self.color = color
        self.font = SysFont('comicsans', 25, True)

    def draw(self, window):
        # draw box
        rect(window, self.color, (self.x, self.y, self.width, self.height))

        # draw text
        text = self.font.render(self.text, 1, (0, 0, 0))
        window.blit(text, (self.x + self.width/2 - text.get_width()/2,
                           self.y + self.height/2 - text.get_height()/2))

    def is_over(self, mouse_pos):
        x = mouse_pos[0]
        y = mouse_pos[1]
        if x > self.x and x < self.x + self.width and\
                y > self.y and y < self.y + self.height:
            return True
        return False
