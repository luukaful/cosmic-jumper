import pygame
import sys
import json
import random
import math

# Initialize Pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 800, 400
GROUND_LEVEL = HEIGHT - 50
GRAVITY = 0.5
JUMP_FORCE = -10
WHITE = (255, 255, 255)
LIGHT_GRAY = (200, 200, 200)
FPS = 60

# Paths
ASSETS_PATH = "assets/"
SPRITES_PATH = ASSETS_PATH + "sprites/"
AUDIO_PATH = ASSETS_PATH + "audio/"
FONT_PATH = ASSETS_PATH + "font.ttf"

# Initialize screen
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Cosmic Jumper")
clock = pygame.time.Clock()

# Load assets
def load_image(path, size=None):
    image = pygame.image.load(path).convert_alpha()
    return pygame.transform.scale(image, size) if size else image

def load_highscore(path="data/highscore.json"):
    """Load the highscore from a JSON file."""
    try:
        with open(path, "r") as file:
            data = json.load(file)
            return data.get("highscore", 0)
    except (FileNotFoundError, json.JSONDecodeError):
        return 0


def save_highscore(highscore, path="highscore.json"):
    """Save the highscore to a JSON file."""
    try:
        with open(path, "w") as file:
            json.dump({"highscore": highscore}, file)
    except IOError as e:
        print(f"Error saving the highscore: {e}")

# Load images
background_image = load_image(ASSETS_PATH + "background.jpg", (WIDTH, HEIGHT))
astronaut_sprites = [load_image(f"{SPRITES_PATH}astronaut{i}.png", (50, 50)) for i in range(2)]
crouch_sprites = [pygame.transform.scale(astronaut_sprite, (50, 25)) for astronaut_sprite in astronaut_sprites]
astronaut_masks = [pygame.mask.from_surface(sprite) for sprite in astronaut_sprites]
rock_images = [load_image(f"{SPRITES_PATH}rock{i}.png", (50, 50)) for i in range(6)]
floor_tile = load_image(SPRITES_PATH + "floor.png", (50, 50))
ufo_image = load_image(SPRITES_PATH + "ufo.png", (100, 50))
comet_image = load_image(SPRITES_PATH + "comet.png", (50, 50))
comet_mask = pygame.mask.from_surface(comet_image)

# Load sounds
jump_sound = pygame.mixer.Sound(AUDIO_PATH + "jump.wav")
collision_sound = pygame.mixer.Sound(AUDIO_PATH + "game_over.wav")
score_sound = pygame.mixer.Sound(AUDIO_PATH + "score.wav")
landing_sound = pygame.mixer.Sound(AUDIO_PATH + "landing.wav")
restart_sound = pygame.mixer.Sound(AUDIO_PATH + "restart.wav")
explosion_sound = pygame.mixer.Sound(AUDIO_PATH + "explosion.wav")
laser_sound = pygame.mixer.Sound(AUDIO_PATH + "laser.wav")
pygame.mixer.music.load(AUDIO_PATH + "bgm.mp3")
pygame.mixer.music.set_volume(0.5)
pygame.mixer.music.play(-1)

# Event for player idle animation
ANIMATION_EVENT = pygame.USEREVENT + 1
pygame.time.set_timer(ANIMATION_EVENT, 500)

# Fonts
font_large = pygame.font.Font(FONT_PATH, 72)
font_medium = pygame.font.Font(FONT_PATH, 34)
font_small = pygame.font.Font(FONT_PATH, 30)
font_very_small = pygame.font.Font(FONT_PATH, 18)

class Game:
    """Main class for the game."""
    def __init__(self, main_menu=True):
        self.player_rect = astronaut_sprites[0].get_rect(midbottom=(100, GROUND_LEVEL))
        self.player_speed = 0
        self.player_rotation_angle = 0
        self.player_fall_speed = 0
        self.current_sprite_index = 0
        self.rocks = []
        self.comets = []
        self.ufos = []
        self.game_over = False
        self.paused = False
        self.score = 0
        self.in_air = False
        self.crouching = False
        self.rock_spawn_range = [5, 10]
        self.rock_spawn_timer = random.randint(*self.rock_spawn_range)
        self.comet_spawn_range = [120, 240]
        self.comet_spawn_timer = random.randint(*self.comet_spawn_range)
        self.ufo_spawn_range = [240, 480]
        self.ufo_spawn_timer = random.randint(*self.ufo_spawn_range)
        self.in_main_menu = main_menu
        self.in_tutorial = False
        self.floor = Floor()
        self.jump_count = 0
        self.highscore = load_highscore()

    def reset(self):
        """Reset the game to its initial state."""
        self.__init__(False)
        restart_sound.play()

    def process_events(self):
        """Process game events, such as input and sprite animations."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                self.reset()
                self.in_main_menu = True

            if not self.game_over:
                # Process keyboard input
                if event.type == pygame.KEYDOWN:
                    if event.key in [pygame.K_SPACE, pygame.K_UP]:
                        if (self.player_rect.bottom >= GROUND_LEVEL or self.jump_count < 2) and not self.crouching:
                            self.player_speed = JUMP_FORCE
                            jump_sound.play()
                            self.jump_count += 1
                    elif event.key in [pygame.K_DOWN, pygame.K_s]:
                        self.crouching = True
                    elif event.key == pygame.K_p:
                        self.paused = not self.paused
                elif event.type == pygame.KEYUP:
                    if event.key in [pygame.K_DOWN, pygame.K_s]:
                        self.crouching = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_pos = pygame.mouse.get_pos()
                    for ufo in self.ufos:
                        if ufo.rect.collidepoint(mouse_pos):
                            self.ufos.remove(ufo)
                            explosion_sound.play()
                            self.score += 500
                # Process the player idle animation event
                elif event.type == ANIMATION_EVENT and not self.paused:
                    self.current_sprite_index = (self.current_sprite_index + 1) % 2
            if event.type == pygame.KEYDOWN and event.key == pygame.K_r:
                self.reset()

    def update(self):
        """Update the game state and process game logic."""
        if self.paused or self.game_over:
            if self.game_over:
                if self.player_rotation_angle < 90:
                    self.player_rotation_angle += 5
                self.player_fall_speed += GRAVITY
                self.player_rect.y += self.player_fall_speed
                if self.score > self.highscore:
                    self.highscore = self.score
                    save_highscore(self.highscore)
            elif self.paused:
                self.draw_pause_text()
            return

        # Apply gravity
        self.player_speed += GRAVITY
        self.player_rect.y += self.player_speed
        if self.player_rect.bottom > GROUND_LEVEL:
            self.player_rect.bottom = GROUND_LEVEL
            if self.in_air:
                landing_sound.play()
                self.in_air = False
                self.jump_count = 0
        else:
            self.in_air = True

        self.floor.update(self.score)

        # Spawn obstacles (rocks, comets, UFOs)
        self.rock_spawn_timer -= 1
        if self.rock_spawn_timer <= 0:
            self.rocks.append(Rock())
            self.rock_spawn_timer = random.randint(*self.comet_spawn_range)

        if self.score >= 2000:
            self.comet_spawn_timer -= 1
            if self.comet_spawn_timer <= 0:
                self.comets.append(Comet())
                self.comet_spawn_timer = random.randint(*self.comet_spawn_range)

        if self.score >= 3000:
            self.ufo_spawn_timer -= 1
            if self.ufo_spawn_timer <= 0:
                self.ufos.append(UFO())
                self.ufo_spawn_timer = random.randint(*self.ufo_spawn_range)

        # Update obstacles using a shallow copy
        self.rocks[:] = [rock for rock in self.rocks if rock.update(self.score)]
        self.comets[:] = [comet for comet in self.comets if comet.update(self.score)]
        self.ufos[:] = [ufo for ufo in self.ufos if ufo.update(self.score)]

        # Check for collisions with obstacles
        player_mask = astronaut_masks[self.current_sprite_index]
        for rock in self.rocks:
            if player_mask.overlap(rock.mask, (rock.rect.x - self.player_rect.x, rock.rect.y - self.player_rect.y)):
                self.game_over = True
                collision_sound.play()

        for comet in self.comets:
            if player_mask.overlap(comet.mask, (comet.rect.x - self.player_rect.x, comet.rect.y - self.player_rect.y)):
                self.game_over = True
                collision_sound.play()

        for ufo in self.ufos:
            for bullet in ufo.bullets:
                if player_mask.overlap(bullet.mask, (bullet.rect.x - self.player_rect.x, bullet.rect.y - self.player_rect.y)):
                    self.game_over = True
                    collision_sound.play()

        # Update score
        self.score += 10
        if self.score % 1000 == 0 and self.score != 0:
            score_sound.play()

    def draw_game_over_text(self):
        """Draw the game over text and the highscore."""
        draw_text("Game Over", font_large, LIGHT_GRAY, WIDTH // 2, HEIGHT // 2)
        draw_text("Press R to restart", font_medium, LIGHT_GRAY, WIDTH // 2, HEIGHT // 2 + 50)
        draw_text(f"Highscore: {self.highscore}", font_small, LIGHT_GRAY, WIDTH // 2, HEIGHT // 2 + 100)

    def draw_screen(self):
        """Display the game elements."""
        screen.blit(background_image, (0, 0))
        self.floor.draw()
        astronaut_sprite = astronaut_sprites[self.current_sprite_index]

        # Play the game-over animation if the player is out (falling through the ground)
        if self.game_over:
            rotated_sprite = pygame.transform.rotate(astronaut_sprite, self.player_rotation_angle)
            rotated_rect = rotated_sprite.get_rect(center=self.player_rect.center)
            screen.blit(rotated_sprite, rotated_rect.topleft)
        else:
            # Crouch animation
            if self.crouching:
                astronaut_sprite = crouch_sprites[self.current_sprite_index]
                self.player_rect.height = 25
            else:
                astronaut_sprite = astronaut_sprites[self.current_sprite_index]
                self.player_rect.height = 50
            screen.blit(astronaut_sprite, self.player_rect)

        # Draw rocks, comets, and UFOs
        for rock in self.rocks:
            rock.draw()
        for comet in self.comets:
            comet.draw()
        for ufo in self.ufos:
            ufo.draw()

        draw_text(f"Score: {self.score}", font_small, LIGHT_GRAY, 150, 30, align_left=True)

        # Game over text
        if self.game_over:
            self.draw_game_over_text()

        pygame.display.update()

    def draw_main_menu(self):
        """Draw the main menu of the game."""
        self.draw_transparent_background()
        draw_text("Cosmic Jumper", font_large, LIGHT_GRAY, WIDTH // 2, HEIGHT // 2 - 100)
        draw_text("Press ENTER to start", font_medium, LIGHT_GRAY, WIDTH // 2, HEIGHT // 2)
        draw_text("Press T to open the tutorial", font_very_small, LIGHT_GRAY, WIDTH // 2, HEIGHT // 2 + 100)
        pygame.display.update()

    def draw_tutorial(self):
        """Draw the tutorial text."""
        self.draw_transparent_background()
        # Game instructions
        instructions = [
            "Instructions:",
            "Use the arrow keys or spacebar to jump.",
            "Use the down arrow key or 'S' to crouch.",
            "Click on UFOs to destroy them.",
            "Press 'P' to pause the game.",
            "Press 'R' to restart.",
            "Avoid rocks and collect points!",
            "\nPress ESC to return to the main menu."
        ]
        for i, line in enumerate(instructions):
            draw_text(line, font_very_small, LIGHT_GRAY, WIDTH // 2, HEIGHT // 2 - 100 + i * 40)
        pygame.display.update()


    @staticmethod
    def draw_transparent_background():
        """Draw the background with a semi-transparent layer (for the main menu)."""
        screen.blit(background_image, (0, 0))
        semi_transparent_rect = pygame.Surface((WIDTH, HEIGHT))
        semi_transparent_rect.set_alpha(128)
        semi_transparent_rect.fill((0, 0, 0))
        screen.blit(semi_transparent_rect, (0, 0))

    @staticmethod
    def draw_pause_text():
        """Draw the pause text."""
        draw_text("Pause", font_large, LIGHT_GRAY, WIDTH // 2, HEIGHT // 2)

class Floor:
    """Class for the floor of the game."""
    def __init__(self):
        self.floor_surface = pygame.Surface((WIDTH + 50, 50))
        for i in range(0, WIDTH + 1, 50):
            self.floor_surface.blit(floor_tile, (i, 0))
        self.x_offset = 0

    def update(self, score):
        """Update the floor speed based on the score."""
        self.x_offset -= get_scroll_speed(score)
        if self.x_offset <= -50:
            self.x_offset += 50

    def draw(self):
        """Draw the floor on the screen."""
        screen.blit(self.floor_surface, (self.x_offset, GROUND_LEVEL))
        if self.x_offset < 0:
            screen.blit(self.floor_surface, (self.x_offset + WIDTH + 50, GROUND_LEVEL))

class Rock:
    """Class for the game rocks."""
    def __init__(self):
        self.image = random.choice(rock_images)
        self.rect = self.image.get_rect(midbottom=(WIDTH, GROUND_LEVEL + 10))
        self.mask = pygame.mask.from_surface(self.image)

    def update(self, score):
        """Update the rock (speed/collision)."""
        self.rect.x -= get_scroll_speed(score)
        return self.rect.right > 0

    def draw(self):
        """Draw the rock."""
        screen.blit(self.image, self.rect)

class Comet:
    """Class for the comets in the game."""
    def __init__(self):
        self.image = comet_image
        self.rect = self.image.get_rect(midbottom=(WIDTH, GROUND_LEVEL - 30))
        self.mask = comet_mask
        self.rotation_angle = 0

    def update(self, score):
        """Update the comet (speed/collision)."""
        self.rect.x -= get_scroll_speed(score) * 1.2
        self.rotation_angle = (self.rotation_angle + 5) % 360
        return self.rect.right > 0

    def draw(self):
        """Draw the comet."""
        rotated_image = pygame.transform.rotate(self.image, self.rotation_angle)
        rotated_rect = rotated_image.get_rect(center=self.rect.center)
        screen.blit(rotated_image, rotated_rect.topleft)

class UFO:
    """Class for the UFO in the game."""
    def __init__(self):
        self.image = ufo_image
        self.rect = self.image.get_rect(midtop=(WIDTH, GROUND_LEVEL + 50))
        self.speed = 5
        self.time = 0
        self.bullets = []

    def update(self, score):
        """Update the UFO (movement and bullets)."""
        self.time += 1
        self.rect.x -= self.speed
        self.rect.y = 50 + 30 * math.sin(self.time * 0.1) # Move in a sinusoidal wave
        if self.rect.right < 0:
            return False
        if self.time % 30 == 0:
            self.shoot_bullet()
        self.bullets = [bullet for bullet in self.bullets if bullet.update(score)]
        return True

    def shoot_bullet(self):
        """Shoot a bullet downward."""
        self.bullets.append(Bullet(self.rect.midbottom))
        laser_sound.play()

    def draw(self):
        """Draw the UFO and its bullets."""
        screen.blit(self.image, self.rect)
        for bullet in self.bullets:
            bullet.draw()

class Bullet:
    """Class for the bullets shot by the UFO."""
    def __init__(self, start_pos):
        self.image = pygame.Surface((10, 20))
        self.image.fill((255, 0, 0))
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect(midtop=start_pos)
        self.speed = 7

    def update(self, score):
        """Update the bullet (movement)."""
        self.rect.x -= get_scroll_speed(score)
        self.rect.y += self.speed
        # Destroy the bullets if they hit the ground
        if self.rect.bottom >= GROUND_LEVEL:
            return False
        return self.rect.top < HEIGHT

    def draw(self):
        """Draw the bullet."""
        screen.blit(self.image, self.rect)

def get_scroll_speed(score):
    """Determine the scroll speed of the game based on the score."""
    if score < 1000:
        return 7
    elif score < 2500:
        return 8
    elif score < 4000:
        return 9
    elif score < 5500:
        return 10
    else:
        return 11

def draw_text(text, font, color, x, y, align_left=False, border_color=(0, 0, 0), border_width=2):
    """Function to conveniently display text on the screen. (partially credited to the StackOverflow community)"""
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect(center=(x, y) if align_left else (x, y))

    # Draw the border by rendering the text multiple times with an offset
    for dx in range(-border_width, border_width + 1):
        for dy in range(-border_width, border_width + 1):
            if dx != 0 or dy != 0:  # Avoid double rendering at the original position
                border_surface = font.render(text, True, border_color)
                border_rect = border_surface.get_rect(center=(x + dx, y + dy) if not align_left else (x + dx, y + dy))
                screen.blit(border_surface, border_rect)

    screen.blit(text_surface, text_rect)

# Instantiate the main class and activate the main loop
if __name__ == "__main__":
    game = Game()
    while True:
        if game.in_main_menu and not game.in_tutorial:
            game.draw_main_menu()
            for event in pygame.event.get():
                if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                    game.in_main_menu = False
                if event.type == pygame.KEYDOWN and event.key == pygame.K_t:
                    game.in_tutorial = True
        elif game.in_tutorial:
            game.draw_tutorial()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    game.in_tutorial = False
        else:
            game.process_events()
            game.update()
            game.draw_screen()
        clock.tick(FPS)
