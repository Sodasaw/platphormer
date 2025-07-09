import json

import pygame as pg
import pytmx

pg.init()

SCREEN_WIDTH = 900
SCREEN_HEIGHT = 600
FPS = 80
TILE_SCALE = 0.4
font = pg.font.Font(None, 30)
class Ball(pg.sprite.Sprite):
    def __init__(self, player_rect, direction):
        super(Ball, self).__init__()
        self.direction = direction
        self.player_rect = player_rect
        self.speed = 10

        self.image = pg.image.load("sprites/ball.png")
        self.image = pg.transform.scale(self.image, (30, 30))

        self.rect = self.image.get_rect()
        if self.direction == "right":
            self.rect.x = self.player_rect.right

        elif self.direction == "left":
            self.rect.x = self.player_rect.left
        self.rect.y = self.player_rect.centery
    def update(self):
        if self.direction == 'right':
            self.rect.x += self.speed
        else:
            self.rect.x -= self.speed


class Platform(pg.sprite.Sprite):
    def __init__(self, image, x, y, width, height):
        super().__init__()
        self.image = pg.transform.scale(image, (width, height))
        self.rect = self.image.get_rect()
        self.rect.x = x * TILE_SCALE
        self.rect.y = y * TILE_SCALE


class Scotty(pg.sprite.Sprite):
    def __init__(self, map_width, map_height):
        super(Scotty, self).__init__()
        self.load_anim()
        self.current_anim = self.anim_right
        self.current_image = 0
        self.image = pg.Surface((100, 100))
        self.image.fill("red")

        self.rect = self.image.get_rect()
        self.rect.center = (200, 100)

        self.velocity_x = 0
        self.velocity_y = 0
        self.left_edge = 800
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
        spritesheet = pg.image.load("sprites/Sprite Pack 5/5 - Moe Scotty/Flying_(32 x 32).png")
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

        self.rect.x += self.velocity_x
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
            self.current_image = (self.current_image + 1) % len(self.current_anim)
            self.image = self.current_anim[self.current_image]
            self.timer = pg.time.get_ticks()


class Wormy(pg.sprite.Sprite):
    def __init__(self, map_width, map_height, start_pos, final_pos):
        super(Wormy, self).__init__()
        self.load_anim()
        self.current_anim = self.anim_right
        self.current_image = 0
        self.image = pg.Surface((100, 100))
        self.image.fill("red")

        self.rect = self.image.get_rect()
        self.rect.bottomleft = start_pos

        self.velocity_x = 0
        self.velocity_y = 0
        self.left_edge = start_pos[0]
        self.right_edge = final_pos[0] + self.image.get_width()
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

        self.rect.x += self.velocity_x
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
            self.current_image = (self.current_image + 1) % len(self.current_anim)
            self.image = self.current_anim[self.current_image]
            self.timer = pg.time.get_ticks()


class Player(pg.sprite.Sprite):
    def __init__(self, map_width, map_height):
        super(Player, self).__init__()
        self.load_anim()
        self.current_anim = self.idle_anim_right
        self.current_image = 0
        self.image = pg.Surface((100, 100))
        self.image.fill("red")

        self.rect = self.image.get_rect()
        self.rect.center = (200, 100)

        self.hp = 10
        self.damage_timer = pg.time.get_ticks()
        self.damage_interval = 1200
        self.velocity_x = 0
        self.velocity_y = 0
        self.mode = "Game"
        self.direction = "right"
        self.gravity = 2
        self.is_jumping = False
        self.is_attacking = False
        self.hurt_timer = pg.time.get_ticks()
        self.map_width = map_width * TILE_SCALE
        self.map_height = map_height * TILE_SCALE
        self.timer = pg.time.get_ticks()
        self.attack_timer = pg.time.get_ticks()
        self.hurt_interval = 500
        self.interval = 200
        self.attack_interval = 400
        self.can_move = True
    def attack_mode(self):
        self.can_move = False

        if self.direction == "right":
            self.current_anim = self.attack_anim_right

        elif self.direction == "left":
            self.current_anim = self.attack_anim_left
    def get_damage(self):
        if pg.time.get_ticks() - self.damage_timer >= self.damage_interval:
            self.hp -= 1
            self.damage_timer = pg.time.get_ticks()
            self.mode = "Hurt"
            self.hurt_timer = pg.time.get_ticks()
            self.can_move = False

            if self.direction == "right":
                self.current_anim = self.hurt_anim_right
            else:
                self.current_anim = self.hurt_anim_left
            self.current_image = 0

    def load_anim(self):
        tile_size = 32
        tile_scale = 100

        # Idle анимация
        self.idle_anim_right = []
        spritesheet = pg.image.load("sprites/Sprite Pack 5/1 - Robo Retro/Idle_(32 x 32).png")
        for i in range(9):
            rect = pg.Rect(i * tile_size, 0, tile_size, tile_size)
            image = spritesheet.subsurface(rect)
            self.idle_anim_right.append(pg.transform.scale(image, (tile_size, tile_scale)))
        self.idle_anim_left = [pg.transform.flip(img, True, False) for img in self.idle_anim_right]

        # Ходьба
        self.move_anim_right = []
        spritesheet = pg.image.load("sprites/Sprite Pack 5/1 - Robo Retro/Walking_(32 x 32).png")
        for i in range(6):
            rect = pg.Rect(i * tile_size, 0, tile_size, tile_size)
            image = spritesheet.subsurface(rect)
            self.move_anim_right.append(pg.transform.scale(image, (tile_size, tile_scale)))
        self.move_anim_left = [pg.transform.flip(img, True, False) for img in self.move_anim_right]

        # Урон
        self.hurt_anim_right = []
        spritesheet = pg.image.load("sprites/Sprite Pack 5/1 - Robo Retro/Hurt_(32 x 32).png")
        for i in range(1):
            rect = pg.Rect(i * tile_size, 0, tile_size, tile_size)
            image = spritesheet.subsurface(rect)
            self.hurt_anim_right.append(pg.transform.scale(image, (tile_size, tile_scale)))
        self.hurt_anim_left = [pg.transform.flip(img, True, False) for img in self.hurt_anim_right]
        # Атака
        self.attack_anim_right = []
        spritesheet = pg.image.load("sprites/Sprite Pack 5/1 - Robo Retro/Spin-attack_(32 x 32).png")
        for i in range(6):
            rect = pg.Rect(i * tile_size, 0, tile_size, tile_size)
            image = spritesheet.subsurface(rect)
            self.hurt_anim_right.append(pg.transform.scale(image, (tile_size, tile_scale)))
        self.attack_anim_left = [pg.transform.flip(img, True, False) for img in self.hurt_anim_right]

    def update(self, platforms):
        # Проверка окончания урона
        if not self.can_move and pg.time.get_ticks() - self.hurt_timer > self.hurt_interval:
            self.can_move = True
            self.mode = "Game"
            if self.direction == "right":
                self.current_anim = self.idle_anim_right
            else:
                self.current_anim = self.idle_anim_left
            self.current_image = 0

        keys = pg.key.get_pressed()


        if self.can_move and self.mode != "Hurt":


            if keys[pg.K_SPACE] and not self.is_jumping:
                self.jump()
            if keys[pg.K_a]:
                self.direction = "left"
                if self.current_anim != self.move_anim_left:
                    self.current_anim = self.move_anim_left
                    self.current_image = 0
                self.velocity_x = -10
            elif keys[pg.K_d]:
                self.direction = "right"
                if self.current_anim != self.move_anim_right:
                    self.current_anim = self.move_anim_right
                    self.current_image = 0
                self.velocity_x = 10
            else:
                if self.current_anim in (self.move_anim_right, self.hurt_anim_right):
                    self.current_anim = self.idle_anim_right
                    self.current_image = 0
                elif self.current_anim in (self.move_anim_left, self.hurt_anim_left):
                    self.current_anim = self.idle_anim_left
                    self.current_image = 0
                self.velocity_x = 0
        else:
            self.velocity_x = 0

        self.rect.x += self.velocity_x
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
            self.current_image = (self.current_image + 1) % len(self.current_anim)
            self.image = self.current_anim[self.current_image]
            self.timer = pg.time.get_ticks()

    def jump(self):
        self.velocity_y = -30
        self.is_jumping = True


class Game:
    def __init__(self):
        self.screen = pg.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pg.display.set_caption("Платформер")
        self.setup()

    def setup(self):
        self.mode = "Game"
        self.clock = pg.time.Clock()
        self.all_sprites = pg.sprite.Group()
        self.platforms = pg.sprite.Group()
        self.enemies = pg.sprite.Group()

        self.tmx_map = pytmx.load_pygame("map1.tmx")
        self.map_tmx_width = self.tmx_map.width * self.tmx_map.tilewidth * TILE_SCALE
        self.map_tmx_height = self.tmx_map.height * self.tmx_map.tileheight * TILE_SCALE

        self.player = Player(self.map_tmx_width, self.map_tmx_height)
        self.all_sprites.add(self.player)

        self.ball = Ball(self.player.rect, self.player.direction)
        self.balls = pg.sprite.Group()




        # self.scotty = Scotty(self.map_tmx_width, self.map_tmx_height)
        # self.all_sprites.add(self.scotty)
        # self.enemies.add(self.scotty)

        for layer in self.tmx_map:
            for x, y, gid in layer:
                tile = self.tmx_map.get_tile_image_by_gid(gid)
                if tile:
                    platform = Platform(
                        tile,
                        x * self.tmx_map.tilewidth,
                        y * self.tmx_map.tileheight,
                        self.tmx_map.tilewidth,
                        self.tmx_map.tileheight
                    )
                    self.all_sprites.add(platform)
                    self.platforms.add(platform)
        with open("level1mobs.json", "r") as jf:
            data = json.load(jf)
            for enemy in data["enemies"]:
                if enemy["name"] == ("Wormy"):
                    x1 = enemy["start_pos"][0] * TILE_SCALE * self.tmx_map.tilewidth
                    y1 = enemy["start_pos"][1] * TILE_SCALE * self.tmx_map.tilewidth
                    x2 = enemy["final_pos"][0] * TILE_SCALE * self.tmx_map.tilewidth
                    y2 = enemy["final_pos"][1] * TILE_SCALE * self.tmx_map.tilewidth
                    wormy = Wormy(self.map_tmx_width, self.map_tmx_height, [x1, y1], [x2, y2])
                    self.all_sprites.add(wormy)
                    self.enemies.add(wormy)

        self.camera_x = 0
        self.camera_y = 0
        self.run()

    def run(self):
        running = True
        while running:
            self.event()
            self.update()
            self.draw()
            self.clock.tick(FPS)
        pg.quit()

    def event(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                return False
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_LSHIFT:
                    self.balls.add(self.ball)
                    self.all_sprites.add(self.ball)
            if self.mode == "Game over" and event.type == pg.KEYDOWN:
                self.setup()
        return True


    def update(self):
        if self.player.hp <= 0:
            self.mode = "Game over"
            return

        for enemy in self.enemies:
            if pg.sprite.collide_mask(self.player, enemy):
                self.player.get_damage()

        self.player.update(self.platforms)
        for enemy in self.enemies.sprites():
            enemy.update(self.platforms)
        for ball in self.balls.sprites():
            ball.update()
        pg.sprite.groupcollide(self.balls, self.enemies, True, True)
        pg.sprite.groupcollide(self.balls, self.platforms, True, False)

        self.camera_x = self.player.rect.x - SCREEN_WIDTH / 2
        self.camera_y = self.player.rect.y - SCREEN_HEIGHT / 2
        self.camera_y = max(0, min(self.camera_y, self.map_tmx_height - SCREEN_HEIGHT))

    def draw(self):
        self.screen.fill("white")

        for sprite in self.all_sprites:
            self.screen.blit(sprite.image, (sprite.rect.x - self.camera_x, sprite.rect.y - self.camera_y))
        for sprite in self.all_sprites:
            self.screen.blit(sprite.image, (sprite.rect.x - self.camera_x, sprite.rect.y - self.camera_y))
        # HP bar
        pg.draw.rect(self.screen, pg.Color("green"), (10, 10, self.player.hp * 20, 20))
        pg.draw.rect(self.screen, pg.Color("black"), (10, 10, 200, 20), 2)

        if self.mode == "Game over":
            text = font.render("GAME OVER - Press any key to restart", True, (255, 0, 0))
            text_rect = text.get_rect(center=(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2))
            self.screen.blit(text, text_rect)

        pg.display.flip()


if __name__ == "__main__":
    game = Game()