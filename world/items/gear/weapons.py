"""
    Weapon Typeclasses
"""

from world.items.items import Equippable
from world.rules import Ability
from world import rules
from evennia import AttributeProperty


class Weapon(Equippable):
    """

    Args:
        Equippable (_type_): _description_
    """

    slots = ["wield1", "wield2"]
    multi_slot = False

    damage_roll = ""
    handedness = 1
    range = "melee"
    attack_type = AttributeProperty(Ability.STR)

    def at_object_creation(self):
        super(Weapon, self).at_object_creation()

        self.db.range = self.range
        self.db.damage_roll = self.damage_roll
        self.db.handedness = self.handedness
        self.db.worn = False

    def at_equip(self, character):
        self.db.worn = True
        # character.traits.PDEF.mod += self.db.physical_bonus
        # character.traits.MDEF.mod += self.db.magical_bonus

    def at_remove(self, character):
        self.db.worn = False
        # character.traits.PDEF.mod -= self.db.physical_bonus
        # character.traits.MDEF.mod -= self.db.magical_bonus

    def at_pre_use(self, user, target=None, *args, **kwargs):
        if target and user.location != target.location:
            # we assume weapons can only be used in the same location
            user.msg("You are not close enough to the target!")
            return False

        if self.db.curr_dura is not None and self.db.curr_dura <= 0:
            user.msg(f"{self.get_display_name(user)} is broken and can't be used!")
            return False
        return super().at_pre_use(user, target=target, *args, **kwargs)

    def use(
        self, attacker, target, *args, advantage=False, disadvantage=False, **kwargs
    ):
        """When a weapon is used, it attacks an opponent"""

        location = attacker.location

        is_hit, quality, txt = rules.dice.opposed_saving_throw(
            attacker,
            target,
            attack_type=self.attack_type,
            defense_type=self.defense_type,
            advantage=advantage,
            disadvantage=disadvantage,
        )
        location.msg_contents(
            f"$You() $conj(attack) $You({target.key}) with {self.key}: {txt}",
            from_obj=attacker,
            mapping={target.key: target},
        )
        if is_hit:
            # enemy hit, calculate damage
            dmg = rules.dice.roll(self.damage_roll)

            if quality is Ability.CRITICAL_SUCCESS:
                # doble damage roll for critical success
                dmg += rules.dice.roll(self.damage_roll)
                message = f" $You() |ycritically|n $conj(hit) $You({target.key}) for |r{dmg}|n damage!"
            else:
                message = f" $You() $conj(hit) $You({target.key}) for |r{dmg}|n damage!"

            location.msg_contents(
                message, from_obj=attacker, mapping={target.key: target}
            )
            # call hook
            target.at_damage(dmg, attacker=attacker)

        else:
            # a miss
            message = f" $You() $conj(miss) $You({target.key})."
            if quality is Ability.CRITICAL_FAILURE:
                message += ".. it's a |rcritical miss!|n, damaging the weapon."
                if self.quality is not None:
                    self.quality -= 1
                location.msg_contents(
                    message, from_obj=attacker, mapping={target.key: target}
                )

    def at_post_use(self, user, *args, **kwargs):
        if self.quality is not None and self.quality <= 0:
            user.msg(
                f"|r{self.get_display_name(user)} breaks and can no longer be used!"
            )
