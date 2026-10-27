import json
import math
import os
import random
import pygame

# ============================================================
# FOX'S ADVENTURES - aventura 2D lateral
# Requiere: python -m pip install pygame
# Ejecutar: python fox_adventures.py
# ============================================================

pygame.init()

WIDTH, HEIGHT = 1100, 650
FPS = 60
TITLE = "FOX'S ADVENTURES"
SAVE_FILE = "fox_save.json"

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption(TITLE)
clock = pygame.time.Clock()

FONT = pygame.font.Font(None, 28)
SMALL = pygame.font.Font(None, 22)
MEDIUM = pygame.font.Font(None, 36)
BIG = pygame.font.Font(None, 64)

WHITE = (245, 245, 235)
BLACK = (20, 24, 28)
DARK = (30, 38, 42)
GOLD = (255, 209, 82)
RED = (220, 75, 72)
GREEN = (95, 190, 105)
BLUE = (100, 175, 230)
PURPLE = (160, 110, 220)
ORANGE = (232, 126, 54)

WORLD_WIDTH = 3300
GROUND_Y = 535

def clamp(value, low, high):
    return max(low, min(value, high))

def draw_text(surface, text, x, y, font=FONT, color=WHITE, center=False):
    img = font.render(str(text), True, color)
    rect = img.get_rect()
    if center:
        rect.center = (x, y)
    else:
        rect.topleft = (x, y)
    surface.blit(img, rect)
    return rect

def draw_panel(surface, rect, color=(24, 31, 37, 225), border=(210, 190, 125)):
    panel = pygame.Surface((rect[2], rect[3]), pygame.SRCALPHA)
    panel.fill(color)
    surface.blit(panel, rect[:2])
    pygame.draw.rect(surface, border, rect, 2, border_radius=10)

def save_game(state):
    try:
        with open(SAVE_FILE, "w", encoding="utf-8") as f:
            json.dump(state, f, indent=2, ensure_ascii=False)
        return True
    except OSError:
        return False

def load_game():
    try:
        with open(SAVE_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
        if isinstance(data, dict) and data.get("version") == 1:
            return data
    except (OSError, json.JSONDecodeError):
        pass
    return None

def make_default_save():
    return {
        "version": 1,
        "player_x": 100,
        "hp": 100,
        "potions": 3,
        "crystals": 0,
        "quest": 0,
        "allies": [],
        "defeated": [],
        "seen_intro": False
    }

class Particle:
    def __init__(self, x, y, color):
        self.x, self.y = x, y
        self.vx = random.uniform(-2.4, 2.4)
        self.vy = random.uniform(-4.0, -0.5)
        self.life = random.randint(18, 34)
        self.color = color
        self.size = random.randint(2, 5)

    def update(self):
        self.x += self.vx
        self.y += self.vy
        self.vy += 0.18
        self.life -= 1

    def draw(self, surf, camera_x):
        if self.life > 0:
            pygame.draw.circle(surf, self.color,
                               (int(self.x-camera_x), int(self.y)), self.size)

class Player:
    def __init__(self, x=100, hp=100, potions=3):
        self.x = float(x)
        self.y = float(GROUND_Y - 66)
        self.w, self.h = 46, 66
        self.vx, self.vy = 0.0, 0.0
        self.speed = 5.0
        self.on_ground = True
        self.facing = 1
        self.hp = hp
        self.max_hp = 100
        self.potions = potions
        self.attack_cooldown = 0
        self.invulnerable = 0
        self.attack_flash = 0

    @property
    def rect(self):
        return pygame.Rect(int(self.x), int(self.y), self.w, self.h)

    def update(self, keys, platforms):
        self.vx = 0
        if keys[pygame.K_a] or keys[pygame.K_LEFT]:
            self.vx = -self.speed
            self.facing = -1
        if keys[pygame.K_d] or keys[pygame.K_RIGHT]:
            self.vx = self.speed
            self.facing = 1

        self.x += self.vx
        self.x = clamp(self.x, 0, WORLD_WIDTH - self.w)

        if (keys[pygame.K_SPACE] or keys[pygame.K_w] or keys[pygame.K_UP]) and self.on_ground:
            self.vy = -13.5
            self.on_ground = False

        previous_bottom = self.y + self.h
        self.vy += 0.62
        self.vy = min(self.vy, 15)
        self.y += self.vy
        self.on_ground = False

        if self.y + self.h >= GROUND_Y:
            self.y = GROUND_Y - self.h
            self.vy = 0
            self.on_ground = True

        for plat in platforms:
            rect = pygame.Rect(*plat)
            player_rect = self.rect
            if player_rect.colliderect(rect) and self.vy >= 0 and previous_bottom <= rect.top + 12:
                self.y = rect.top - self.h
                self.vy = 0
                self.on_ground = True

        if self.attack_cooldown > 0:
            self.attack_cooldown -= 1
        if self.invulnerable > 0:
            self.invulnerable -= 1
        if self.attack_flash > 0:
            self.attack_flash -= 1

    def attack_rect(self):
        if self.facing == 1:
            return pygame.Rect(int(self.x + self.w - 2), int(self.y + 12), 48, 38)
        return pygame.Rect(int(self.x - 46), int(self.y + 12), 48, 38)

    def draw(self, surf, camera_x):
        x, y = int(self.x-camera_x), int(self.y)
        if self.invulnerable and (self.invulnerable // 5) % 2 == 0:
            return
        # Cola
        tail_points = [(x+10, y+43), (x-12 if self.facing == 1 else x+58, y+37),
                       (x-4 if self.facing == 1 else x+50, y+55), (x+15, y+54)]
        pygame.draw.polygon(surf, ORANGE, tail_points)
        # Cuerpo y cabeza
        pygame.draw.ellipse(surf, (226, 112, 44), (x+5, y+25, 36, 37))
        pygame.draw.circle(surf, (239, 130, 49), (x+25, y+19), 20)
        # Orejas
        pygame.draw.polygon(surf, (225, 108, 43), [(x+10,y+8),(x+9,y-9),(x+21,y+4)])
        pygame.draw.polygon(surf, (225, 108, 43), [(x+29,y+4),(x+42,y-8),(x+40,y+13)])
        pygame.draw.polygon(surf, (250, 190, 165), [(x+12,y+3),(x+12,y-3),(x+17,y+4)])
        # Hocico
        muzzle_x = x+36 if self.facing == 1 else x+1
        pygame.draw.ellipse(surf, (255, 220, 178), (muzzle_x, y+17, 15, 11))
        pygame.draw.circle(surf, BLACK, (x+31 if self.facing == 1 else x+17, y+15), 2)
        pygame.draw.circle(surf, BLACK, (x+47 if self.facing == 1 else x+1, y+21), 2)
        # Pecho
        pygame.draw.ellipse(surf, (255, 219, 165), (x+17, y+32, 20, 25))
        # Patas
        pygame.draw.rect(surf, (100, 60, 38), (x+11,y+53,9,12), border_radius=3)
        pygame.draw.rect(surf, (100, 60, 38), (x+30,y+53,9,12), border_radius=3)
        if self.attack_flash > 0:
            ar = self.attack_rect()
            pygame.draw.arc(surf, GOLD, (ar.x-camera_x, ar.y, ar.w, ar.h), 0.2, 2.9, 5)

class Enemy:
    def __init__(self, name, x, hp, damage, color, kind="sombra", boss=False):
        self.name = name
        self.x = float(x)
        self.y = GROUND_Y - 48
        self.w, self.h = (62, 70) if boss else (44, 48)
        self.hp = hp
        self.max_hp = hp
        self.damage = damage
        self.color = color
        self.kind = kind
        self.boss = boss
        self.alive = True
        self.direction = random.choice([-1, 1])
        self.patrol_origin = x
        self.cooldown = 0
        self.hit_flash = 0

    @property
    def rect(self):
        return pygame.Rect(int(self.x), int(self.y), self.w, self.h)

    def update(self, player):
        if not self.alive:
            return
        if self.cooldown > 0:
            self.cooldown -= 1
        if self.hit_flash > 0:
            self.hit_flash -= 1
        if abs(player.x - self.x) < 260:
            self.direction = 1 if player.x > self.x else -1
            self.x += self.direction * (1.0 if self.boss else 1.35)
        else:
            self.x += self.direction * 0.7
            if abs(self.x - self.patrol_origin) > 95:
                self.direction *= -1
        self.x = clamp(self.x, 0, WORLD_WIDTH - self.w)

    def draw(self, surf, camera_x):
        if not self.alive:
            return
        x, y = int(self.x-camera_x), int(self.y)
        color = WHITE if self.hit_flash else self.color
        if self.kind == "lobo":
            pygame.draw.ellipse(surf, color, (x+4,y+14,self.w-8,self.h-16))
            pygame.draw.polygon(surf, color, [(x+10,y+18),(x+6,y),(x+23,y+14)])
            pygame.draw.polygon(surf, color, [(x+30,y+15),(x+42,y+1),(x+40,y+24)])
            pygame.draw.circle(surf, GOLD, (x+31,y+25), 3)
        elif self.boss:
            pygame.draw.ellipse(surf, color, (x+4,y+12,self.w-8,self.h-12))
            pygame.draw.polygon(surf, color, [(x+8,y+22),(x-4,y-2),(x+22,y+14)])
            pygame.draw.polygon(surf, color, [(x+42,y+18),(x+60,y-4),(x+52,y+29)])
            pygame.draw.circle(surf, RED, (x+43,y+30), 4)
            pygame.draw.circle(surf, RED, (x+24,y+30), 4)
        else:
            pygame.draw.ellipse(surf, color, (x+2,y+9,self.w-4,self.h-8))
            pygame.draw.circle(surf, color, (x+self.w//2,y+12), 16)
            pygame.draw.circle(surf, RED, (x+14,y+18), 3)
            pygame.draw.circle(surf, RED, (x+29,y+18), 3)
        # Barra de vida
        bar_w = self.w
        pygame.draw.rect(surf, (50,25,25), (x,y-10,bar_w,6), border_radius=3)
        pygame.draw.rect(surf, RED, (x,y-10,int(bar_w*max(0,self.hp)/self.max_hp),6), border_radius=3)
        draw_text(surf, self.name, x + self.w//2, y-25, SMALL, WHITE, center=True)

class NPC:
    def __init__(self, name, x, color, message, ally_id):
        self.name, self.x, self.color = name, x, color
        self.message, self.ally_id = message, ally_id
        self.w, self.h = 42, 58
        self.y = GROUND_Y - self.h

    @property
    def rect(self):
        return pygame.Rect(int(self.x), int(self.y), self.w, self.h)

    def draw(self, surf, camera_x, met):
        x, y = int(self.x-camera_x), int(self.y)
        pygame.draw.ellipse(surf, self.color, (x+4,y+15,34,40))
        pygame.draw.circle(surf, self.color, (x+21,y+13), 15)
        pygame.draw.circle(surf, WHITE, (x+16,y+12), 3)
        pygame.draw.circle(surf, WHITE, (x+26,y+12), 3)
        pygame.draw.circle(surf, BLACK, (x+16,y+12), 1)
        pygame.draw.circle(surf, BLACK, (x+26,y+12), 1)
        draw_text(surf, self.name, x+21, y-13, SMALL, GOLD if met else WHITE, center=True)
        if not met:
            draw_text(surf, "E", x+21, y-31, SMALL, GOLD, center=True)

class Game:
    def __init__(self):
        self.state = "menu"
        self.data = make_default_save()
        self.player = None
        self.camera_x = 0
        self.enemies = []
        self.npcs = []
        self.platforms = []
        self.particles = []
        self.dialog = None
        self.dialog_timer = 0
        self.message = ""
        self.message_timer = 0
        self.attack_pressed = False
        self.interact_pressed = False
        self.quest_names = [
            "Habla con la anciana del pueblo",
            "Derrota a las Sombras del Bosque",
            "Rescata a Luma, la exploradora",
            "Encuentra la entrada de las ruinas",
            "Derrota al Guardián y recupera el cristal"
        ]
        self.setup_world()

    def setup_world(self):
        self.platforms = [(360, 430, 150, 18), (720, 385, 140, 18),
                          (1120, 440, 170, 18), (1570, 390, 160, 18),
                          (2040, 430, 150, 18), (2550, 390, 180, 18)]
        self.enemies = [
            Enemy("Sombra", 560, 34, 8, (83, 90, 125)),
            Enemy("Lobo salvaje", 900, 42, 10, (110, 120, 135), "lobo"),
            Enemy("Sombra", 1320, 38, 9, (83, 90, 125)),
            Enemy("Lobo salvaje", 1730, 48, 12, (110, 120, 135), "lobo"),
            Enemy("Sombra antigua", 2240, 55, 13, (95, 70, 135)),
            Enemy("Guardián del Cristal", 2920, 190, 17, (65, 55, 105), boss=True)
        ]
        self.npcs = [
            NPC("Anciana Mara", 210, (150, 95, 65),
                "El cristal protege nuestra aldea. Ve al bosque y busca las marcas azules.", "mara"),
            NPC("Luma", 1480, (90, 155, 125),
                "¡Gracias por rescatarme! Te acompañaré con consejos. Las ruinas están al este.", "luma"),
            NPC("Timo", 2400, (95, 135, 190),
                "Soy Timo, guardián de los senderos. Te dejo una poción para el último combate.", "timo")
        ]

    def new_game(self):
        self.data = make_default_save()
        self.player = Player()
        self.state = "playing"
        self.camera_x = 0
        self.setup_world()
        self.say("¡Comienza tu aventura! Acércate a Mara y presiona E.", 240)

    def continue_game(self):
        data = load_game()
        if not data:
            self.say("No hay una partida guardada. Elegí Nueva partida.", 180)
            return
        self.data = data
        self.player = Player(data.get("player_x", 100), data.get("hp", 100), data.get("potions", 3))
        self.state = "playing"
        self.setup_world()
        defeated = set(data.get("defeated", []))
        for enemy in self.enemies:
            if enemy.name + ":" + str(int(enemy.patrol_origin)) in defeated:
                enemy.alive = False
                enemy.hp = 0
        self.say("Partida cargada. ¡A seguir la aventura!", 180)

    def save(self):
        if not self.player:
            return
        self.data.update({
            "player_x": int(self.player.x),
            "hp": self.player.hp,
            "potions": self.player.potions,
            "defeated": [e.name + ":" + str(int(e.patrol_origin)) for e in self.enemies if not e.alive]
        })
        if save_game(self.data):
            self.say("Partida guardada.", 120)
        else:
            self.say("No se pudo guardar la partida.", 180)

    def say(self, text, frames=180):
        self.message = text
        self.message_timer = frames

    def open_dialog(self, title, text, choices=None):
        self.dialog = (title, text, choices or [])
        self.state_before_dialog = self.state
        self.state = "dialog"

    def close_dialog(self):
        self.dialog = None
        self.state = getattr(self, "state_before_dialog", "playing")

    def quest_progress(self):
        quest = self.data["quest"]
        if quest == 0:
            return "Misión: habla con Mara"
        if quest == 1:
            alive = sum(1 for e in self.enemies[:3] if e.alive)
            return f"Misión: derrota a las Sombras del Bosque ({3-alive}/3)"
        if quest == 2:
            return "Misión: encuentra a Luma y presiona E"
        if quest == 3:
            return "Misión: llega a las ruinas al este"
        if quest == 4:
            return "Misión: derrota al Guardián del Cristal"
        return "¡Misión cumplida: el cristal volvió a la aldea!"

    def interact(self):
        p = self.player
        nearby_npc = next((n for n in self.npcs if abs((n.x+20)-(p.x+p.w/2)) < 85), None)
        if nearby_npc:
            if nearby_npc.ally_id == "mara":
                if self.data["quest"] == 0:
                    self.data["quest"] = 1
                    self.open_dialog("Mara, la anciana",
                        "El cristal fue robado por una criatura de las ruinas. Derrota a tres enemigos del bosque y sigue hacia el este.")
                else:
                    self.open_dialog("Mara", "Confío en vos, pequeño héroe. ¡La aldea necesita el cristal!")
            elif nearby_npc.ally_id == "luma":
                if "Luma" not in self.data["allies"]:
                    self.data["allies"].append("Luma")
                    self.data["quest"] = max(self.data["quest"], 3)
                    self.open_dialog("Luma se une a tu aventura",
                        nearby_npc.message + " Como agradecimiento, recuperaste 15 puntos de vida.")
                    self.player.hp = min(self.player.max_hp, self.player.hp + 15)
                else:
                    self.open_dialog("Luma", "¡Sigamos! No falta mucho para las ruinas.")
            elif nearby_npc.ally_id == "timo":
                if "Timo" not in self.data["allies"]:
                    self.data["allies"].append("Timo")
                    self.player.potions += 1
                    self.open_dialog("Timo, guardián del sendero",
                        nearby_npc.message + " Recibiste una poción.")
                else:
                    self.open_dialog("Timo", "¡El Guardián está al final del camino. Ten cuidado!")
            return

        if self.player.x > 2730 and self.data["quest"] >= 3:
            self.data["quest"] = 4
            self.say("Has llegado a las ruinas. ¡El Guardián protege el cristal!", 240)
            return
        self.say("No hay nadie cerca para hablar. Acércate a un personaje.", 120)

    def attack(self):
        p = self.player
        if p.attack_cooldown > 0:
            return
        p.attack_cooldown = 24
        p.attack_flash = 8
        hitbox = p.attack_rect()
        hit_any = False
        for enemy in self.enemies:
            if enemy.alive and hitbox.colliderect(enemy.rect):
                damage = random.randint(16, 24)
                enemy.hp -= damage
                enemy.hit_flash = 7
                hit_any = True
                for _ in range(8):
                    self.particles.append(Particle(enemy.x+enemy.w/2, enemy.y+20, GOLD))
                self.say(f"¡Golpeaste a {enemy.name}! -{damage} HP", 75)
                if enemy.hp <= 0:
                    enemy.alive = False
                    self.data["crystals"] += 1
                    if enemy.name == "Guardián del Cristal":
                        self.data["quest"] = 5
                        self.open_dialog("¡Victoria!", "¡Derrotaste al Guardián y recuperaste el Cristal de Fox! La aldea vuelve a estar a salvo.")
                    elif self.data["quest"] == 1 and sum(1 for e in self.enemies[:3] if e.alive) == 0:
                        self.data["quest"] = 2
                        self.say("¡El bosque está despejado! Busca a Luma en el sendero.", 240)
                break
        if not hit_any:
            self.say("Tu golpe no alcanzó a ningún enemigo.", 45)

    def use_potion(self):
        if self.player.potions > 0 and self.player.hp < self.player.max_hp:
            self.player.potions -= 1
            self.player.hp = min(self.player.max_hp, self.player.hp + 35)
            self.say("Usaste una poción: +35 HP.", 120)
            for _ in range(12):
                self.particles.append(Particle(self.player.x+20, self.player.y+20, GREEN))
        elif self.player.potions <= 0:
            self.say("No te quedan pociones.", 100)
        else:
            self.say("Tu vida ya está completa.", 100)

    def update(self, keys):
        if self.state != "playing" or not self.player:
            return
        self.player.update(keys, self.platforms)
        for enemy in self.enemies:
            enemy.update(self.player)
            if enemy.alive and enemy.rect.colliderect(self.player.rect) and enemy.cooldown == 0:
                if self.player.invulnerable == 0:
                    self.player.hp -= enemy.damage
                    self.player.invulnerable = 55
                    enemy.cooldown = 60
                    self.say(f"{enemy.name} te hizo {enemy.damage} de daño.", 90)
                    for _ in range(7):
                        self.particles.append(Particle(self.player.x+20, self.player.y+20, RED))
        for part in self.particles[:]:
            part.update()
            if part.life <= 0:
                self.particles.remove(part)
        target_camera = self.player.x - WIDTH * 0.38
        self.camera_x = clamp(target_camera, 0, WORLD_WIDTH - WIDTH)
        if self.message_timer > 0:
            self.message_timer -= 1
        if self.player.hp <= 0:
            self.state = "gameover"

    def draw_background(self):
        # Cielo con degradado por bandas
        for i in range(HEIGHT):
            t = i / HEIGHT
            color = (int(28+30*t), int(53+55*t), int(83+42*t))
            pygame.draw.line(screen, color, (0,i), (WIDTH,i))
        # Luna / sol
        pygame.draw.circle(screen, (255, 230, 165), (875, 105), 42)
        # Montañas
        for i in range(-1, 7):
            bx = i*240 - int(self.camera_x*0.20) % 240
            pygame.draw.polygon(screen, (47, 73, 83),
                [(bx, GROUND_Y), (bx+120, 225+(i%3)*30), (bx+260, GROUND_Y)])
        # Bosque lejano
        for i in range(-1, 17):
            bx = i*100 - int(self.camera_x*0.45) % 100
            pygame.draw.rect(screen, (38, 74, 58), (bx+28, 385, 12, 150))
            pygame.draw.circle(screen, (36, 95, 64), (bx+34, 375), 38)
            pygame.draw.circle(screen, (42, 111, 69), (bx+10, 395), 24)
        # Suelo
        pygame.draw.rect(screen, (70, 100, 56), (0, GROUND_Y, WIDTH, HEIGHT-GROUND_Y))
        pygame.draw.rect(screen, (104, 142, 72), (0, GROUND_Y, WIDTH, 12))
        # Flores y piedras en mundo
        for wx in range(40, WORLD_WIDTH, 135):
            sx = wx - self.camera_x
            if -20 < sx < WIDTH+20:
                pygame.draw.circle(screen, (239, 204, 105), (int(sx), GROUND_Y+30+(wx%17)), 3)
        for plat in self.platforms:
            x, y, w, h = plat
            sx = x-self.camera_x
            pygame.draw.rect(screen, (94, 72, 54), (sx,y,w,h), border_radius=5)
            pygame.draw.rect(screen, (129, 155, 83), (sx,y,w,5), border_radius=3)
        # Hito de ruinas al final
        ruins_x = 2840 - self.camera_x
        pygame.draw.rect(screen, (88, 84, 91), (ruins_x, 380, 24, 155))
        pygame.draw.rect(screen, (88, 84, 91), (ruins_x+90, 380, 24, 155))
        pygame.draw.rect(screen, (103, 97, 100), (ruins_x-10, 365, 145, 22))
        pygame.draw.polygon(screen, (72, 68, 77), [(ruins_x-16,365),(ruins_x+63,315),(ruins_x+140,365)])
        pygame.draw.circle(screen, (100, 210, 255), (int(ruins_x+57), 420), 10)
        pygame.draw.circle(screen, (170, 235, 255), (int(ruins_x+57), 420), 4)

    def draw_hud(self):
        p = self.player
        draw_panel(screen, (16, 14, 315, 90))
        draw_text(screen, "FOX", 29, 21, MEDIUM, ORANGE)
        pygame.draw.rect(screen, (70,35,35), (95, 26, 205, 18), border_radius=6)
        pygame.draw.rect(screen, RED, (95, 26, int(205*max(0,p.hp)/p.max_hp), 18), border_radius=6)
        draw_text(screen, f"HP {max(0,p.hp)}/{p.max_hp}", 100, 47, SMALL)
        draw_text(screen, f"Pociones: {p.potions}   Aliados: {len(self.data['allies'])}", 29, 73, SMALL)
        draw_panel(screen, (WIDTH-410, 14, 394, 62))
        draw_text(screen, self.quest_progress(), WIDTH-395, 28, SMALL, GOLD)
        draw_text(screen, "A/D o ←/→ mover  •  ESPACIO saltar  •  J atacar  •  E hablar  •  Q poción  •  F5 guardar",
                  WIDTH//2, HEIGHT-25, SMALL, WHITE, center=True)

    def draw(self):
        if self.state == "menu":
            self.draw_menu()
            return
        if self.state in ("playing", "dialog", "gameover", "victory"):
            self.draw_background()
            for npc in self.npcs:
                npc.draw(screen, self.camera_x, npc.ally_id in self.data["allies"])
            for enemy in self.enemies:
                enemy.draw(screen, self.camera_x)
            for part in self.particles:
                part.draw(screen, self.camera_x)
            if self.player:
                self.player.draw(screen, self.camera_x)
            self.draw_hud()
            if self.message_timer > 0 and self.message:
                rect = pygame.Rect(150, 112, WIDTH-300, 42)
                draw_panel(screen, rect, (24,31,37,215))
                draw_text(screen, self.message, WIDTH//2, 133, SMALL, WHITE, center=True)
            if self.state == "dialog":
                self.draw_dialog()
            elif self.state == "gameover":
                self.draw_overlay("TE HAN DERROTADO", "Pulsa R para volver a intentarlo o ESC para el menú")
            elif self.state == "victory":
                self.draw_overlay("¡AVENTURA COMPLETADA!", "El Cristal de Fox ha vuelto a la aldea. Pulsa ESC para el menú.")

    def draw_menu(self):
        screen.fill((20, 32, 49))
        # Fondo estilizado
        pygame.draw.circle(screen, (255, 224, 153), (WIDTH-170, 120), 58)
        for i in range(10):
            x = i*135
            pygame.draw.polygon(screen, (35, 67, 68), [(x,HEIGHT),(x+85,280+(i%3)*40),(x+170,HEIGHT)])
        pygame.draw.rect(screen, (54, 87, 49), (0, GROUND_Y, WIDTH, HEIGHT-GROUND_Y))
        pygame.draw.rect(screen, (104, 142, 72), (0, GROUND_Y, WIDTH, 12))
        draw_text(screen, "FOX'S ADVENTURES", WIDTH//2, 150, BIG, ORANGE, center=True)
        draw_text(screen, "El Cristal Robado", WIDTH//2, 208, MEDIUM, GOLD, center=True)
        # Fox icon
        pygame.draw.ellipse(screen, ORANGE, (WIDTH//2-45,300,90,95))
        pygame.draw.circle(screen, (239,130,49), (WIDTH//2, 300), 40)
        pygame.draw.polygon(screen, ORANGE, [(WIDTH//2-28,278),(WIDTH//2-40,235),(WIDTH//2-7,267)])
        pygame.draw.polygon(screen, ORANGE, [(WIDTH//2+15,267),(WIDTH//2+43,236),(WIDTH//2+34,283)])
        pygame.draw.ellipse(screen, (255,220,178), (WIDTH//2+7,300,34,22))
        pygame.draw.circle(screen, BLACK, (WIDTH//2+12,289), 4)
        draw_panel(screen, (WIDTH//2-210, 420, 420, 145))
        draw_text(screen, "ENTER  Nueva partida", WIDTH//2, 448, MEDIUM, WHITE, center=True)
        draw_text(screen, "C  Continuar partida guardada", WIDTH//2, 488, FONT, WHITE, center=True)
        draw_text(screen, "ESC  Salir", WIDTH//2, 526, FONT, WHITE, center=True)
        draw_text(screen, "Una aventura de amistad, valentía y un cristal perdido", WIDTH//2, 605, SMALL, (205,220,210), center=True)

    def draw_dialog(self):
        if not self.dialog:
            return
        title, text, _ = self.dialog
        rect = pygame.Rect(80, HEIGHT-190, WIDTH-160, 145)
        draw_panel(screen, rect, (20,27,33,245), GOLD)
        draw_text(screen, title, rect.x+22, rect.y+15, MEDIUM, GOLD)
        # Wrap text
        words = text.split()
        lines, line = [], ""
        for word in words:
            test = (line+" "+word).strip()
            if FONT.size(test)[0] > rect.width-45:
                lines.append(line)
                line = word
            else:
                line = test
        if line:
            lines.append(line)
        for i, ln in enumerate(lines[:3]):
            draw_text(screen, ln, rect.x+22, rect.y+55+i*25, SMALL, WHITE)
        draw_text(screen, "ENTER / E para continuar", rect.right-245, rect.bottom-26, SMALL, GOLD)

    def draw_overlay(self, title, subtitle):
        shade = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
        shade.fill((0,0,0,175))
        screen.blit(shade, (0,0))
        draw_text(screen, title, WIDTH//2, HEIGHT//2-35, BIG, GOLD, center=True)
        draw_text(screen, subtitle, WIDTH//2, HEIGHT//2+25, FONT, WHITE, center=True)

    def handle_event(self, event):
        if self.state == "menu":
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    self.new_game()
                elif event.key == pygame.K_c:
                    self.continue_game()
                elif event.key == pygame.K_ESCAPE:
                    return False
            return True

        if self.state == "dialog":
            if event.type == pygame.KEYDOWN and event.key in (pygame.K_RETURN, pygame.K_e, pygame.K_SPACE):
                self.close_dialog()
                if self.data.get("quest") == 5:
                    self.state = "victory"
            return True

        if self.state == "gameover":
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    self.new_game()
                elif event.key == pygame.K_ESCAPE:
                    self.state = "menu"
            return True

        if self.state == "victory":
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                self.state = "menu"
            return True

        if self.state == "playing" and event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                self.state = "menu"
            elif event.key == pygame.K_j:
                self.attack()
            elif event.key == pygame.K_e:
                self.interact()
            elif event.key == pygame.K_q:
                self.use_potion()
            elif event.key == pygame.K_F5:
                self.save()
            elif event.key == pygame.K_F9:
                self.continue_game()
        return True

    def run(self):
        running = True
        while running:
            clock.tick(FPS)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif not self.handle_event(event):
                    running = False
            keys = pygame.key.get_pressed()
            self.update(keys)
            self.draw()
            pygame.display.flip()
        pygame.quit()

if __name__ == "__main__":
    Game().run()
