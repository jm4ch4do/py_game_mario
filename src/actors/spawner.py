import json as _json

import pygame as _pyg

import src.actors.enemies as _ene
import src.actors.treasure as _tre


class Spawner:
    def __init__(self, world, status, player):
        self.actors = _pyg.sprite.Group()
        self.world, self.status, self.player = world, status, player
        self.actor_map = self.load_actor_map()
        self.actor_index = 0
        self.actor_types = {
            "Snail": _ene.Snail,
            "Treasure": _tre.Treasure,
            "Coin": _tre.Coin,
        }

    def spawn_from_map(self):
        if self.actor_index >= len(self.actor_map):
            return None

        actor = self.actor_map[self.actor_index]
        game_time = _pyg.time.get_ticks() - self.status.start_time
        if game_time > actor["time"]:
            self.actor_index += 1
            self.spawn_actor(
                actor.get("type"),
                (actor.get("x_pos"), actor.get("y_pos")),
                actor.get("scale"),
            )

    def load_actor_map(self):
        source = "data/actor_map.json"
        with open(source) as f:
            actor_map = _json.load(f)
        return actor_map["actors"]

    def spawn_actor(self, type, ini_pos, scale=1):
        ActorClass = self.actor_types[type]
        actor = ActorClass(
            world=self.world,
            status=self.status,
            player=self.player,
            react_to_event=self.react_to_event,
            scale=scale,
            ini_pos=ini_pos,
        )
        self.actors.add(actor)

    def react_to_event(self, event, actor):
        if event == "leaving":
            self.actors.remove(actor)
        elif event == "hits_player":
            self.status.gameover = True
        elif event == "found":
            if isinstance(actor, _tre.Treasure):
                self.status.gameover = True
                self.status.victory = True
            else:
                self.status.score += 1
                self.actors.remove(actor)

    def update(self):
        self.spawn_from_map()
        self.actors.update()

    def draw(self, screen):
        self.actors.draw(screen)
