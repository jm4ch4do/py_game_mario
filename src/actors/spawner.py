import json as _json

import pygame as _pyg

import src.actors.enemies as _ene
import src.actors.treasure as _tre


class Spawner:
    def __init__(self, world, status, player):
        self.actors = _pyg.sprite.Group()
        self.world, self.status, self.player = world, status, player
        self.actor_map = ActorMap.load()
        self.actor_index = 0

    def spawn_from_map(self):
        if self.actor_index >= len(self.actor_map):
            return None

        act = self.actor_map[self.actor_index]
        game_time = _pyg.time.get_ticks() - self.status.start_time
        if game_time > act.time:
            self.actor_index += 1
            self.spawn_actor(act.type, (act.x_pos, act.y_pos), act.scale)

    def spawn_actor(self, type, ini_pos, scale=1):
        SelectedActorClass = type
        actor = SelectedActorClass(
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


class ActorMap:

    @classmethod
    def load(cls, source="data/actor_map.json"):
        with open(source) as f:
            raw_actor_map = _json.load(f)["actors"]

        return [
            ActorInfo(
                r.get("type"),
                r.get("time"),
                r.get("x_pos"),
                r.get("y_pos"),
                r.get("scale"),
            )
            for r in raw_actor_map
        ]


class ActorInfo:

    ACTOR_TYPES = {
        "Snail": _ene.Snail,
        "Bird": _ene.Bird,
        "Frog": _ene.Frog,
        "Treasure": _tre.Treasure,
        "Coin": _tre.Coin,
    }

    def __init__(self, type, time, x_pos=None, y_pos=None, scale=1):
        self.type = self.ACTOR_TYPES[type]
        self.time = time * 1000
        self.x_pos = x_pos
        self.y_pos = y_pos
        self.scale = scale
