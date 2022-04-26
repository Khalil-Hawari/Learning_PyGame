import pygame
import random
from pygame.locals import (
  RLEACCEL, #Type of surface that blits faster but 'modifies' slower?
  K_UP,
  K_DOWN,
  K_LEFT,
  K_RIGHT,
  K_ESCAPE,
  K_w,
  K_a,
  K_s,
  K_d,
  KEYDOWN,
  QUIT,
)
# Initialize pygame
pygame.init()

# Screen dimensions
SCREEN_WIDTH = 600
SCREEN_HEIGHT = 300

# Defines a player object
class Player(pygame.sprite.Sprite):
  def __init__(self):
    super(Player, self).__init__()
    self.surf = pygame.image.load("ship.dib").convert()
    self.surf.set_colorkey((255, 255, 255), RLEACCEL)
    self.surf = pygame.transform.rotate(self.surf, 270) #allows to rotate imgs
    self.rect = self.surf.get_rect(center = (0, SCREEN_HEIGHT/2))
    self.speed = 10

  # Method to move the player based on keypresses
  def update(self, pressed_keys):
    if pressed_keys[K_w]:
      self.rect.move_ip(0, -self.speed)
    if pressed_keys[K_s]:
      self.rect.move_ip(0, self.speed)
    if pressed_keys[K_a]:
      self.rect.move_ip(-self.speed, 0)
    if pressed_keys[K_d]:
      self.rect.move_ip(self.speed, 0)

    # Keep player on the screen
    if self.rect.left < 0:
      self.rect.left = 0
    if self.rect.right > SCREEN_WIDTH:
      self.rect.right = SCREEN_WIDTH
    if self.rect.top <= 0:
      self.rect.top = 0
    if self.rect.bottom >= SCREEN_HEIGHT:
      self.rect.bottom = SCREEN_HEIGHT

      
# Defines enemy objects
class Enemy(pygame.sprite.Sprite):
  def __init__(self):
    super(Enemy, self).__init__()
    self.surf = pygame.image.load("laser.PNG").convert()
    self.surf.set_colorkey((0, 0, 0), RLEACCEL)
    self.rect = self.surf.get_rect(
      center=(
        random.randint(SCREEN_WIDTH + 20, SCREEN_WIDTH + 100),
        random.randint(0, SCREEN_HEIGHT),
          )
        )
    self.speed = random.randint(20, 30)

  # Moves enemies based on speed 
  def update(self):
    self.rect.move_ip(-self.speed, 0)
    if self.rect.right < 0:
      self.kill()

# Stars in the background
class Star(pygame.sprite.Sprite):
  def __init__(self):
    super(Star, self).__init__()
    self.surf = pygame.Surface((1, 1))
    self.surf.fill((255, 255, 255))
    self.rect = self.surf.get_rect(
      center=(
        random.randint(0, SCREEN_WIDTH + 100),
        random.randint(0, SCREEN_HEIGHT),
          )
        )
  
  # Moves stars back to their starting position once they have crossed the entire visible screen
  def update(self):
    self.rect.move_ip(-7, 0)
    if self.rect.right < 0:
      self.rect.move_ip(SCREEN_WIDTH + 100, 0)

    
# Screen object
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

# Custom event for adding a new enemy
ADDENEMY = pygame.USEREVENT + 1
pygame.time.set_timer(ADDENEMY, 700)

# Making a player object
my_player = Player()

# Groups to hold enemy sprites and all sprites
# -enemies is used for collision detection and position updates
# -all_sprites is used for rendering
enemies = pygame.sprite.Group()
stars = pygame.sprite.Group()
all_sprites = pygame.sprite.Group()
all_sprites.add(my_player)

# Draw a ton of stars
for i in range(100):
  new_star = Star()
  stars.add(new_star)
  all_sprites.add(new_star)

# Clock to control framerate
clock = pygame.time.Clock()

running = True
while running:
  # Checks the event queue for if the user has pressed the escape key, and ends the program if so
  for event in pygame.event.get():
    if event.type == KEYDOWN:
      
      if event.key == K_ESCAPE:
        running = False

    elif event.type == QUIT:
      running = False
    
    # Checks for if the ADDENEMY event has occurred in the queue
    elif event.type == ADDENEMY:
      # Make a new enemy and add it to sprite groups
      new_enemy = Enemy()
      enemies.add(new_enemy)
      all_sprites.add(new_enemy)

  # Getting a dictionary of keys pressed at the start of the frame
  pressed_keys = pygame.key.get_pressed()
  # Using method to update player's location 
  my_player.update(pressed_keys)
  # Updating enemy positions
  enemies.update()
  # Updating the stars' position
  stars.update()

  # Checks for collision between player & enemies
  if pygame.sprite.spritecollideany(my_player, enemies):
    # If so, then remove the player and stop the loop
    my_player.kill()
    running = False
  
  # Clear the frame before it changes
  screen.fill((0, 0, 0))
  
  # Draw sprites on screen
  for entity in all_sprites:
    screen.blit(entity.surf, entity.rect)
  # Update display
  pygame.display.flip()
  # 20 FPS
  clock.tick(20)

pygame.quit()
