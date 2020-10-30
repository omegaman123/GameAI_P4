

def if_neutral_planet_available(state):
    return any(state.neutral_planets())


def have_largest_fleet(state):
    return sum(planet.num_ships for planet in state.my_planets()) \
             + sum(fleet.num_ships for fleet in state.my_fleets()) \
           > sum(planet.num_ships for planet in state.enemy_planets()) \
             + sum(fleet.num_ships for fleet in state.enemy_fleets())


def strong_fleet_check(state):
    hundred_planets = [planet for planet in state.my_planets() if planet.num_ships >= 100]
    return len(hundred_planets) > 0


def is_start(state):
    my_planets = state.my_planets()
    return len(my_planets) < 2

def fleets(state):
    f = state.my_fleets()
    if not f:
        return True
    else:
        return False

def planet_control_check(state):
    enemy_fleets = state.enemy_planets()
    my_planets = state.my_planets()
    return my_planets <= enemy_fleets

def planet_control_check_winning(state):
    enemy_fleets = state.enemy_planets()
    my_planets = state.my_planets()
    return my_planets > enemy_fleets
