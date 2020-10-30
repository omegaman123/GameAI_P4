#!/usr/bin/env python
#

"""
// There is already a basic strategy in place here. You can use it as a
// starting point, or you can throw it out entirely and replace it with your
// own.
"""
import logging, traceback, sys, os, inspect
logging.basicConfig(filename=__file__[:-3] +'.log', filemode='w', level=logging.DEBUG)
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.append(parentdir)

from behavior_tree_bot.behaviors import *
from behavior_tree_bot.checks import *
from behavior_tree_bot.bt_nodes import Selector, Sequence, Action, Check

from planet_wars import PlanetWars, finish_turn

# You have to improve this tree or create an entire new one that is capable
# of winning against all the 5 opponent bots
def setup_behavior_tree():

    # Top-down construction of behavior tree
    root = Selector(name='High Level Ordering of Strategies')
    # This sequence is only executed at the beginning of the game,
    # it spreads to the 4 weakest/nearest planets to establish a foothold
    initialize_sequence = Sequence(name='Initialize Sequence')
    start = Check(is_start)
    fleet_check = Check(fleets)
    spread_action = Action(spread_to_closest_weak_planets)
    initialize_sequence.child_nodes = [start, fleet_check, spread_action]

    # This is the plan of attack that is used throughout the bots strategy
    # The bot checks to see if it has an arbitrarily set strong enough store of ships on its planet
    # and attacks enemy or neutral planets with those numbers.
    attack_plan = Sequence(name='Attacking Plan')
    strong_fleet = Check(strong_fleet_check)
    attack = Action(strong_attack)
    attack_plan.child_nodes = [strong_fleet, attack]

    # This strategy is executed when the bot is losing, it will begin to attack the enemy more agressively,
    # taking the enemies weakest planets to regain ground
    less_planet_strategy = Sequence(name='Losing Plan')
    less_planets = Check(planet_control_check)
    take_weakest_planet = Action(take_weakest_planets)
    less_planet_strategy.child_nodes = [less_planets, take_weakest_planet]

    # This strategy executes when the bot is winning.
    # It will shift into a defensive mode, reinforcing currently owned planets while still seeking to spread
    more_planet_strategy = Sequence(name='Winning Plan')
    more_planets = Check(planet_control_check_winning)
    defend_planets = Action(defend)
    defense_spread = Action(spread)
    more_planet_strategy.child_nodes = [more_planets, defend_planets, defense_spread]

    root.child_nodes = [initialize_sequence, less_planet_strategy, more_planet_strategy, attack_plan]

    logging.info('\n' + root.tree_to_string())
    return root

# You don't need to change this function
def do_turn(state):
    behavior_tree.execute(planet_wars)

if __name__ == '__main__':
    logging.basicConfig(filename=__file__[:-3] + '.log', filemode='w', level=logging.DEBUG)

    behavior_tree = setup_behavior_tree()
    try:
        map_data = ''
        while True:
            current_line = input()
            if len(current_line) >= 2 and current_line.startswith("go"):
                planet_wars = PlanetWars(map_data)
                do_turn(planet_wars)
                finish_turn()
                map_data = ''
            else:
                map_data += current_line + '\n'

    except KeyboardInterrupt:
        print('ctrl-c, leaving ...')
    except Exception:
        traceback.print_exc(file=sys.stdout)
        logging.exception("Error in bot.")
