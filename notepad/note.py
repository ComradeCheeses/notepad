import pygame

class Note():
    def __init__(self, coords: tuple, surface, display: None):
        pygame.init()
        self.pos = coords
        self.surface = surface
        self.display = display if display else surface
        self.title = 'BLANK NOTE'
        self.body = 'BLANK NOTE'

    def changecoords(self, newcoords):
        self.pos = newcoords

    def data_set(self, newtitle, newbody):
        self.title = newtitle
        self.body = newbody
    
    def data_get(self):
        return {'title': self.title, 'body': self.body}
    
    def disp(self, offset: int):

        font = pygame.font.Font('freesansbold.ttf', 32)

        self.coords = (self.pos[0], self.pos[1]-offset)
        pygame.draw.polygon(self.surface, (100, 100, 100), (self.coords, (self.coords[0]+490, self.coords[1]), (self.coords[0]+490, self.coords[1]+42), (self.coords[0], self.coords[1]+42)))
        self.surface.blit(font.render(self.title, True, (30, 30, 30), (100, 100, 100)), (self.coords[0]+5, self.coords[1]+5))
        pygame.draw.polygon(self.surface, (30, 30, 30), ((self.coords[0]+453, self.coords[1]+5), (self.coords[0]+485, self.coords[1]+5), (self.coords[0]+485, self.coords[1]+37), (self.coords[0]+453, self.coords[1]+37)))
        self.surface.blit(font.render('D', True, (100, 100, 100), (30, 30, 30)), (self.coords[0]+458, self.coords[1]+6))
        pygame.draw.polygon(self.surface, (30, 30, 30), ((self.coords[0]+416, self.coords[1]+5), (self.coords[0]+448, self.coords[1]+5), (self.coords[0]+448, self.coords[1]+37), (self.coords[0]+416, self.coords[1]+37)))
        self.surface.blit(font.render('E', True, (100, 100, 100), (30, 30, 30)), (self.coords[0]+421, self.coords[1]+6))
        pygame.draw.polygon(self.surface, (30, 30, 30), ((self.coords[0]+379, self.coords[1]+5), (self.coords[0]+411, self.coords[1]+5), (self.coords[0]+411, self.coords[1]+37), (self.coords[0]+379, self.coords[1]+37)))
        self.surface.blit(font.render('R', True, (100, 100, 100), (30, 30, 30)), (self.coords[0]+384, self.coords[1]+6))
    
    def getbuttoncoords(self, offset):
        self.coords = (self.pos[0], self.pos[1]-offset)

        return [((self.coords[0]+453, self.coords[1]+5), (self.coords[0]+485, self.coords[1]+5), (self.coords[0]+485, self.coords[1]+37), (self.coords[0]+453, self.coords[1]+37)),
        ((self.coords[0]+416, self.coords[1]+5), (self.coords[0]+448, self.coords[1]+5), (self.coords[0]+448, self.coords[1]+37), (self.coords[0]+416, self.coords[1]+37)),
        ((self.coords[0]+379, self.coords[1]+5), (self.coords[0]+411, self.coords[1]+5), (self.coords[0]+411, self.coords[1]+37), (self.coords[0]+379, self.coords[1]+37))]


