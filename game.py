import pygame, sys, random, os.path
from models.Hero import Hero
from models.Constant import Direction, Status
from models.Soldier import Soldier

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
bg_music = pygame.mixer.music.set_volume(0.5)
bg_music = pygame.mixer.music.play(-1)

# Set up bộ đếm thời gian
clock = pygame.time.Clock()

# Tạo background
bg_game = pygame.image.load('./images/bkgd.png')
bg_game_rect = bg_game.get_rect()
bg_game = pygame.transform.scale(bg_game,(bg_game_rect.width, SCREEN_HEIGHT))
# bg_rect = bg_game.get_rect()
x_scroll = bg_game_rect.x

# Tạo background game over
bg_game_over = pygame.image.load('./images/gameover.jpg')
bg_game_over = pygame.transform.scale(bg_game_over, (SCREEN_WIDTH, SCREEN_HEIGHT))

# Tạo đối tượng hero:
hero = Hero()

# Tạo lst_soldier cứ mỗi 5 giây thì sẽ append lính vào
arr_soldier:list[Soldier] = []
time_render_soldier_start = 0

# Thời gian bắt đầu chết
time_start_die = 0

# check file đã lưu có tồn tại không rồi mới load game
path = './hero.json'
check_file = os.path.isfile(path)
check_access = os.access(path, os.R_OK)
if check_file and check_access:
    hero.load_game()

# Tạo vòng lặp game
running = True
while running:
    # FPS 60s/screen
    clock.tick(60)
    
    screen.fill((255,255,255))
    
    for event in pygame.event.get():
        # Xử lý thoát game
        if event.type == pygame.QUIT:
            if hero.live > 0:
                hero.save_game()
            running = False
            
        # Start - Hero di chuyển
    key = pygame.key.get_pressed()
    if key[pygame.K_d] and x_scroll > - (bg_game.get_width() - SCREEN_WIDTH): #d là qua phải
        hero.move(Direction.right) 
        x_scroll -= hero.speed * 2.5
        # Âm thanh di chuyển
        pygame.mixer.Sound.set_volume(hero.move_sound, 0.1)
        pygame.mixer.Sound.play(hero.move_sound, 0, 0, 0)
    elif key[pygame.K_a] and x_scroll < 0: #a là qua trái
        hero.move(Direction.left)
        x_scroll += hero.speed * 2.5
        # Âm thanh di chuyển
        pygame.mixer.Sound.set_volume(hero.move_sound, 0.1)
        pygame.mixer.Sound.play(hero.move_sound, 0, 0, 0)
    elif key[pygame.K_j]: #j là phím bắn
        hero.attack()
        # Âm thanh bắn
        pygame.mixer.Sound.set_volume(hero.attack_sound, 0.2)
        pygame.mixer.Sound.play(hero.attack_sound, 0,0,0)
    else:
        hero.status = Status.freeze
    if key[pygame.K_k]: #k là phím nhảy
        hero.jump()
        # Âm thanh di chuyển
        pygame.mixer.Sound.set_volume(hero.move_sound, 0.1)
        pygame.mixer.Sound.play(hero.move_sound, 0, 0, 0)
    # End - Hero di chuyển
    
    # Render background
    screen.blit(bg_game, (x_scroll, bg_game_rect.x))
    
    # Random soldier ngẫu nhiên xuất hiện
    current_time_render_soldier = pygame.time.get_ticks()
    if current_time_render_soldier - time_render_soldier_start >= 5000:
        # Tạo lính
        new_soldier = Soldier()
        new_soldier.rect.y = SCREEN_HEIGHT - 250
        new_soldier.rect.x = random.randint(0, 2000)
        if new_soldier.rect.x > hero.rect.x:
            new_soldier.direction = Direction.left
        # Đưa soldier vào list
        arr_soldier.append(new_soldier)
        # Gán lại mốc thời gian
        time_render_soldier_start = current_time_render_soldier
    
    # Render lính
    for soldier in arr_soldier:
        soldier.draw(screen, hero)
    
    # Xử lý hero và soldier
    for bullet_hero in hero.lst_bullet:
        for soldier in arr_soldier:
            if bullet_hero.rect.colliderect(soldier.rect) and soldier.status != Status.die:
                soldier.status = Status.die
                if len(hero.lst_bullet) > 0:
                    hero.lst_bullet.remove(bullet_hero)
                hero.score += 100
    
    # Xử lý 3 giây cho nhân vật khi chết
    time_current_die = pygame.time.get_ticks()
    if time_current_die - time_start_die > 3000:
        # Xử lý chết
        for soldier in arr_soldier:
            if soldier.status == Status.die:
                # Âm thanh chết
                pygame.mixer.Sound.set_volume(soldier.die_sound, 0.3)
                pygame.mixer.Sound.play(soldier.die_sound, 0, 0, 0)
                arr_soldier.remove(soldier)
            # if hero.status == Status.die:
            #     # Âm thanh chết
            #     pygame.mixer.Sound.set_volume(hero.die_sound, 0.3)
            #     pygame.mixer.Sound.play(hero.die_sound, 0, 0, 0)
        # Gán lại mốc thời gian chết
        time_start_die = time_current_die
    
    # Render hero
    hero.draw(screen)
    # Render game over
    if hero.live < 0:
        screen.blit(bg_game_over, (0,0))
        sound_game_over = pygame.mixer.Sound('./sounds/gameover.wav')
        pygame.mixer.Sound.set_volume(sound_game_over, 0.5)
        pygame.mixer.Sound.play(sound_game_over,-1,0,0)    
    pygame.display.flip()

pygame.quit()
sys.exit()
