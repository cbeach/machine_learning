#!/usr/bin/env python
import math
import heapq
import logging
import gc
from ants import *

# define a class with a do_turn method
# the Ants.run method will parse and update bot input
# it will also run the do_turn method for us
class MyBot:
    def __init__(self):
        # define class level variables, will be remembered between turns
        pass
    
    # do_setup is run once at the start of the game
    # after the bot has received the game settings
    # the ants class is created and setup by the Ants.run method
    def do_setup(self, ants):
        # initialize data structures after learning the game settings
        self.unseen = []
        self.hills = []
        self.counter = 0
        self.do_error = True
        self.counter = 0
        self.targets = {}
        self.orders = {}
        for row in range(ants.rows):
            for col in range(ants.cols):
                self.unseen.append((row, col))

        self.logger = logging.basicConfig()
    

    # do turn is run once per turn
    # the ants class has the game state and is updated by the Ants.run method
    # it also has several helper methods to use
    def do_turn(self, ants):
        # track all moves, prevent collisions
        logging.error("hello world %d", self.counter)
        self.counter = self.counter + 1
        orders = {}
        def do_move_direction(loc, direction):
            new_loc = ants.destination(loc, direction[0])
            if (ants.unoccupied(new_loc) and new_loc not in orders):
                ants.issue_order((loc, direction))
                orders[new_loc] = loc
                return True
            else:
                return False
        targets = {}

        def do_move_location(loc, dest):
            logging.error("starting the search")
            temp = a_star_search(loc,dest)
            logging.error("finished the search")
            if True in temp:
                do_move_direction(loc, temp[1])
                return True
            return False

        def a_star_h(loc, dest):
            return abs(loc[0] - dest[0] + loc[1] - dest[1])
        
        def a_star_pop(dest, open_list, g_val):
            best_cost = 999999999;
            best_loc = open_list[0]
            for element in open_list:
                if a_star_h(element, dest) + g_val[element] < best_cost:
                    best_cost = a_star_h(element, dest) + g_val[element]
                    best_loc = element
            open_list.remove(best_loc)
            return best_loc


        def a_star_search(loc, dest):
            open_list = []
            closed_list = []
            came_from = {}
            current_node = None
            counter = 0

            g_score = {}
            f_score = {}
            h_score = {}

            tentative_g_score = 99999

            open_list.append(loc)
            
            g_score[loc] = 0

            while len(open_list) > 0 and counter < 1000:
                counter = counter + 1
                logging.error
                temp = a_star_pop(dest, open_list, g_score)
                closed_list.append(temp)
                
                if temp == dest:
                    current_node = temp
                    while came_from[current_node] != loc:
                        current_node = came_from[current_node]
                        #logging.error(str(current_node))
                    del closed_list, open_list, came_from, g_score, h_score, f_score
                    gc.collect()
                    return (True, ants.direction(loc,current_node)[0])
                    #diff = (current_path[0] - loc[0], current_path[1] -loc[1]) 
                    #for i in ants.AIM.keys():
                        #if ants.AIM[i] == diff:
                            #return (True, ants.direction(loc, current_path[1]))

                for direction in ('n', 's', 'e', 'w'):

                    child = ants.destination(temp,direction)
                    tentative_g_score = g_score[temp] + 1
                    if ants.passable(child) == True and child not in open_list and child not in closed_list:
                        open_list.append(child)
                        g_score[child] = tentative_g_score
                        came_from[child] = temp
                    if child in g_score.keys() and tentative_g_score < g_score[child]:
                        came_from[child] = temp
                        g_score[child] = tentative_g_score
                        h_score[child] = a_star_h(child, dest)
                        f_score[child] = g_score[child] + h_score[child]
                    

            self.do_error = False   
            return (False, '') 

        ant_dist = []
        # default move
        logging.error("entering default move")
        for hill_loc in ants.my_hills():
            orders[hill_loc] = None
        # gather food
        logging.error("entering food gather")
        logging.error("********************************************************************")
        logging.error("I have " + str(len(ants.my_ants())) + " ants\n")
        logging.error("can see " + str(len(ants.food())) + " food\n")
        
        for food_loc in ants.food():
            for ant_loc in ants.my_ants():
                dist = ants.distance(ant_loc, food_loc)
                ant_dist.append((dist, ant_loc, food_loc))
        ant_dist.sort()
        self.counter = 0
        for dist, ant_loc, food_loc in ant_dist:
            if food_loc not in self.targets and ant_loc not in self.targets.values():
                self.counter = self.counter + 1
                do_move_location(ant_loc, food_loc)
                self.targets[food_loc] = ant_loc
                food_list = ants.food()
        for food_key in self.targets.keys():
            if food_key not in food_list:
                del self.targets[food_key]
                
        logging.error(str(self.counter) + " times through A*")
        logging.error("********************************************************************")
        logging.error("attacking hills")
        #attach hills
        for hill_loc, hill_owner in ants.enemy_hills():
            if hill_loc not in self.hills:
                self.hills.append(hill_loc)
        ant_dist = []
        for hill_loc in self.hills:
            for ant_loc in ants.my_ants():
                if ant_loc not in orders.values():
                    dist = ants.distance(ant_loc, hill_loc)
                    ant_dist.append((dist, ant_loc))
        ant_dist.sort()
        for dist, ant_loc in ant_dist:
            do_move_location(ant_loc, hill_loc)

        # unblock the hill
        for hill_loc in ants.my_hills():
            for hill_loc, hill_owner in ants.enemy_hills():
                if hill_loc not in self.hills:
                    self.hills.append(hill_loc)
        ant_dist = []
        for hill_loc in self.hills:
            for ant_loc in ants.my_ants():
                if ant_loc not in orders.values():
                    dist = ants.distance(ant_loc, hill_loc)
                    ant_dist.append((dist, ant_loc))
        ant_dist.sort()
        for dist, ant_loc in ant_dist:
            do_move_location(ant_loc, hill_loc)
            if hill_loc in ants.my_hills() and hill_loc not in orders.values():
                for direction in ('n', 's', 'e', 'w'):
                    if do_move_direction(hill_loc, direction):
                        break
        logging.error("exploring")
        #explore
        for loc in self.unseen[:]:
            if ants.visible(loc):
                self.unseen.remove(loc)
        for ant_loc in ants.my_ants():
            if ant_loc not in orders.values():
                unseen_dist = []
                for unseen_loc in self.unseen:
                    dist = ants.distance(ant_loc, unseen_loc)
                    unseen_dist.append((dist, unseen_loc))
                unseen_dist.sort()
                for dist, unseen_loc in unseen_dist:
                    if do_move_location(ant_loc, unseen_loc):
                        break
                    

if __name__ == '__main__':
    # psyco will speed up python a little, but is not needed
    try:
        import psyco
        psyco.full()
    except ImportError:
        pass
    
    try:
        # if run is passed a class with a do_turn method, it will do the work
        # this is not needed, in which case you will need to write your own
        # parsing function and your own game state class
        #Ants.run(MyBot())
        argv = sys.argv[1:]
        Ants.run(MyBot())    
    except KeyboardInterrupt:
        print('ctrl-c, leaving ...')
