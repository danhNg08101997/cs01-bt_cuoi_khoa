import pygame, sys

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
bg_music = pygame.mixer.music.set_volume(0.3)
bg_music = pygame.mixer.music.play(-1)

# Set up bộ đếm thời gian
clock = pygame.time.Clock()

# Tạo background
bg_game = pygame.image.load('./images/bkgd.png')
bg_game_rect = bg_game.get_rect()
bg_game = pygame.transform.scale(bg_game,(bg_game_rect.width, SCREEN_HEIGHT))

# Tạo vòng lặp game
running = True
while running:
    clock.tick(60)
    
    screen.fill((255,255,255))
    
    for event in pygame.event.get():
        # Xử lý thoát game
        if event.type == pygame.QUIT:
            running = False
            
    pygame.display.flip()
    
pygame.quit()
sys.exit()
