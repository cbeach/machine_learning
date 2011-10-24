#!/usr/bin/env python
from random import shuffle
from ants import *

class MyBot:

    def do_turn(self, ants):
        # track all moves, prevent collisions
        orders = {}
        def do_move_direction(loc, direction):
            new_loc = ants.destination(loc, direction)
            if (ants.unoccupied(new_loc) and new_loc not in orders):
                ants.issue_order((loc, direction))
                orders[new_loc] = loc
                return True
            else:
                return False

        # default move
        for ant_loc in ants.my_ants():
            directions = ('n','e','s','w')
            for direction in directions:
                if do_move_direction(ant_loc, direction):
                    break

