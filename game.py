import pgzrun

WIDTH = 587
HEIGHT = 626
TITLE = "Jogo KODLAND"

game_state = "menu"  # 'menu', 'playing', or 'gameover'
music_on = True  # Track music state

# Button rectangles for click detection
play_button_rect = Rect((WIDTH//2 - 100, HEIGHT//2 - 30), (200, 60))
music_button_rect = Rect((WIDTH//2 - 100, HEIGHT//2 + 50), (200, 60))
quit_button_rect = Rect((WIDTH//2 - 100, HEIGHT//2 + 130), (200, 60))

class Player(Actor):
    def __init__(self, x, y):
        super().__init__("idle")
        self.start_pos = (x, y)  # Store starting position for reset
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

    def reset(self):
        self.pos = self.start_pos  # Reset to starting position
        self.image = "idle"  # Reset to idle sprite

class Enemy(Actor):
    def __init__(self, x, y, image="saw_a"):
        super().__init__(image)
        self.pos = (x, y)
        self.x_speed = 200
        self.y_speed = 200
        self.x_direction = 1
        self.y_direction = 1
        self.frame = 0
        self.animation_speed = 0.15
        self.timer = 0

    def animate(self, dt):
        self.timer += dt
        if self.timer >= self.animation_speed:
            self.timer = 0
            self.frame = (self.frame + 1) % 2
            self.image = f"saw_{'a' if self.frame == 0 else 'b'}"

    def update(self, dt):
        # Move diagonally
        self.x += self.x_direction * self.x_speed * dt
        self.y += self.y_direction * self.y_speed * dt
        # Bounce off horizontal edges
        if self.left < 0 or self.right > WIDTH:
            self.x_direction *= -1
        # Bounce off vertical edges
        if self.top < 0 or self.bottom > HEIGHT:
            self.y_direction *= -1
        # Animate saw
        self.animate(dt)

player = Player(100, 100)
enemy = Enemy(400, HEIGHT - 40)

def update(dt):
    global game_state
    if game_state == "playing":
        player.update(dt)
        enemy.update(dt)
        # Check for collision between player and enemy
        if player.colliderect(enemy):
            sounds.hurt.play()  # Play hurt sound
            music.stop()  # Stop background music
            game_state = "gameover"  # Switch to game over state

def draw():
    screen.clear()
    screen.fill((255, 255, 255))
    if game_state == "menu":
        screen.draw.text("Jogo KODLAND", center=(WIDTH//2, HEIGHT//2 - 150), fontsize=60, color="black")
        # Draw buttons as textboxes with colored backgrounds
        screen.draw.filled_rect(play_button_rect, (100, 100, 100))  # Gray background
        screen.draw.textbox("Jogar", play_button_rect)
        screen.draw.filled_rect(music_button_rect, (100, 100, 100))
        screen.draw.textbox("Música: " + ("Ligada" if music_on else "Desligada"), music_button_rect)
        screen.draw.filled_rect(quit_button_rect, (100, 100, 100))
        screen.draw.textbox("Sair", quit_button_rect)
    elif game_state == "playing":
        screen.blit("background", (0, 0))  # Draw background image
        player.draw()
        enemy.draw()
    elif game_state == "gameover":
        screen.draw.text("Game Over", center=(WIDTH//2, HEIGHT//2 - 50), fontsize=60, color="red")
        screen.draw.text("Pressione R para reiniciar", center=(WIDTH//2, HEIGHT//2 + 20), fontsize=40, color="gray")

def on_key_down(key):
    global game_state
    if game_state == "gameover" and key == keys.R:
        game_state = "playing"
        player.reset()  # Reset player position
        enemy.pos = (400, HEIGHT - 40)  # Reset enemy position
        enemy.x_direction = 1  # Reset enemy direction
        enemy.y_direction = 1
        if music_on:
            music.play('music')  # Restart background music if enabled

def on_mouse_down(pos):
    global game_state, music_on
    if game_state == "menu":
        if play_button_rect.collidepoint(pos):
            game_state = "playing"
            if music_on:
                music.play('music')  # Start background music
                music.set_volume(0.5)  # Set music volume to 50%
            sounds.hurt.set_volume(0.7)  # Set hurt sound volume to 70%
        elif music_button_rect.collidepoint(pos):
            music_on = not music_on  # Toggle music state
            if not music_on:
                music.stop()  # Stop music if toggled off
            elif game_state == "playing":
                music.play('music')  # Resume music if toggled on during play
                music.set_volume(0.5)
        elif quit_button_rect.collidepoint(pos):
            pgzrun.quit()  # Quit the game using Pygame Zero's quit function

pgzrun.go()