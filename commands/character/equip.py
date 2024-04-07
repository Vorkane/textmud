# from evennia import CmdSet
# from evennia.commands.command import Command as BaseCommand
from evennia.utils.evtable import EvTable
from commands.command import MuxCommand

from world.items.gear.crafting_tools import CraftingTool
from world.items.gear.crafting_tools import PickAxe
from world.items.gear.armor import Torso, Helm, Boots, Gloves, Necklace, Bracers, Belt, Ring
from world.items.gear.weapons import Weapon

# __all__ = ('CmdEquip', 'CmdWear', 'CmdWield', 'CmdRemove')
__all__ = ('CmdEquip', 'CmdInventory', 'CmdWield', 'CmdRemove')


_INVENTORY_ERRMSG = "You don't have '{}' in your inventory."
_EQUIP_ERRMSG = "You do not have '{}' equipped."

wield_slots = ['primary', 'off-hand']
armor_slots = ['helm', 'necklace', 'cloak', 'torso', 'belt', 'bracers', 'gloves', 'ring1', 'ring2', 'boots']
clothing_slots = ['hat', 'accessory', 'overtop', 'bottom', 'belt2', 'accessory2', 'gloves2', 'accessory3', 'accessory4', 'shoes']


class CmdInventory(MuxCommand):
    """
    view inventory

    Usage:
        inventory
        inv

    Shows your inventory.
    """

    # Alternate version of the inventory command which separates
    # worn and carried items.

    key = "inventory"
    aliases = ["inv", "i"]
    locks = "cmd:all()"
    arg_regex = r"$"

    def func(self):
        """check inventory"""
        if not self.caller.contents:
            self.caller.msg("You are not carrying or wearing anything.")
            return

        message_list = []

        items = self.caller.contents

        carry_table = EvTable(border="header")
        wear_table = EvTable(border="header")

        carried = [obj for obj in items if not obj.db.worn]
        names_and_descs = [(obj.get_extra_display_name_info(self.caller), obj.get_display_desc(self.caller)) for obj in set(carried)]
        carried_sums = {tup: names_and_descs.count(tup) for tup in set(names_and_descs)}
        worn = [obj for obj in items if obj.db.worn]

        # message_list.append("|wYou are carrying:|n")
        # for item in carried:
        for (name, desc), count in carried_sums.items():
            carry_table.add_row(
                # item.get_display_name(self.caller), item.get_display_desc(self.caller)
                f"{count}x {name}", desc
            )
        if carry_table.nrows == 0:
            carry_table.add_row("Nothing.", "")
        message_list.append(str(carry_table))

        # message_list.append("|wYou are wearing:|n")
        for item in worn:
            item_name = item.get_extra_display_name_info(self.caller)
            if item.db.covered_by:
                item_name += " (hidden)"
            wear_table.add_row(item_name, item.get_display_desc(self.caller))
        if wear_table.nrows == 0:
            wear_table.add_row("Nothing.", "")
        message_list.append(str(wear_table))

        inv_header = """
|015=================================|n
            |035Inventory
        Weight {current_weight}/{max_weight}|n
|015=================================|n
Wielding: {wielding}
Armors: {armor}
Clothing: {clothing}
Carrying:
{carrying}

|015=================================|n""".format(
            current_weight="".join(str([self.caller.stats.ENC.current])),
            max_weight="".join(str([self.caller.stats.ENC.max])),
            wielding="\n\t  ".join([self.caller.equip.get(slot).get_display_name(self.caller) for slot in wield_slots if self.caller.equip.get(slot)]),
            armor="\n\t".join([self.caller.equip.get(slot).get_extra_display_name_info(self.caller) for slot in armor_slots if self.caller.equip.get(slot)]),
            clothing="\n\t".join([self.caller.equip.get(slot).get_extra_display_name_info(self.caller) for slot in clothing_slots if self.caller.equip.get(slot)]),
            carrying=str(carry_table))

        message_list.append(inv_header)

        self.caller.msg("\n".join(message_list))


class CmdEquip(MuxCommand):
    """
    view equipment
    Usage:
        equip[/swap] [<item>]
    Switches:
        s[wap] - replaces any currently equipped item
    Equips an item to its required slot(s). If no item
    specified, lists your current equipment.
    """
    key = "equip"
    aliases = ["eq"]
    locks = "cmd:all()"

    def func(self):
        caller = self.caller
        args = self.args.strip()
        swap = any(s.startswith('s') for s in self.switches)

        if args:
            if hasattr(self, "item"):
                obj = self.item
                del self.item
            else:
                obj = caller.search(
                    args,
                    candidates=caller.contents,
                    nofound_string=_INVENTORY_ERRMSG.format(args))

            if obj:
                if hasattr(self, "action"):
                    action = self.action
                    del self.action
                else:
                    if any(isinstance(obj, i) for i in (CraftingTool, PickAxe, Weapon)):
                        action = 'wield'
                    elif any(isinstance(obj, i) for i in (Torso, Helm, Boots, Gloves, Necklace, Bracers, Belt, Ring)):
                        action = 'wear'
                    else:
                        caller.msg("You can't equip {}.".format(obj.get_display_name(caller)))

                if not obj.access(caller, 'equip'):
                    caller.msg("You can't {} {}.".format(action, obj.get_display_name(caller)))
                    return

                if obj in caller.equip:
                    caller.msg("You're already {}ing {}.".format(action, obj.get_display_name(caller)))
                    return

                # check whether slots are occupied
                occupied_slots = [caller.equip.get(s) for s in obj.db.slots if caller.equip.get(s)]
                if obj.db.multi_slot:
                    if len(occupied_slots) > 0:
                        if swap:
                            for item in occupied_slots:
                                caller.equip.remove(item)
                        else:
                            caller.msg("You can't {} {}. ".format(action, obj.get_display_name(caller)) + "You already have something there.")
                            return
                else:
                    if len(occupied_slots) == len(obj.db.slots):
                        if swap:
                            caller.equip.remove(occupied_slots[0])
                        else:
                            caller.msg("You can't {} {}. ".format(
                                action,
                                obj.get_display_name(caller)) + "You have no open {} slot{}.".format(
                                ", or ".join(obj.db.slots),
                                "s" if len(obj.db.slots) != 1 else ""
                            ))
                            return

                if not caller.equip.add(obj):
                    caller.msg("You can't {} {}.".format(action, obj.get_display_name(caller)))
                    return

                # call hook
                if hasattr(obj, "at_equip"):
                    obj.at_equip(caller)

                caller.msg("You {} {}.".format(action, obj.get_display_name(caller)))
                caller.location.msg_contents(
                    "{actor} {action}s {obj}.",
                    mapping=dict(actor=caller, obj=obj, action=action),
                    exclude=caller)
        else:
            # no arguments; display current equip
            data = []
            s_width = max(len(s) for s in caller.equip.slots)
            for slot, item in caller.equip:
                if not item or not item.access(caller, 'view'):
                    continue
                stat = " "
                if item.attributes.has('damage_roll'):
                    stat += "(|rDamage: {:>2}|n) ".format(item.db.damage_roll)
                if item.attributes.has('physical_bonus'):
                    stat += "(|yPhysical bonus: {:>2}|n)".format(item.db.physical_bonus)
                if item.attributes.has('magical_bonus'):
                    stat += "(|yMagical bonus: {:>2}|n)".format(item.db.magical_bonus)
                if item.attributes.has('range'):
                    stat += "(|G{}|n) ".format(item.db.range.capitalize())

                data.append(
                    "  |b{slot:>{swidth}.{swidth}}|n: {item:<20.20} {stat}".format(
                        slot=slot.capitalize(),
                        swidth=s_width,
                        item=item.name,
                        stat=stat,
                    )
                )
            if len(data) <= 0:
                output = "You have nothing in your equipment."
            else:
                table = EvTable(header=False, border=None, table=[data])
                output = "|YYour equipment:|n\n{}".format(table)

            caller.msg(output)


class CmdWear(MuxCommand):
    """
    wear an item
    Usage:
      wear[/swap] <item>
    Switches:
      s[wap] - replaces any currently equipped item
    Equips a set of armor from your inventory to an available armor
    equipment slot on your character.
    """
    key = "wear"
    locks = "cmd:all()"
    wield = False

    def func(self):
        caller = self.caller
        args = self.args.strip()

        if not args:
            caller.msg("Wear what?")
            return

        obj = caller.search(
            args,
            candidates=caller.contents,
            nofound_string=_INVENTORY_ERRMSG.format(args))

        if not obj:
            return

        elif any(obj.is_typeclass(i, exact=False) for i in (Torso, Helm, Boots, Gloves, Necklace, Bracers, Belt, Ring)):
            sw = ("/{}".format("/".join(self.switches))
                  if self.switches else "")

            caller.execute_cmd('equip',
                               args=' '.join((sw, args)),
                               item=obj,
                               action='wear')
        else:
            caller.msg("You can't wear {}.".format(
                obj.get_display_name(caller)))


class CmdWield(MuxCommand):
    """
    wield an item
    Usage:
        wield[/swap] <item>
    Switches:
        s[wap] - replaces any currently equipped item
    Equips a weapon or shield from your inventory to an available
    "wield" equipment slot on your character.
    """
    key = "wield"
    locks = "cmd:all()"

    def func(self):
        caller = self.caller
        args = self.args.strip()

        if not args:
            caller.msg("Wield what?")
            return

        obj = caller.search(
            args,
            candidates=caller.contents,
            nofound_string=_INVENTORY_ERRMSG.format(args))

        if not obj:
            return
        elif any(obj.is_typeclass(i, exact=False) for i in (CraftingTool, PickAxe, Weapon)):
            sw = ("/{}".format("/".join(self.switches)) if self.switches else "")

            caller.execute_cmd('equip', args=' '.join((sw, args)), item=obj, action='wield')
        else:
            caller.msg("You can't wield {}.".format(
                obj.get_display_name(caller)))


class CmdRemove(MuxCommand):
    """
    remove item
    Usage:
      remove <obj>
    Remove an equipped object and return it to your inventory.
    """
    key = "unequip"
    aliases = ["remove"]
    locks = "cmd:all()"

    def func(self):
        caller = self.caller
        args = self.args.strip()

        if not args:
            caller.msg("Remove what?")
            return

        # search for target in our equip
        equipped_items = [i[1] for i in caller.equip if i[1]]
        obj = caller.search(
            args,
            candidates=equipped_items,
            nofound_string=_EQUIP_ERRMSG.format(args))

        if not obj:
            return

        if not caller.equip.remove(obj):
            return

        # call hook
        if hasattr(obj, "at_remove"):
            obj.at_remove(caller)

        caller.msg("You remove {}.".format(
            obj.get_display_name(caller)))
        caller.location.msg_contents(
            "{actor} removes {item}.",
            mapping=dict(actor=caller, item=obj),
            exclude=caller)
