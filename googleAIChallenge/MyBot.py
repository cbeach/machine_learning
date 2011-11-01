#!/usr/bin/env python
import math
import heapq
import logging
import gc
import random
from ants import *

# define a class with a do_turn method
# the Ants.run method will parse and update bot input
# it will also run the do_turn method for us
class MyBot:


    ant_id = {}
    orders = {}
    ant_state = {}
    live_ants = []
    ant_counter = 0
    movements = {}
    enemy_hills = []
    unseen = []
    food = {}        
    a_star = True
    turn_counter = 1

    def __init__(self):
        # define class level variables, will be remembered between turns
        self.mission = {"idle":0, "gather":1, "scout":2, "infantry":3, "calvary":4}
        random.seed()

    def do_setup(self, ants):
        # initialize data structiures after learning the game settings
        for row in range(ants.rows):
            for col in range(ants.cols):
                self.unseen.append((row, col))

        self.logger = logging.basicConfig()


    def do_move_direction(self, ants, loc, direction):
        direction_index = 0;
        if len(direction) > 1:
            direction_index = random.randrange(0,1,1)
            #logging.error(str(direction[direction_index]))
            new_loc = ants.destination(loc, direction[direction_index])
        elif len(direction) == 1:
            new_loc = ants.destination(loc, direction[0])
        else:
            return False
        
        if ants.unoccupied(new_loc) and ants.passable(new_loc) and new_loc not in self.ant_id.values():
            ants.issue_order((loc, direction[direction_index]))
            return True
        else:
            return False

    def a_star_h(self, loc, dest):
        return abs(loc[0] - dest[0] + loc[1] - dest[1])
    
    def a_star_pop(self, dest, open_list, g_val):
        best_cost = 999999999;
        best_loc = open_list[0]
        for element in open_list:
            if self.a_star_h(element, dest) + g_val[element] < best_cost:
                best_cost = self.a_star_h(element, dest) + g_val[element]
                best_loc = element
        open_list.remove(best_loc)
        return best_loc

    
    def a_star_search(self, ants, loc, dest):
        
        """given a starting and an ending location, A* will locate a best path and returns an ordered list of nodes"""
        open_list = []
        closed_list = []
        came_from = {}
        best_path = []
        current_node = None
        counter = 0

        g_score = {}
        f_score = {}
        h_score = {}

        tentative_g_score = 99999

        open_list.append(loc)
        
        g_score[loc] = 0

        while len(open_list) > 0:
            counter = counter + 1
            temp = self.a_star_pop(dest, open_list, g_score)
            closed_list.append(temp)
            if temp == dest:
                current_node = temp
                while current_node != loc:
#                    logging.error("current " + str(current_node) + "  came from" + str(came_from[current_node]))
                    best_path.append(current_node)
                    current_node = came_from[current_node]
#                logging.error("dest " + str(dest))
#                logging.error("best_path " + str(best_path))
#                logging.error("order " + str(best_path[-1]) + " pos " + str(self.ant_id[0]))
                return best_path
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
                    h_score[child] = self.a_star_h(child, dest)
                    f_score[child] = g_score[child] + h_score[child]
                

        self.do_error = False   
        return []

    def get_closest_ant(self, ants, food_loc, ant_role = 0):
        temp_ant = None
        for ant in self.ant_state.keys():
            if self.ant_state[ant] == ant_role:
                if temp_ant == None:
                    temp_ant = ant
                elif (ants.distance(self.ant_id[ant], food_loc) 
                < ants.distance(self.ant_id[temp_ant], food_loc)):
                    temp_ant = ant                
        return temp_ant

    def do_orders(self,ants):
        success = False
        for ant in self.ant_id.keys():
            try:
                #logging.error("ant: " + str(ant) + " : orders " + str(self.orders[ant]))
                if len(self.orders[ant]) > 0:
                    success = (self.do_move_direction(ants, self.ant_id[ant], 
                    ants.direction(self.ant_id[ant], self.orders[ant][-1])))
                    #logging.error("success = " + str(success))
                    if success == True:
                        #logging.error("\n\n updating position \n\n")
                        self.ant_id[ant] = self.orders[ant].pop()
                        if len(self.orders[ant]) == 0:
                            logging.error("setting ant " + str(ant) + " to idle")
                            self.ant_state[ant] == self.mission["idle"]
               
            except KeyError:
                logging.error("this ant does not have orders")
                self.ant_state[ant] = self.mission["idle"]
#            logging.error("\n\n" + str(success) + "\n\n")
#        for hill_loc in ants.my_hills():
#            if hill_loc in self.ant_id.values():
#                for direction in ['n','s','e','w']:
#                    if (ants.passable(ants.destination(hill_loc, direction)) 
#                    and ants.destination(hill_loc, direction) 
#                    not in self.ant_id.values()):
#                        self.do_move_direction(ants, hill_loc, direction)
    def give_idle_orders(self, ants):
        for ant in ants.my_ants():
            if len(self.orders[ant]:
                order = self.order.pop()
                if 


    def turn(self, ants):
        if self.a_star == True:
            self.ant_id[0] = ants.my_ants()[0]
            if len(ants.food()) > 0:
                self.orders[0] = self.a_star_search(ants, self.ant_id[0], ants.food()[0])
            self.do_orders(ants)


    def update_visible_map(self, ants):
        for square in ants.visible():
            try:
                self.unseen.remove(square)
            except ValueError:
                pass


    def do_turn(self, ants):
        logging.error("turn #: " + str(self.turn_counter) + "-------------------")        
        self.turn_counter = self.turn_counter + 1
        
        #are there any new ants that we should add to the roster?
        for check_ant in ants.my_ants():
#            logging.error("check ant " + str(check_ant) + " " + str(self.ant_id.values()))
            if check_ant not in self.ant_id.values():
                self.live_ants.append(self.ant_counter) 
                self.ant_id[self.ant_counter] = check_ant
                self.ant_state[self.ant_counter] = self.mission["idle"]
                self.ant_counter = self.ant_counter + 1
        #did any ants die during combat?
#        logging.error("ants " + str(ants.my_ants()))
        for check_for_dead in self.live_ants:
            dead_ant_loc = self.ant_id[check_for_dead]
            if dead_ant_loc not in ants.my_ants():
                logging.error("killing ant " + str(check_for_dead))
                del self.orders[check_for_dead]
                del self.ant_state[check_for_dead]
                del self.ant_id[check_for_dead]
                self.live_ants.remove(check_for_dead)
        #logging.error("I see " + str(ants.food()) + " food") 
        #all of the updating is done, delegate tasks
        ############break out into function later
        do_idle_orders(ants)
        



        logging.error(" ants : " + str(self.ant_id.values()))
        logging.error(" food : " + str(ants.food()))        
        logging.error(" state keys : " + str(self.ant_state.keys()))
        logging.error(" state : " + str(self.ant_state.values()) + "\n")
        
        for ant in self.live_ants:
            try:
#                logging.error("ant " + str(ant) + " Status " 
#                + str(self.ant_state[ant]) + " position " + 
#                str(self.ant_id[ant]) + " next move " + str(self.orders[ant][-1]))
                pass
            except KeyError:
                logging.error("Waiting for Orders")
        self.do_orders(ants)



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
