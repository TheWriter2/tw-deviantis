import pygame
import json
import gui_ext
import math

pygame.init()

class App:
    def __init__(self, width, height):
        self.display = pygame.display.set_mode((width, height))
        self.clock = pygame.time.Clock()
        self.state = 0
    
    def start(self):
        self.state = 2

        print("Initializing...")

        m_hover = 0

        # Defining Fonts
        self.fonts = {
            "default":None
        }

        # Defining Topbars
        self.topbars = [
            gui_ext.Topbar("white", pygame.color.Color(0, 100, 100), 0.08)
        ]

        # Defining Items
        self.buttons = [
            gui_ext.Button("default", pygame.color.Color(0, 0, 0), pygame.color.Color(0, 220, 160), pygame.color.Color(0, 250, 200))
        ]

        # Loading Main Screen
        temp_file = open("screens/main.json", "r")
        temp_screen = json.loads(temp_file.read())

        temp_file.close()

        self.screen = self.load_screen_from_json(temp_screen)

        # Debug
        #print("[DEBUG]")
        #print("Screen Loaded: " + str(self.screen.title))
        #print("Items:")
        #for i in self.screen.items:
        #    print("= " + str(i.type))
        #    print("= " + str(i.text))

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
            c_topbar_font = pygame.font.Font(self.fonts[self.screen.topbar_font], 32)

            self.display.fill(c_topbar.background_color, pygame.rect.Rect(0.0, 0.0, self.display.get_width(), self.display.get_height() * c_topbar.height_scale))
            self.display.blit(
                c_topbar_font.render(self.screen.title, True, c_topbar.color, None),
                c_topbar_font.render(self.screen.title, True, c_topbar.color, None).get_rect(center=(self.display.get_width() / 2, (self.display.get_height() * c_topbar.height_scale) / 2))
            )

            # Items
            c_button = self.buttons[self.screen.button_style]
            c_button_font = pygame.font.Font(size=20)
            c_button_size = 20
            for i in self.screen.items:
                if i.type == "button":
                    c_button_size = i.font_size
                    c_button_font = pygame.font.Font(self.fonts[c_button.font], c_button_size)
                    self.display.fill(c_button.background_color, pygame.rect.Rect(i.position.x, i.position.y, i.size.x, i.size.y))
                    self.display.blit(
                        c_button_font.render(i.text, True, c_button.color, None),
                        c_button_font.render(i.text, True, c_button.color, None).get_rect(center=(i.position.x + (i.size.x / 2), i.position.y + (i.size.y / 2)))
                    )

            # Update
            pygame.display.flip()

            self.clock.tick(60.0)
        
        pygame.quit()
    
    def center_font(self, surface_height, font_height):
        return surface_height / 2 - (font_height / 2)

    def load_screen_from_json(self, loaded_json):
        new_screen = gui_ext.Screen(loaded_json["title"], loaded_json["topbar"]["style"], loaded_json["topbar"]["font"], loaded_json["style"]["button"])
        for i in loaded_json["items"]:
            new_screen.items.append(gui_ext.Item(
                i["type"].lower(),
                i["text"],
                gui_ext.Vector2(i["size"]["x"], i["size"]["y"]),
                gui_ext.Vector2(i["position"]["x"], i["position"]["y"]),
                i["font_size"]
            ))

        return new_screen