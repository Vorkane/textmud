from commands.command import MuxCommand
from evennia.utils.evform import EvForm
# from evennia.utils import evtable
from prettytable import PrettyTable as Table
# from typeclasses.characters import wield_slots
# from typeclasses.characters import armor_slots
# from typeclasses.characters import clothing_slots

# armor="\n\t".join([self.caller.equip.get(slot).get_display_name(self.caller) for slot in armor_slots if self.caller.equip.get(slot)])


class CmdEquipmentSheet(MuxCommand):
    """
    view characters equipment

    Usage: eqsheet
    """
    key = "eqsheet"
    locks = "cmd:all()"

# https://github.com/InspectorCaracal/evennia-minimud/blob/06812187bdd096ace4675afcc122d75d68533470/commands/skills.py#L4

    def func(self):

        # carry_table = evtable.EvTable(border="header")
        # wear_table = evtable.EvTable(border="header")

        # carried = [obj for obj in items if not obj.db.worn]
        # names_and_descs = [(obj.get_display_name(self.caller), obj.get_display_desc(self.caller)) for obj in set(carried)]
        # carried_sums = {tup: names_and_descs.count(tup) for tup in set(names_and_descs)}
        # worn = [obj for obj in items if obj.db.worn]

        # # message_list.append("|wYou are carrying:|n")
        # # for item in carried:
        # for (name, desc), count in carried_sums.items():
        #     carry_table.add_row(
        #         # item.get_display_name(self.caller), item.get_display_desc(self.caller)
        #         f"{count}x {name}", desc
        #     )

        armor_table = Table(header=False)

        # armor_table.add_row("Test1")
        # armor_table.add_row("Test2")
        # armor_table.add_row("Test3")

        armor_slots = ['Helm', 'Torso', 'Bracers', 'Belt', 'Legs', 'Boots']

        # armor_table.add_column()
        for armor in armor_slots:
            armor_table.add_row([f"{armor}", self.caller.equip.get(str(armor).lower()).get_display_name(self.caller) if callable(getattr(self.caller.equip.get(str(armor).lower()), 'get_display_name', False)) else "Empty"])

        # self.caller.msg(armor_table)
        # table = Table(title="Star Wars Movies", width=80)

        # table.add_column("Released", no_wrap=True)
        # table.add_column("Title")
        # table.add_column("Box Office", justify="right")

        # table.add_row("Dec 20, 2019", "Star Wars: The Rise of Skywalker", "$952,110,690")
        # table.add_row("May 25, 2018", "Solo: A Star Wars Story", "$393,151,347")
        # table.add_row("Dec 15, 2017", "Star Wars Ep. V111: The Last Jedi", "$1,332,539,889")
        # table.add_row("Dec 16, 2016", "Rogue One: A Star Wars Story", "$1,332,439,889")

        # table = evtable.EvTable(header=False, border="cells", header_line_char="-")
        # table.add_header("Equipment")
        # tableA = evtable.EvTable(header=False, border="cells", header_line_char="-")
        # tableA.add_header("Armor")
        # tableA.add_column('Head', 'Chest', 'Arms', 'Belt', 'Legs', 'Feet', xpos=0, enforce_size=True, width=12, hpad_char="*", fill_char=" ")
        # tableA.add_column(self.caller.equip.get('helm').get_display_name(self.caller) if callable(getattr(self.caller.equip.get('helm'), 'get_display_name', False)) else "Empty",
        #                                                   self.caller.equip.get('torso').get_display_name(self.caller) if callable(getattr(self.caller.equip.get('torso'), 'get_display_name', False)) else "Empty",
        #                                                   self.caller.equip.get('bracers').get_display_name(self.caller) if callable(getattr(self.caller.equip.get('bracers'), 'get_display_name', False)) else "Empty",
        #                                                   self.caller.equip.get('belt').get_display_name(self.caller) if callable(getattr(self.caller.equip.get('belt'), 'get_display_name', False)) else "Empty",
        #                                                   self.caller.equip.get('legs').get_display_name(self.caller) if callable(getattr(self.caller.equip.get('legs'), 'get_display_name', False)) else "Empty",
        #                                                   self.caller.equip.get('boots').get_display_name(self.caller) if callable(getattr(self.caller.equip.get('boots'), 'get_display_name', False)) else "Empty", xpos=1, width=30, hpad_char="*", hfill_char="^")

        # tableA.add_row('Head', self.caller.equip.get('helm').get_display_name(self.caller) if callable(getattr(self.caller.equip.get('helm'), 'get_display_name', False)) else "Empty", hfill_char="*")
        # tableA.add_row('Chest', self.caller.equip.get('torso').get_display_name(self.caller) if callable(getattr(self.caller.equip.get('torso'), 'get_display_name', False)) else "Empty")
        # tableA.add_row('Arms', self.caller.equip.get('bracers').get_display_name(self.caller) if callable(getattr(self.caller.equip.get('bracers'), 'get_display_name', False)) else "Empty")
        # tableA.add_row('Belt', self.caller.equip.get('belt').get_display_name(self.caller) if callable(getattr(self.caller.equip.get('belt'), 'get_display_name', False)) else "Empty")
        # tableA.add_row('Legs', self.caller.equip.get('legs').get_display_name(self.caller) if callable(getattr(self.caller.equip.get('legs'), 'get_display_name', False)) else "Empty")
        # tableA.add_row('Feet', self.caller.equip.get('boots').get_display_name(self.caller) if callable(getattr(self.caller.equip.get('boots'), 'get_display_name', False)) else "Empty")
        # table.reformat(width=80, maxwidth=80)
        # tableA.reformat(width=50, maxwidth=60)
        # tableA = evtable.EvTable(
        #               table=[['Head', 'Chest', 'Arms', 'Belt', 'Legs', 'Feet'],
        #                                                  [self.caller.equip.get('helm').get_display_name(self.caller) if callable(getattr(self.caller.equip.get('helm'), 'get_display_name', False)) else "Empty",
        #                                                   self.caller.equip.get('torso').get_display_name(self.caller) if callable(getattr(self.caller.equip.get('torso'), 'get_display_name', False)) else "Empty",
        #                                                   self.caller.equip.get('bracers').get_display_name(self.caller) if callable(getattr(self.caller.equip.get('bracers'), 'get_display_name', False)) else "Empty",
        #                                                   self.caller.equip.get('belt').get_display_name(self.caller) if callable(getattr(self.caller.equip.get('belt'), 'get_display_name', False)) else "Empty",
        #                                                   self.caller.equip.get('legs').get_display_name(self.caller) if callable(getattr(self.caller.equip.get('legs'), 'get_display_name', False)) else "Empty",
        #                                                   self.caller.equip.get('boots').get_display_name(self.caller) if callable(getattr(self.caller.equip.get('boots'), 'get_display_name', False)) else "Empty"]])
        # self.caller.msg(armor_table)

        # console = Console()

        # # console.print(armor_table)

        # with console.capture() as capture:
        #     console.print(armor_table)

        # text = capture.get()
        self.caller.msg(armor_table)


class CmdEquipmentSheetOld(MuxCommand):
    """
    view characters equipment

    Usage: eqsheet
    """

    key = "eqsheet"
    locks = "cmd:all()"

    def func(self):
        """
        Handle displaying equipment sheet
        """
        # wield1 = self.caller.equip.get('wield1').get_display_name(self.caller) if callable(getattr(self.caller.equip.get('wield1'), 'get_display_name', False)) else "Empty"
        # wield2 = self.caller.equip.get('wield2').get_display_name(self.caller) if callable(getattr(self.caller.equip.get('wield2'), 'get_display_name', False)) else "Empty"
        # wield1 = callable(getattr(self.caller.equip.get('wield1'), 'get_display_name', 'Empty'))

        form = EvForm('commands.templates.equipsheet', align='c')
        form.map(cells={
            'A': self.caller.equip.get('helm').get_display_name(self.caller) if callable(getattr(self.caller.equip.get('helm'), 'get_display_name', False)) else "Empty",
            'B': self.caller.equip.get('torso').get_display_name(self.caller) if callable(getattr(self.caller.equip.get('torso'), 'get_display_name', False)) else "Empty",
            'C': self.caller.equip.get('bracers').get_display_name(self.caller) if callable(getattr(self.caller.equip.get('bracers'), 'get_display_name', False)) else "Empty",
            'D': self.caller.equip.get('belt').get_display_name(self.caller) if callable(getattr(self.caller.equip.get('belt'), 'get_display_name', False)) else "Empty",
            'E': self.caller.equip.get('legs').get_display_name(self.caller) if callable(getattr(self.caller.equip.get('legs'), 'get_display_name', False)) else "Empty",
            'F': self.caller.equip.get('boots').get_display_name(self.caller) if callable(getattr(self.caller.equip.get('boots'), 'get_display_name', False)) else "Empty",
            'G': 'Necklace',
            'H': 'Trinket',
            'I': 'Earring 1',
            'J': 'Earring 2',
            'K': 'Ring 1',
            'L': 'Ring 2',
            'M': self.caller.equip.get('wield1').get_display_name(self.caller) if callable(getattr(self.caller.equip.get('wield1'), 'get_display_name', False)) else "Empty",
            'N': self.caller.equip.get('wield2').get_display_name(self.caller) if callable(getattr(self.caller.equip.get('wield2'), 'get_display_name', False)) else "Empty"
        })

        # fields = {
        #     'C': self.caller.equip.get('wield1').get_display_name(self.caller),
        #     'D': getattr(self.caller.equip.get('wield2'), self.caller.get_display_name(self.caller), "Empty")

        # }
        # form.map({k: self._format_trait_val(v) for k, v in fields.items()})

        self.caller.msg(form)

    def _format_trait_val(self, val):
        """Format trait values as bright white."""
        return "|w{}|n".format(val)
