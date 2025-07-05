import pygame as pg
import pytmx
pg.init()

SCREEN_WIDTH = 900
SCREEN_HEIGHT = 600
FPS = 80
TILE_SCALE = 0.4


class Platform(pg.sprite.Sprite):
    def __init__(self, image, x, y, width, height,):
        super().__init__()
        self.image = pg.transform.scale(image, (width, height))
        self.rect = self.image.get_rect()
        self.rect.x = x * TILE_SCALE
        self.rect.y = y * TILE_SCALE
class Wormy(pg.sprite.Sprite):
    def __init__(self, map_width, map_height):
        super(Wormy, self).__init__()
        self.load_anim()
        self.current_anim = self.anim_right
        self.current_image = 0
        self.image = pg.Surface((100,100))
        self.image.fill("red")

        self.rect = self.image.get_rect()
        self.rect.center = (200, 100)  # Начальное положение персонажа

        # Начальная скорость и гравитация
        self.velocity_x = 0
        self.velocity_y = 0
        self.left_edge = 150
        self.right_edge = 500
        self.direction = "right"
        self.gravity = 2
        self.is_jumping = False
        self.map_width = map_width * TILE_SCALE
        self.map_height = map_height * TILE_SCALE
        self.timer = pg.time.get_ticks()
        self.interval = 200

    def load_anim(self):
       tile_size = 32
       tile_scale = 100
       self.anim_right = []
       num_images = 3
       spritesheet = pg.image.load("sprites/Sprite Pack 5/4 - Squirmy Wormy/Movement_(32 x 32).png")
       for i in range(num_images):
           x = i * tile_size
           y = 0
           rect = pg.Rect(x, y, tile_size, tile_size)
           image = spritesheet.subsurface(rect)
           image = pg.transform.scale(image, (tile_size, tile_scale))
           self.anim_right.append(image)
       self.anim_left = [pg.transform.flip(image, True, False) for image in self.anim_right]


    def update(self, platforms):
        if self.direction == "right":
            self.velocity_x = 1
            if self.rect.right >= self.right_edge:
                self.direction = "left"
                self.current_anim = self.anim_right
        elif self.direction == "left":
            self.velocity_x = -1
            if self.rect.left <= self.left_edge:
                self.direction = "right"
                self.current_anim = self.anim_left
        new_x = self.rect.x + self.velocity_x
        self.rect.x = new_x
        self.velocity_y += self.gravity
        self.rect.y += self.velocity_y
        for platform in platforms:
            if platform.rect.collidepoint(self.rect.midbottom):
                self.rect.bottom = platform.rect.top
                self.velocity_y = 0
                self.is_jumping = False
            if platform.rect.collidepoint(self.rect.midtop):
                self.rect.top = platform.rect.bottom
                self.velocity_y = 0
            if platform.rect.collidepoint(self.rect.midright):
                self.rect.right = platform.rect.left
            if platform.rect.collidepoint(self.rect.midleft):
                self.rect.left = platform.rect.right

        if pg.time.get_ticks() - self.timer > self.interval:
            self.current_image += 1
            if self.current_image >= len(self.current_anim):
                self.current_image = 0
            self.image = self.current_anim[self.current_image]
            self.timer = pg.time.get_ticks()
class Player(pg.sprite.Sprite):
    def __init__(self, map_width, map_height):
        super(Player, self).__init__()
        self.load_anim()
        self.current_anim = self.idle_anim_right
        self.current_image = 0
        self.image = pg.Surface((100,100))
        self.image.fill("red")

        self.rect = self.image.get_rect()
        self.rect.center = (200, 100)  # Начальное положение персонажа

        # Начальная скорость и гравитация
        self.velocity_x = 0
        self.velocity_y = 0
        self.gravity = 2
        self.is_jumping = False
        self.map_width = map_width * TILE_SCALE
        self.map_height = map_height * TILE_SCALE
        self.timer = pg.time.get_ticks()
        self.interval = 200

    def load_anim(self):
        tile_size = 32
        tile_scale = 100

        self.idle_anim_right = []
        num_images = 9
        spritesheet = pg.image.load("sprites/Sprite Pack 5/1 - Robo Retro/Idle_(32 x 32).png")
        for i in range(num_images):
            x = i * tile_size
            y = 0
            rect = pg.Rect(x, y, tile_size, tile_size)
            image = spritesheet.subsurface(rect)
            image = pg.transform.scale(image, (tile_size, tile_scale))
            self.idle_anim_right.append(image)
        self.idle_anim_left = [pg.transform.flip(image, True, False) for image in self.idle_anim_right]
        self.move_anim_right = []
        num_images = 6
        spritesheet = pg.image.load("sprites/Sprite Pack 5/1 - Robo Retro/Walking_(32 x 32).png")
        for i in range(num_images):
            x = i * tile_size
            y = 0
            rect = pg.Rect(x, y, tile_size, tile_size)
            image = spritesheet.subsurface(rect)
            image = pg.transform.scale(image, (tile_size, tile_scale))
            self.move_anim_right.append(image)
        self.move_anim_left = [pg.transform.flip(image, True, False) for image in self.move_anim_right]
    def update(self, platforms):

        keys = pg.key.get_pressed()
        if keys[pg.K_SPACE] and not self.is_jumping:
            self.jump()
        if keys[pg.K_a]:
            if self.current_anim != self.move_anim_left:
                self.current_anim = self.move_anim_left
                self.current_image = 0
            self.velocity_x = -10
        elif keys[pg.K_d]:
            if self.current_anim != self.move_anim_right:
                self.current_anim = self.move_anim_right
                self.current_image = 0
            self.velocity_x = 10
        else:
            if self.current_anim == self.move_anim_right:
                self.current_anim = self.idle_anim_right
                self.current_image = 0
            elif self.current_anim == self.move_anim_left:
                self.current_anim = self.idle_anim_left
                self.current_image = 0

            self.velocity_x = 0
        new_x = self.rect.x + self.velocity_x
        self.rect.x = new_x
        self.velocity_y += self.gravity
        self.rect.y += self.velocity_y
        for platform in platforms:
            if platform.rect.collidepoint(self.rect.midbottom):
                self.rect.bottom = platform.rect.top
                self.velocity_y = 0
                self.is_jumping = False
            if platform.rect.collidepoint(self.rect.midtop):
                self.rect.top = platform.rect.bottom
                self.velocity_y = 0
            if platform.rect.collidepoint(self.rect.midright):
                self.rect.right = platform.rect.left
            if platform.rect.collidepoint(self.rect.midleft):
                self.rect.left = platform.rect.right

        if pg.time.get_ticks() - self.timer > self.interval:
            self.current_image += 1
            if self.current_image >= len(self.current_anim):
                self.current_image = 0
            self.image = self.current_anim[self.current_image]
            self.timer = pg.time.get_ticks()
    def jump(self):
        self.velocity_y = -30
        self.is_jumping = True


class Game:
    def __init__(self):
        self.screen = pg.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pg.display.set_caption("Платформер")
        self.clock = pg.time.Clock()

        self.all_sprites = pg.sprite.Group()
        self.platforms = pg.sprite.Group()

        self.is_running = False
        self.tmx_map = pytmx.load_pygame("map1.tmx")
        self.map_tmx_width = self.tmx_map.width * self.tmx_map.tilewidth * TILE_SCALE
        self.map_tmx_height = self.tmx_map.height * self.tmx_map.tileheight * TILE_SCALE
        self.player = Player(self.map_tmx_width, self.map_tmx_height)
        self.all_sprites.add(self.player)
        self.wormy = Wormy(self.map_tmx_width, self.map_tmx_height)
        self.all_sprites.add(self.wormy)
        for layer in self.tmx_map:
            for x,y,gid in layer:
                tile = self.tmx_map.get_tile_image_by_gid(gid)
                if tile:
                    platform = Platform(tile, x * self.tmx_map.tilewidth, y * self.tmx_map.tileheight, self.tmx_map.tilewidth, self.tmx_map.tileheight)
                    self.all_sprites.add(platform)
                    self.platforms.add(platform)
        self.camera_x = 0
        self.camera_y = 0
        self.camera_speed = 4

        self.run()

    def run(self):
        self.is_running = True
        while self.is_running:
            self.event()
            self.update()
            self.draw()
            self.clock.tick(FPS)
        pg.quit()
        quit()

    def event(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.is_running = False
        keys = pg.key.get_pressed()

        # if keys[pg.K_d]:
        #     self.camera_x += self.camera_speed
        # if keys[pg.K_a]:
        #     self.camera_x -= self.camera_speed
        # if keys[pg.K_w]:
        #     self.camera_y += self.camera_speed
        # if keys[pg.K_s]:
        #     self.camera_y -= self.camera_speed

    def update(self):
        self.player.update(self.platforms)
        self.wormy.update(self.platforms)

        self.camera_x = self.player.rect.x - SCREEN_WIDTH / 2
        self.camera_y = self.player.rect.y - SCREEN_HEIGHT / 2
        self.camera_y = max(0, min(self.camera_y, self.map_tmx_height - SCREEN_HEIGHT))

    def draw(self):
        self.screen.fill("white")
        for sprite in self.all_sprites:
            self.screen.blit(sprite.image, sprite.rect.move(-self.camera_x, -self.camera_y))



        pg.display.flip()


if __name__ == "__main__":
    game = Game()