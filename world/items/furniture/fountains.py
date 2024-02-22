from evennia.contrib.game_systems.containers import ContribContainer


class Fountain(ContribContainer):

    def at_object_creation(self):
        super().at_object_creation()

        self.locks.add("get:false()")

    @property
    def is_liquid_container(self):
        return True
