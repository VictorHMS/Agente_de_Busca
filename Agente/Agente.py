import sys, pygame, random, math

class objeto:
    def __init__(self, position, imagem, speed):
        self.x = position[0]
        self.y = position[1]
        self.vx = speed[0]
        self.vy = speed[1]
        self.vel = ((self.vx**2) + (self.vy**2))**(1.0/2.0)
        self.position = position
        self.img = imagem
    
    def mover(self, dt):
        self.x += self.vx * dt
        self.y += self.vy * dt
    
    def setSpeed(self, vx, vy):
        self.vx = vx
        self.vy = vy
    
    def setPosition(self, position):
        self.position = position
        self.x = position[0]
        self.y = position[1]
        
    def topleft(self):
        w,h = self.img.get_size()
        w = w/2
        h = h/2
        return (self.x - w), (self.y - h)

class botao:
    def __init__(self,es,dir,cima,baixo):
        self.es = es
        self.dir = dir
        self.cima = cima
        self.baixo = baixo
    
    def pegou(self, x, y):
        if (x >= self.es and x <= self.dir) and (y >= self.cima and y <= self.baixo):
            return True
        return False

def blitRotate2(surf, image, topleft, angle):
    
    rotated_image = pygame.transform.rotate(image, angle)
    new_rect = rotated_image.get_rect(center = image.get_rect(topleft = topleft).center)

    surf.blit(rotated_image, new_rect.topleft)
    

def calcDes(goal, seta):
    dx = float(goal.x - seta.x)
    dy = float((-goal.y) - (-seta.y))
    
    norma = ((dx**2) + (dy**2))**(1.0/2.0)
    
    udx = dx/norma
    udy = dy/norma
    
    angRad = 0
    if(abs(udx) <= 0.001):
        if(udy >= 0):angRad = math.pi/2.0
        else: angRad = 3*math.pi/2.0
    else:
        angRad = math.atan(dy/dx)
        if(udx < 0 and udy >= 0): angRad += math.pi
        if(udx < 0 and udy < 0): angRad += math.pi
        
    angRad += 2*math.pi
    
    while(angRad >= 2*math.pi): angRad -= 2*math.pi
    
    angulo = (angRad * 180.0)/math.pi
    angulo = angulo + 360
   
    while angulo >= 360:
        angulo -= 360
    
    return angulo, angRad

def pertinho(seta,goal):
    dx = goal.x - seta.x
    dy = (-goal.y) - (-seta.y)
    norma = ((dx**2) + (dy**2))**(1.0/2.0)
    
    if norma <= 15:
        return True
    return False
    
def main():
    tela = width, height = 640, 480
    screen = pygame.display.set_mode(tela)
    pygame.font.init()
    screenBGColor = 25,25,112
    
    stbuttons = ['play', 'pause', 'reset']
    
    btplay = pygame.image.load('play.png')
    btplay = pygame.transform.scale(btplay,(40,40))
    plps = (30,30)
    
    btpause = pygame.image.load('pause.png')
    btpause = pygame.transform.scale(btpause,(40,40))
    psps = (80,30)
    
    btreset = pygame.image.load('reset.png')
    btreset = pygame.transform.scale(btreset,(40,40))
    rsps = (130,30)
    
    buttons = [botao(plps[0], plps[0] + btplay.get_size()[0], plps[1], plps[0] + btplay.get_size()[1])]
    buttons.append(botao(psps[0], psps[0] + btpause.get_size()[0], psps[1], psps[0] + btpause.get_size()[1]))
    buttons.append(botao(rsps[0], rsps[0] + btreset.get_size()[0], psps[1], psps[0] + btreset.get_size()[1]))
    
    fonte = pygame.font.get_default_font()
    fontesys=pygame.font.SysFont(fonte, 32) 
    text = fontesys.render("Comidas: 0", 1, (255,255,255))
    
    textRect = text.get_rect()
    textRect.center = (320, 20)
    
    FPS = 60
    fpsClock = pygame.time.Clock()

    arrow = pygame.image.load('arrow.png')
    arrowRect = arrow.get_rect()
    arrow = pygame.transform.scale(arrow, (30,30))
    arrowSpeed = (0.1,0.1)
    initialPosition = (320, 240)
    angle = 0
    angleOffset = +90
    
    seta = objeto(initialPosition,arrow,arrowSpeed)
    
    
    comida = pygame.image.load('biscoito.png')
    comida = pygame.transform.scale(comida, (10,10))
    
    goal = objeto((0,0), comida, (0,0))

    comidaX = (random.randint(20, 635))
    comidaY = (random.randint(100, 475))
    
    state = 'reset'
    ncom = 0
    
    while(1):
        dt = fpsClock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT: 
                sys.exit()
            
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse = pygame.mouse.get_pos()
                for i in range(len(buttons)):
                    if buttons[i].pegou(mouse[0],mouse[1]):
                        state = stbuttons[i]
                        print(state)
                        break
                    
        screen.fill(screenBGColor)
        
        if state == 'play':
            
            desAngle, radAng = calcDes(goal,seta)
            mAngle = angle+angleOffset
            
            if(mAngle >= 360): mAngle -= 360
            while(mAngle < 0): mAngle += 360
            
            
            if abs(desAngle - mAngle) > 0.01:
                passo = 2
                stp = 1
                
                if(desAngle > mAngle):
                    
                    if desAngle - mAngle < mAngle + (360-desAngle):
                        passo = min(stp*dt,desAngle - mAngle)
                    else:
                        passo = max(-stp*dt, -(mAngle + (360-desAngle)))
                        
                else:
                    if mAngle - desAngle < desAngle + (360-mAngle):
                        passo = max(-stp*dt, desAngle - mAngle)
                    else:
                        passo = min(-stp*dt,desAngle + (360-mAngle))
                
                angle += passo

                if(angle >= 360): angle -= 360

            elif pertinho(seta,goal):
                ncom += 1
                
                while(pertinho(seta, goal)):
                    comidaX = (random.randint(20, 635))
                    comidaY = (random.randint(100, 475))
                    goal.setPosition((comidaX,comidaY))
        
            else:
                nvel = seta.vel
                seta.setSpeed(nvel*math.cos(radAng), -nvel*math.sin(radAng))
                seta.mover(dt)
            
        if state == 'reset':
            ncom = 0
            
            angle = (random.randint(0, 359))
            novoX = (random.randint(20, 635))
            novoY = (random.randint(100, 475)) 
            seta.setPosition((novoX,novoY))
            
            comidaX = (random.randint(20, 635))
            comidaY = (random.randint(100, 475))
            goal.setPosition((comidaX,comidaY))
            
            while(pertinho(seta, goal)):
                comidaX = (random.randint(20, 635))
                comidaY = (random.randint(100, 475))
                goal.setPosition((comidaX,comidaY))
            
            state = 'pause'
                   
        goal.setPosition((comidaX,comidaY))
        
        blitRotate2(screen, goal.img, goal.topleft(), 0)
        blitRotate2(screen, seta.img, seta.topleft(), angle)
        pygame.draw.circle(arrow, (255,0,0), arrow.get_rect().center, 2)
    
        estado = ''
        if state == 'pause': estado = 'Pausado '
        text = fontesys.render(estado + "Comidas: " + str(ncom), 1, (255,255,255))
        
        screen.blit(btplay, plps)
        screen.blit(btpause, psps)
        screen.blit(btreset, rsps)
        screen.blit(text, textRect)
        pygame.display.flip()
        

if __name__ == '__main__':
    main()

