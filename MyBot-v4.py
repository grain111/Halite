import hlt
import logging

game = hlt.Game("MegaBot-v4")
logging.info("Starting my Megabot!")

while True:
    game_map = game.update_map()
    command_queue = []
    planets = game_map.all_planets()
    ships = game_map._all_ships()
    for ship in game_map.get_me().all_ships():
        if ship.docking_status != ship.DockingStatus.UNDOCKED:
            continue

        planets_by_distance = sorted(planets, key = lambda planet: ship.calculate_distance_between(planet))
        empty_planets = list(filter(lambda planet: not planet.is_owned(), planets_by_distance))

        ships_by_distance = sorted(ships, key = lambda ship: ship.calculate_distance_between(ship))
        enemy_ships = list(filter(lambda ship: ship.owner != game_map.get_me(), ships_by_distance))

        if empty_planets and ship.calculate_distance_between(empty_planets[0]) < game_map.width * 0.7:
            target = empty_planets[0]
            planets.remove(target)

            if ship.can_dock(target):
                command_queue.append(ship.dock(target))
            else:
                navigate_command = ship.navigate(
                    ship.closest_point_to(target),
                    game_map,
                    speed=int(hlt.constants.MAX_SPEED),
                    ignore_ships=False)
                if navigate_command:
                    command_queue.append(navigate_command)
        else:
            target = enemy_ships[0]
            navigate_command = ship.navigate(
                ship.closest_point_to(target),
                game_map,
                speed=int(hlt.constants.MAX_SPEED),
                ignore_ships=False)
            if navigate_command:
                command_queue.append(navigate_command)

    game.send_command_queue(command_queue)
    # TURN END
# GAME END
