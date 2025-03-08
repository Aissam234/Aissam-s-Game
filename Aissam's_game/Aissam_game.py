import pygame
from sys import exit
from random import randint, choice

class Player(pygame.sprite.Sprite):
    def __init__(self, level):
        super().__init__()

        self.level = level
        player_walk_1 = pygame.image.load("player_walk_1.png").convert_alpha()
        player_walk_2 = pygame.image.load("player_walk_2.png").convert_alpha()
        self.player_walk = [player_walk_1, player_walk_2]
        self.player_index = 0
        self.player_jump = pygame.image.load('jump.png').convert_alpha()

        self.image = self.player_walk[self.player_index]
        self.rect = self.image.get_rect(midbottom=(80, 300))
        self.gravity = 0
        self.jump_sound = pygame.mixer.Sound('jump.mp3')
        self.jump_sound.set_volume(0.3)

    def player_input(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE] and self.rect.bottom >= 300:
            if self.level == 1:
                self.gravity = -20
            elif self.level == 2:
                self.gravity = -30  # Higher jump for level 2
            self.jump_sound.play()

    def apply_gravity(self):
        self.gravity += 1
        self.rect.y += self.gravity
        if self.rect.bottom >= 300:
            self.rect.bottom = 300

    def anim(self):
        if self.rect.bottom < 300:
            self.image = self.player_jump
        else:
            self.player_index += 0.1
            if self.player_index >= len(self.player_walk):
                self.player_index = 0
            self.image = self.player_walk[int(self.player_index)]

    def update(self):
        self.player_input()
        self.apply_gravity()
        self.anim() 

class Obstacle(pygame.sprite.Sprite):
    def __init__(self, type, level):
        super().__init__()

        self.level = level
        if level == 1:
            if type == 'fly':
                fly_1 = pygame.image.load('Fly1.png').convert_alpha()
                fly_2 = pygame.image.load('Fly2.png').convert_alpha()
                self.frames = [fly_1, fly_2]
                y_pos = 210
            else:
                snail_1 = pygame.image.load('snail1.png').convert_alpha()
                snail_2 = pygame.image.load('snail2.png').convert_alpha()
                self.frames = [snail_1, snail_2]
                y_pos = 300
        else:
            crow_frames = self.load_crow_frames()
            self.frames = crow_frames
            y_pos = 300  # Align with player's y position

        self.anim_index = 0
        self.image = self.frames[self.anim_index]
        self.rect = self.image.get_rect(midbottom=(randint(900, 1200), y_pos))

        if level == 2:
            self.rect = pygame.Rect(self.rect.x, self.rect.y, self.image.get_width(), self.image.get_height())
            self.rect.midbottom = (self.rect.midbottom[0], 300)

    def load_crow_frames(self):
        frames = []
        for i in range(1, 5):  # Assuming the files are named crow_walk_1.png to crow_walk_4.png
            frame = pygame.image.load(f'crow_walk_{i}.png').convert_alpha()
            frames.append(frame)
        return frames

    def animation_state(self):
        self.anim_index += 0.1
        if self.anim_index >= len(self.frames):
            self.anim_index = 0
        self.image = self.frames[int(self.anim_index)]

    def update(self, score):
        self.animation_state()
        speed = 6
        if score >= 5:
            speed_multiplier = 1 + (score - 5) / 15
            speed *= min(speed_multiplier, 2)
        self.rect.x -= speed
        self.destroy()

    def destroy(self):
        if self.rect.x <= -100:
            self.kill()

def display_score():
    time = int(pygame.time.get_ticks() / 1000) - start_time
    score_surf = test_font.render(f'Score: {time}', False, (64, 64, 64))
    score_rect = score_surf.get_rect(center=(400, 50))
    screen.blit(score_surf, score_rect)
    return time

def collisions_splite():
    if pygame.sprite.spritecollide(player.sprite, obstacle_group, False):
        collision_sound.play()  # Play the collision sound
        obstacle_group.empty()
        return False
    else:
        return True

def level_transition_screen(level):
    level_message = test_font.render(f'Level {level}', False, (111, 196, 169))
    level_message_rect = level_message.get_rect(center=(400, 200))
    screen.fill((94, 129, 162))
    screen.blit(level_message, level_message_rect)
    pygame.display.update()
    pygame.time.delay(2000)

def play_level_music(level):
    if level == 1:
        pygame.mixer.music.load('music_zapsplat_easy_cheesy.mp3')
    elif level == 2:
        pygame.mixer.music.load('music_zapsplat_game_music_action_agressive_pounding_tense_electro_synth_028.mp3')
    pygame.mixer.music.play(-1)  # Loop the music

pygame.init()
screen = pygame.display.set_mode((800, 400))
pygame.display.set_caption('Ohoyaho')
clock = pygame.time.Clock()
test_font = pygame.font.Font('Pixeltype.ttf', 50)
game_active = False
level = 1

# Load collision sound
collision_sound = pygame.mixer.Sound('zapsplat_cartoon_duck_quack_006_78898.mp3')

# Level 1 Assets
sky_surface_level_1 = pygame.image.load('Sky.png').convert()
floor_surface_level_1 = pygame.image.load('ground.png').convert_alpha()
snail_frame_1 = pygame.image.load('snail1.png').convert_alpha()
snail_frame_2 = pygame.image.load('snail2.png').convert_alpha()
snail_frames = [snail_frame_1, snail_frame_2]
snail_index = 0
snail_surf = snail_frames[snail_index]

fly_frame_1 = pygame.image.load('Fly1.png').convert_alpha()
fly_frame_2 = pygame.image.load('Fly2.png').convert_alpha()
fly_frames = [fly_frame_1, fly_frame_2]
fly_index = 0
fly_surf = fly_frames[fly_index]

# Level 2 Assets
sky_surface_level_2 = pygame.image.load('new_background.jpg').convert()
floor_surface_level_2 = pygame.image.load('new_ground.png').convert_alpha()

player = pygame.sprite.GroupSingle()
player.add(Player(level))

player_rect = player.sprite.rect  # Use the sprite group's rect
player_gravity = 0
start_time = 0
score = 0

# groups
player = pygame.sprite.GroupSingle()
player.add(Player(level))

obstacle_group = pygame.sprite.Group()
player_stand = pygame.image.load('player_walk_1.png').convert_alpha()
player_stand = pygame.transform.rotozoom(player_stand, 0, 2)
player_stand_rect = player_stand.get_rect(center=(400, 200))
game_name = test_font.render("AISSAM'S GAME", False, (111, 196, 169))
game_name_rect = game_name.get_rect(center=(400, 75))
game_message = test_font.render('Press space to start', False, (111, 196, 169))
game_message_rect = game_message.get_rect(center=(400, 350))

# timer
obstacle_timer = pygame.USEREVENT + 1
pygame.time.set_timer(obstacle_timer, 1500)

snail_timer = pygame.USEREVENT + 2
pygame.time.set_timer(snail_timer, 500)

fly_timer = pygame.USEREVENT + 3
pygame.time.set_timer(fly_timer, 200)

# Debug Mode Toggle
debug_mode = True

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        if game_active:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and player.sprite.rect.bottom == 300:
                    player_gravity = -25
        else:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                game_active = True
                start_time = int(pygame.time.get_ticks() / 1000)
                player.sprite.level = level  # Update player level on game start
                play_level_music(level)  # Play music for the current level
        if game_active:
            if event.type == obstacle_timer:
                if level == 1:
                    obstacle_group.add(Obstacle(choice(['fly', 'snail']), level))
                else:
                    obstacle_group.add(Obstacle('monster', level))
            if event.type == snail_timer and level == 1:
                if snail_index == 0:
                    snail_index = 1
                else:
                    snail_index = 0
                snail_surf = snail_frames[snail_index]
            if event.type == fly_timer and level == 1:
                if fly_index == 0:
                    fly_index = 1
                else:
                    fly_index = 0
                fly_surf = fly_frames[fly_index]

    if game_active:

        if score == 20 and level == 1:
            level_transition_screen(2)
            level = 2      
            player.sprite.level = level  # Update player level on level transition
            play_level_music(level)  # Play music for the new level
            start_time = int(pygame.time.get_ticks() / 1000)

        if level == 1:
            screen.blit(sky_surface_level_1, (0, 0))
            screen.blit(floor_surface_level_1, (0, 300))
        else:
            screen.blit(sky_surface_level_2, (0, 0))
            screen.blit(floor_surface_level_2, (0, 300))

        player.draw(screen)
        player.update()
        obstacle_group.draw(screen)
        obstacle_group.update(score)
        score = display_score()

        # if debug_mode:
        #     # Draw collision rectangles for debugging
        #     pygame.draw.rect(screen, (255, 0, 0), player.sprite.rect, 2)  # Player rectangle
        #     for obstacle in obstacle_group:
        #         pygame.draw.rect(screen, (255, 0, 0), obstacle.rect, 2)  # Obstacle rectangles

        game_active = collisions_splite()
    else:
        screen.fill((94, 129, 162))
        screen.blit(player_stand, player_stand_rect)
        obstacle_group.empty()
        player.sprite.rect.midbottom = (80, 300)
        player_gravity = 0
        score_message = test_font.render(f'Your Score: {score}', False, (111, 196, 169))
        score_message_rect = score_message.get_rect(center=(400, 330))
        screen.blit(game_name, game_name_rect)

        if score == 0:
            screen.blit(game_message, game_message_rect)
        else:
            screen.blit(score_message, score_message_rect)

    pygame.display.update()
    clock.tick(60)
