from note import Note
import pygame
import sqlite3
import settings
import os

# Consider adding email verification

class Notepad():
    def __init__(self):
        pygame.init()
        self.fontS = pygame.font.Font('freesansbold.ttf', 24)
        self.font = pygame.font.Font('freesansbold.ttf', 32)
        self.dbname = settings.DBNAME
        self.connection = sqlite3.connect(f'{os.path.dirname(__file__)}/data/{self.dbname}')
        self.display = pygame.display.set_mode((500, 500))
        self.cur = self.connection.cursor()
        try: self.cur.execute('CREATE TABLE notes (title TEXT, body TEXT, coord1 INTEGER, coord2 INTEGER)')
        except: pass
        #for i in range(15):
        #    self.cur.execute('INSERT INTO notes VALUES ("title", "body", 5, ?)', ((i*47)+5,))
        self.notes = self.cur.execute('SELECT title, body, coord1, coord2 FROM notes').fetchall()
        self.notelist = [Note((i[2], i[3]), self.display, None) for i in self.notes]
        [note.data_set(data[0], data[1]) for note, data in zip(self.notelist, self.notes)]
        self.connection.commit()
    
    def collide(self, point, polygon):
        assert len(polygon) >= 3

        px, py = point
        n = len(polygon)

        for i in range(n):
            x0, y0 = polygon[i]
            x1, y1 = polygon[(i+1) % n]
            x2, y2 = polygon[(i+2) % n]

            area1 = abs((x0-px)*(y1-py) - (x1-px)*(y0-py))
            area2 = abs((x1-px)*(y2-py) - (x2-px)*(y1-py))
            area3 = abs((x2-px)*(y0-py) - (x0-px)*(y2-py))

            area = abs((x1-x0)*(y2-y0) - (x2-x0)*(y1-y0))
            if area1 + area2 + area3 == area:
                return True

        return False

    def read(self, index):
        note = self.notelist[index]
        data = note.data_get()
        title = data.get('title')
        body = data.get('body')
        self.display.fill((30, 30, 30))
        while True:
            pygame.draw.polygon(self.display, (100, 100, 100), ((5, 5), (495, 5), (495, 47), (5, 47)))
            self.display.blit(self.font.render(title, True, (30, 30, 30), (100, 100, 100)), (10, 10))

            pygame.draw.polygon(self.display, (30, 30, 30), ((458, 10), (490, 10), (490, 42), (458, 42)))
            self.display.blit(self.font.render('B', True, (100, 100, 100), (30, 30, 30)), (463, 11))

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if self.collide(pygame.mouse.get_pos(), ((458, 10), (490, 10), (490, 42), (458, 42))):
                        self.display.fill((30, 30, 30))
                        return

            self.drawText(self.display, body, (100, 100, 100), (5, 50, 490, 445), self.font, aa=True, bkg=None)
            pygame.display.flip()
    
    def edit(self, index):
        note = self.notelist[index]
        title = note.data_get().get('title')
        body = note.data_get().get('body')
        self.display.fill((30, 30, 30))
        color = color2 = (100, 100, 100)
        while True:
            self.display.fill((30, 30, 30))
            pygame.draw.polygon(self.display, color, ((5, 5), (495, 5), (495, 47), (5, 47)))
            self.display.blit(self.font.render(title, True, (30, 30, 30), color), (10, 10))

            pygame.draw.polygon(self.display, (30, 30, 30), ((458, 10), (490, 10), (490, 42), (458, 42)))
            self.display.blit(self.font.render('B', True, (100, 100, 100), (30, 30, 30)), (463, 11))

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    exit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if self.collide(pygame.mouse.get_pos(), ((458, 10), (490, 10), (490, 42), (458, 42))):
                        self.display.fill((30, 30, 30))
                        self.notelist[index].data_set(title, body)
                        return
                    elif self.collide(pygame.mouse.get_pos(), ((5, 5), (495, 5), (495, 47), (5, 47))):
                        color = (255, 255, 255)
                    else:
                        color = (100, 100, 100)
                    
                    if self.collide(pygame.mouse.get_pos(), ((5, 50), (495, 50), (495, 495), (5, 495))):
                        color2 = (255, 255, 255)
                    else:
                        color2 = (100, 100, 100)
                elif event.type == pygame.KEYDOWN and color == (255, 255, 255):
                    if event.key == pygame.K_BACKSPACE:
                        title = title[:-1]
                    else:
                        title += event.unicode
                elif event.type == pygame.KEYDOWN and color2 == (255, 255, 255):
                    if event.key == pygame.K_BACKSPACE:
                        body = body[:-1]
                    else:
                        body += event.unicode
            self.cur.execute('DELETE FROM notes WHERE coord1 = ? AND coord2 = ?', (note.pos[0], note.pos[1]))
            self.cur.execute('INSERT INTO notes VALUES (?, ?, ?, ?)', (title, body, note.pos[0], note.pos[1]))
            self.drawText(self.display, body, color2, (5, 50, 490, 445), self.font, aa=True, bkg=None)
            pygame.display.update()

    def delete(self, index):
        notedata = self.notelist.pop(index)
        self.cur.execute('DELETE FROM notes WHERE coord1 = ? AND coord2 = ?', (notedata.pos[0], notedata.pos[1]))
        for i in reversed(range(index, len(self.notelist))):
            self.cur.execute('DELETE FROM notes WHERE coord1 = ? AND coord2 = ?', (self.notelist[i].pos[0], self.notelist[i].pos[1]))
            self.notelist[i].changecoords((self.notelist[i].pos[0], self.notelist[i].pos[1]-47))
            self.cur.execute('INSERT INTO notes VALUES (?, ?, ?, ?)', (self.notelist[i].data_get().get('title'), self.notelist[i].data_get().get('body'), self.notelist[i].pos[0], self.notelist[i].pos[1]))
        self.connection.commit()

    def drawText(self, surface, text, color, rect, aa=True, bkg=None):
        rect = pygame.Rect(rect)
        y = rect.top
        lineSpacing = -2
        fontHeight = self.fontS.size("Tg")[1]
        while text:
            i = 1
            if y + fontHeight > rect.bottom:
                break
            while self.fontS.size(text[:i])[0] < rect.width and i < len(text):
                i += 1   
            if i < len(text): 
                i = text.rfind(" ", 0, i) + 1
            if bkg:
                image = self.fontS.render(text[:i], 1, color, bkg)
                image.set_colorkey(bkg)
            else:
                image = self.fontS.render(text[:i], aa, color)

            surface.blit(image, (rect.left, y))
            y += fontHeight + lineSpacing
            text = text[i:]

        return text

    def head(self):
        self.coords = (5, 5)
        pygame.draw.polygon(self.display, (100, 100, 100), (self.coords, (self.coords[0]+490, self.coords[1]), (self.coords[0]+490, self.coords[1]+42), (self.coords[0], self.coords[1]+42)))
        self.display.blit(self.font.render('Notepad', True, (30, 30, 30), (100, 100, 100)), (self.coords[0]+5, self.coords[1]+5))
        pygame.draw.polygon(self.display, (30, 30, 30), ((self.coords[0]+416, self.coords[1]+5), (self.coords[0]+448, self.coords[1]+5), (self.coords[0]+448, self.coords[1]+37), (self.coords[0]+416, self.coords[1]+37)))
        self.display.blit(self.font.render('A', True, (100, 100, 100), (30, 30, 30)), (self.coords[0]+421, self.coords[1]+6))
        pygame.draw.polygon(self.display, (30, 30, 30), ((self.coords[0]+379, self.coords[1]+5), (self.coords[0]+411, self.coords[1]+5), (self.coords[0]+411, self.coords[1]+37), (self.coords[0]+379, self.coords[1]+37)))
        self.display.blit(self.font.render('Q', True, (100, 100, 100), (30, 30, 30)), (self.coords[0]+384, self.coords[1]+6))

    def disp(self):
        offset = 0
        while True:
            #print(self.cur.execute('SELECT coord2 FROM notes').fetchall())
            self.display.fill((30, 30, 30))
            if offset == 0:
                self.head()
            [note.disp(offset) for note in self.notelist]
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    return
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 4 and offset > 0:
                        offset -= 20
                        if offset < 0:
                            offset = 0
                    if event.button == 5 and self.notelist[-1].pos[1] + 47 - offset > 500:
                        offset += 20
                    if event.button == 1:
                        for index, note in enumerate(self.notelist):
                            for type, coords in enumerate(note.getbuttoncoords(offset)):
                                if self.collide(pygame.mouse.get_pos(), coords):
                                    if type == 2:
                                        self.read(index)
                                    elif type == 1:
                                        self.edit(index)
                                    elif type == 0:
                                        self.delete(index)
                        if self.collide(pygame.mouse.get_pos(), ((self.coords[0]+416, self.coords[1]+5), (self.coords[0]+448, self.coords[1]+5), (self.coords[0]+448, self.coords[1]+37), (self.coords[0]+416, self.coords[1]+37))):
                            self.notelist.append(Note((5, (len(self.notelist)+1)*47 + 5), self.display, None))
                            self.notelist[-1].data_set('Blank Note', 'Blank Note')
                            self.cur.execute('INSERT INTO notes VALUES (?, ?, ?, ?)', (self.notelist[-1].data_get().get('title'), self.notelist[-1].data_get().get('body'), 5, (len(self.notelist))*47 + 5))
                            self.connection.commit()
                        elif self.collide(pygame.mouse.get_pos(), ((self.coords[0]+379, self.coords[1]+5), (self.coords[0]+411, self.coords[1]+5), (self.coords[0]+411, self.coords[1]+37), (self.coords[0]+379, self.coords[1]+37))):
                            self.connection.commit()
                            self.cur.close()
                            self.connection.close()
                            pygame.quit()
                            return
            pygame.display.update()

note = Notepad()
note.disp()

