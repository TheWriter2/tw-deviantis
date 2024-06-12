import pygame
import json

pygame.init()

class Vector2:
    def __init__(self, x=0, y=0):
        self.x = x
        self.y = y

        self.tuple = (self.x, self.y)

class Item:
    def __init__(self, type="", text="", size=Vector2(), position=(), events={}):
        self.type = type
        self.text = text
        self.size = size
        self.position = position
        self.events = events

class Screen:
    def __init__(self, title="", topbar_style=0, button_style=0, items=[]):
        self.title = title
        self.topbar_style = topbar_style
        self.button_style = button_style
        self.items = items

class Topbar:
    def __init__(self, font, color, back_color, height_scale = 0.1):
        self.font = font
        self.color = color
        self.background_color = back_color
        self.height_scale = height_scale

class Button:
    def __init__(self, font, color, back_color, hover_color):
        self.font = font
        self.color = color,
        self.background_color = back_color
        self.hover_color = hover_color

class App:
    def __init__(self, width, height):
        self.display = pygame.display.set_mode((width, height))
        self.clock = pygame.time.Clock()
        self.state = 0
    
    def start(self):
        self.state = 2

        print("Initializing...")

        m_hover = 0

        # Loading Fonts
        self.font_default_title = pygame.font.Font(size=36)
        self.font_default_text = pygame.font.Font(size=20)

        # Defining Topbars
        self.topbars = [
            Topbar(self.font_default_title, "white", pygame.color.Color(0, 100, 100), 0.08)
        ]

        # Defining Items
        self.buttons = [
            Button(self.font_default_text, pygame.color.Color(0, 0, 0), pygame.color.Color(0, 220, 160), pygame.color.Color(0, 250, 200))
        ]

        # Loading Main Screen
        temp_file = open("screens/main.json", "r")
        temp_screen = json.loads(temp_file.read())

        temp_file.close()

        self.screen = self.load_screen_from_json(temp_screen)

        # Debug
        print("[DEBUG]")
        print("Screen Loaded: " + str(self.screen.title))
        print("Items:")
        for i in self.screen.items:
            print("= " + str(i.type))
            print("= " + str(i.text))

        # Main Loop
        self.state = 1
        while self.state == 1:
            # Event Handling
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.state = 0
                    break
            
            # Start Drawing
            if (self.screen.topbar_style == 0):
                self.display.fill(pygame.color.Color(0, 50, 50))
            else:
                self.display.fill("white")

            # Topbar
            c_topbar = self.topbars[self.screen.topbar_style]

            self.display.fill(c_topbar.background_color, pygame.rect.Rect(0.0, 0.0, self.display.get_width(), self.display.get_height() * c_topbar.height_scale))
            self.display.blit(c_topbar.font.render(self.screen.title, True, c_topbar.color, None), pygame.rect.Rect(self.display.get_width() / 100, self.center_font(self.display.get_height() * c_topbar.height_scale, c_topbar.font.get_height()), 0.0, 0.0))

            # Items
            c_button = self.buttons[self.screen.button_style]
            for i in self.screen.items:
                if i.type == "button":
                    self.display.fill(c_button.background_color, pygame.rect.Rect(i.position.x, i.position.y, i.size.x, i.size.y))
                    self.display.blit(
                        c_button.font.render(i.text, True, c_button.color, None),
                        pygame.rect.Rect(i.position.x + (i.position.x / 2) - (i.size.x / 2), self.center_font((i.position.y * 2) + i.size.y, c_button.font.get_height()), 0.0, 0.0)
                    )

            # Update
            pygame.display.flip()

            self.clock.tick(60.0)
        
        pygame.quit()
    
    def center_font(self, surface_height, font_height):
        return surface_height / 2 - (font_height / 2)

    def load_screen_from_json(self, loaded_json):
        new_screen = Screen(loaded_json["title"], loaded_json["topbar_style"], loaded_json["button_style"])
        for i in loaded_json["items"]:
            new_screen.items.append(Item(
                i["type"].lower(),
                i["text"],
                Vector2(i["size"]["x"], i["size"]["y"]),
                Vector2(i["position"]["x"], i["position"]["y"])
            ))

        return new_screen