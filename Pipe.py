from pygame.draw import rect
from pygame import Rect
from pygame.image import load
from pygame.transform import flip, scale


class Pipe():
    def __init__(self, x, y, width, gap, s_width, s_height, vel):
        self.x = x
        self.y = y
        self.width = width
        self.gap = gap
        self.s_width = s_width
        self.s_height = s_height
        self.vel = vel
        self.color = (0, 0, 0)

        source = load('pipe_img.png')
        self.lower_img = scale(source,
                               (self.width,
                                self.s_height - self.y - self.gap + 10))
        self.head_height = int(self.width * 165 / 351)
        self.lower_head = scale(load('pipe_head.png'),
                                (self.width, self.head_height))
        self.upper_img = scale(flip(source, False, True),
                               (self.width, self.y - self.head_height + 10))
        self.upper_head = flip(self.lower_head, False, True)

    def draw(self, window):
        # the upper pipe
        window.blit(self.upper_img, (self.x, 0))
        window.blit(self.upper_head, (self.x, self.y - self.head_height))

        # the lower pipe
        l_y = self.y + self.gap
        window.blit(self.lower_img,
                    (self.x, l_y + self.head_height - 10))
        window.blit(self.lower_head, (self.x, l_y))

        self.x -= self.vel

    # return the box collider for the upper pipe
    def get_upper_collider(self):
        return Rect(self.x, 0, self.width, self.y)

    # return the box collider for the lower pipe
    def get_lower_collider(self):
        l_y = self.y + self.gap
        return Rect(self.x, l_y, self.width, self.s_height-l_y)

    # check if pip is off screen
    def offscreen(self):
        if self.x + self.width < 0:
            return True
        return False

    def __repr__(self):
        return str(self.x)
