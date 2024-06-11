import pygame

pygame.init()

class App:
    def __init__(self, width, height):
        self.display = pygame.display.set_mode((width, height))
        self.clock = pygame.time.Clock()
        self.state = 0
    
    def start(self):
        self.state = 1

        while self.state == 1:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.state = 0
                    break
            
            self.display.fill("white")
            pygame.display.flip()

            self.clock.tick(60.0)
        
        pygame.quit()