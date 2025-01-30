from ThimeusConstants import MELEE_ATTACK, RANGED_ATTACK, SWORD, FLAMETHROWER, AXE, STAFF, HOOK, GUN


# Class of the Weapon for Player and Enemies
class Weapon:
    def __init__(self, character_height, weapon_type):
        self.type = weapon_type

        if self.type == SWORD:
            self.duration = 14
            self.delay = self.duration + 7
            self.attack = MELEE_ATTACK
            self.l = character_height
            self.w = self.l / 3
            self.blit_point = (self.w / 3, -self.l / 12 * 11)
            self.projectile_pos = (self.w * 2, -self.l / 5)
            self.polygons = [[(self.w / 4, 0), (self.w / 4 * 3, self.l / 6),
                              (self.w / 4 * 3, self.l / 4 * 3), (self.w / 4, self.l / 4 * 3)],

                             [(self.w / 16 * 7, self.l / 6 * 5), (self.w / 16 * 9, self.l / 6 * 5),
                              (self.w / 16 * 9, self.l), (self.w / 16 * 7, self.l)],

                             [(0, self.l / 4 * 3), (self.w, self.l / 4 * 3),
                              (self.w / 4 * 3, self.l / 6 * 5), (self.w / 4, self.l / 6 * 5)],

                             [(self.w / 8 * 2.8, self.l / 12 * 9.5), (self.w / 2, self.l / 12 * 8.5),
                              (self.w / 8 * 5.2, self.l / 12 * 9.5)]]
            self.damage = 30

        elif self.type == FLAMETHROWER:
            self.duration = 4
            self.delay = self.duration + 1
            self.attack = RANGED_ATTACK
            self.l = character_height / 5
            self.w = self.l * 4
            self.blit_point = (self.w / 100, -self.l / 1.7)
            self.projectile_pos = (self.w * 1.3, -self.l / 3)
            self.polygons = [[(self.w / 4, self.l / 6), (self.w / 12 * 11, self.l / 6),
                              (self.w / 12 * 11, self.l / 2), (self.w / 4, self.l / 2)],

                             [(0, self.l), (self.w / 4, self.l), (self.w / 12 * 5, self.l / 6),
                              (self.w / 6, self.l / 6)],

                             [(self.w / 6 * 5, 0), (self.w, 0), (self.w, self.l / 3 * 2),
                              (self.w / 6 * 5, self.l / 3 * 2)],

                             [(self.w / 12 * 5, self.l / 2), (self.w / 3 * 2, self.l / 2),
                              (self.w / 4 * 3, self.l), (self.w / 2, self.l)]]
            self.damage = 4

        elif self.type == AXE:
            self.duration = 7
            self.delay = self.duration + 36
            self.attack = MELEE_ATTACK
            self.l = character_height
            self.w = self.l / 12 * 5
            self.blit_point = (self.w / 3, -self.l / 12 * 8)
            self.projectile_pos = (self.w * 3, -self.l / 6)
            self.polygons = [[(self.w / 5 * 2, 0), (self.w / 5, self.l / 12),
                              (self.w / 5, self.l), (self.w / 5 * 2, self.l / 6 * 5)],

                             [(0, self.l / 6), (self.w / 5 * 2, self.l / 6), (self.w, self.l / 12),
                              (self.w, self.l / 12 * 5), (self.w / 5 * 3.5, self.l / 12 * 7),
                              (self.w / 2, self.l / 3), (0, self.l / 3)]]
            self.damage = 30

        elif self.type == STAFF:
            self.duration = 11
            self.delay = self.duration + 70
            self.attack = RANGED_ATTACK
            self.l = character_height * 1.5
            self.w = self.l / 9 * 2
            self.blit_point = (self.w * 0.3, -self.l * 0.6)
            self.projectile_pos = (self.w * 1.5, -self.l / 3)
            self.polygons = [[(self.w / 16 * 7, self.l / 3), (self.w / 16 * 9, self.l / 3),
                              (self.w / 16 * 9, self.l), (self.w / 16 * 7, self.l)],

                             [(self.w / 4, 0), (self.w / 2, self.l / 18 * 3.5),
                              (self.w / 4, self.l / 18 * 4.5), (self.w / 4 * 1.25, self.l / 3),
                              (self.w / 4 * 2.75, self.l / 3), (self.w / 4 * 2.5, self.l / 18 * 4.5),
                              (self.w / 4 * 3.5, self.l / 18 * 3.5)],

                             [(self.w / 4 * 0.8, self.l / 3), (self.w / 4 * 3.2, self.l / 3),
                              (self.w / 2, self.l / 9 * 4)]]
            self.damage = 15

        elif self.type == HOOK:
            self.duration = 11
            self.delay = self.duration + 7
            self.attack = MELEE_ATTACK
            self.l = character_height
            self.w = self.l / 12 * 5
            self.blit_point = (self.w / 5, -self.l / 12 * 10)
            self.projectile_pos = (self.w * 2, -self.l / 5)
            self.polygons = [[(0, 0), (self.w, 0), (self.w / 5 * 3.25, self.l / 12 * 8.5),
                              (self.w / 5 * 1.75, self.l / 12 * 8.5), (self.w / 5 * 4, self.l / 12),
                              (self.w / 5, self.l / 12), (self.w / 5, self.l / 3)],

                             [(self.w / 5 * 2.25, self.l / 4 * 3),
                              (self.w / 5 * 2.75, self.l / 4 * 3),
                              (self.w / 5 * 2.75, self.l / 12 * 11),
                              (self.w / 5 * 2.25, self.l / 12 * 11)],

                             [(self.w / 5, self.l / 12 * 8.5), (self.w / 5 * 4, self.l / 12 * 8.5),
                              (self.w / 5 * 3.5, self.l / 4 * 3), (self.w / 5 * 1.5, self.l / 4 * 3)],

                             [(self.w / 5 * 2, self.l / 12 * 11), (self.w / 5 * 3, self.l / 12 * 11),
                              (self.w / 2, self.l)]]
            self.damage = 20

        elif self.type == GUN:
            self.duration = 7
            self.delay = 7
            self.attack = RANGED_ATTACK
            self.l = character_height / 2.5
            self.w = self.l * 2
            self.blit_point = (self.w / 7, -self.l * 0.68)
            self.projectile_pos = (self.w * 1.3, -self.l / 3)
            self.polygons = [[(self.w / 12 * 5.5, self.l / 3), (self.w / 12 * 10.5, self.l / 3),
                              (self.w, self.l / 6 * 0.5), (self.w / 12 * 7, self.l / 6 * 0.5)],

                             [(self.w / 12 * 6.5, self.l / 6 * 2.5), (self.w / 3 * 2, self.l / 3 * 2),
                              (self.w, self.l / 3 * 2), (self.w / 12 * 10.5, self.l / 6 * 2.5)],

                             [(0, self.l / 6 * 5), (self.w / 12, self.l / 2),
                              (self.w / 12 * 2.5, self.l / 2), (self.w / 12 * 1.5, self.l / 6 * 5)],

                             [(self.w / 3, self.l / 2), (self.w / 12 * 5.5, self.l / 2),
                              (self.w / 12 * 6.5, self.l), (self.w / 12 * 5, self.l)],

                             [(0, self.l / 6 * 1.5), (self.w / 4 * 3, self.l / 6 * 1.5),
                              (self.w / 6 * 5, self.l / 2), (self.w / 12, self.l / 2)]]
            self.damage = 10
