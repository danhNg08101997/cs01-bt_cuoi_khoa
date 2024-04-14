import pygame, sys
from models.Hero import Hero
from models.Constant import Direction, Status

# Khởi tạo game
pygame.init()

# Set up chiều dài, chiều rộng khung hình
SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720

# Khởi tạo màn hình game
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

# Tiêu đề game
pygame.display.set_caption('Metal Slug')

# Thiết lập âm thanh nhạc nền
bg_music = pygame.mixer.music.load('./sounds/music.mp3')
bg_music = pygame.mixer.music.set_volume(0.2)
bg_music = pygame.mixer.music.play(-1)

# Set up bộ đếm thời gian
clock = pygame.time.Clock()

# Tạo background
bg_game = pygame.image.load('./images/bkgd.png')
bg_game_rect = bg_game.get_rect()
bg_game = pygame.transform.scale(bg_game,(bg_game_rect.width, SCREEN_HEIGHT))
bg_rect = bg_game.get_rect()
x_scroll = bg_rect.x

# Tạo đối tượng hero:
hero = Hero()

# Tạo vòng lặp game
running = True
while running:
    # FPS 60s/screen
    clock.tick(60)
    
    screen.fill((255,255,255))
    
    for event in pygame.event.get():
        # Xử lý thoát game
        if event.type == pygame.QUIT:
            running = False
            
        # Start - Hero di chuyển
    key = pygame.key.get_pressed()
    if key[pygame.K_d] and x_scroll > - (bg_game.get_width() - SCREEN_WIDTH): #d là qua phải
        hero.move(Direction.right)
        x_scroll -= hero.speed * 2.5
    elif key[pygame.K_a] and x_scroll < 0: #a là qua trái
        hero.move(Direction.left)
        x_scroll += hero.speed * 2.5
    elif key[pygame.K_j]: #j là phím bắn
        hero.attack()
    else:
        hero.status = Status.freeze
    if key[pygame.K_k]: #k là phím nhảy
        hero.jump()
    # End - Hero di chuyển
    
    # Render background
    screen.blit(bg_game, (x_scroll, bg_rect.x))
    
    # Render hero
    hero.draw(screen)
    
    pygame.display.flip()
    
pygame.quit()
sys.exit()
