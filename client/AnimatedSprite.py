import pygame
import json


class _Spritesheet(object):
    """
    This class handles sprite sheets,
    source-code inspired by: www.scriptefun.com/transcript-2-using
    sprite-sheets-and-drawing-the-background
    Note: When calling images_at the rect is the format:
    (x, y, x + offset, y + offset)
    """

    def __init__(self, ressource_pygame_ratio11, scale=2):
        self.sheet = ressource_pygame_ratio11  #.convert()
        if scale != 1:
            self.sheet = pygame.transform.scale(
                self.sheet, (self.sheet.get_width() * scale, self.sheet.get_height() * scale)
            )

    def image_at(self, rectangle, colorkey):
        """
        Loads a specific image from a specific rectangle
        :param rectangle: a given (x,y, x+offset,y+offset)
        :param colorkey:  for handling transparency (color identified by colorkey is not drawn)
        :return: pygame surface
        """
        rect = pygame.Rect(rectangle)
        # convert() converts to the same pixel format as the display Surface
        image = pygame.Surface(rect.size).convert()
        image.blit(self.sheet, (0, 0), rect)  # blits sheet's rect to (0,0) in image
        if colorkey is not None:
            image.set_colorkey(colorkey)
        return image

    def images_at(self, rects, colorkey):
        """
        Loads a bunch of images at once
        :param rects: a list of coordinates
        :param colorkey:
        :return: several images as a list
        """
        return [self.image_at(rect, colorkey) for rect in rects]

    def load_strip(self, rect, image_count, colorkey=None):
        """Loads a strip of images and returns them as a list, rect must cut out the 1st img"""
        tups = [(rect[0] + rect[2] * x, rect[1], rect[2], rect[3])
                for x in range(image_count)]
        return self.images_at(tups, colorkey)



class AnimatedSprite(pygame.sprite.Sprite):
    def __init__(self, srcpath):
        super().__init__()
        self.img_source = srcpath+'.png'
        self.infospath = srcpath+'.json'

        self._twidth, self._theight = None, None
        self._ck_desc = None
        self.total_nb_img = 0

        self._data = None
        self._animations = dict()  # the default anim always has the name "idle"

        # for one given animation
        self._curr_anim_name = None
        self._curr_img_list = None
        self._curr_nb_frames = 0
        self.k = 0
        self.delay_per_frame = 100 / 1000  # 100ms by default
        self.stack_time = 0

    def load_data(self):
        with open(self.infospath, 'r') as fptr:
            infos_obj = json.load(fptr)
            self._twidth, self._theight = infos_obj['tilesize']
            self._ck_desc = infos_obj['colorkey']
            self.total_nb_img = 12

            # TODO la cest fait a la main, automatiser ca
            tmp = list()
            tmp.extend(  # 1er ligne
                _Spritesheet(pygame.image.load(self.img_source), 1).load_strip(
                    (0, 0, self._twidth, self._theight), 6, pygame.color.Color(self._ck_desc))
            )
            tmp.extend(  # 2e
                _Spritesheet(pygame.image.load(self.img_source), 1).load_strip(
                    (0, self._theight, self._twidth, self._theight), 6, pygame.color.Color(self._ck_desc))
            )
            self._data = tmp
            self.total_nb_img = len(self._data)

            self._load_anims(infos_obj['animations'])
            self.play('idle')

    def _load_anims(self, obj):
        """
        being given a JSON-like structure, example:
        "animations":{
            "idle":{"set":"0-5","delay":100},
            "attack":{"set":[6,7,8,9,10,11],"delay":250}
        }
        this method returns a dict name <> pair a,b
        where a is the list of images,
        b is the interframe delay
        """
        self._animations.clear()

        for k, v in obj.items():
            tmp = list()
            for idx in v['set']:

                if idx >= self.total_nb_img:
                    err_m = 'in animation "{}" given range is {} but, no corresp. data in the SpriteSheet!'.format(
                        k, v['set']
                    )
                    raise ValueError(err_m)
                tmp.append(self._data[idx])
            self._animations[k] = (tmp, v['delay'] / 1000)  # defined as millisec

    def play(self, anim_name):
        self._curr_anim_name = anim_name
        self.k = 0
        self._curr_img_list, self.delay_per_frame = self._animations[anim_name]
        self._curr_nb_frames = len(self._curr_img_list)

    def update_anim(self, dt):
        self.stack_time += dt

        if self.stack_time > self.delay_per_frame:
            self.stack_time -= self.delay_per_frame
            self.k += 1
            if self.k >= self._curr_nb_frames:
                self.play('idle')
            self.image = self._curr_img_list[self.k]
