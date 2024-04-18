import pygame, json
from models.Constant import Status, Direction, F_gane
from models.Bullet import Bullet

class Hero():
    def __init__(self) -> None:
        self.image = pygame.image.load('./images/player/0/0/0/0.png')
        self.rect = self.image.get_rect()
        self.status = Status.attack_freeze
        self.direction = Direction.right
        self.frame = 0
        self.time_frame_start = 0
        self.speed = 5
        self.live  = 3
        self.score = 0
        self.lst_bullet:list[Bullet] = []
        self.speed_jump = -15
        self.gravity = 0.5
        self.jump_velocity = 0
        self.jumping = True
        self.font = F_gane.f_game_2.value
        self.attack_sound = pygame.mixer.Sound('./sounds/pistol.wav')
        self.die_sound = pygame.mixer.Sound('./sounds/marco.wav')
        self.move_sound = pygame.mixer.Sound('./sounds/button.wav')
        self.file_game = 'hero.json'

    
    def draw(self, screen:pygame.Surface):
        # Xử lý nhảy
        if self.jumping:
            self.jump_velocity += self.gravity
            self.rect.y += self.jump_velocity
            # chạm đất
            if self.rect.y > screen.get_height() - 250:
                self.jumping = False
                self.jump_velocity = 0
        # Load đạn
        for bullet in self.lst_bullet:
            bullet.draw(screen)
            bullet.move()
            if bullet.rect.x > screen.get_width() or bullet.rect.x < 0:
                self.lst_bullet.remove(bullet)
        
        # Thay đổi trạng thái
        time_frame_current = pygame.time.get_ticks()
        if time_frame_current - self.time_frame_start >= 300:
            self.frame += 1
            self.time_frame_start = time_frame_current
        self.update_status()
        # render mạng và điểm lên màn hình
        f_game = pygame.font.Font(self.font, 48)
        title_live = f_game.render(f'Live: {self.live}', True, 'Red')
        title_score = f_game.render(f'Score: {self.score}', True, 'Red')
        screen.blit(title_live, (0,0))
        screen.blit(title_score, (screen.get_width() - title_score.get_width(),0))
        # draw hero
        screen.blit(self.image, self.rect)
    
    def update_status(self):
        img_source = ''
        direction = '0'
        if self.direction == Direction.left:
            direction = '1'
        elif self.direction == Direction.right:
            direction = '0'
        if self.status == Status.freeze:
            img_source = f'./images/player/{direction}/0/{self.status.value}/{self.frame%3}.png'
        elif self.status == Status.move:
            img_source = f'./images/player/{direction}/0/{self.status.value}/{self.frame%4}.png'
        elif self.status == Status.jump:
            img_source = f'./images/player/{direction}/0/{self.status.value}/{self.frame%2}.png'
        elif self.status == Status.attack_freeze:
            img_source = f'./images/player/{direction}/0/{self.status.value}/{self.frame%4}.png'
        elif self.status == Status.attack_move:
            img_source = f'./images/player/{direction}/0/{self.status.value}/{self.frame%4}.png'
        elif self.status == Status.attack_jump:
            img_source = f'./images/player/{direction}/0/{self.status.value}/{self.frame%4}.png'
        elif self.status == Status.die:
            img_source = f'./images/player/{direction}/0/{self.status.value}/{self.frame%19}.png'
        self.image = pygame.image.load(img_source)
    
    def attack(self):
        # Thay đổi trạng thái thành bắn
        self.status = Status.attack_freeze
        # Tạo ra 1 viên đạn theo hướng của hero
        new_bullet = Bullet()
        new_bullet.direction = self.direction
        if self.direction == Direction.left:
            new_bullet.rect.x = self.rect.x - 10
            new_bullet.rect.y = self.rect.y + self.rect.height / 2 - 25
        elif self.direction == Direction.right:
            new_bullet.rect.x = self.rect.x + self.rect.width + 15
            new_bullet.rect.y = self.rect.y + self.rect.height / 2 - 25
        # Đưa đạn vào list
        self.lst_bullet.append(new_bullet)
    
    def jump(self):
        if not self.jumping:
            self.jumping = True
            self.jump_velocity = self.speed_jump
        self.status = Status.attack_jump
    
    def move(self, direction):
        self.status = Status.move
        self.direction = direction
        if self.direction == Direction.left:
            self.rect.x -= self.speed
        elif self.direction == Direction.right:
            self.rect.x += self.speed
    
    def save_game(self):
        data ={"Score":self.score, "Live": self.live}
        with open(self.file_game, 'w') as json_file:
            json.dump(data, json_file)
    
    def load_game(self):
        with open(self.file_game, 'r') as json_file:
            data = json.load(json_file)
            self.score = data["Score"]
            self.live = data["Live"]