import pgzrun

WIDTH = 587
HEIGHT = 626
TITLE = "Plataforma Teste"

BOX = Rect((WIDTH - 30, HEIGHT - 30), (30, 30))

game_state = "menu"  # 'menu' or 'playing'

class Player(Actor):
    def __init__(self, x, y):
        super().__init__("idle")
        self.pos = (x, y)
        self.x_speed = 300
        self.y_speed = 300
        self.walk_frame = 0
        self.walk_animation_speed = 0.1
        self.walk_timer = 0

    def animate_walking(self, dt):
        self.walk_timer += dt
        if self.walk_timer >= self.walk_animation_speed:
            self.walk_timer = 0
            self.walk_frame = (self.walk_frame + 1) % 2
            self.image = f"walk_{'a' if self.walk_frame == 0 else 'b'}"

    def update(self, dt):
         # Prevent the player from moving below the bottom edge
        if self.bottom > HEIGHT:
            self.bottom = HEIGHT
        # Prevent the player from moving above the top edge
        if self.top < 0:
            self.top = 0
        # Prevent the player from moving beyond the left edge
        if self.left < 0:
            self.left = 0
        # Prevent the player from moving beyond the right edge
        if self.right > WIDTH:
            self.right = WIDTH

        if self.y_speed == 0 and not (keyboard.left or keyboard.right or keyboard.up or keyboard.down):
            self.image = "idle"

        if keyboard.left:
            self.x -= self.x_speed * dt
            self.animate_walking(dt)
        if keyboard.right:
            self.x += self.x_speed * dt
            self.animate_walking(dt)

        if keyboard.up:
            self.y -= self.y_speed * dt
            self.animate_walking(dt)
        if keyboard.down:
            self.y += self.y_speed * dt
            self.animate_walking(dt)

class Enemy(Actor):
    def __init__(self, x, y, image="saw_a"):
        super().__init__(image)
        self.pos = (x, y)
        self.speed = 200
        self.direction = 1

    def update(self, dt):
        self.x += self.direction * self.speed * dt
        if self.left < 0 or self.right > WIDTH:
            self.direction *= -1

class Platform(Actor):
    def __init__(self, x, y, width, height):
        super().__init__("platform")
        self.pos = (x, y)
        self.width = width
        self.height = height

    def draw(self):
        screen.draw.rect(self.topleft, (self.width, self.height), (0, 0, 0))

player = Player(100, 100)
enemy = Enemy(400, HEIGHT - 40)

def update(dt):
    if game_state == "playing":
        player.update(dt)
        enemy.update(dt)

def draw():
    screen.clear()
    screen.fill((255, 255, 255))
    if game_state == "menu":
        screen.draw.text("PLATAFORMA TESTE", center=(WIDTH//2, HEIGHT//2 - 50), fontsize=60, color="black")
        screen.draw.text("Pressione ENTER para jogar", center=(WIDTH//2, HEIGHT//2 + 20), fontsize=40, color="gray")
    elif game_state == "playing":
        screen.blit("background", (0, 0))  # Draw background image at the top-left corner
        player.draw()
        enemy.draw()

def on_key_down(key):
    global game_state
    if game_state == "menu" and key == keys.RETURN:
        game_state = "playing"

pgzrun.go()