import serial
import pygame
import math
import time

#servo:10,trig:8,echo:9
pygame.init()
win=pygame.display.set_mode((900,500))
arduino=serial.Serial("COM7",9600,timeout=10)
run=True
pygame.font.init()
h=0
scalefactor=2
theta=0
previnfo=""
rendered=[]
l=["",""]
oldtheta=0


def getcoords_realistic(h,theta,startpos):
    x = startpos[0] + int(h * math.cos(math.radians(theta)))
    y = startpos[1] + int(h * math.sin(math.radians(theta)))
    return (x, y)
def getcoords(h,theta):
    x = 450 + int(h *4* math.cos(math.radians(theta)))
    y = 500 + int(h *4* math.sin(math.radians(theta)))
    return (x, y)
def refreshradar(distance=0,theta=0):
    pygame.draw.circle(win,(0,255,0),(450,500),388)
    pygame.draw.circle(win,(66, 61, 60),(450,500),386)
    pygame.draw.circle(win,(0,255,0),(450,500),242)
    pygame.draw.circle(win,(66, 61, 60),(450,500),240)
    pygame.draw.circle(win,(0,255,0),(450,500),122)
    pygame.draw.circle(win,(66, 61, 60),(450,500),120)
    font = pygame.font.SysFont('Calibri', 30)
    for i in range(30,180,30):
        ep=getcoords_realistic(-386,i,(450,500))
        pygame.draw.line(win,(0,255,0),(450,500),ep,2)
        tsfc= font.render(str(i), False, (0, 255, 0))
        textpoint=getcoords_realistic(-420,i,(450,500))
        win.blit(tsfc,textpoint)
    pygame.draw.rect(win,(0,0,0),pygame.Rect(0,0,900,70))
    win.blit(font.render(f"distance:{distance}cm",False,(0,255,0)),(0,0))
    win.blit(font.render(f"angle:{theta}",False,(0,255,0)),(780,0))


refreshradar()
while run:
    for event in pygame.event.get():
        if event.type==pygame.QUIT:
            run=False
    ch=arduino.read().decode()
    if ch==".":
        l[1]=l[0]
        l[0]=""
    l[0]+=ch
    info=l[1][1:].split(",")
    try:
        h=int(info[1])
        if h<96:
            theta=int(info[0])
            object=getcoords(-h,theta)
            transformed=(object[0],object[1])
            disp=pygame.Rect(transformed[0],transformed[1],5,5)
            rendered.append(disp)
        refreshradar(h,theta)
        pygame.draw.line(win,(0,255,0),(450,500),getcoords_realistic(-386,theta,(450,500)),3)
        for items in rendered:
            pygame.draw.rect(win,(255,0,0),items)
        oldtheta=theta
        pygame.display.update()
        if theta==165 or theta==15:
            rendered=[]
    except IndexError:
        print("init")
pygame.quit()