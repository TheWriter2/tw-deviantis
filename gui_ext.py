class Vector2:
    def __init__(self, x=0, y=0):
        self.x = x
        self.y = y

        self.tuple = (self.x, self.y)

class Item:
    def __init__(self, type="", text="", size=Vector2(), position=(), font_size=20, events={}):
        self.type = type
        self.text = text
        self.size = size
        self.font_size = font_size
        self.position = position
        self.events = events

class Screen:
    def __init__(self, title="", topbar_style=0, topbar_font="default", button_style=0, items=[]):
        self.title = title

        self.topbar_style = topbar_style
        self.topbar_font = topbar_font
        
        self.button_style = button_style
        
        self.items = items

class Topbar:
    def __init__(self, color, back_color, height_scale = 0.1):
        self.color = color
        self.background_color = back_color
        self.height_scale = height_scale

class Button:
    def __init__(self, font, color, back_color, hover_color):
        self.font = font
        self.color = color,
        self.background_color = back_color
        self.hover_color = hover_color