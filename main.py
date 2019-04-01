#!/usr/bin/env python3
#__*__ coding: utf-8 __*__

import pygame,sys,time,random
from pygame.locals import *
import Dstar
import Block

redColour = pygame.Color(255,0,0)
blackColour = pygame.Color(0,0,0)
whiteColour = pygame.Color(255,255,255)
greenColour = pygame.Color(0,255,0)
greyColour = pygame.Color(200,200,200)

def conflict(route, new_block):
    for point in route:
        if point in new_block:
            return True

    return False

class PIC:
    pic_idx = 1

def simulation(playSurface, pygame, fpsClock, block_width, wall1, wall2, d_starobj, \
               snakePosition, raspberryPosition, route):
    while True:
        while True:
            wall1.move()
            wall2.move()
            wall1.new_block_capture()
            wall2.new_block_capture()
            new_white_buf = wall1.__new_white_buf__() + wall2.__new_white_buf__()
            new_black_buf = wall1.__new_black_buf__() + wall2.__new_black_buf__()

            snakePosition = [x for x in route[0]]
            route.pop(0)

            playSurface.fill(whiteColour)
            for position in route:
                pygame.draw.rect(playSurface, greyColour, Rect(position[0] * block_width, position[1] * block_width, block_width, block_width))
            for position in wall1.__loc_buf__():
                pygame.draw.rect(playSurface, blackColour, Rect(position[0] * block_width, position[1] * block_width, block_width, block_width))
            for position in wall2.__loc_buf__():
                pygame.draw.rect(playSurface, blackColour, Rect(position[0] * block_width, position[1] * block_width, block_width, block_width))
            pygame.draw.rect(playSurface, redColour, Rect(raspberryPosition[0] * block_width, raspberryPosition[1] * block_width, block_width, block_width))
            pygame.draw.rect(playSurface, greenColour, Rect(snakePosition[0] * block_width, snakePosition[1] * block_width, block_width, block_width))
            pygame.display.flip()
            fpsClock.tick(5)

            fname = str(PIC.pic_idx) + '.jpg'
            pygame.image.save(playSurface, fname)
            PIC.pic_idx = PIC.pic_idx + 1

            if conflict(route, new_black_buf):
                break

            if snakePosition == raspberryPosition:
                return

        print('Conflict!')
        d_starobj.clear_history()
        # d_starobj.add_change_point(new_black_buf, new_white_buf)
        d_starobj.D_star_search(snakePosition, raspberryPosition, wall1.__loc_buf__() + wall2.__loc_buf__())
        d_starobj.recall_route(snakePosition, raspberryPosition)
        route = d_starobj.__route__()
        wall1.clear_history()
        wall2.clear_history()

def main():
    pygame.init()
    playSurface = pygame.display.set_mode((640,480))
    fpsClock = pygame.time.Clock()
    pygame.display.set_caption('Snake HEGSNS')

    block_width = 20
    wall1 = Block.Block([[10, idx] for idx in range(0,10)])
    wall2 = Block.Block([[20, idx] for idx in range(15,24)])
    snakePosition = [2, 2]
    snakeSegments = [[2,2],[1,2],[0,2]]
    raspberryPosition = [31,22]

    d_starobj = Dstar.Dstar()
    while True:
        # A_star search
        d_starobj.D_star_search(snakePosition, raspberryPosition, wall1.__loc_buf__() + wall2.__loc_buf__())
        d_starobj.recall_route(snakePosition, raspberryPosition)
        route = d_starobj.__route__()
        simulation(playSurface, pygame, fpsClock, block_width, wall1, wall2, d_starobj, snakePosition, \
            raspberryPosition, route)
        # print(route)



        while True:
            x = random.randrange(1, 32)
            y = random.randrange(1, 24)
            tabu_table_tmp = wall1.__loc_buf__() + wall2.__loc_buf__() + snakeSegments
            if [x, y] not in tabu_table_tmp:
                break
        snakePosition = raspberryPosition
        raspberryPosition = [int(x), int(y)]
        d_starobj.clear_history()

        for event in pygame.event.get():
            if event.type == QUIT:
                exit()

    return


if __name__ == "__main__":
    main()