# Salvo
# v0_9_6_9zj

#Notes To Self

#SIGN OFF NOTES 11/07/19 1:30am:
# * Must finish integration of the Obstacle class within the MasterSector, as it currently does not allow the instantiate_unit method to be used on it, and as such it cannot be created within the scope
#of the MasterSector itself, as opposed to as an outside object - this is crucial as, to avoid unnecessary cluttering, all objects will be housed within the MasterSector and any outside necessities will
#utilize the unit_id, which is returned from the instantiate_unit method.
# ^> Much of the integration of the Obstacle class has been complete, and the instantiate_unit method has been ammended to include the Obstacle class successfully. Currently, the obstacle (much like the other units)
#is still generated from code outside of the MasterSector class, which must be remedied entirely in order to preserve consistency and ensure that objects are completely deleted when called for, rather than referenced
#by forgotten variables outside of the scope of the MasterSector.
# * Must add death animation/functionality, though the current methods are working as intended.
# * The solution to true, legitimate integration has been realized, as the only outliers are currently the AI's and the issues that they possess - including the player. The resolution, however, is simple:
#The AIs must also be housed within the MasterSector, and their generation functions must be integrated as well. The direct affecting of the unit - as well as the housing of the unit within the AI - will cease,
#to be replaced with references. The connection between the two will be the unit_id, as it should have been all along. The AI will reference the tank (or whatever unit it is associated with) by the unit_id, which
#it will share and be referenced by in kind. Thus, when the MasterSector deletes a unit_object, it may also delete any AI_objects that share the same unit_id, resolving their existance and ensuring no unnecessary
#objects remain in memory due to circular referencing.
# ^> The player will be somewhat similar, however I am beginning to consider the possibility that, perhaps, the player might require their own class, which will allow for control of their unit much the same as the
#AI controls theirs. This would also allow for the quick exchange of vehicles, should alternate units ever be implemented (for example, a mecha-soldier)
# * The unit_objects still require a deletion method, as well. This will be implemented following the inclusion of this revelation regarding the AI/player-class, as they will require deletion simultaneously with
#their object (more than likely not the player, however, as this would represent significant difficulties for the game as a whole.)

#CURRENT VERSION CHANGES
# * Checked the integration of the Obstacle class within the MasterSector class, and all seems well - granted this is suspicious in and of itself, and will be regarded with distrust for the forseeable future.
# * Integrated the Munition and Impact classes within the MasterSector class, housing them completely within the MasterSector and delegating the responsibility to it, as well. They are now spawned into being
#within the MasterSector class (well - the Impact class is, the Munition class still requires that final touch) and the Munition class is slated for the damage methodology to be implemented, as it receives the
#unit_id of the colliding unit prior to its deletion, which it currently ignores. This information is ready for the development of a legitimate health and damage system.

#
#Current Version To-Do:
# *1 Implement true obstacles as a feature in the game and a legitimate object integrated within the MasterSector class.
# *2 Health and Damage system, as an Enemy AI cannot be created without such a feature.
# *3 Create an AI for the enemy to utilize that includes firing capabilities.
# *4 Properly implement munitions colliding with obstacles using the MasterSector features necessary to do so.


#To-do:
#AI's, obviously. Also, eventually a ground-soldier, to appease Spencer.
#
#Create a radio that may be unlocked / utilized by the player - perhaps by simply obtaining a component to repair it that allows codes to be entered
#in the style of an outdated flip-phone text message, allowing for cheat codes and easter eggs to be unlocked. Nuclear launch codes may also be
#obtained and utilized, by combining multiple codes and striking the designated area.
#
#Health / Damage mechanism, area-of-effect detonation from munitions/impact functions for non-explosive rounds
#
# * Create variant munition types - for example, a missile-style round that creates a curved trajectory towards the desired target, exploding
#in an area of effect style, which could be useful for barrages of missiles. There could also be a munition that explodes on a timed-delay. There
#also needs to be a munition style that acts as a bomb, falling from above to explode like an air-strike.

#Other:
# * Create a vehicle unit that is not a tank, but more like a truck. Create a trailer-type vehicle unit that can be moved with the truck and dropped
#in position. This will be difficult. The trailers could house their own weapon systems - anti-tank-guns, anti-air-guns, turrets, etc, and could
#even be manned by soldier units, requiring a gunner in order to function.
# * Adding to the radio specified above, which WILL happen, create a sort of kill-streak/something mechanism, allowing for designating targets for
#air support, as well. These, instead of being the bonuses from kills accumulating into a reward, will be picked up as dropped-items with varying
#degrees of rarity. In order to ensure that the nuke remains special, all other dropped call-in items will be a single code that can be used without
#manual input into the radio. The atomic bomb, however, will require manual input of a special series of multiple codes entered into the radio. They
#will come in partial sections (e.g, "Bravo-Niner-Alpha", "Kilo-Delta-Two", "Foxtrot-Three-Seven"), once the full code is entered, the nuclear bomb
#may be designated.
# * Also create a radio-system that allows for cassettes to be played for different music. These cassettes can be picked up and loaded in, creating
#various tracks to be used for music as either a loaded system like trays (cassette-1, cassette-2, cassette-3, etc) all being played in order, or
#with a repeat option, playing one cassette on a loop.
#
#KNOWN ERRORS:
# * (v0_9_6_9e) 10/24/19 - collision_correction_circle_width
#A ValueError returned from the collision correction system, recognized when one of the draw.circle methods attempts to draw its circle, yet has a radius
#of less than 1, causing a crash.
# * (v0_9_6_9e) 10/24/19 - collision_correction_object_overlap
#A bug causing the collision correction system not to properly correct a collision, resulting in the overlap of two objects and causing
#them to occupy the same space simultaneously, which is known to be considerably issuous in terms of physics for multiple reasons. A potential
#solution would be to provide legitimate object relocation, repositioning objects as necessary to avoid such difficulties entirely based on
#criteria that recognize an overlap occurance. 


import os, pygame, sys, random, math, copy
from math import sqrt
from pygame.locals import *
import pathfinding_salvo_rework
import numpy
import copy

import time #UNIMPORT UPON TESTING COMPLETION


get_line = pathfinding_salvo_rework.get_line
vec2int = pathfinding_salvo_rework.vec2int
vec = pygame.math.Vector2

WINDOWWIDTH = 1080
WINDOWHEIGHT = 640

FPS = 60

#R G B
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
BLUE = (0, 0, 155)
BRIGHTBLUE = (0, 0, 255)
RED = (155, 0, 0)
BRIGHTRED = (255, 0, 0)
GREEN = (0, 155, 0)
BRIGHTGREEN = (0, 255, 0)
NINETYFOURGREY = (148, 148, 148)
FORTYFOURGREY = (68, 68, 68)
BEIGE = (255, 255, 200)
VIOLET = (185, 132, 255)

BGCOLOR = BEIGE

UP = 'up'
DOWN = 'down'
LEFT = 'left'
RIGHT = 'right'

CURRENT_TIME = 0



#----------------Tank Class
class Tank():
    def __init__(self, chassis, turret, munitions_omni, alt_start_ammo, chassis_pos, allegiance, master_sector):

        chassis = dict(chassis)
        chassis['chassis_move_speed'] = dict(chassis['chassis_move_speed'])
        chassis['chassis_direction'] = dict(chassis['chassis_direction'])
        chassis['health'] = dict(chassis['health'])
        turret = dict(turret)
        munitions_omni = list(munitions_omni)
        for x in range(len(munitions_omni)):
            munitions_omni[x] = dict(munitions_omni[x])

        self.unit_type = 'tank'
        self.health = chassis['health']
        self.chassis_img = chassis['img']
        self.turret_img = turret['img']
        self.chassis_move_speed = chassis['chassis_move_speed']
        self.chassis_turn_speed = chassis['chassis_turn_speed']
        self.turret_rotation_speed = turret['turret_rotation_speed']
        self.chassis_pos = chassis_pos
        self.degree_val = 0.0
        self.chassis_degree_val = 0.0
        self.chassis_move_pos = chassis_pos
        self.turret_pos = chassis_pos
        self.chassis_bounding_offsets = chassis['bounding_offsets']
        self.weapon_bounding_offsets = [{'bounding_offsets': turret['weapons'][x][4], 'center': turret['weapons'][x][5]} for x in range(len(turret['weapons']))]
        self.chassis_turret_offset = chassis['turret_offsets']
        self.chassis_direction = chassis['chassis_direction']
        self.previous_degree_val = 0.0
        self.rotated_chassis = chassis['img']
        self.rotated_chassis_rect = chassis['img'].get_rect()
        self.rotated_turret = turret['img']
        self.rotated_turret_rect = turret['img'].get_rect()
        self.prior_chassis_position = self.rotated_chassis_rect.center
        self.prior_turret_position = self.rotated_turret_rect.center
        self.prior_chassis_degree_val = self.chassis_degree_val
        self.prior_turret_degree_val = self.degree_val
        self.chassis_turret_pos = None
        self.chassis_rotate_offset = chassis['rotate_offset']
        self.turret_rotate_offset = turret['rotate_offset']
        self.current_turret_tip_pos = None
        self.absolute_turret_tip_pos = []
        self.weapon_variables = turret['weapons']
        self.weapon_firing = [{'firing': False, 'release_required': False, 'last_shot': 0, 'reload_required': True, 'reload_initiated_ms': -10000} if self.weapon_variables[x][2] == 'semi' else {'firing': False, 'release_required': None, 'last_shot': 0,  'reload_required': True, 'reload_initiated_ms': -10000} for x in range(len(turret['weapons']))]
        self.weapon_loadout = [{'weapon': x, 'munition_loaded': None, 'munition_object': None, 'ammo_loaded': 0} for x in range(len(turret['weapons']))]
        self.alt_start_ammo = alt_start_ammo
        self.ammunition_loadout = {munitions_omni[x]['munition_type']: {'firing_rate': munitions_omni[x]['firing_rate'], 'round_capacity': munitions_omni[x]['round_capacity'], 'reload_time_ms': munitions_omni[x]['reload_time_ms'], 'ammo_quantity': alt_start_ammo[munitions_omni[x]['munition_type']], 'maximum_ammo': munitions_omni[x]['maximum_ammo']} if munitions_omni[x]['munition_type'] in alt_start_ammo else {'firing_rate': munitions_omni[x]['firing_rate'], 'round_capacity': munitions_omni[x]['round_capacity'], 'reload_time_ms': munitions_omni[x]['reload_time_ms'], 'ammo_quantity': munitions_omni[x]['initial_ammo'], 'maximum_ammo': munitions_omni[x]['maximum_ammo']} for x in range(len(munitions_omni))} 
        self.chassis_mask = None
        self.turret_mask = None
        self.munitions_omni = munitions_omni
        self.target = (0, 0)
        self.chassis_sprite = self.create_sprite('chassis')
        self.turret_sprite = self.create_sprite('turret')
        self.load_munitions()
        self.unit_id = self.generate_unit_id()
        self.allegiance = allegiance
        self.node_distance = chassis['node_distance']
        self.rotate_chassis()
        self.bounding_points = None
        self.weapon_bounding_points = None
        self.get_chassis_turret_pos()
        self.get_chassis_bounding_points()
        self.get_weapon_bounding_points()
        self.furthest_turret_tip_offset = self.get_turret_furthest_tip_offset()
        self.furthest_turret_tip_pos = None
        self.master_sector = master_sector
        self.master_sector.create_unit(self.unit_id, self.allegiance, self.unit_type, {'chassis': {'rect': self.rotated_chassis_rect, 'degree_val': self.chassis_degree_val, 'pos': self.chassis_pos, 'bounding_points': self.bounding_points, 'rot_axis': self.rotated_chassis_rect.center, 'unit_spec': 'chassis', 'unit_sprite': self.chassis_sprite}, 'turret': {'rect': self.rotated_turret_rect, 'degree_val': self.degree_val, 'pos': (self.rotated_turret_rect.x, self.rotated_turret_rect.y), 'weapon_bounding_points': self.weapon_bounding_points, 'rot_axis': self.chassis_turret_pos, 'unit_spec': 'turret', 'unit_sprite': self.turret_sprite}})


    def generate_unit_id(self):
        raw_unit_id = next(ID_GENERATOR)
        unit_id_time = pygame.time.get_ticks()
        unit_id = raw_unit_id[0] + str(unit_id_time) + raw_unit_id[1]
        return unit_id


    def move_chassis(self): #(chassis_direction, chassis_turn_speed, chassis_degree_val): # 1
        chassis_direction = self.chassis_direction
        chassis_turn_speed = self.chassis_turn_speed
        chassis_degree_val = self.chassis_degree_val

        if chassis_direction['turn'] == 'clockwise':
            if chassis_degree_val <= 180 - chassis_turn_speed:
                chassis_degree_val += chassis_turn_speed
            elif chassis_degree_val > 180 - chassis_turn_speed:
                chassis_degree_val = chassis_degree_val + chassis_turn_speed - 360
        elif chassis_direction['turn'] == 'counterclock':
            if chassis_degree_val - chassis_turn_speed > -180:
                chassis_degree_val -= chassis_turn_speed
            elif chassis_degree_val - chassis_turn_speed <= -180:
                chassis_degree_val = chassis_degree_val - chassis_turn_speed + 360

        self.chassis_degree_val = chassis_degree_val


    def rotate_chassis(self): #(chassis_img, chassis_degree_val, chassis_pos): # 2
        chassis_img = self.chassis_img
        chassis_degree_val = self.chassis_degree_val
        chassis_pos = self.chassis_pos
        rotate_offset = self.chassis_rotate_offset
        
        chassis_width, chassis_height = chassis_img.get_size()
        chassis_original_center = (chassis_pos[0] + chassis_width / 2, chassis_pos[1] + chassis_height / 2)

        offset = pygame.math.Vector2(rotate_offset)
        rotated_chassis = pygame.transform.rotozoom(chassis_img, -chassis_degree_val, 1)
        rotated_chassis_offset = offset.rotate(0.0) #(chassis_degree_val)
        rotated_chassis_rect = rotated_chassis.get_rect(center=chassis_original_center + rotated_chassis_offset)

        self.rotated_chassis = rotated_chassis
        self.rotated_chassis_rect = rotated_chassis_rect
        self.chassis_degree_val = chassis_degree_val
        self.chassis_mask = pygame.mask.from_surface(self.rotated_chassis)
        


    def drive_chassis(self): #(rotated_chassis, chassis_degree_val, chassis_pos, rotated_chassis_rect, chassis_direction): # 3
        rotated_chassis = self.rotated_chassis
        rotated_chassis_rect = self.rotated_chassis_rect
        chassis_degree_val = self.chassis_degree_val
        chassis_pos = self.chassis_pos
        chassis_direction = self.chassis_direction
        chassis_move_speed = self.chassis_move_speed


        if chassis_direction['move'] == 'forward':
            chassis_velocity = pygame.math.Vector2(1, 0).rotate(chassis_degree_val) * chassis_move_speed['forward']
            chassis_move_pos = chassis_pos + chassis_velocity
            self.chassis_move_pos = chassis_move_pos
        
        elif chassis_direction['move'] == 'reverse':
            chassis_velocity = pygame.math.Vector2(1, 0).rotate(chassis_degree_val) * chassis_move_speed['reverse']
            chassis_move_pos = chassis_pos + chassis_velocity
            self.chassis_move_pos = chassis_move_pos
            
        else:
            self.chassis_move_pos = chassis_pos


    def get_chassis_turret_pos(self): #(rotated_chassis, chassis_degree_val, chassis_pos, rotated_chassis_rect): # 4
        rotated_chassis = self.rotated_chassis
        rotated_chassis_rect = self.rotated_chassis_rect
        chassis_degree_val = self.chassis_degree_val
        chassis_pos = self.chassis_pos
        chassis_img = self.chassis_img
    
        chassis_width, chassis_height = chassis_img.get_size()
        chassis_original_center = rotated_chassis_rect.center

        offset = pygame.math.Vector2(-18, -1)
        rotated_chassis = pygame.transform.rotozoom(chassis_img, -chassis_degree_val, 1)
        rotated_chassis_offset = offset.rotate(chassis_degree_val)
        rotated_chassis_rect = rotated_chassis.get_rect(center=chassis_original_center + rotated_chassis_offset)

        chassis_turret_pos = rotated_chassis_rect.center

        self.chassis_turret_pos = chassis_turret_pos


    def get_chassis_bounding_points(self):
        rotated_chassis = self.rotated_chassis
        rotated_chassis_rect = self.rotated_chassis_rect
        chassis_degree_val = self.chassis_degree_val
        chassis_pos = self.chassis_pos
        chassis_img = self.chassis_img

        chassis_width, chassis_height = chassis_img.get_size()
        chassis_original_center = rotated_chassis_rect.center

        bounding_points = []

        bounding_offsets = self.chassis_bounding_offsets
        for x in range(len(bounding_offsets)):
            offset = pygame.math.Vector2(bounding_offsets[x][0], bounding_offsets[x][1])
            rotated_chassis = pygame.transform.rotozoom(chassis_img, -chassis_degree_val, 1)
            rotated_chassis_offset = offset.rotate(chassis_degree_val)
            rotated_chassis_rect = rotated_chassis.get_rect(center=chassis_original_center + rotated_chassis_offset)
            bounding_pos_x = rotated_chassis_rect.center
            bounding_points.append(bounding_pos_x)
        self.bounding_points = bounding_points


    def get_turret_center_pos(self): #(chassis_turret_pos): # 5
        chassis_turret_pos = self.chassis_turret_pos
        turret_img = self.turret_img

        turret_pos_center = chassis_turret_pos
        turret_width, turret_height = turret_img.get_size()
        turret_pos_x = turret_pos_center[0] - (turret_width / 2)
        turret_pos_y = turret_pos_center[1] - (turret_height / 2)
        turret_pos = (turret_pos_x, turret_pos_y)

        self.turret_pos = turret_pos

    def get_turret_furthest_tip_offset(self):
        furthest_center_offset = 0
        for x in range(len(self.weapon_variables)):
            weapon_x = self.weapon_variables[x]
            if weapon_x[0][0] > furthest_center_offset:
                furthest_center_offset = weapon_x[0][0]
        furthest_turret_tip_offset = (furthest_center_offset, 0)
        return furthest_turret_tip_offset


    def get_turret_center_tip_pos(self): #This is the solution to avoiding needless rotation of the image in order to determine positions of rotated points.
        turret_pos = self.turret_pos
        degree_val = self.degree_val
        turret_img = self.turret_img
        offset = pygame.math.Vector2(self.furthest_turret_tip_offset)

        turret_width, turret_height = turret_img.get_size()
        turret_original_center = (turret_pos[0] + turret_width / 2, turret_pos[1] + turret_height / 2)
        rotated_offset = offset.rotate(degree_val)

        rotated_turret_tip_rect = self.rotated_turret.get_rect(center=turret_original_center + rotated_offset)

        rotated_turret_tip_pos = rotated_turret_tip_rect.center

        self.furthest_turret_tip_pos = rotated_turret_tip_pos
        


    def get_turret_tip_pos(self): #(turret_pos, degree_val): # 6
        turret_pos = self.turret_pos
        degree_val = self.degree_val
        turret_img = self.turret_img

        offset = pygame.math.Vector2(0, 0)
        turret_width, turret_height = turret_img.get_size()
        turret_original_center = (turret_pos[0] + turret_width / 2, turret_pos[1] + turret_height / 2)

        rotated_turret = pygame.transform.rotozoom(turret_img, -degree_val, 1)
        rotated_offset = offset.rotate(degree_val)
        rotated_turret_rect = rotated_turret.get_rect(center=turret_original_center + rotated_offset)

        current_turret_tip_pos = rotated_turret_rect.center
        
        self.current_turret_tip_pos = current_turret_tip_pos


    def get_absolute_turret_tip_pos(self, weapon_x): # 10
        turret_pos = self.turret_pos
        degree_val = self.degree_val
        turret_img = self.turret_img
        weapon_x_offset = weapon_x[0]

        absolute_offset = pygame.math.Vector2(weapon_x_offset)
        turret_width, turret_height = turret_img.get_size()
        absolute_turret_original_center = (turret_pos[0] + turret_width /2, turret_pos[1] + turret_height / 2)
        absolute_rotated_offset = absolute_offset.rotate(degree_val)

        rotated_turret = pygame.transform.rotozoom(turret_img, -degree_val, 1)
        rotated_turret_rect = rotated_turret.get_rect(center=absolute_turret_original_center + absolute_rotated_offset)

        absolute_turret_tip_pos = rotated_turret_rect.center

        self.absolute_turret_tip_pos.append(absolute_turret_tip_pos)
        

    def get_mouse_turret_angle(self): #(mouse, current_turret_tip_pos, previous_degree_val): # 7
        mouse = {}
        mouse['mouse_x'] = self.target[0]
        mouse['mouse_y'] = self.target[1]
        current_turret_tip_pos = self.current_turret_tip_pos
        previous_degree_val = self.previous_degree_val
        rotation_speed = self.turret_rotation_speed

        targeting_radians = math.atan2(mouse['mouse_y'] - current_turret_tip_pos[1], mouse['mouse_x'] - current_turret_tip_pos[0])
        targeting_degrees = math.degrees(targeting_radians)

        previous_360 = previous_degree_val
        targeting_360 = targeting_degrees
        opposite_360 = targeting_360 - 180
        if previous_360 < 0:
            previous_360 = previous_360 + 360
        if targeting_360 < 0:
            targeting_360 = targeting_degrees + 360    
        if opposite_360 < 0:
            opposite_360 = opposite_360 + 360        

        clockwise_dist = 0
        counterclock_dist = 0
        direction = None

        if targeting_360 > previous_360:
            clockwise_dist = targeting_360 - previous_360
            counterclock_dist = previous_360 + (360 - targeting_360)
        elif targeting_360 < previous_360:
            clockwise_dist = (360 - previous_360) + targeting_360
            counterclock_dist = previous_360 - targeting_360

        if clockwise_dist < counterclock_dist:
            direction = 'clockwise'
        elif clockwise_dist > counterclock_dist:
            direction = 'counterclock'
        elif clockwise_dist == counterclock_dist:
            direction = 'clockwise'

        if direction == 'clockwise':
            if clockwise_dist <= rotation_speed:
                targeting_degrees = targeting_degrees
            else:
                if previous_360 + rotation_speed > 180:
                    targeting_degrees = (previous_360 + rotation_speed) - 360
                elif previous_360 + rotation_speed <= 180:
                    targeting_degrees = previous_360 + rotation_speed
        elif direction == 'counterclock':
            if counterclock_dist <= rotation_speed:
                targeting_degrees = targeting_degrees
            else:
                if previous_360 - rotation_speed > 180:
                    targeting_degrees = (previous_360 - rotation_speed) - 360
                elif previous_360 - rotation_speed <= 180 and previous_360 - rotation_speed >= 0:
                    targeting_degrees = previous_360 - rotation_speed
                elif previous_360 - rotation_speed < 0:
                    targeting_degrees = previous_360 - rotation_speed

        self.degree_val = targeting_degrees


    def rotate_on_turret_pivot_point(self): #(turret_img, degree_val, turret_pos): # 8
        turret_img = self.turret_img
        degree_val = self.degree_val
        turret_pos = self.turret_pos
        rotate_offset = self.turret_rotate_offset

        turret_width, turret_height = turret_img.get_size()
        turret_original_center = (turret_pos[0] + turret_width / 2, turret_pos[1] + turret_height / 2)

        offset = pygame.math.Vector2(rotate_offset)
        rotated_turret = pygame.transform.rotozoom(turret_img, -degree_val, 1)
        rotated_offset = offset.rotate(degree_val)
        rotated_turret_rect = rotated_turret.get_rect(center=turret_original_center + rotated_offset)
        #start_turret = pygame.transform.rotozoom(turret_img, -0.0, 1)
        #start_turret_rect = start_turret.get_rect(center=turret_original_center + offset.rotate(0.0))

        self.rotated_turret = rotated_turret
        self.rotated_turret_rect = rotated_turret_rect
        self.degree_val = degree_val
        self.turret_mask = pygame.mask.from_surface(self.rotated_turret)
        self.rect = rotated_turret_rect
        self.mask = self.turret_mask


    def get_weapon_bounding_points(self):
        turret_pos = self.turret_pos
        rotated_turret = self.rotated_turret
        rotated_turret_rect = self.rotated_turret_rect
        turret_width, turret_height = self.turret_img.get_size()
        turret_original_center = (turret_pos[0] + turret_width /2, turret_pos[1] + turret_height / 2)

        bounding_groups = []

        for x in range(len(self.weapon_bounding_offsets)):
            bounding_x = []
            for i in range(len(self.weapon_bounding_offsets[x]['bounding_offsets'])):
                bounding_offset_x = self.weapon_bounding_offsets[x]['bounding_offsets'][i]
                offset = pygame.math.Vector2(bounding_offset_x[0], bounding_offset_x[1])
                rotated_turret_offset = offset.rotate(self.degree_val)
                rotated_turret_rect = rotated_turret.get_rect(center=turret_original_center + rotated_turret_offset)
                bounding_pos_i = rotated_turret_rect.center
                bounding_x.append(bounding_pos_i)
            center_offset = pygame.math.Vector2(self.weapon_bounding_offsets[x]['center'][0], self.weapon_bounding_offsets[x]['center'][1])
            rotated_turret_offset = center_offset.rotate(self.degree_val)
            rotated_turret_rect = rotated_turret.get_rect(center=turret_original_center + rotated_turret_offset)
            center_pos = rotated_turret_rect.center
            
            bounding_groups.append({'bounding_points': bounding_x, 'center': center_pos})
        self.weapon_bounding_points = bounding_groups
                
        


    def update_target_via_mouse(self, mouse):
        self.target = (mouse['mouse_x'], mouse['mouse_y'])


    def update_chassis_direction_via_keys(self, chassis_direction):
        self.chassis_direction = chassis_direction


    def fire_selected_battery(self, battery_num):
        batteries = ['primary', 'secondary', 'tertiary']
        selected_battery = batteries[battery_num]
        for x in range(len(self.weapon_loadout)):
            weapon = x
            if self.weapon_variables[x][1] == selected_battery:
                if self.weapon_firing[weapon]['release_required'] == None or self.weapon_firing[weapon]['release_required'] == False:
                    ready_to_fire = self.weapon_firing_rate_check(weapon)
                    if ready_to_fire == True:
                        ammo_remaining = self.munitions_ammo_check(weapon)
                        if ammo_remaining == True:
                            if self.weapon_firing[weapon]['reload_required'] == False:
                                munition = Munition(self.weapon_loadout[weapon]['munition_object'], self.degree_val, self.absolute_turret_tip_pos[weapon], self.unit_id, self.allegiance, self.master_sector)
                                self.master_sector.add_munition_object(munition)
                                self.weapon_loadout[weapon]['ammo_loaded'] -= 1
                                recheck_ammo = self.munitions_ammo_check(weapon)
                                if self.weapon_firing[weapon]['release_required'] == False:
                                    self.weapon_firing[weapon]['release_required'] = True

                                self.weapon_firing[weapon]['last_shot'] = CURRENT_TIME
                                #return munition
                                return None
        return None


    def update_firing_check(self, weapon_firing):

        for x in range(len(self.weapon_loadout)):
            self.weapon_firing[x]['firing'] = weapon_firing[self.weapon_variables[x][1]]

            if self.weapon_variables[x][2] == 'semi' and weapon_firing[self.weapon_variables[x][1]] == False and self.weapon_firing[x]['release_required'] == True:
                self.weapon_firing[x]['release_required'] = False

            


    def weapons_firing_initiate(self):

        for x in range(len(self.weapon_loadout)):
            if self.weapon_firing[x]['firing'] == True and self.weapon_variables[x][1] == 'primary':
                self.fire_selected_battery(0)
            elif self.weapon_firing[x]['firing'] == True and self.weapon_variables[x][1] == 'secondary':
                self.fire_selected_battery(1)
            elif self.weapon_firing[x]['firing'] == True and self.weapon_variables[x][1] == 'tertiary':
                self.fire_selected_battery(2)



    def load_munitions(self):
        for x in range(len(self.weapon_variables)):
            munition_loaded = None
            munition_object = None
            for i in range(len(self.munitions_omni)):
                if self.weapon_variables[x][1] == self.munitions_omni[i]['designation'] and self.munitions_omni[i]['munition_type'] in self.weapon_variables[x][3]:
                    munition_loaded = self.munitions_omni[i]['munition_type']
                    munition_object = self.munitions_omni[i]
                    break
            self.weapon_loadout[x]['munition_loaded'] = munition_loaded
            self.weapon_loadout[x]['munition_object'] = munition_object

        return None
            

    def reload_weapons(self):
        for x in range(len(self.weapon_loadout)):
            weapon_x = self.weapon_loadout[x]
            weapon_x_firing = self.weapon_firing[x]
            if weapon_x_firing['reload_required'] == True:
                if CURRENT_TIME - weapon_x_firing['reload_initiated_ms'] >= self.ammunition_loadout[weapon_x['munition_loaded']]['reload_time_ms']:
                    self.weapon_firing[x]['reload_required'] = False
                    self.weapon_firing[x]['reload_initiated_ms'] = 0
                    if self.ammunition_loadout[weapon_x['munition_loaded']]['ammo_quantity'] > 0:
                        if self.ammunition_loadout[weapon_x['munition_loaded']]['round_capacity'] <= self.ammunition_loadout[weapon_x['munition_loaded']]['ammo_quantity']:
                            self.weapon_loadout[x]['ammo_loaded'] = self.ammunition_loadout[weapon_x['munition_loaded']]['round_capacity']
                            self.ammunition_loadout[weapon_x['munition_loaded']]['ammo_quantity'] -= self.ammunition_loadout[weapon_x['munition_loaded']]['round_capacity']
                        else:
                            self.weapon_loadout[x]['ammo_loaded'] = self.ammunition_loadout[weapon_x['munition_loaded']]['ammo_quantity']
                            self.ammunition_loadout[weapon_x['munition_loaded']]['ammo_quantity'] = 0
                
    

    def munitions_ammo_check(self, weapon):

        if self.weapon_loadout[weapon]['ammo_loaded'] > 0:
            return True
        else:
            if self.weapon_firing[weapon]['reload_required'] == False:
                self.weapon_firing[weapon]['reload_required'] = True
                self.weapon_firing[weapon]['reload_initiated_ms'] = CURRENT_TIME
            return False


    def initiate_reload_requirement(self, weapon):
        weapon_types = ['primary', 'secondary', 'tertiary']
        weapon_reloading = weapon_types[weapon]
        
        for x in range(len(self.weapon_variables)):
            if self.weapon_variables[x][1] == weapon_reloading:
                if self.weapon_loadout[x]['ammo_loaded'] < self.ammunition_loadout[self.weapon_loadout[x]['munition_loaded']]['round_capacity']:
                    self.ammunition_loadout[self.weapon_loadout[x]['munition_loaded']]['ammo_quantity'] += self.weapon_loadout[x]['ammo_loaded']
                    self.weapon_loadout[x]['ammo_loaded'] = 0



    def weapon_firing_rate_check(self, weapon):

        firing_rate = self.ammunition_loadout[self.weapon_loadout[weapon]['munition_loaded']]['firing_rate']
        firing_pause = 1000 / firing_rate

        if CURRENT_TIME - self.weapon_firing[weapon]['last_shot'] > firing_pause:
            return True
        else:
            return False
            
    

    def create_sprite(self, sprite):
        if sprite == 'chassis':
            img = self.chassis_img
            rect = self.chassis_img.get_rect()
            mask = pygame.mask.from_surface(img.convert_alpha())

            chassis_sprite = gameSprite(img, rect, mask)

            return chassis_sprite

        elif sprite == 'turret':
            img = self.turret_img
            rect = self.turret_img.get_rect()
            mask = pygame.mask.from_surface(img.convert_alpha())

            turret_sprite = gameSprite(img, rect, mask)

            return turret_sprite


    def update_sprite(self, sprite):
        if sprite == 'chassis':
            self.chassis_sprite.img = self.rotated_chassis
            self.chassis_sprite.rect = self.rotated_chassis_rect
            self.chassis_sprite.mask = self.chassis_mask

        elif sprite == 'turret':
            self.turret_sprite.img = self.rotated_turret
            self.turret_sprite.rect = self.rotated_turret_rect
            self.turret_sprite.mask = self.turret_mask     


    def update_master_sector(self):
        self.master_sector.update_unit(self.unit_id, self.allegiance, self.unit_type, {'chassis': {'rect': self.rotated_chassis_rect, 'degree_val': self.chassis_degree_val, 'pos': self.chassis_pos, 'bounding_points': self.bounding_points, 'rot_axis': self.rotated_chassis_rect.center, 'unit_sprite': self.chassis_sprite}, 'turret': {'rect': self.rotated_chassis_rect, 'degree_val': self.chassis_degree_val, 'pos': self.chassis_pos, 'bounding_points': self.bounding_points, 'rot_axis': self.rotated_chassis_rect.center}, 'turret': {'rect': self.rotated_turret_rect, 'degree_val': self.degree_val, 'pos': (self.rotated_turret_rect.x, self.rotated_turret_rect.y), 'weapon_bounding_points': self.weapon_bounding_points, 'rot_axis': self.chassis_turret_pos, 'unit_sprite': self.turret_sprite}})


    def check_unit_collision(self):
        if self.prior_chassis_pos != self.rotated_chassis_rect.center or self.prior_chassis_degree_val != self.chassis_degree_val:
            degree_change = self.master_sector.reorient_unit_collisions_omni(self.unit_id)
            if degree_change != 0.0:
                self.chassis_degree_val += degree_change
                self.rotate_chassis()
                self.get_chassis_turret_pos()
                self.get_turret_center_pos()
                self.get_turret_tip_pos()
                self.previous_degree = self.degree_val
                self.absolute_turret_tip_pos = []
                for x in range(len(self.weapon_variables)):
                    weapon_x = self.weapon_variables[x]
                    self.get_absolute_turret_tip_pos(weapon_x)
                self.get_turret_center_tip_pos()
                self.get_chassis_bounding_points()
                self.get_weapon_bounding_points()
                self.update_sprite('chassis')
                self.update_sprite('turret')
                self.update_master_sector()

        if self.prior_turret_pos != self.chassis_turret_pos or self.prior_turret_degree_val != self.degree_val:
            degree_change = self.master_sector.reorient_turret_collisions_omni(self.unit_id)
            if degree_change != 0.0:
                self.degree_val += degree_change
                self.get_turret_tip_pos()
                self.previous_degree_val = self.degree_val
                self.absolute_turret_tip_pos = []
                for x in range(len(self.weapon_variables)):
                    weapon_x = self.weapon_variables[x]
                    self.get_absolute_turret_tip_pos(weapon_x)
                self.get_turret_center_tip_pos()
                self.get_weapon_bounding_points()
                self.update_sprite('turret')
                self.update_master_sector()

    
    def create_health_bar(self):
        health_surf = pygame.Surface((100, 10))
        damage_surf = pygame.Surface((100, 10))
        health_surf.fill((0, 255, 0))
        damage_surf.fill((255, 0, 0))
        health_percent = int((self.health['health'] / self.health['max_health']) * 100)
        health_surf.blit(damage_surf, (health_percent, 0))
        health_surf_rect = health_surf.get_rect()
        health_surf_rect.center = self.rotated_chassis_rect.center
        DISPSURF.blit(health_surf, health_surf_rect)

                

            


    def generate_tank(self, DISPSURF):

        self.prior_chassis_pos = self.rotated_chassis_rect.center
        self.prior_turret_pos = self.rotated_turret_rect.center
        self.prior_chassis_degree_val = self.chassis_degree_val
        self.prior_turret_degree_val = self.degree_val

        self.move_chassis() #1

        self.rotate_chassis() #2

        self.drive_chassis() #3
            
        self.get_chassis_turret_pos() #4

        self.get_turret_center_pos() #5

        self.get_turret_tip_pos() #6
        
        self.previous_degree_val = self.degree_val
        
        self.get_mouse_turret_angle() #7

        self.rotate_on_turret_pivot_point() #8

        self.chassis_pos = self.chassis_move_pos #9

        self.absolute_turret_tip_pos = []
        for x in range(len(self.weapon_variables)):
            weapon_x = self.weapon_variables[x]
            self.get_absolute_turret_tip_pos(weapon_x)

        self.get_turret_center_tip_pos()


        self.reload_weapons()

        self.get_chassis_bounding_points()
        self.get_weapon_bounding_points()

        self.update_sprite('chassis')
        self.update_sprite('turret')

        self.update_master_sector()
        self.check_unit_collision()
        DISPSURF.blit(self.rotated_chassis, self.rotated_chassis_rect)
        DISPSURF.blit(self.rotated_turret, self.rotated_turret_rect)
        self.create_health_bar()


    
#--------------------MUNITION CLASS

        #{'img': standard_shell_img, 'munition_move_speed': 21, 'maximum_distance': 2000, 'designation': 'primary', 'munition_offset': (10, 0)}

class Munition():
    def __init__(self, munition, munition_degree_val, munition_pos, unit_id, allegiance, master_sector):

        #WILL NEED TO MAKE SEPARATE DICTS/LISTS IN SIMILAR FASHION TO TANK TO AVOID
        #ISSUES WITH DICT OR LIST REFERENCES ALTERING INTENDED EFFECTS IN UNFORSEEABLE
        #YET HILARIOUS WAYS

        #print('mun{}, deg{}, pos{}, id{}, alleg{}'.format(munition, munition_degree_val, munition_pos, unit_id, allegiance))
        
        self.munition_img = munition['img']
        self.munition_type = munition['munition_type']
        self.munition_move_speed = munition['munition_move_speed']
        self.munition_damage = munition['damage']
        self.degree_variance = munition['degree_variance']
        self.munition_degree_val = munition_degree_val
        self.munition_degree_change = False
        self.munition_pos = munition_pos
        self.rotated_munition = None
        self.rotated_munition_rect = None
        self.rotated_munition_center = None
        self.munition_origin_pos = None
        self.absolute_munition_pos = None
        self.distance_traveled = 0
        self.maximum_distance = munition['maximum_distance']
        self_munition_offset = munition['munition_offset']
        self.exceeded_distance = False
        self.collision_check = False
        self.previous_munition_pos = None
        self.impact_variables = munition['impact']
        self.munition_mask = None
        self.munition_sprite = self.create_sprite()
        self.apply_degree_variance()
        self.impact_degree_val = munition_degree_val
        self.unit_id = unit_id
        self.munition_id = self.generate_munition_id()
        self.allegiance = allegiance
        self.get_munition_center()
        self.rotate_munition()
        self.master_sector = master_sector
        self.master_sector.create_munition(self.munition_id, self.unit_id, self.allegiance, self.munition_type, {'rect': self.rotated_munition_rect, 'degree_val': self.munition_degree_val, 'pos': self.munition_pos, 'rot_axis': self.rotated_munition_rect.center, 'unit_sprite': self.munition_sprite})
       

    def generate_munition_id(self):
        raw_unit_id = next(ID_GENERATOR)
        unit_id_time = pygame.time.get_ticks()
        unit_id = raw_unit_id[0] + str(unit_id_time) + raw_unit_id[1]
        return unit_id


    def rotate_munition(self):
        
        munition_img = self.munition_img
        munition_degree_val = self.munition_degree_val
        munition_pos = self.munition_origin_pos
        
        munition_width, munition_height = munition_img.get_size()
        munition_original_center = (munition_pos[0] + munition_width / 2, munition_pos[1] + munition_height / 2)

        munition_offset = pygame.math.Vector2(10, 0)
        rotated_munition = pygame.transform.rotozoom(munition_img, -munition_degree_val, 1)
        rotated_munition_offset = munition_offset.rotate(munition_degree_val)
        rotated_munition_rect = rotated_munition.get_rect(center=munition_pos + rotated_munition_offset) #(center=munition_original_center + rotated_munition_offset)
        rotated_munition_center = rotated_munition_rect.center
        rotated_munition_rect.center = munition_pos + rotated_munition_offset
        

        self.rotated_munition_center = rotated_munition_center
        self.rotated_munition = rotated_munition
        self.rotated_munition_rect = rotated_munition_rect
        self.munition_mask = pygame.mask.from_surface(rotated_munition)


    def get_munition_circle_pos(self):
        munition_pos = self.munition_origin_pos
        munition_degree_val = self.munition_degree_val
        munition_img = self.munition_img

        absolute_offset = pygame.math.Vector2(0, 0)
        munition_width, munition_height = munition_img.get_size()
        absolute_munition_original_center = (munition_pos[0] + munition_width /2, munition_pos[1] + munition_height / 2)
        absolute_rotated_offset = absolute_offset.rotate(munition_degree_val)

        rotated_munition = pygame.transform.rotozoom(munition_img, -munition_degree_val, 1)
        rotated_munition_rect = rotated_munition.get_rect(center=absolute_munition_original_center + absolute_rotated_offset)

        absolute_munition_pos = rotated_munition_rect.center

        self.absolute_munition_pos = absolute_munition_pos


    def get_munition_center(self):
        munition_img = self.munition_img
        munition_origin_pos = self.munition_pos

        munition_width, munition_height = munition_img.get_size()
        munition_pos_x = munition_origin_pos[0] - (munition_width / 2)
        munition_pos_y = munition_origin_pos[1] - (munition_height / 2)
        munition_pos = (munition_pos_x, munition_pos_y)

        self.munition_origin_pos = munition_origin_pos


    def apply_degree_variance(self):
        degree_val = self.munition_degree_val
        if self.degree_variance != 0:
            degree_change = random.uniform(-self.degree_variance, self.degree_variance)


            if degree_val + degree_change <= -180:
                degree_val = (degree_val + degree_change) + 360
            elif degree_val + degree_change > 180:
                degree_val = (degree_val + degree_change) - 360
            else:
                degree_val += degree_change

        self.munition_degree_val = degree_val
        self.munition_degree_change = True
        


    def move_munition(self):
        self.previous_munition_pos = self.munition_pos
        
        rotated_munition = self.rotated_munition
        rotated_munition_rect = self.rotated_munition_rect
        munition_degree_val = self.munition_degree_val
        munition_pos = self.munition_pos
        munition_move_speed= self.munition_move_speed

        munition_velocity = pygame.math.Vector2(1, 0).rotate(munition_degree_val) * munition_move_speed
        munition_move_pos = munition_pos + munition_velocity
        munition_move_pos = (round(munition_move_pos[0]), round(munition_move_pos[1]))

        self.munition_pos = munition_move_pos
        self.distance_traveled += munition_move_speed

        if self.distance_traveled >= self.maximum_distance:
            self.exceeded_distance = True


    def create_sprite(self):
        img = self.munition_img
        rect = self.munition_img.get_rect()
        mask = pygame.mask.from_surface(self.munition_img)

        munition_sprite = gameSprite(img, rect, mask)

        return munition_sprite


    def update_sprite(self):
        self.munition_sprite.img = self.rotated_munition
        self.munition_sprite.rect = self.rotated_munition_rect
        self.munition_sprite.mask = self.munition_mask


    def generate_impact_orientation(self):
        if self.impact_variables['impact_orientation'] == 'random':
            self.impact_degree_val = random.uniform(0.0001, 360) - 180
        elif self.impact_variables['impact_orientation'] == 'inverse':
            if self.impact_degree_val <= 0:
                self.impact_degree_val += 180
            elif self.impact_degree_val > 0:
                self.impact_degree_val -= 180

        if self.impact_variables['impact_degree_variance'] != 0:
            self.impact_degree_val = random.uniform(self.impact_degree_val - self.impact_variables['impact_degree_variance'], self.impact_degree_val + self.impact_variables['impact_degree_variance'])

        if self.impact_variables['special_degree_fix'] != 0:
            if self.impact_degree_val + self.impact_variables['special_degree_fix'] <= 180:
                self.impact_degree_val += self.impact_variables['special_degree_fix']
            else:
                self.impact_degree_val += self.impact_variables['special_degree_fix'] - 360
            


    def impact_initiation(self):
        self.collision_check = True
        self.generate_impact_orientation()
        impact_object = ImpactAnimation(self.impact_variables['impact_animation'], self.impact_variables['columns_rows'], self.impact_variables['impact_offset'], self.previous_munition_pos, self.impact_degree_val, self.munition_id, self.master_sector)

        return impact_object

    
    def update_master_sector(self):
        self.master_sector.update_munition(self.munition_id, self.unit_id, self.allegiance, self.munition_type, {'rect': self.rotated_munition_rect, 'degree_val': self.munition_degree_val, 'pos': self.munition_pos, 'rot_axis': self.rotated_munition_rect.center, 'unit_sprite': self.munition_sprite})        


    def check_munition_collision(self):
        colliding_unit = self.master_sector.check_munition_sprite_collision(self.munition_id)
        if colliding_unit != None:
            impact_object = self.impact_initiation()
            self.master_sector.add_impact_object(impact_object)
            self.master_sector.cull_munition(self.munition_id)
            self.master_sector.enact_munition_damage(colliding_unit, self.munition_damage, self.rotated_munition_rect.center)

    
    def check_munition_distance(self):
        if self.exceeded_distance == True:
            self.master_sector.cull_munition(self.munition_id)


    def generate_munition(self):

        self.get_munition_center()
        self.rotate_munition()
        self.get_munition_circle_pos()
        self.update_master_sector()
        self.update_sprite()
        
        

        DISPSURF.blit(self.rotated_munition, self.rotated_munition_rect)

        self.move_munition()
        self.check_munition_collision()
        self.check_munition_distance()
        

#-------------------GameSprite Class
class gameSprite(pygame.sprite.Sprite):
    def __init__(self, img, rect, mask):
        self.img = img
        self.rect = rect
        self.mask = mask

        pygame.sprite.Sprite.__init__(self)




#----------------------GameSpriteSheet Class
class gameSpriteSheet():
    def __init__(self, spritesheet, columns, rows):
        self.spritesheet = spritesheet
        self.columns = columns
        self.rows = rows
        self.total_cell_count = columns * rows
        self.rect = self.spritesheet.get_rect()
        self.cell_width = int(self.rect.width / columns)
        self.cell_height = int(self.rect.height / rows)
        self.halfwidth, self.halfheight = (int(self.cell_width / 2), int(self.cell_height / 2))

        self.cells = list([(index % columns * self.cell_width, int(index / columns) * self.cell_height, self.cell_width, self.cell_height) for index in range(self.total_cell_count)])
        self.handle = list([
            (0, 0), (-self.halfwidth, 0), (-self.cell_width, 0),
            (0, -self.halfheight), (-self.halfwidth, -self.halfheight), (-self.cell_width, -self.halfheight),
            (0, -self.cell_height), (-self.halfwidth, -self.cell_height), (-self.cell_width, -self.cell_height),])


    def create_image(self, cell_index, handle=0):
        #surface = pygame.Surface((self.cell_width, self.cell_height))
        #surface.blit(self.spritesheet, (0 + self.handle[handle][0], 0 + self.handle[handle][1]), self.cells[cell_index])

        surface = self.spritesheet.subsurface(self.cells[cell_index])

        return surface



    

#------------------------ImpactAnimation Class
class ImpactAnimation():
    def __init__(self, spritesheet, columns_rows, impact_offset, impact_pos, degree_val, impact_id, master_sector):
        self.impact_id = impact_id
        self.master_sector = master_sector
        self.spritesheet = spritesheet
        self.columns = columns_rows[0]
        self.rows = columns_rows[1]
        self.spritesheet_object = gameSpriteSheet(self.spritesheet, self.columns, self.rows)
        self.sheet_index = 0
        self.tick_counter = 0
        self.tick_maximum = 2
        self.max_index = self.columns * self.rows - 1
        self.current_sprite = None
        self.impact_offset = impact_offset
        self.impact_pos = impact_pos
        self.degree_val = degree_val
        self.animation_complete = False
        self.rotated_sprite = None
        self.rotated_sprite_rect = None
        self.get_current_sprite(initializing=True)
        self.rotate_sprite()
        self.master_sector.create_impact(self.impact_id, {'rect': self.rotated_sprite_rect, 'degree_val': self.degree_val, 'pos': self.impact_pos, 'rot_axis': self.rotated_sprite_rect.center, 'unit_sprite': self.current_sprite})
        


    def get_current_sprite(self, initializing=False):
        if self.animation_complete == False:
            self.current_sprite = self.spritesheet_object.create_image(self.sheet_index, 0)
            if initializing == False:
                self.tick_counter += 1
            if self.tick_counter == self.tick_maximum:
                if self.sheet_index < self.max_index:
                    self.sheet_index += 1
                    self.tick_counter = 0
                else:
                    self.animation_complete = True


    def rotate_sprite(self):
        image = self.current_sprite
        degree_val = self.degree_val
        
        image_width, image_height = image.get_size()
        image_original_center = (self.impact_pos[0], self.impact_pos[1])
        offset = pygame.math.Vector2(self.impact_offset)

        rotated_image = pygame.transform.rotozoom(image, -degree_val, 1)
        rotated_offset = offset.rotate(0.0) #(degree_val)
        rotated_image_rect = rotated_image.get_rect(center=image_original_center + rotated_offset)

        self.rotated_sprite = rotated_image
        self.rotated_sprite_rect = rotated_image_rect

    
    def update_master_sector(self):
        self.master_sector.update_impact(self.impact_id, {'rect': self.rotated_sprite_rect, 'degree_val': self.degree_val, 'pos': self.impact_pos, 'rot_axis': self.rotated_sprite_rect.center, 'unit_sprite': self.current_sprite})


    def check_animation_status(self):
        if self.animation_complete == True:
            self.master_sector.cull_impact(self.impact_id)


    def generate_impact(self):
        self.get_current_sprite()
        self.rotate_sprite()
        self.update_master_sector()
        self.check_animation_status()
        DISPSURF.blit(self.rotated_sprite, self.rotated_sprite_rect)




#-----------------------------------Obstacle Class
class Obstacle():
    def __init__(self, obstacle, obs_pos, degree_val, master_sector):
        self.obs_img = obstacle['img']
        self.obs_pos = obs_pos
        self.health = obstacle['health']
        self.degree_val = degree_val
        self.rotate_offset = obstacle['rotate_offset']
        self.rotated_obs = self.obs_img
        self.rotated_obs_rect = self.obs_img.get_rect()
        self.obs_sprite = self.create_sprite()
        self.bounding_offsets = obstacle['bounding_offsets']
        self.bounding_points = None
        self.rotate_obs()
        self.get_bounding_points()
        self.previous_degree_val = self.degree_val
        self.previous_pos = self.obs_pos
        self.obs_mask = None
        self.obs_sprite = self.create_sprite()
        self.allegiance = 'OBSTACLE'
        self.unit_spec = 'obstacle'
        self.unit_type = 'obstacle'
        self.unit_id = self.generate_unit_id()
        self.master_sector = master_sector
        self.master_sector.create_unit(self.unit_id, self.allegiance, self.unit_type, {'rect': self.rotated_obs_rect, 'degree_val': self.degree_val, 'pos': self.obs_pos, 'bounding_points': self.bounding_points, 'rot_axis': self.rotated_obs_rect.center, 'unit_spec': self.unit_spec, 'unit_sprite': self.obs_sprite})



    def create_sprite(self):
        img = self.rotated_obs
        rect = self.rotated_obs_rect
        mask = pygame.mask.from_surface(self.obs_img)

        obstacle_sprite = gameSprite(img, rect, mask)

        return obstacle_sprite

    
    def generate_unit_id(self):
        raw_unit_id = next(ID_GENERATOR)
        unit_id_time = pygame.time.get_ticks()
        unit_id = raw_unit_id[0] + str(unit_id_time) + raw_unit_id[1]
        return unit_id

    
    def rotate_obs(self):
        obs_img = self.obs_img
        degree_val = self.degree_val
        obs_pos = self.obs_pos
        rotate_offset = self.rotate_offset
        
        obs_width, obs_height = obs_img.get_size()
        obs_original_center = (obs_pos[0] + obs_width / 2, obs_pos[1] + obs_height / 2)

        offset = pygame.math.Vector2(rotate_offset)
        rotated_obs = pygame.transform.rotozoom(obs_img, -degree_val, 1)
        rotated_obs_offset = offset.rotate(0.0)
        rotated_obs_rect = rotated_obs.get_rect(center=obs_original_center + rotated_obs_offset)

        self.rotated_obs = rotated_obs
        self.rotated_obs_rect = rotated_obs_rect
        self.degree_val = degree_val
        self.obs_mask = pygame.mask.from_surface(self.rotated_obs)

    
    def get_bounding_points(self):
        rotated_obs = self.rotated_obs
        rotated_obs_rect = self.rotated_obs_rect
        degree_val = self.degree_val
        obs_pos = self.obs_pos
        obs_img = self.obs_img

        obs_width, obs_height = obs_img.get_size()
        obs_original_center = rotated_obs_rect.center

        bounding_points = []

        bounding_offsets = self.bounding_offsets
        for x in range(len(bounding_offsets)):
            offset = pygame.math.Vector2(bounding_offsets[x][0], bounding_offsets[x][1])
            rotated_obs = pygame.transform.rotozoom(obs_img, -degree_val, 1)
            rotated_obs_offset = offset.rotate(degree_val)
            rotated_obs_rect = rotated_obs.get_rect(center=obs_original_center + rotated_obs_offset)
            bounding_pos_x = rotated_obs_rect.center
            bounding_points.append(bounding_pos_x)
        self.bounding_points = bounding_points

    def update_sprite(self):
        self.obs_sprite.img = self.rotated_obs
        self.obs_sprite.rect = self.rotated_obs_rect
        self.obs_sprite.mask = self.obs_mask

    
    def draw_self(self):
        DISPSURF.blit(self.rotated_obs, self.rotated_obs_rect)

    
    def generate_obs(self):
        if self.previous_pos != self.obs_pos or self.previous_degree_val != self.degree_val:
            self.rotate_obs()
            self.get_bounding_points()
            self.update_sprite()
        self.draw_self()
        





#-----------------------------------Sector CLass
class Sector():
    def __init__(self, sector_rect):
        self.sector_rect = sector_rect
        self.sector_id = next(SECTOR_ID)
        self.unit_dict = {'PLAYER': [], 'ENEMY': [], 'ROGUE': [], 'OBSTACLE': []}
        self.unit_list_omni = []
        self.turret_list_omni = []
        self.munition_dict = {'PLAYER': [], 'ENEMY': [], 'ROGUE': []}
        self.munition_list_omni = []
        self.impact_list_omni = []


    def check_if_contained(self, unit_rect):
        containment = self.sector_rect.contains(unit_rect)
        return containment


    def add_unit(self, unit_allegiance, unit_id):
        if unit_id not in self.unit_dict[unit_allegiance]:
            self.unit_dict[unit_allegiance].append(unit_id)
            self.unit_list_omni.append(unit_id)


    def remove_unit(self, unit_allegiance, unit_id):
        if unit_id in self.unit_dict[unit_allegiance]:
            self.unit_dict[unit_allegiance].remove(unit_id)
            self.unit_list_omni.remove(unit_id)


    def add_turret(self, unit_id):
        if unit_id not in self.turret_list_omni:
            self.turret_list_omni.append(unit_id)

    def remove_turret(self, unit_id):
        if unit_id in self.turret_list_omni:
            self.turret_list_omni.remove(unit_id)

    
    def add_munition(self, unit_allegiance, munition_id):
        if munition_id not in self.munition_list_omni:
            self.munition_list_omni.append(munition_id)
            self.munition_dict[unit_allegiance].append(munition_id)

    
    def remove_munition(self, unit_allegiance, munition_id):
        if munition_id in self.munition_list_omni:
            self.munition_list_omni.remove(munition_id)
            self.munition_dict[unit_allegiance].remove(munition_id)
    

    def add_impact(self, impact_id):
        if impact_id not in self.impact_list_omni:
            self.impact_list_omni.append(impact_id)
    

    def remove_impact(self, impact_id):
        if impact_id in self.impact_list_omni:
            self.impact_list_omni.remove(impact_id)


    def draw_self(self, DISPSURF):
        pygame.draw.rect(DISPSURF, (0, 0, 0), self.sector_rect, 1)



#------------------------------------MasterSector Class
class MasterSector():
    def __init__(self):
        self.sectors_point_dict = {}
        self.sector_info = None
        self.sectors = self.generate_sectors()
        self.sector_keys = self.get_sector_keys()
        self.units = {}
        self.unit_objects = {}
        self.turrets = {}
        self.munitions = {}
        self.munition_objects = {}
        self.impacts = {}
        self.impact_objects = {}
        self.artificial_objects = {}



    def generate_sectors(self):
        sectors_dict = {}
        
        width_divisors = [x for x in range(1, WINDOWWIDTH) if WINDOWWIDTH % x == 0]
        height_divisors = [x for x in range(1, WINDOWHEIGHT) if WINDOWHEIGHT % x == 0]
        sector_size_width = max(width_divisors)
        max_sector_size = 300
        if sector_size_width > max_sector_size:
            while sector_size_width > max_sector_size:
                width_divisors.remove(sector_size_width)
                sector_size_width = max(width_divisors)
        sector_size_height = max(height_divisors)
        if sector_size_height > max_sector_size:
            while sector_size_height > max_sector_size:
                height_divisors.remove(sector_size_height)
                sector_size_height = max(height_divisors)

        self.sectors_info = {'sector_width': sector_size_width, 'sector_height': sector_size_height, 'sectors_x': int(WINDOWWIDTH / sector_size_width), 'sectors_y': int(WINDOWHEIGHT / sector_size_height)}

        current_x = 0
        current_y = 0

        for x in range(int(WINDOWHEIGHT / sector_size_height)):
            for i in range(int(WINDOWWIDTH / sector_size_width)):
                sector_rect_width = sector_size_width
                sector_rect_height = sector_size_height
                sector_rect = (current_x, current_y, sector_rect_width, sector_rect_height)
                sector_object = Sector(sector_rect)
                sectors_dict[sector_object.sector_id] = sector_object
                self.sectors_point_dict[(current_x, current_y)] = sector_object.sector_id

                current_x += sector_size_width
            current_x = 0
            current_y += sector_size_height

        return sectors_dict


    def get_sector_keys(self):
        sector_keys = [key_x for key_x in self.sectors.keys()]
        return sector_keys


    def sector_collision_check_all(self, unit_rect):
        colliding_sectors = [self.sectors[self.sector_keys[key_x]].sector_id for key_x in range(len(self.sector_keys)) if unit_rect.colliderect(self.sectors[self.sector_keys[key_x]].sector_rect) == True]
        return colliding_sectors


    def create_unit(self, unit_id, unit_allegiance, unit_type, unit_dict):
        if unit_type == 'tank':
            self.units[unit_id] = {'unit_id': unit_id, 'allegiance': unit_allegiance, 'unit_type': unit_type, 'sectors': [], 'unit_rect': unit_dict['chassis']['rect'], 'degree_val': unit_dict['chassis']['degree_val'], 'pos': unit_dict['chassis']['pos'], 'bounding_points': unit_dict['chassis']['bounding_points'], 'bounding_connections': {}, 'rot_axis': unit_dict['chassis']['rot_axis'], 'unit_spec': unit_dict['chassis']['unit_spec'], 'unit_sprite': unit_dict['chassis']['unit_sprite']}
            self.units[unit_id]['sectors'] = self.sector_point_collision_omni(unit_dict['chassis']['rect'])
            self.units[unit_id]['bounding_connections'] = self.get_unit_bounding_connections(unit_dict['chassis']['rect'], unit_dict['chassis']['bounding_points'])
            for x in range(len(self.units[unit_id]['sectors'])):
                sector_x_id = self.units[unit_id]['sectors'][x]
                self.sectors[sector_x_id].add_unit(unit_allegiance, unit_id)
            self.turrets[unit_id] = {'unit_id': unit_id, 'allegiance': unit_allegiance, 'unit_type': unit_type, 'sectors': [], 'unit_rect': unit_dict['turret']['rect'], 'degree_val': unit_dict['turret']['degree_val'], 'pos': unit_dict['turret']['pos'], 'weapon_bounding_points': unit_dict['turret']['weapon_bounding_points'], 'weapon_bounding_connections': {}, 'rot_axis': unit_dict['turret']['rot_axis'], 'unit_spec': unit_dict['turret']['unit_spec'], 'unit_sprite': unit_dict['turret']['unit_sprite']}
            self.turrets[unit_id]['sectors'] = self.sector_point_collision_omni(unit_dict['turret']['rect'])
            turret_bounding_connections = []
            for x in range(len(unit_dict['turret']['weapon_bounding_points'])):
                temp_rect = pygame.Rect(unit_dict['turret']['rect'])
                temp_rect.center = unit_dict['turret']['weapon_bounding_points'][x]['center']
                bounding_connections_x = self.get_unit_bounding_connections(temp_rect, unit_dict['turret']['weapon_bounding_points'][x]['bounding_points'])
                turret_bounding_connections.append(bounding_connections_x)
            self.turrets[unit_id]['weapon_bounding_connections'] = turret_bounding_connections
            for x in range(len(self.turrets[unit_id]['sectors'])):
                sector_x_id = self.turrets[unit_id]['sectors'][x]
                self.sectors[sector_x_id].add_turret(unit_id)

        elif unit_type == 'obstacle':
            self.units[unit_id] = {'unit_id': unit_id, 'allegiance': unit_allegiance, 'unit_type': unit_type, 'sectors': [], 'unit_rect': unit_dict['rect'], 'degree_val': unit_dict['degree_val'], 'pos': unit_dict['pos'], 'bounding_points': unit_dict['bounding_points'], 'bounding_connections': {}, 'rot_axis': unit_dict['rot_axis'], 'unit_spec': unit_dict['unit_spec'], 'unit_sprite': unit_dict['unit_sprite']}
            self.units[unit_id]['sectors'] = self.sector_point_collision_omni(unit_dict['rect'])
            self.units[unit_id]['bounding_connections'] = self.get_unit_bounding_connections(unit_dict['rect'], unit_dict['bounding_points'])
            for x in range(len(self.units[unit_id]['sectors'])):
                sector_x_id = self.units[unit_id]['sectors'][x]
                self.sectors[sector_x_id].add_unit(unit_allegiance, unit_id)

    
    def create_impact(self, impact_id, impact_dict):
        self.impacts[impact_id] = {'impact_id': impact_id, 'sectors': [], 'unit_rect': impact_dict['rect'], 'degree_val': impact_dict['degree_val'], 'pos': impact_dict['pos'], 'rot_axis': impact_dict['rot_axis'], 'unit_sprite': impact_dict['unit_sprite']}
        self.impacts[impact_id]['sectors'] = self.sector_point_collision_omni(impact_dict['rect'])
        for x in range(len(self.impacts[impact_id]['sectors'])):
            sector_x_id = self.impacts[impact_id]['sectors'][x]
            self.sectors[sector_x_id].add_impact(impact_id)


    def update_sectors_for_impact(self, impact_id, unit_rect):
        updated_sectors = self.sector_point_collision_omni(unit_rect)
        for x in range(len(self.impacts[impact_id]['sectors'])):
            if self.impacts[impact_id]['sectors'][x] not in updated_sectors:
                self.sectors[self.impacts[impact_id]['sectors'][x]].remove_impact(impact_id)
        for x in range(len(updated_sectors)):
            if impact_id not in self.sectors[updated_sectors[x]].impact_list_omni:
                self.sectors[updated_sectors[x]].add_impact(impact_id)
        return updated_sectors

    
    def instantiate_unit(self, unit_dict):
        '''
        Instantiates and houses various unit objects based upon specified type, requiring a passed dictionary appropriate to the unit type being instantiated.
        '''
        if unit_dict['unit_type'] == 'tank':
            new_unit = Tank(unit_dict['chassis'], unit_dict['turret'], unit_dict['munitions'], unit_dict['ammo'], unit_dict['pos'], unit_dict['allegiance'], self)
            self.unit_objects[new_unit.unit_id] = new_unit
            return new_unit.unit_id
        elif unit_dict['unit_type'] == 'obstacle': #Obstacle(pine_obs, obs_positions[x][0], obs_positions[x][1], master_sector)
            new_unit = Obstacle(unit_dict['obstacle'], unit_dict['pos'], unit_dict['degree_val'], self)
            self.unit_objects[new_unit.unit_id] = new_unit
            return new_unit.unit_id

    
    def instantiate_artificial(self, unit_id):
        '''
        Instantiates and houses an EnemyAI object, requiring that the corresponding unit-object has already been created. The EnemyAI object, referred to as an artificial, will
        be housed within the MasterSector.artificial_objects attribute.
        '''
        new_artificial = EnemyAI(unit_id, self)
        self.artificial_objects[new_artificial.unit_id] = new_artificial

    
    def create_munition(self, munition_id, unit_id, unit_allegiance, munition_type, munition_dict):
        self.munitions[munition_id] = {'munition_id': munition_id, 'unit_id': unit_id, 'allegiance': unit_allegiance, 'munition_type': munition_type, 'sectors': [], 'unit_rect': munition_dict['rect'], 'degree_val': munition_dict['degree_val'], 'pos': munition_dict['pos'], 'rot_axis': munition_dict['rot_axis'], 'unit_sprite': munition_dict['unit_sprite']}
        self.munitions[munition_id]['sectors'] = self.sector_point_collision_omni(munition_dict['rect'])
        for x in range(len(self.munitions[munition_id]['sectors'])):
            sector_x_id = self.munitions[munition_id]['sectors'][x]
            self.sectors[sector_x_id].add_munition(unit_allegiance, munition_id)


    def update_sectors_for_munition(self, munition_id, unit_allegiance, unit_rect):
        updated_sectors = self.sector_point_collision_omni(unit_rect)
        for x in range(len(self.munitions[munition_id]['sectors'])):
            if self.munitions[munition_id]['sectors'][x] not in updated_sectors:
                self.sectors[self.munitions[munition_id]['sectors'][x]].remove_munition(unit_allegiance, munition_id)
        for x in range(len(updated_sectors)):
            if munition_id not in self.sectors[updated_sectors[x]].munition_list_omni:
                self.sectors[updated_sectors[x]].add_munition(unit_allegiance, munition_id)
        return updated_sectors


    def check_munition_sprite_collision(self, munition_id):
        for x in range(len(self.munitions[munition_id]['sectors'])):
            sector_x = self.munitions[munition_id]['sectors'][x]
            for i in range(len(self.sectors[sector_x].unit_list_omni)):
                unit_i = self.sectors[sector_x].unit_list_omni[i]
                if self.munitions[munition_id]['unit_id'] != unit_i:
                    if self.munitions[munition_id]['unit_rect'].colliderect(self.units[unit_i]['unit_rect']):
                        mask_collision = pygame.sprite.collide_mask(self.munitions[munition_id]['unit_sprite'], self.units[unit_i]['unit_sprite'])
                        if mask_collision != None:
                            return unit_i


    def cull_unit(self, unit_id):
        '''
        Culls a unit from any sectors it inhabits, along with the MasterSector.units attribute, as well as the MasterSector.unit_objects attribute, erasing the unit.
        '''
        unit_allegiance = self.units[unit_id]['allegiance']
        for x in range(len(self.units[unit_id]['sectors'])):
            self.sectors[self.units[unit_id]['sectors'][x]].remove_unit(unit_allegiance, unit_id)
        del self.units[unit_id]
        del self.unit_objects[unit_id]
        if unit_id in self.artificial_objects:
            self.cull_artificial(unit_id)

    
    def cull_munition(self, munition_id):
        '''
        Culls a munition object from any sectors it inhabits, along with the MasterSector.munitions attribute, as well as the MasterSector.munition_objects attribute, erasing the munition.
        '''
        unit_allegiance = self.munitions[munition_id]['allegiance']
        for x in range(len(self.munitions[munition_id]['sectors'])):
            self.sectors[self.munitions[munition_id]['sectors'][x]].remove_munition(unit_allegiance, munition_id)
        del self.munitions[munition_id]
        del self.munition_objects[munition_id]

    
    def cull_impact(self, impact_id):
        '''
        Culls an impact object from any sectors it inhabits, along with the MasterSector.impacts attribute, as well as the MasterSector.impact_objects attribute, erasing the impact.
        '''
        for x in range(len(self.impacts[impact_id]['sectors'])):
            self.sectors[self.impacts[impact_id]['sectors'][x]].remove_impact(impact_id)
        del self.impacts[impact_id]
        del self.impact_objects[impact_id]
        
    
    def cull_artificial(self, unit_id):
        '''
        Culls an artificial object from the MasterSector.artificial_objects attribute.
        '''
        del self.artificial_objects[unit_id]
    


    def update_sectors_for_unit(self, unit_id, unit_allegiance, unit_rect, object_type='tank'):
        if object_type == 'tank':
            updated_sectors = self.sector_point_collision_omni(unit_rect)

            for x in range(len(self.units[unit_id]['sectors'])):
                if self.units[unit_id]['sectors'][x] not in updated_sectors:
                    self.sectors[self.units[unit_id]['sectors'][x]].remove_unit(unit_allegiance, unit_id)
            for x in range(len(updated_sectors)):
                if unit_id not in self.sectors[updated_sectors[x]].unit_dict[unit_allegiance]:
                    self.sectors[updated_sectors[x]].add_unit(unit_allegiance, unit_id)
            return updated_sectors
        elif object_type == 'turret':
            updated_sectors = self.sector_point_collision_omni(unit_rect)
            for x in range(len(self.turrets[unit_id]['sectors'])):
                if self.turrets[unit_id]['sectors'][x] not in updated_sectors:
                    self.sectors[self.turrets[unit_id]['sectors'][x]].remove_turret(unit_id)
            for x in range(len(updated_sectors)):
                if unit_id not in self.sectors[updated_sectors[x]].turret_list_omni:
                    self.sectors[updated_sectors[x]].add_turret(unit_id)
            return updated_sectors
        
        elif object_type == 'obstacle':
            updated_sectors = self.sector_point_collision_omni(unit_rect)
            for x in range(len(self.units[unit_id]['sectors'])):
                if self.units[unit_id]['sectors'][x] not in updated_sectors:
                    self.sectors[self.units[unit_id]['sectors'][x]].remove_unit(unit_allegiance, unit_id)
            for x in range(len(updated_sectors)):
                if unit_id not in self.sectors[updated_sectors[x]].unit_dict[unit_allegiance]:
                    self.sectors[updated_sectors[x]].add_unit(unit_allegiance, unit_id)
            return updated_sectors

    
    def update_impact(self, impact_id, impact_dict):
        if self.impacts[impact_id]['degree_val'] != impact_dict['degree_val'] or self.impacts[impact_id]['rot_axis'] != impact_dict['rot_axis'] or self.impacts[impact_id]['unit_sprite'] != impact_dict['unit_sprite']:
            self.impacts[impact_id]['degree_val'] = impact_dict['degree_val']
            self.impacts[impact_id]['pos'] = impact_dict['pos']
            self.impacts[impact_id]['unit_rect'] = impact_dict['rect']
            self.impacts[impact_id]['rot_axis'] = impact_dict['rot_axis']
            self.impacts[impact_id]['unit_sprite'] = impact_dict['unit_sprite']
            self.impacts[impact_id]['sectors'] = self.update_sectors_for_impact(impact_id, impact_dict['rect'])

    
    def update_munition(self, munition_id, unit_id, unit_allegiance, munition_type, munition_dict):
        if self.munitions[munition_id]['degree_val'] != munition_dict['degree_val'] or self.munitions[munition_id]['rot_axis'] != munition_dict['rot_axis']:
            self.munitions[munition_id]['degree_val'] = munition_dict['degree_val']
            self.munitions[munition_id]['pos'] = munition_dict['pos']
            self.munitions[munition_id]['unit_rect'] = munition_dict['rect']
            self.munitions[munition_id]['rot_axis'] = munition_dict['rot_axis']
            self.munitions[munition_id]['unit_sprite'] = munition_dict['unit_sprite']
            self.munitions[munition_id]['sectors'] = self.update_sectors_for_munition(munition_id, unit_allegiance, munition_dict['rect'])


    def update_unit(self, unit_id, unit_allegiance, unit_type, unit_dict):
        if unit_type == 'tank':
            if self.units[unit_id]['degree_val'] != unit_dict['chassis']['degree_val'] or self.units[unit_id]['rot_axis'] != unit_dict['chassis']['rot_axis']:
                self.units[unit_id]['degree_val'] = unit_dict['chassis']['degree_val']
                self.units[unit_id]['pos'] = unit_dict['chassis']['pos']
                self.units[unit_id]['unit_rect'] = unit_dict['chassis']['rect']
                self.units[unit_id]['bounding_points'] = unit_dict['chassis']['bounding_points']
                self.units[unit_id]['rot_axis'] = unit_dict['chassis']['rot_axis']
                self.units[unit_id]['unit_sprite'] = unit_dict['chassis']['unit_sprite']
                self.units[unit_id]['sectors'] = self.update_sectors_for_unit(unit_id, unit_allegiance, unit_dict['chassis']['rect'])

            if self.turrets[unit_id]['degree_val'] != unit_dict['turret']['degree_val'] or self.turrets[unit_id]['pos'] != unit_dict['turret']['pos']:
                self.turrets[unit_id]['degree_val'] = unit_dict['turret']['degree_val']
                self.turrets[unit_id]['pos'] = unit_dict['turret']['pos']
                self.turrets[unit_id]['unit_rect'] = unit_dict['turret']['rect']
                self.turrets[unit_id]['weapon_bounding_points'] = unit_dict['turret']['weapon_bounding_points']
                self.turrets[unit_id]['rot_axis'] = unit_dict['turret']['rot_axis']
                self.turrets[unit_id]['unit_sprite'] = unit_dict['turret']['unit_sprite']
                self.turrets[unit_id]['sectors'] = self.update_sectors_for_unit(unit_id, unit_allegiance, unit_dict['turret']['rect'], 'turret')
        
        elif unit_type == 'obstacle':
            if self.units[unit_id]['degree_val'] != unit_dict['degree_val'] or self.units[unit_id]['rot_axis'] != unit_dict['rot_axis']:
                self.units[unit_id]['degree_val'] = unit_dict['degree_val']
                self.units[unit_id]['pos'] = unit_dict['pos']
                self.units[unit_id]['unit_rect'] = unit_dict['rect']
                self.units[unit_id]['bounding_points'] = unit_dict['bounding_points']
                self.units[unit_id]['rot_axis'] = unit_dict['rot_axis']
                self.units[unit_id]['unit_sprite'] = unit_dict['unit_sprite']
                self.units[unit_id]['sectors'] = self.update_sectors_for_unit(unit_id, unit_allegiance, unit_dict['rect'])



    def get_unit_stats(self, unit_id):
        """
        Provides a dict bearing the unit-information from the MasterSector.
        """
        unit_stats = dict(self.units[unit_id])
        return unit_stats


    def get_turret_stats(self, unit_id):
        """
        Provides a dict bearing the turret-information from the MasterSector.
        """
        turret_stats = dict(self.turrets[unit_id])
        return turret_stats
        


    def sector_point_collision_omni(self, unit_rect):

        first_sector = ((unit_rect.x // self.sectors_info['sector_width']) * self.sectors_info['sector_width'], (unit_rect.y // self.sectors_info['sector_height']) * self.sectors_info['sector_height'])

        if first_sector[0] < 0:
            first_sector = (0, first_sector[1])
        if first_sector[1] < 0:
            first_sector = (first_sector[0], 0)
        
        sectors_x = int((unit_rect.topright[0] - first_sector[0]) / self.sectors_info['sector_width'])
        sectors_y = int((unit_rect.bottomleft[1] - first_sector[1]) / self.sectors_info['sector_height'])


        sectors_occupied = []


        for x in range(sectors_y + 1):
            for i in range(sectors_x + 1):
                sector_point = (first_sector[0] + (i * self.sectors_info['sector_width']), first_sector[1] + (x * self.sectors_info['sector_height']))
                if sector_point in self.sectors_point_dict:
                    sectors_occupied.append(self.sectors_point_dict[sector_point])

        return sectors_occupied

    
    def add_unit_object(self, unit_object):
        '''
        Adds a unit object into the MasterSector.unit_objects attribute to allow for proper generation and control.
        '''
        self.unit_objects[unit_object.unit_id] = unit_object

    
    def add_munition_object(self, munition_object):
        '''
        Adds a munition object spawned by a unit into the MasterSector.munition_objects attribute to allow for proper generation and control.
        '''
        self.munition_objects[munition_object.munition_id] = munition_object


    def add_impact_object(self, impact_object):
        '''
        Adds an impact object spawned by a munition into the MasterSector.impact_objects attribute to allow for proper generation and control.
        '''
        self.impact_objects[impact_object.impact_id] = impact_object

    
    def generate_units(self):
        '''
        Generates the various unit objects housed within the MasterSector unit_objects attribute.
        '''
        unit_keys = list(self.units.keys())
        for x in range(len(unit_keys)):
            if self.unit_objects[unit_keys[x]].unit_type == 'tank':
                self.unit_objects[unit_keys[x]].generate_tank()
            elif self.unit_objects[unit_keys[x]].unit_type == 'obstacle':
                self.unit_objects[unit_keys[x]].generate_obs()


    def generate_munitions(self):
        '''
        Generates the various munition objects housed within the MasterSector munition_objects attribute.
        '''
        generated_munitions_list = list(self.munition_objects.keys())
        for x in range(len(generated_munitions_list)):
            munition_x = self.munition_objects[generated_munitions_list[x]]
            munition_x.generate_munition()
        generated_munitions_list = None

    
    def generate_impacts(self):
        '''
        Generates the various impact objects housed within the MasterSector impact_objects attribute.
        '''
        generated_impacts_list = list(self.impact_objects.keys())
        for x in range(len(generated_impacts_list)):
            impact_x = self.impact_objects[generated_impacts_list[x]]
            impact_x.generate_impact()
        generated_impacts_list = None

    
    def generate_artificials(self):
        '''
        Generates the various artificial objects housed within the MasterSector artificial_objects attribute.
        '''
        generated_artificials_list = list(self.artificial_objects.keys())
        for x in range(len(artificial_objects_list)):
            artificial_x = self.artificial_objects[generated_artificials_list[x]]
            artificial_x.operations_management()
        generated_artificials_list = None

    
    def enact_munition_damage(self, colliding_unit, damage_dict, collision_pos):
        '''
        Receives the colliding unit_id, a damage_dict containing relevant damage data and an origin position for the impact.
        Provides the damage_dict to the colliding_unit to allow it to calculate the damage done and then checks for area-of-effect
        damage, if any, and provides the damage_dict to those affected units as well, ensuring not to cause the colliding_unit to
        render damage twice.
        '''
        self.administer_unit_damage(colliding_unit, damage_dict['direct'])
        if damage_dict['area'] != None:
            damage_dict['area']['sprite'].rect.center = collision_pos
            damage_sectors = self.sector_point_collision_omni(damage_dict['area']['sprite'].rect)
            area_list_omni = list(set([self.sectors[damage_sectors[x]].unit_list_omni[i] for x in range(len(damage_sectors)) for i in range(len(self.sectors[damage_sectors[x]].unit_list_omni)) if self.sectors[damage_sectors[x]].unit_list_omni[i] != colliding_unit]))
            for x in range(len(area_list_omni)):
                rect_collide = damage_dict['area']['sprite'].rect.colliderect(self.units[area_list_omni[x]]['unit_rect'])
                if rect_collide == True:
                    sprite_collide = pygame.sprite.collide_mask(damage_dict['area']['sprite'], self.units[area_list_omni[x]]['unit_sprite'])
                    if sprite_collide != None:
                        self.administer_unit_damage(area_list_omni[x], damage_dict['area'])

    
    def administer_unit_damage(self, unit_id, damage_dict):
        '''
        Receives a damage dictionary from a munition object and applies the values in order to adjust the unit instance's health
        appropriately.
        '''
        if self.unit_objects[unit_id].health['mortal'] == False:
            return None

        current_health = self.unit_objects[unit_id].health['health']
        unit_pen_mod = self.unit_objects[unit_id].health['pen_mod']
        unit_he_mod = self.unit_objects[unit_id].health['he_mod']

        pen_dmg = (damage_dict['pen_dmg'] * (1 + (damage_dict['pen_mod'] / 1000)) * (1 - (unit_pen_mod / 1000))) - (unit_pen_mod / 10)
        if pen_dmg < 0:
            pen_dmg = 0
        he_dmg = (damage_dict['he_dmg'] * (1 + (damage_dict['he_mod'] / 1000)) * (1 - (unit_he_mod / 1000))) - (unit_he_mod / 10)
        if he_dmg < 0:
            he_dmg = 0
        total_dmg = pen_dmg + he_dmg

        current_health -= total_dmg
        if current_health < 0:
            current_health = 0
        self.unit_objects[unit_id].health['health'] = int(current_health)
        self.check_unit_health(unit_id)

    
    def check_unit_health(self, unit_id):
        health = self.unit_objects[unit_id].health['health']
        if health <= 0:
            self.cull_unit(unit_id)
            if unit_id in self.artificial_objects:
                self.cull_artificial(unit_id)
                    



    def get_unit_bounding_connections(self, unit_rect, unit_bounding_points):
        unit_bounding_stats = {}
        
        for x in range(len(unit_bounding_points)):
            bounding_x = unit_bounding_points[x]

            center_degrees = angle_between_points(unit_rect.center, bounding_x)

            point_degrees = [(unit_bounding_points[i], angle_between_points(unit_bounding_points[i], bounding_x)) for i in range(len(unit_bounding_points)) if unit_bounding_points[i] != bounding_x]
            clockwise = []
            counterclock = []
            for i in range(len(point_degrees)):
                point_direction_i = (point_degrees[i][0], get_closest_degree_direction(center_degrees, point_degrees[i][1]))
                if point_direction_i[1][0] == 'clockwise':
                    clockwise.append(point_direction_i)
                else:
                    counterclock.append(point_direction_i)

            max_clock = max([clockwise[i][1][1] for i in range(len(clockwise))])
            max_counter = max([counterclock[i][1][1] for i in range(len(counterclock))])
            clockwise_pos = [clockwise[i][0] for i in range(len(clockwise)) if clockwise[i][1][1] == max_clock][0]
            counterclock_pos = [counterclock[i][0] for i in range(len(counterclock)) if counterclock[i][1][1] == max_counter][0]

            clockwise_index = [i for i in range(len(unit_bounding_points)) if unit_bounding_points[i] == clockwise_pos][0]
            counterclock_index = [i for i in range(len(unit_bounding_points)) if unit_bounding_points[i] == counterclock_pos][0]

            unit_bounding_stats[x] = {'clockwise_index': clockwise_index, 'counterclock_index': counterclock_index}

        return unit_bounding_stats


    def get_closest_bounding_points_two_units(self, unit_id_a, unit_id_b):
        closest_to_a_center = [(x, self.units[unit_id_b]['bounding_points'][x], distance_between_positions(self.units[unit_id_a]['unit_rect'].center, self.units[unit_id_b]['bounding_points'][x])) for x in range(len(self.units[unit_id_b]['bounding_points']))]
        closest_to_b_center = [(x, self.units[unit_id_a]['bounding_points'][x], distance_between_positions(self.units[unit_id_b]['unit_rect'].center, self.units[unit_id_a]['bounding_points'][x])) for x in range(len(self.units[unit_id_a]['bounding_points']))]

        min_a_center = closest_to_a_center[0]
        min_b_center = closest_to_b_center[0]
        for x in range(len(closest_to_a_center)):
            if closest_to_a_center[x][2] < min_a_center[2]:
                min_a_center = closest_to_a_center[x]
        for x in range(len(closest_to_b_center)):
            if closest_to_b_center[x][2] < min_b_center[2]:
                min_b_center = closest_to_b_center[x]


        return min_b_center[0], min_a_center[0]


    def get_bounding_stats(self, unit_id, point_index):
        chosen_point = self.units[unit_id]['bounding_points'][point_index]
        clockwise_point = self.units[unit_id]['bounding_points'][self.units[unit_id]['bounding_connections'][point_index]['clockwise_index']]
        counterclock_point = self.units[unit_id]['bounding_points'][self.units[unit_id]['bounding_connections'][point_index]['counterclock_index']]

        clockwise_degrees = angle_between_points(clockwise_point, chosen_point)
        counterclock_degrees = angle_between_points(counterclock_point, chosen_point)

        return [clockwise_degrees, counterclock_degrees, chosen_point]


    def bounding_stats_for_bounding_box(self, bounding_box, point_index):
        '''
        Provides the clockwise and counterclock degree-field for a given bounding-point from a provided index
        for a free bounding-box, consisting of a list containing the clockwise-degrees, counterclock-degrees and origin-point.
        Requires the bounding-points and bounding-connections to be provided as a tuple.
        '''
        chosen_point = bounding_box[0][point_index]
        clockwise_point = bounding_box[0][bounding_box[1][point_index]['clockwise_index']]
        counterclock_point = bounding_box[0][bounding_box[1][point_index]['counterclock_index']]

        clockwise_degrees = angle_between_points(clockwise_point, chosen_point)
        counterclock_degrees = angle_between_points(counterclock_point, chosen_point)

        return [clockwise_degrees, counterclock_degrees, chosen_point]
                

    def check_unit_to_unit_collision(self, unit_id_a, unit_id_b):
        '''
        Tests two units for collisions with one another, first
        comparing rect collisions, then comparing degree-field
        collisions should the rects collide.
        '''
        rect_collision = self.units[unit_id_a]['unit_rect'].colliderect(self.units[unit_id_b]['unit_rect'])
        if rect_collision == True:
            closest_index_a, closest_index_b = self.get_closest_bounding_points_two_units(unit_id_a, unit_id_b)
            degree_field_a = self.get_bounding_stats(unit_id_a, closest_index_a)
            degree_field_b = self.get_bounding_stats(unit_id_b, closest_index_b)

            collision_a = is_degree_in_degree_range(degree_field_a[0], degree_field_a[1], angle_between_points(degree_field_b[2], degree_field_a[2]))
            collision_b = is_degree_in_degree_range(degree_field_b[0], degree_field_b[1], angle_between_points(degree_field_a[2], degree_field_b[2]))

            if collision_a == True or collision_b == True:
                return True
        return False


    def closest_points_between_bounding_boxes(self, box_a, box_b, center_a=False, center_b=False):#, center_a, center_b):
        '''
        Provides the closest bounding-point's index to an opposite bounding-box from each
        bounding-box. Requires two bounding-boxes and their rects in the form of a tuple.
        '''
        if center_a == False:
            center_a = box_a[1].center
        if center_b == False:
            center_b = box_b[1].center
            
        closest_to_a_center = [(x, box_b[0][x], distance_between_positions(center_a, box_b[0][x])) for x in range(len(box_b[0]))]
        closest_to_b_center = [(x, box_a[0][x], distance_between_positions(center_b, box_a[0][x])) for x in range(len(box_a[0]))]

        min_a_center = closest_to_a_center[0]
        min_b_center = closest_to_b_center[0]
        for x in range(len(closest_to_a_center)):
            if closest_to_a_center[x][2] < min_a_center[2]:
                min_a_center = closest_to_a_center[x]
        for x in range(len(closest_to_b_center)):
            if closest_to_b_center[x][2] < min_b_center[2]:
                min_b_center = closest_to_b_center[x]
        return min_b_center[0], min_a_center[0]


    def furthest_bounding_point_degree_field(self, degree_field, box):
        '''
        Provides the furthest-bounding-point to a given degree-field (consisting of clockwise-degrees,
        counterclock-degrees and an origin-point) from a bounding-box.
        '''

        points_in_degrees = [(box[x], x) for x in range(len(box)) if is_degree_in_degree_range(degree_field[0], degree_field[1], angle_between_points(box[x], degree_field[2])) == True]
        if len(points_in_degrees) > 0:
            dist_to_points = [(points_in_degrees[x][0], distance_between_positions(degree_field[2], points_in_degrees[x][0]), points_in_degrees[x][1]) for x in range(len(points_in_degrees))]
            lowest_dist = dist_to_points[0][1]
            point = dist_to_points[0][0]
            point_index = dist_to_points[0][2]
            for x in range(len(dist_to_points)):
                if dist_to_points[x][1] < lowest_dist:
                    lowest_dist = dist_to_points[x][1]
                    point = dist_to_points[x][0]
                    point_index = dist_to_points[x][2]
            return (point, point_index)
        return False
            

    def check_bounding_box_collision(self, box_a, box_b, center_a=False, center_b=False):
        '''
        Tests two bounding-boxes for collisions, requires two tuples containing
        the information of the bounding-boxes to be passed, consisting of the bounding-points and
        the bounding-connections.
        '''
        
        rect_a = self.create_rect_from_points(box_a[0])
        rect_b = self.create_rect_from_points(box_b[0])
        rect_collision = rect_a.colliderect(rect_b)
        if rect_collision == True: #MUST FIX furthest_bounding_point_degree_field, as it is improperly detecting collisions due to utilizing the degree_field of the furthest-bounding point, leading to false-positives.
            closest_point_a, closest_point_b = self.closest_points_between_bounding_boxes((box_a[0], rect_a), (box_b[0], rect_b))#, center_a, center_b)
            degree_field_a = self.bounding_stats_for_bounding_box(box_a, closest_point_a)
            degree_field_b = self.bounding_stats_for_bounding_box(box_b, closest_point_b)
            pygame.draw.circle(DISPSURF, (255, 0, 255), box_b[0][closest_point_b], 10, 1)
            pygame.draw.circle(DISPSURF, (255, 0, 0), rect_a.center, 5, 1)

            collision_a = is_degree_in_degree_range(degree_field_a[0], degree_field_a[1], angle_between_points(degree_field_b[2], degree_field_a[2]))
            collision_b = is_degree_in_degree_range(degree_field_b[0], degree_field_b[1], angle_between_points(degree_field_a[2], degree_field_b[2]))

            if collision_a != False:
                collision_a = self.furthest_bounding_point_degree_field(degree_field_a, box_b[0])
            if collision_b != False:
                collision_b = self.furthest_bounding_point_degree_field(degree_field_b, box_a[0])

            if collision_a != False and collision_b != False:
                return (degree_field_a[2], collision_a[0]), (degree_field_b[2], collision_b[0])
            elif collision_a != False:
                return (degree_field_a[2], collision_a[0]), False
            if collision_b != False:
                return False, (degree_field_b[2], collision_b[0])
            
        return False, False
            


    def create_rect_from_points(self, point_list):
        '''
        Receives n number of points in (x, y) format and converts them into a pygame-rect.
        '''
        x_points = [point_list[x][0] for x in range(len(point_list))]
        y_points = [point_list[x][1] for x in range(len(point_list))]
        created_rect = pygame.Rect(min(x_points), min(y_points), max(x_points) - min(x_points), max(y_points) - min(y_points))
        return created_rect
        


    def check_unit_sectors_omni(self, unit_id):
        same_sector_ids = []
        for x in range(len(self.units[unit_id]['sectors'])):
            sector_x = self.units[unit_id]['sectors'][x]
            if len(self.sectors[sector_x].unit_list_omni) > 1:
                for i in range(len(self.sectors[sector_x].unit_list_omni)):
                    if self.sectors[sector_x].unit_list_omni[i] != unit_id:
                        same_sector_ids.append(self.sectors[sector_x].unit_list_omni[i])
        return same_sector_ids

    def check_turret_sectors_omni(self, unit_id):
        same_sector_ids = []
        for x in range(len(self.turrets[unit_id]['sectors'])):
            sector_x = self.turrets[unit_id]['sectors'][x]
            if len(self.sectors[sector_x].unit_list_omni) > 1:
                for i in range(len(self.sectors[sector_x].unit_list_omni)):
                    if self.sectors[sector_x].unit_list_omni[i] != unit_id:
                        same_sector_ids.append(self.sectors[sector_x].unit_list_omni[i])
        return same_sector_ids
    


    def check_unit_collisions_omni(self, unit_id):
        same_sector_ids = self.check_unit_sectors_omni(unit_id)
        for x in range(len(same_sector_ids)):
            collision_check = self.check_unit_to_unit_collision(unit_id, same_sector_ids[x])
            if collision_check == True:
                return True
        return False


    def bounding_collision_a(self, unit_dict, obs_dict, bounding_collision_a):
        """
        Performs collision correction between two objects - a "unit" and an "obstacle" - based on the
        resolutions necessary for what has been dubbed a "class-A collision", whereby a bounding-point on
        an obstacle is intersecting one of the bounding-lines (that is, a line drawn from one bounding-point
        to one of its connection-points) on the unit. Should this result in what has been deemed a "class-A head-on
        collision", whereby one of the bounding-points of the obstacle is intersecting a line drawn between the two fore-most
        or two rear-most points on the unit, it will be resolved utilizing the class-B collision correction system, as such
        a methodology has been deemed the only appropriate measure to correct such a collision. This is signified by the
        returned collision_reassignment tuple, which consists of a boolean, a connection-point, a specified degree-val (either
        standard or polar) and the reversal of the bounding_collision_a points to appropriately fit the specifications of a
        class-B collision, respectively.
        Requires a unit_dict, an obs_dict and the information of a class-A bounding-collision, all of which can be obtained from the
        "self.get_unit_dict" and "self.check_bounding_box_collision" methods of the MasterSector class.
        Returns a degree-adjustment value as a float, as well as the collision_reassignment tuple specified above.
        """
        collision_reassignment = (False, None, None, None)
        degree_adjustment = 0.0
        polar_degree_val = polarize_degree(unit_dict['degree_val'])

        for x in range(len(unit_dict['bounding_points'])):
            if unit_dict['bounding_points'][x] == bounding_collision_a[0]:
                bounding_index = x
                break
        for x in range(len(obs_dict['bounding_points'])):
            if obs_dict['bounding_points'][x] == bounding_collision_a[1]:
                obs_index = x
                break

        counter_conn_degrees = get_degree_diff(angle_between_points(unit_dict['bounding_points'][unit_dict['bounding_connections'][bounding_index]['counterclock_index']], bounding_collision_a[0]), angle_between_points(bounding_collision_a[1], bounding_collision_a[0]))
        clock_conn_degrees = get_degree_diff(angle_between_points(unit_dict['bounding_points'][unit_dict['bounding_connections'][bounding_index]['clockwise_index']], bounding_collision_a[0]), angle_between_points(bounding_collision_a[1], bounding_collision_a[0]))
        counter_conn_dist = distance_between_positions(unit_dict['bounding_points'][unit_dict['bounding_connections'][bounding_index]['counterclock_index']], bounding_collision_a[1])
        clock_conn_dist = distance_between_positions(unit_dict['bounding_points'][unit_dict['bounding_connections'][bounding_index]['clockwise_index']], bounding_collision_a[1])
        bound_coll_dist = distance_between_positions(bounding_collision_a[0], bounding_collision_a[1])

        counter_dist_viable = True
        clock_dist_viable = True
        if counter_conn_dist < 10 and bound_coll_dist < 10:
            counter_dist_viable = False
        if clock_conn_dist < 10 and bound_coll_dist < 10:
            clock_dist_viable = False

        if abs(counter_conn_degrees) < abs(clock_conn_degrees) and counter_dist_viable == True or clock_dist_viable == False:
            chosen_index = 'counterclock_index'
        else:
            chosen_index = 'clockwise_index'

        unit_center_to_bounding = angle_between_points(bounding_collision_a[0], unit_dict['unit_rect'].center)
        chosen_conn = unit_dict['bounding_points'][unit_dict['bounding_connections'][bounding_index][chosen_index]]
        
        unit_center_to_conn = angle_between_points(chosen_conn, unit_dict['unit_rect'].center)
        deg_val_bounding_diff = get_degree_diff(unit_dict['degree_val'], unit_center_to_bounding)
        polar_val_bounding_diff = get_degree_diff(polar_degree_val, unit_center_to_bounding)
        if abs(deg_val_bounding_diff) < abs(polar_val_bounding_diff):
            chosen_degree_line = unit_dict['degree_val']
        else:
            chosen_degree_line = polar_degree_val
        unit_center_to_coll = angle_between_points(bounding_collision_a[1], unit_dict['unit_rect'].center)
        unit_coll_bounding_dir = get_closest_degree_direction(unit_center_to_coll, unit_center_to_bounding)[0]
        unit_conn_deg_dir = [['clockwise', 'counterclock'][x] for x in range(len(['clockwise', 'counterclock'])) if ['clockwise', 'counterclock'][x] != unit_coll_bounding_dir][0]
        unit_bounding_deg_stats = (unit_coll_bounding_dir, unit_center_to_bounding)
        unit_conn_deg_stats = (unit_conn_deg_dir, unit_center_to_conn)
        unit_bounding_conn_deg_stats = [unit_bounding_deg_stats, unit_conn_deg_stats]
        unit_deg_stats_omni = {unit_bounding_conn_deg_stats[x][0]: unit_bounding_conn_deg_stats[x][1] for x in range(len(unit_bounding_conn_deg_stats))}

        if unit_deg_stats_omni['clockwise'] == unit_center_to_bounding:
            bounding_deg_range_dir = 'clockwise'
        else:
            bounding_deg_range_dir = 'counterclock'
        degrees_in_range = is_degree_in_degree_range(unit_deg_stats_omni['clockwise'], unit_deg_stats_omni['counterclock'], chosen_degree_line)

        if degrees_in_range == True:
            unit_center_obs_center = angle_between_points(obs_dict['unit_rect'].center, unit_dict['unit_rect'].center)
            obs_center_in_range = is_degree_in_degree_range(unit_deg_stats_omni['clockwise'], unit_deg_stats_omni['counterclock'], unit_center_obs_center)

            coll_bound_prox = get_degree_diff(unit_center_to_bounding, unit_center_to_coll)
            coll_conn_prox = get_degree_diff(unit_center_to_conn, unit_center_to_coll)

            if abs(coll_bound_prox) < 5 or abs(coll_conn_prox) < 5:
                proximity_alert = True
            else:
                proximity_alert = False
            if obs_center_in_range == False or proximity_alert == True:
                degrees_in_range = False


        if degrees_in_range == False:
            unit_deg_conn_diff = get_degree_diff(unit_dict['degree_val'], unit_center_to_conn)
            selected_point_change = False
            bounding_coll_dist = distance_between_positions(bounding_collision_a[0], bounding_collision_a[1])
            conn_coll_dist = distance_between_positions(chosen_conn, bounding_collision_a[1])

            if bounding_coll_dist < conn_coll_dist:
                conn_adjust = get_degree_diff(angle_between_points(bounding_collision_a[0], chosen_conn), angle_between_points(bounding_collision_a[1], chosen_conn))
                degree_adjustment = abs(conn_adjust)
            else:
                conn_adjust = get_degree_diff(angle_between_points(chosen_conn, bounding_collision_a[0]), angle_between_points(bounding_collision_a[1], bounding_collision_a[0]))
                degree_adjustment = abs(conn_adjust)
            bounding_dir = get_closest_degree_direction(angle_between_points(chosen_conn, bounding_collision_a[0]), angle_between_points(bounding_collision_a[1], bounding_collision_a[0]))[0]

            pygame.draw.circle(DISPSURF, (0, 255, 0), chosen_conn, 10, 1)
            pygame.draw.circle(DISPSURF, (0, 255, 255), bounding_collision_a[0], 10, 1)
            pygame.draw.circle(DISPSURF, (0, 255, 255), bounding_collision_a[1], 10, 1)
            
            if bounding_coll_dist < conn_coll_dist or unit_dict['unit_spec'] == 'turret':
                if bounding_dir == 'clockwise':
                    bounding_dir = 'counterclock'
                else:
                    bounding_dir = 'clockwise'
            if bounding_dir == 'counterclock':
                degree_adjustment = degree_adjustment * -1

            temp_deg_point = pos_from_degrees(unit_dict['rot_axis'], unit_dict['degree_val'] + degree_adjustment, 150)
            pygame.draw.aaline(DISPSURF, (255, 0, 0), unit_dict['rot_axis'], temp_deg_point, True)

        else:
            degree_adjustment = 0.0
            bounding_collision_b = (bounding_collision_a[1], bounding_collision_a[0])
            collision_reassignment = (True, chosen_conn, chosen_degree_line, bounding_collision_b)

        return degree_adjustment, collision_reassignment


    

            
        

    def bounding_collision_b(self, unit_dict, obs_dict, bounding_collision_b, collision_reassignment=(False, None, None, None)):
        """
        Performs a class-B collision-correction upon two objects, a unit and an obstacle, based on the methodologies
        of what has been dubbed a "class-B collision", whereby determinations are made regarding the appropriate points to utilize
        for calculations that have been thoroughly tested to ensure validity and the avoidance of fatal-errors or inappropriate
        corrections, and finally a correction-degree is determined utilizing trigonometry to ensure the proper adjustment of an
        infracting bounding-point. A class-B collision, unsurprisingly the opposite of a class-A collision, is when a bounding-point
        on the unit is intersecting a bounding-line (the line between an obstacle bounding-point and one of its connection-points.)
        This method requires a unit_dict, an obs_dict, a bounding_collision_b tuple as well as a collision_reassignment tuple, which
        consists of a boolean, a connection-point (from the bounding-point selected of the unit), a degree-val (either standard or polar),
        and a bounding_collision_b tuple, consisting of the reversed bounding_collision_a points to accurately fit the specifications of
        a class-B collision.
        A warning that this method should never be utilized without first performing a class-A collision check, in order to ensure
        that a class-A head-on collision has not occured. The collision-reassignment argument has a default, but to use it for any
        purposes aside from testing will yield improper corrections in niche-cases as a best-case scenario, and fatal-errors at worst.
        Returns a degree-adjustment.
        """
        degree_adjustment = 0.0
        polar_degree_val = polarize_degree(unit_dict['degree_val'])
        collision_reassignment_b = False

        for x in range(len(unit_dict['bounding_points'])):
            if unit_dict['bounding_points'][x] == bounding_collision_b[1]:
                bounding_index = x
                break
        for x in range(len(obs_dict['bounding_points'])):
            if obs_dict['bounding_points'][x] == bounding_collision_b[0]:
                obs_index = x
                break
        obs_conns = obs_dict['bounding_connections'][obs_index]
        obs_conns = [obs_conns['clockwise_index'], obs_conns['counterclock_index']]
        obs_conns = [obs_dict['bounding_points'][obs_conns[0]], obs_dict['bounding_points'][obs_conns[1]]]
        obs_conn_a_deg = angle_between_points(obs_conns[0], bounding_collision_b[0])
        obs_conn_b_deg = angle_between_points(obs_conns[1], bounding_collision_b[0])
        coll_point_deg = angle_between_points(bounding_collision_b[1], bounding_collision_b[0])
        
        unit_conns = unit_dict['bounding_connections'][bounding_index]
        unit_conns = [unit_conns['clockwise_index'], unit_conns['counterclock_index']]
        unit_conns = [unit_dict['bounding_points'][unit_conns[0]], unit_dict['bounding_points'][unit_conns[1]]]

        unit_center_coll = angle_between_points(bounding_collision_b[1], unit_dict['unit_rect'].center)
        unit_deg_coll_diff = get_degree_diff(unit_center_coll, unit_dict['degree_val'])
        unit_polar_coll_diff = get_degree_diff(unit_center_coll, polar_degree_val)

        if abs(unit_deg_coll_diff) < abs(unit_polar_coll_diff):
            coll_rotation_dir = get_closest_degree_direction(unit_center_coll, unit_dict['degree_val'])[0]
            degree_dir_selected = 'degree'
            selected_deg_val = unit_dict['degree_val']
        else:
            bounding_rotation_dir = get_closest_degree_direction(unit_center_coll, polar_degree_val)[0]
            degree_dir_selected = 'polar'
            selected_deg_val = polar_degree_val

        unit_center_unit_conn_a = angle_between_points(unit_conns[0], unit_dict['unit_rect'].center)
        unit_center_unit_conn_b = angle_between_points(unit_conns[1], unit_dict['unit_rect'].center)
        unit_center_obs_bound = angle_between_points(bounding_collision_b[0], unit_dict['unit_rect'].center)

        sel_deg_unit_conn_a_diff = get_degree_diff(selected_deg_val, unit_center_unit_conn_a)
        sel_deg_unit_conn_b_diff = get_degree_diff(selected_deg_val, unit_center_unit_conn_b)
        if abs(sel_deg_unit_conn_a_diff) < abs(sel_deg_unit_conn_b_diff):
            unit_select_conn = unit_conns[0]
        else:
            unit_select_conn = unit_conns[1]
        sel_conn_in_obs_bound_deg_field = is_degree_in_degree_range(obs_conn_a_deg, obs_conn_b_deg, angle_between_points(unit_select_conn, bounding_collision_b[0]))
        if sel_conn_in_obs_bound_deg_field == True and unit_dict['unit_spec'] != 'turret': #C-zc: TEMPORARY ATTEMPT AT CORRECTION VIA UNIT_SPEC
            pygame.draw.circle(DISPSURF, (0, 0, 0), unit_dict['rot_axis'], 200, 1)
            collision_reassignment = (True, unit_select_conn, selected_deg_val, bounding_collision_b)
        if sel_conn_in_obs_bound_deg_field:
            collision_reassignment_b = True

        obs_bound_unit_center = angle_between_points(unit_dict['unit_rect'].center, bounding_collision_b[0])
        obs_conn_a_deg_diff = get_degree_diff(obs_bound_unit_center, obs_conn_a_deg)
        obs_conn_b_deg_diff = get_degree_diff(obs_bound_unit_center, obs_conn_b_deg)
        obs_conn_diffs = [abs(obs_conn_a_deg_diff), abs(obs_conn_b_deg_diff)]
        lowest_deg_diff = min(obs_conn_diffs)
        if min(obs_conn_diffs) == abs(obs_conn_a_deg_diff):
            select_conn_point = obs_conns[0]
        else:
            select_conn_point = obs_conns[1]
        true_lowest_deg_diff = lowest_deg_diff
        true_select_conn = select_conn_point

        obs_bound_dist_conn_a = distance_between_positions(bounding_collision_b[0], obs_conns[0])
        obs_bound_dist_conn_b = distance_between_positions(bounding_collision_b[0], obs_conns[1])

        obs_bound_coll_unit_dir = get_closest_degree_direction(coll_point_deg, obs_bound_unit_center)[0]
        obs_bound_coll_conn_a_dir = get_closest_degree_direction(coll_point_deg, obs_conn_a_deg)[0]
        obs_bound_coll_conn_b_dir = get_closest_degree_direction(coll_point_deg, obs_conn_b_deg)[0]

        obs_bound_obs_center = angle_between_points(obs_dict['unit_rect'].center, bounding_collision_b[0])

        if unit_dict['unit_spec'] != 'turret':
            if obs_bound_coll_conn_a_dir == obs_bound_coll_conn_b_dir:
                obs_bound_center_conn_a_dir = get_closest_degree_direction(obs_bound_obs_center, obs_conn_a_deg)[0]
                obs_bound_center_conn_b_dir = get_closest_degree_direction(obs_bound_obs_center, obs_conn_b_deg)[0]
                obs_bound_center_coll_dir = get_closest_degree_direction(obs_bound_obs_center, coll_point_deg)[0]

                if obs_bound_center_conn_a_dir == obs_bound_center_coll_dir:
                    select_conn_point = obs_conns[0]
                elif obs_bound_center_conn_b_dir == obs_bound_center_coll_dir:
                    select_conn_point = obs_conns[1]
            elif obs_bound_coll_unit_dir == obs_bound_coll_conn_a_dir:
                select_conn_point = obs_conns[0]
            elif obs_bound_coll_unit_dir == obs_bound_coll_conn_b_dir:
                select_conn_point = obs_conns[1]
        else:
            unit_center_obs_bound_deg = angle_between_points(bounding_collision_b[0], unit_dict['unit_rect'].center)
            unit_center_coll_deg = angle_between_points(bounding_collision_b[1], unit_dict['unit_rect'].center)
            #unit_center_obs_bound_coll_prox = get_degree_diff(unit_center_coll_deg, unit_center_obs_bound_deg)
            obs_center_obs_bound_coll_prox = get_degree_diff(angle_between_points(bounding_collision_b[0], obs_dict['unit_rect'].center), angle_between_points(bounding_collision_b[1], obs_dict['unit_rect'].center))
            obs_bound_center_conn_a_dir = get_closest_degree_direction(obs_bound_obs_center, obs_conn_a_deg)[0]
            obs_bound_center_conn_b_dir = get_closest_degree_direction(obs_bound_obs_center, obs_conn_b_deg)[0]

            #if abs(unit_center_obs_bound_coll_prox) < 10:
            select_unit_point = bounding_collision_b[1]
            if abs(obs_center_obs_bound_coll_prox) < 15:
                pygame.draw.circle(DISPSURF, (0, 255, 255), obs_dict['unit_rect'].center, 12, 0)
                obs_bound_unit_bound_omni_dist = []
                obs_bound_unit_bound_omni_keys = {}
                for x in range(len(unit_dict['bounding_points'])):
                    bound_x_dist = distance_between_positions(unit_dict['bounding_points'][x], bounding_collision_b[0])
                    obs_bound_unit_bound_omni_dist.append(bound_x_dist)
                    obs_bound_unit_bound_omni_keys[bound_x_dist] = unit_dict['bounding_points'][x]
                if obs_bound_unit_bound_omni_keys[min(obs_bound_unit_bound_omni_dist)] != bounding_collision_b[1]:
                    select_unit_point = obs_bound_unit_bound_omni_keys[min(obs_bound_unit_bound_omni_dist)]
                    #select_unit_point = bounding_collision_b[1] ###
                else:
                    select_unit_point = bounding_collision_b[1]
                unit_rot_coll_dist = distance_between_positions(unit_dict['rot_axis'], bounding_collision_b[1])
                unit_center_coll_dist = distance_between_positions(unit_dict['unit_rect'].center, select_unit_point)
                unit_deg_val_coll_deg_diff = abs(get_degree_diff(unit_dict['degree_val'], angle_between_points(select_unit_point, unit_dict['unit_rect'].center)))
                unit_deg_coll_dir = get_closest_degree_direction(unit_dict['degree_val'], angle_between_points(select_unit_point, unit_dict['unit_rect'].center))[0]
                if unit_deg_coll_dir == 'clockwise':
                    unit_deg_val_coll_deg_diff = unit_deg_val_coll_deg_diff * -1
                temp_coll_point_reassign = pos_from_degrees(unit_dict['unit_rect'].center, unit_dict['degree_val'] + unit_deg_val_coll_deg_diff, unit_center_coll_dist)
                temp_coll_point_reassign = (int(temp_coll_point_reassign[0]), int(temp_coll_point_reassign[1]))
                pygame.draw.circle(DISPSURF, (0, 0, 0), temp_coll_point_reassign, 7, 2)
                obs_bound_temp_coll_deg = angle_between_points(temp_coll_point_reassign, bounding_collision_b[0])
                obs_bound_temp_coll_dir = get_closest_degree_direction(obs_bound_obs_center, obs_bound_temp_coll_deg)[0]
                if obs_bound_center_conn_a_dir == obs_bound_temp_coll_dir:
                    select_conn_point = obs_conns[0]
                elif obs_bound_center_conn_b_dir == obs_bound_temp_coll_dir:
                    select_conn_point = obs_conns[1]
            else:
                obs_bound_center_coll_dir = get_closest_degree_direction(obs_bound_obs_center, coll_point_deg)[0]
                if obs_bound_center_conn_a_dir == obs_bound_center_coll_dir:
                    select_conn_point = obs_conns[0]
                elif obs_bound_center_conn_b_dir == obs_bound_center_coll_dir:
                    select_conn_point = obs_conns[1]

        pygame.draw.circle(DISPSURF, (255, 0, 0), bounding_collision_b[1], 10, 1)
        pygame.draw.circle(DISPSURF, (255, 0, 255), bounding_collision_b[0], 10, 1)

        if select_conn_point == obs_conns[0]:
            obs_conn_deg = obs_conn_a_deg
            obs_conn_point = obs_conns[0]
            obs_conn_dist = obs_bound_dist_conn_a
            obs_conn_unit_center_dist = distance_between_positions(unit_dict['rot_axis'], obs_conn_point)
        else:
            obs_conn_deg = obs_conn_b_deg
            obs_conn_point = obs_conns[1]
            obs_conn_dist = obs_bound_dist_conn_b
            obs_conn_unit_center_dist = distance_between_positions(unit_dict['rot_axis'], obs_conn_point)

        if collision_reassignment[0] == True:
            obs_conn_dir = get_closest_degree_direction(obs_bound_obs_center, obs_conn_deg)[0]
            obs_bound_coll_dir = get_closest_degree_direction(obs_bound_obs_center, coll_point_deg)[0]
            obs_bound_unit_conn_dir = get_closest_degree_direction(obs_bound_obs_center, angle_between_points(collision_reassignment[1], bounding_collision_b[0]))[0]

            obs_bound_conn_a_dir = get_closest_degree_direction(obs_bound_obs_center, obs_conn_a_deg)[0]
            obs_bound_conn_b_dir = get_closest_degree_direction(obs_bound_obs_center, obs_conn_b_deg)[0]
            
            unit_center_obs_conn_a = angle_between_points(obs_conns[0], unit_dict['unit_rect'].center)
            unit_center_obs_conn_b = angle_between_points(obs_conns[1], unit_dict['unit_rect'].center)
            unit_rot_coll_deg = angle_between_points(bounding_collision_b[1], unit_dict['unit_rect'].center)
            unit_deg_rot_coll_diff = get_degree_diff(unit_rot_coll_deg, unit_dict['degree_val'])
            unit_polar_rot_coll_diff = get_degree_diff(unit_rot_coll_deg, polar_degree_val)

            if abs(unit_deg_rot_coll_diff) < abs(unit_polar_rot_coll_diff):
                select_deg_val = unit_dict['degree_val']
            else:
                select_deg_val = polar_degree_val

            unit_bound_select_deg_dir = get_closest_degree_direction(unit_rot_coll_deg, select_deg_val)[0]
            unit_obs_bound_conn_a_diff = get_degree_diff(unit_center_obs_bound, unit_center_obs_conn_a)
            unit_obs_bound_conn_b_diff = get_degree_diff(unit_center_obs_bound, unit_center_obs_conn_b)

            if unit_bound_select_deg_dir == obs_bound_conn_a_dir:
                if abs(unit_obs_bound_conn_a_diff) > 10:
                    select_conn_point_b = obs_conns[0]
                else:
                    select_conn_point_b = obs_conns[1]
            else:
                if abs(unit_obs_bound_conn_b_diff) > 10:
                    select_conn_point_b = obs_conns[1]
                else:
                    select_conn_point_b = obs_conns[0]
            if select_conn_point_b == obs_conns[0]:
                obs_chosen_conn_dir = obs_bound_conn_a_dir
                select_conn_point_b = obs_conns[0]
            else:
                obs_chosen_conn_dir = obs_bound_conn_b_dir
                select_conn_point_b = obs_conns[1]

            unit_center_coll_deg = angle_between_points(bounding_collision_b[1], unit_dict['unit_rect'].center)
            unit_center_conn_deg = angle_between_points(collision_reassignment[1], unit_dict['unit_rect'].center)
            unit_coll_dir = get_closest_degree_direction(select_deg_val, unit_center_coll_deg)[0]
            unit_conn_dir = get_closest_degree_direction(select_deg_val, unit_center_conn_deg)[0]

            if unit_coll_dir == obs_chosen_conn_dir:
                unit_selected_bounding = collision_reassignment[1]
                select_coll_point = collision_reassignment[1]
            elif unit_conn_dir == obs_chosen_conn_dir:
                unit_selected_bounding = bounding_collision_b[1]
                select_coll_point = bounding_collision_b[1]
            else:
                unit_selected_bounding = collision_reassignment[1]
                select_coll_point = collision_reassignment[1]

            if select_coll_point != bounding_collision_b[1]:
                select_colliding_point = collision_reassignment[1]
                bounding_collision_b = (bounding_collision_b[0], collision_reassignment[1])
                coll_point_deg = angle_between_points(bounding_collision_b[1], bounding_collision_b[0])
                for x in range(len(unit_dict['bounding_points'])):
                    if unit_dict['bounding_points'][x] == bounding_collision_b[1]:
                        bounding_index = x
                        break
            select_conn_point = select_conn_point_b

        obs_bound_unit_rot_dist = distance_between_positions(bounding_collision_b[0], unit_dict['rot_axis'])
        unit_rot_coll_deg = angle_between_points(bounding_collision_b[1], unit_dict['rot_axis'])
        unit_rot_coll_dist = distance_between_positions(bounding_collision_b[1], unit_dict['rot_axis'])
        if select_conn_point == obs_conns[0]:
            obs_conn_deg = obs_conn_a_deg
            obs_conn_point = obs_conns[0]
            obs_conn_dist = obs_bound_dist_conn_a
            obs_conn_unit_rot_dist = distance_between_positions(obs_conn_point, unit_dict['rot_axis'])
        else:
            obs_conn_deg = obs_conn_b_deg
            obs_conn_point = obs_conns[1]
            obs_conn_dist = obs_bound_dist_conn_b
            obs_conn_unit_rot_dist = distance_between_positions(obs_conn_point, unit_dict['rot_axis'])

        pygame.draw.circle(DISPSURF, (255, 0, 0), obs_conn_point, 5, 2)
        pygame.draw.circle(DISPSURF, (255, 0, 255), bounding_collision_b[0], 3, 0)
        pygame.draw.circle(DISPSURF, (0, 255, 255), bounding_collision_b[1], 3, 0)

        trig_a_calc = True
        trig_b_calc = True
                

        if trig_a_calc == True:
            try:
                side_a = obs_conn_dist
                first_a = side_a
                side_b = obs_bound_unit_rot_dist
                side_c = obs_conn_unit_rot_dist
                first_c = side_c
                angle_c = math.acos((side_a**2 + side_b**2 - side_c**2) / (2 * side_a * side_b))
                side_c = unit_rot_coll_dist
                angle_b = math.asin((math.sin(angle_c) * side_b) / side_c)

                if trig_a_calc == True:
                    angle_a = math.radians(180.00 - math.degrees(angle_b) - math.degrees(angle_c))
                    side_a = (math.sin(angle_a) * side_b) / math.sin(angle_b)

                    new_bounding_pos_a = pos_from_degrees(bounding_collision_b[0], obs_conn_deg, side_a)
                    new_bounding_pos_a = (int(new_bounding_pos_a[0]), int(new_bounding_pos_a[1]))
                    rotation_value_a = get_degree_diff(unit_rot_coll_deg, angle_between_points(new_bounding_pos_a, unit_dict['rot_axis']))
                    new_degree_val_a = unit_dict['degree_val'] + rotation_value_a
                    new_bounding_a_diff = get_degree_diff(unit_dict['degree_val'], new_degree_val_a)
            except (ZeroDivisionError, ValueError) as author_error:
                rotation_value_a = None
                angle_a = None
                side_a = None
                trig_a_calc = None

        if trig_b_calc == True:
            try:
                side_a_b = obs_conn_dist
                first_a_b = side_a_b
                side_b_b = distance_between_positions(unit_dict['rot_axis'], obs_conn_point)
                first_b_b = side_b_b
                side_c_b = obs_bound_unit_rot_dist
                first_c_b = side_c_b
                angle_c_b = math.acos((side_a_b**2 + side_b_b**2 - side_c_b**2) / (2 * side_a_b * side_b_b))
                side_c_b = unit_rot_coll_dist
                if angle_c_b == 0:
                    zero_error = 1 / 0
                angle_b_b = math.asin((math.sin(angle_c_b) * side_b_b) / side_c_b)

                if trig_b_calc == True:
                    angle_a_b = math.radians(180.00 - math.degrees(angle_b_b) - math.degrees(angle_c_b))
                    side_a_b_b = (math.sin(angle_a_b) * side_b_b) / math.sin(angle_b_b)

                    new_bounding_pos_b = pos_from_degrees(obs_conn_point, polarize_degree(obs_conn_deg), side_a_b_b)
                    new_bounding_pos_b = (int(new_bounding_pos_b[0]), int(new_bounding_pos_b[1]))
                    rotation_value_b = get_degree_diff(unit_rot_coll_deg, angle_between_points(new_bounding_pos_b, unit_dict['rot_axis']))
                    new_degree_val_b = unit_dict['degree_val'] + rotation_value_b
                    new_bounding_b_diff = get_degree_diff(unit_dict['degree_val'], new_degree_val_b)
            except (ZeroDivisionError, ValueError) as author_error:
                rotation_value_b = None
                angle_a_b = None
                side_a_b = None
                trig_b_calc = None

        if rotation_value_a == None or rotation_value_b == None:
            new_bounding_pos_a, new_bounding_pos_b = circle_line_intersect((unit_dict['rot_axis'], distance_between_positions(unit_dict['rot_axis'], bounding_collision_b[1])), bounding_collision_b[0], obs_conn_point)
            if new_bounding_pos_a != None:
                pygame.draw.circle(DISPSURF, (0, 255, 255), unit_dict['rot_axis'], 150, 1)
                rotation_value_a = get_degree_diff(unit_rot_coll_deg, angle_between_points(new_bounding_pos_a, unit_dict['rot_axis']))
                new_degree_val_a = unit_dict['degree_val'] + rotation_value_a
                new_bounding_a_diff = get_degree_diff(unit_dict['degree_val'], new_degree_val_a)
            if new_bounding_pos_b != None:
                pygame.draw.circle(DISPSURF, (255, 0, 0), unit_dict['rot_axis'], 175, 1)
                rotation_value_b = get_degree_diff(unit_rot_coll_deg, angle_between_points(new_bounding_pos_b, unit_dict['rot_axis']))
                new_degree_val_b = unit_dict['degree_val'] + rotation_value_b
                new_bounding_b_diff = get_degree_diff(unit_dict['degree_val'], new_degree_val_b)
        if rotation_value_a == None and rotation_value_b == None:
            rotation_change_val = 0.0
        elif rotation_value_a == None or rotation_value_b == None:
            rotation_change_val = [[rotation_value_a, rotation_value_b][x] for x in range(len([rotation_value_a, rotation_value_b])) if [rotation_value_a, rotation_value_b][x] != None][0]
        else:
            if abs(new_bounding_a_diff) < abs(new_bounding_b_diff) or collision_reassignment[0] == True:
                rotation_change_val = rotation_value_a
            else:
                rotation_change_val = rotation_value_b

        unit_deg_val_point = pos_from_degrees(unit_dict['rot_axis'], unit_dict['degree_val'], 200)
        unit_deg_val_point = (int(unit_deg_val_point[0]), int(unit_deg_val_point[1]))
        pygame.draw.aaline(DISPSURF, (0, 255, 0), unit_dict['rot_axis'], unit_deg_val_point, True)
        if new_bounding_pos_a != None:
            pygame.draw.circle(DISPSURF, (0, 255, 255), new_bounding_pos_a, 5, 0)
            pygame.draw.aaline(DISPSURF, (0, 255, 255), unit_dict['rot_axis'], new_bounding_pos_a, True)
        if new_bounding_pos_b != None:
            pygame.draw.circle(DISPSURF, (255, 0, 255), new_bounding_pos_b, 5, 0)
            pygame.draw.aaline(DISPSURF, (255, 0, 255), unit_dict['rot_axis'], new_bounding_pos_b, True)

        return rotation_change_val, collision_reassignment_b #, trig_omni_dict



    def reorient_unit_collisions_omni(self, unit_id):
        "Adjusts the specified unit in the event of a collision with one or more units."

        same_sector_ids = self.check_unit_sectors_omni(unit_id)
        collision_reassignment_b = False
        new_degree_val = 0.0

        for x in range(len(same_sector_ids)):
            degree_val_x = 0.0
            obs_x = same_sector_ids[x]
            if unit_id in self.units:
                unit_bounding_box = (self.units[unit_id]['bounding_points'], self.units[unit_id]['bounding_connections'])
                obs_bounding_box = (self.units[obs_x]['bounding_points'], self.units[obs_x]['bounding_connections'])
                unit_rect = self.units[unit_id]['unit_rect']
                obs_rect = self.units[obs_x]['unit_rect']
            bounding_collision_a, bounding_collision_b = self.check_bounding_box_collision(unit_bounding_box, obs_bounding_box, unit_rect.center, obs_rect.center)

            if bounding_collision_a != False or bounding_collision_b != False:
                unit_dict = self.get_unit_stats(unit_id)
                obs_dict = self.get_unit_stats(obs_x)

                degree_rotation_change_a = 0.0
                degree_rotation_change_b = 0.0

                if bounding_collision_a != False:
                    degree_rotation_change_a, collision_reassignment = self.bounding_collision_a(unit_dict, obs_dict, bounding_collision_a)
                else:
                    collision_reassignment = (False, None, None, None)
                if bounding_collision_b != False or collision_reassignment[0] == True:
                    if collision_reassignment[0] == True:
                        bounding_collision_b = collision_reassignment[3]
                    degree_rotation_change_b, collision_reassignment_b = self.bounding_collision_b(unit_dict, obs_dict, bounding_collision_b, collision_reassignment)

                if abs(degree_rotation_change_a) > abs(degree_rotation_change_b) and collision_reassignment_b == False:
                    chosen_degree_val = degree_rotation_change_a
                else:
                    chosen_degree_val = degree_rotation_change_b
                    
                if abs(chosen_degree_val) > abs(new_degree_val):
                    new_degree_val = chosen_degree_val
        return new_degree_val


    def reorient_turret_collisions_omni(self, unit_id):

        if self.turrets[unit_id]['allegiance'] != 'PLAYER':
            return 0.0

        same_sector_ids = self.check_turret_sectors_omni(unit_id)
        collision_reassignment_b = False
        new_degree_val = 0.0

        for x in range(len(self.turrets[unit_id]['weapon_bounding_points'])):
            for i in range(len(same_sector_ids)):
                degree_val_i = 0.0
                obs_i = same_sector_ids[i]
                if unit_id in self.turrets:
                    weapon_bounding_box = (self.turrets[unit_id]['weapon_bounding_points'][x]['bounding_points'], self.turrets[unit_id]['weapon_bounding_connections'][x])
                    obs_bounding_box = (self.units[obs_i]['bounding_points'], self.units[obs_i]['bounding_connections'])
                    weapon_rect = self.create_rect_from_points(self.turrets[unit_id]['weapon_bounding_points'][x]['bounding_points'])
                    obs_rect = self.units[obs_i]['unit_rect']
                bounding_collision_a, bounding_collision_b = self.check_bounding_box_collision(weapon_bounding_box, obs_bounding_box, weapon_rect.center, obs_rect.center)

                if bounding_collision_a != False or bounding_collision_b != False:
                    weapon_dict = self.get_turret_stats(unit_id)
                    weapon_dict['unit_rect'] = weapon_rect
                    weapon_dict['bounding_points'] = self.turrets[unit_id]['weapon_bounding_points'][x]['bounding_points']
                    weapon_dict['bounding_connections'] = self.turrets[unit_id]['weapon_bounding_connections'][x]
                    obs_dict = self.get_unit_stats(obs_i)

                    degree_rotation_change_a = 0.0
                    degree_rotation_change_b = 0.0

                    if bounding_collision_a != False:
                        degree_rotation_change_a, collision_reassignment = self.bounding_collision_a(weapon_dict, obs_dict, bounding_collision_a)
                    else:
                        collision_reassignment = (False, None, None, None)
                    if bounding_collision_b != False or collision_reassignment[0] == True:
                        if collision_reassignment[0] == True:
                            bounding_collision_b = collision_reassignment[3]
                        degree_rotation_change_b, collision_reassignment_b = self.bounding_collision_b(weapon_dict, obs_dict, bounding_collision_b, collision_reassignment)

                    if abs(degree_rotation_change_a) > abs(degree_rotation_change_b) and collision_reassignment_b == False:
                        chosen_degree_val = degree_rotation_change_a
                    else:
                        chosen_degree_val = degree_rotation_change_b

                    if abs(chosen_degree_val) > abs(new_degree_val):
                        new_degree_val = chosen_degree_val
                        
        return new_degree_val
                
                                               
                                                    
            
            

        


    
    
        



#-----------------------------------EnemyAI Class


class EnemyAI():
    def __init__(self, unit_id, master_sector):
        self.unit_id = unit_id
        self.master_sector = master_sector
        self.tank = self.master_sector.unit_objects[self.unit_id]
        self.allegiance = self.tank.allegiance
        self.desired_pos = None
        self.confirmed_desired_pos = None
        self.desired_degree_val = None
        self.chassis_direction = {'turn': None, 'move': None}
        self.target_unit = None
        self.path_info = {'graph': None, 'path': None, 'start': None, 'goal': None, 'closest_node_start': None, 'closest_node_goal': None, 'tested_nodes': None}
        self.path_stats = {'path_gen': None, 'path_followed': False, 'path_initiated': False}
        self.fov_deltoid = None
        self.fov_rect = None
        self.fov_unit_stats = {}
        self.fov_unit_keys = []
        self.sighted_units = {}
        self.sighted_units_keys = []
        self.currently_sighted = {'keys': [], 'units': {}}
        self.focal_point = None #DELETE ME EVENTUALLY MAYBE UNLESS I BECOME USEFUL
        self.furthest_points_delete_me = [] #HEY I JUST MET YOU AND THIS IS CRAZY BUT IM SO USELESS DELETE ME MAYBE
        self.temp_line_collision_delete_me = False #SERIOUSLY DELETE ME FFS
        


    def get_desired_degree_val(self):
        if self.desired_pos != None:
            targeting_radians = math.atan2(self.desired_pos[1] - self.tank.rotated_chassis_rect.center[1], self.desired_pos[0] - self.tank.rotated_chassis_rect.center[0])
            targeting_degrees = math.degrees(targeting_radians)
            
            self.desired_degree_val = targeting_degrees


    def clear_path_vars(self, target='omni'):
        if target == 'omni' or target == 'info':
            path_info_keys = [key_x for key_x in self.path_info.keys()]
            for x in range(len(path_info_keys)):
                self.path_info[path_info_keys[x]] = None
        if target == 'omni' or target == 'stats':
            path_stats_keys = [key_x for key_x in self.path_stats.keys()]
            for x in range(len(path_stats_keys)):
                self.path_info[path_stats_keys[x]] = None


    def change_desired_pos(self, pos):
        if self.path_info['path'] != None:
            self.clear_path_vars()       
        self.desired_pos = pos
        self.get_desired_degree_val()


    def halt_tank_movement(self):
        self.tank.chassis_direction['turn'] = None
        self.tank.chassis_direction['move'] = None


    def turn_chassis_to_desired(self):
        if self.desired_pos == None:
            self.chassis_direction['turn'] = None
            return
        temp_dist_to_desired = distance_between_positions(self.tank.rotated_chassis_rect.center, self.desired_pos)
        if temp_dist_to_desired == 0:
            self.chassis_direction['turn'] = None
            return
        degree_difference = abs(self.desired_degree_val - self.tank.chassis_degree_val)
        if degree_difference <= self.tank.chassis_turn_speed:
            self.tank.chassis_degree_val = self.desired_degree_val
            self.tank.chassis_direction['turn'] = None
        else:
            desired_360 = self.desired_degree_val
            if desired_360 < 0:
                desired_360 += 360
            chassis_360 = self.tank.chassis_degree_val
            if chassis_360 < 0:
                chassis_360 += 360
            if desired_360 > chassis_360:
                clockwise_dist = desired_360 - chassis_360
                counterclock_dist = chassis_360 + (360 - desired_360)
            elif desired_360 < chassis_360:
                clockwise_dist = (360 - chassis_360) + desired_360
                counterclock_dist = chassis_360 - desired_360

            if counterclock_dist < clockwise_dist:
                self.tank.chassis_direction['turn'] = 'counterclock'
            elif clockwise_dist < counterclock_dist:
                self.tank.chassis_direction['turn'] = 'clockwise'
            elif clockwise_dist == counterclock_dist:
                self.tank.chassis_direction['turn'] = random.choice(['counterclock', 'clockwise'])


    def move_chassis_to_desired(self):
        if self.desired_pos != None:
            desired_dist = distance_between_positions(self.tank.rotated_chassis_rect.center, self.desired_pos)
            if desired_dist == 0 and self.path_stats['path_followed'] == True:
                self.desired_pos = None
                self.halt_tank_movement()
            #change the order to stop the tank from reorienting upon arrival at the desired_pos, as the elif statements cause the tank to correct
            #the chassis_degree_val prior to teleporting to the desired_pos
            elif desired_dist > self.tank.chassis_move_speed['forward'] and desired_dist < 100 and self.tank.chassis_degree_val != self.desired_degree_val:
                self.tank.chassis_direction['move'] = None
            elif desired_dist <= (self.tank.chassis_move_speed['forward'] * 2):
                chassis_velocity = pygame.math.Vector2(1, 0).rotate(self.desired_degree_val) * desired_dist
                chassis_move_pos = self.tank.chassis_pos + chassis_velocity
                self.tank.chassis_pos = chassis_move_pos
                
                if self.path_info['path'] != None and self.path_stats['path_followed'] == False:
                    if self.desired_pos == self.path_info['closest_node_goal'].center:
                        self.clear_path_vars('stats')
                        self.halt_tank_movement()
                    else:
                        self.follow_path()
                else:
                    self.desired_pos = None
                    self.halt_tank_movement()
                
            else:
                self.tank.chassis_direction['move'] = 'forward'


    def path_generator(self):
        vec2int = pathfinding_salvo_rework.vec2int
        self.path_stats['path_initiated'] = True

        next_node = vec2int(vec(self.path_info['closest_node_start'].center) + self.path_info['path'][self.path_info['closest_node_start'].center])
        closest_start_dist = distance_between_positions(self.path_info['closest_node_start'].center, next_node)
        current_pos_dist = distance_between_positions(self.tank.rotated_chassis_rect.center, next_node)
        closest_start_v = vec(self.path_info['closest_node_start'].center)

        if current_pos_dist <= closest_start_dist:
            current = closest_start_v + self.path_info['path'][vec2int(closest_start_v)]
            yield vec2int(current)
        else:           
            current = closest_start_v
            yield self.path_info['closest_node_start'].center
        
        max_len = len(self.path_info['path'])
             
        for x in range(max_len + 1):
            last_pos = vec2int(current)
            if vec2int(current) not in self.path_info['path']:
                break
            current = current + self.path_info['path'][vec2int(current)]
            yield last_pos
        
            


    def follow_path(self):
        if self.path_info['path'] == None:
            return
        if self.path_stats['path_gen'] == None:
            self.path_stats['path_gen'] = self.path_generator()
        self.desired_pos = next(self.path_stats['path_gen'])



    def create_fov(self):
        view_distance = 400
        origin_pos = self.tank.chassis_turret_pos
        sight_degree_val = 30

        degree_val_a = self.tank.degree_val + sight_degree_val / 2 #clockwise
        degree_val_b = self.tank.degree_val - sight_degree_val / 2 #counterclock
        degree_val_c = self.tank.degree_val

        deltoid_velocity_a = pygame.math.Vector2(1, 0).rotate(degree_val_a) * view_distance
        deltoid_velocity_b = pygame.math.Vector2(1, 0).rotate(degree_val_b) * view_distance
        deltoid_velocity_c = pygame.math.Vector2(1, 0).rotate(degree_val_c) * view_distance
        deltoid_pos_a = origin_pos + deltoid_velocity_a
        deltoid_pos_b = origin_pos + deltoid_velocity_b
        deltoid_pos_c = origin_pos + deltoid_velocity_c

        fov_info = {'a': {'degree_val': degree_val_a, 'velocity': deltoid_velocity_a, 'pos': deltoid_pos_a},
                    'b': {'degree_val': degree_val_b, 'velocity': deltoid_velocity_b, 'pos': deltoid_pos_b},
                    'c': {'degree_val': degree_val_c, 'velocity': deltoid_velocity_c, 'pos': deltoid_pos_c},
                    'origin': {'degree_val': self.tank.degree_val, 'pos': self.tank.chassis_turret_pos},
                    'stats': {'view_distance': view_distance, 'sight_degree_val': sight_degree_val}}

        coords = [origin_pos, deltoid_pos_a, deltoid_pos_b, deltoid_pos_c]
        coords_x_positions = [coords[x][0] for x in range(len(coords))]
        coords_y_positions = [coords[x][1] for x in range(len(coords))]
        rect_top_left = (min(coords_x_positions), min(coords_y_positions))
        rect_width = max(coords_x_positions) - rect_top_left[0]
        rect_height = max(coords_y_positions) - rect_top_left[1]

        fov_rect = pygame.Rect(rect_top_left[0], rect_top_left[1], rect_width, rect_height)

        self.fov_deltoid = fov_info
        self.fov_rect = fov_rect


    def assess_fov(self):
        self.fov_unit_stats = {}
        self.fov_unit_keys = []

        
        sectors_in_sight = self.master_sector.sector_point_collision_omni(self.fov_rect)
        
        player_units_in_sectors = list(set([self.master_sector.sectors[sectors_in_sight[x]].unit_dict['PLAYER'][i] for x in range(len(sectors_in_sight))
                                for i in range(len(self.master_sector.sectors[sectors_in_sight[x]].unit_dict['PLAYER'])) if self.master_sector.sectors[sectors_in_sight[x]].unit_dict['PLAYER'][i] != self.tank.unit_id]))

        enemy_units_in_sectors = list(set([self.master_sector.sectors[sectors_in_sight[x]].unit_dict['ENEMY'][i] for x in range(len(sectors_in_sight))
                                for i in range(len(self.master_sector.sectors[sectors_in_sight[x]].unit_dict['ENEMY'])) if self.master_sector.sectors[sectors_in_sight[x]].unit_dict['ENEMY'][i] != self.tank.unit_id]))

        rogue_units_in_sectors = list(set([self.master_sector.sectors[sectors_in_sight[x]].unit_dict['ROGUE'][i] for x in range(len(sectors_in_sight))
                                for i in range(len(self.master_sector.sectors[sectors_in_sight[x]].unit_dict['ROGUE'])) if self.master_sector.sectors[sectors_in_sight[x]].unit_dict['ROGUE'][i] != self.tank.unit_id]))
        
        obs_units_in_sectors = list(set([self.master_sector.sectors[sectors_in_sight[x]].unit_dict['OBSTACLE'][i] for x in range(len(sectors_in_sight))
                                for i in range(len(self.master_sector.sectors[sectors_in_sight[x]].unit_dict['OBSTACLE'])) if self.master_sector.sectors[sectors_in_sight[x]].unit_dict['OBSTACLE'][i] != self.tank.unit_id]))

        player_units_fov_rect = [player_units_in_sectors[x] for x in range(len(player_units_in_sectors)) if self.fov_rect.colliderect(self.master_sector.units[player_units_in_sectors[x]]['unit_rect']) == True]
        enemy_units_fov_rect = [enemy_units_in_sectors[x] for x in range(len(enemy_units_in_sectors)) if self.fov_rect.colliderect(self.master_sector.units[enemy_units_in_sectors[x]]['unit_rect']) == True]
        rogue_units_fov_rect = [rogue_units_in_sectors[x] for x in range(len(rogue_units_in_sectors)) if self.fov_rect.colliderect(self.master_sector.units[rogue_units_in_sectors[x]]['unit_rect']) == True]
        obs_units_fov_rect = [obs_units_in_sectors[x] for x in range(len(obs_units_in_sectors)) if self.fov_rect.colliderect(self.master_sector.units[obs_units_in_sectors[x]]['unit_rect']) == True]

        player_units_fov_deltoid = []
        for x in range(len(player_units_fov_rect)):
            fov_unit_stats, unit_sighted = self.check_unit_in_fov(player_units_fov_rect[x], 'PLAYER')
            if unit_sighted == True:
                player_units_fov_deltoid.append(player_units_fov_rect[x])
                self.fov_unit_stats[player_units_fov_rect[x]] = fov_unit_stats
                self.fov_unit_keys.append(player_units_fov_rect[x])

        enemy_units_fov_deltoid = []
        for x in range(len(enemy_units_fov_rect)):
            fov_unit_stats, unit_sighted = self.check_unit_in_fov(enemy_units_fov_rect[x], 'ENEMY')
            if unit_sighted == True:
                enemy_units_fov_deltoid.append(enemy_units_fov_rect[x])
                self.fov_unit_stats[enemy_units_fov_rect[x]] = fov_unit_stats
                self.fov_unit_keys.append(enemy_units_fov_rect[x])

        rogue_units_fov_deltoid = []
        for x in range(len(rogue_units_fov_rect)):
            fov_unit_stats, unit_sighted = self.check_unit_in_fov(rogue_units_fov_rect[x], 'ROGUE')
            if unit_sighted == True:
                rogue_units_fov_deltoid.append(rogue_units_fov_rect[x])
                self.fov_unit_stats[rogue_units_fov_rect[x]] = fov_unit_stats
                self.fov_unit_keys.append(rogue_units_fov_rect[x])
        
        obs_units_fov_deltoid = []
        for x in range(len(obs_units_fov_rect)):
            fov_unit_stats, unit_sighted = self.check_unit_in_fov(obs_units_fov_rect[x], 'OBSTACLE')
            if unit_sighted == True:
                obs_units_fov_deltoid.append(obs_units_fov_rect[x])
                self.fov_unit_stats[obs_units_fov_rect[x]] = fov_unit_stats
                self.fov_unit_keys.append(obs_units_fov_rect[x])


        for x in range(len(player_units_fov_deltoid)):
            self.check_unit_points(player_units_fov_deltoid[x])
        for x in range(len(enemy_units_fov_deltoid)):
            self.check_unit_points(enemy_units_fov_deltoid[x])
        for x in range(len(rogue_units_fov_deltoid)):
            self.check_unit_points(rogue_units_fov_deltoid[x])
        for x in range(len(obs_units_fov_deltoid)):
            self.check_unit_points(obs_units_fov_deltoid[x])

        self.order_sighted_units_dist()

        for x in range(len(self.fov_unit_keys)):
            if self.master_sector.units[self.fov_unit_keys[x]]['allegiance'] != self.allegiance:
                self.check_target_sighted(self.fov_unit_keys[x])
        
                                


    def check_unit_in_fov(self, unit_id, allegiance):
        unit_stats = self.master_sector.get_unit_stats(unit_id)

        within_degrees = False
        focal_point = None
        within_range = False
        point_sighted = False
        unit_sighted = False

        fov_unit_stats = {'center': False, 'bounding_points': [], 'allegiance': allegiance}

        
        clockwise = self.fov_deltoid['a']['degree_val']
        counterclock = self.fov_deltoid['b']['degree_val']
        origin_degree = self.fov_deltoid['origin']['degree_val']

        unit_center_degree = angle_between_points(unit_stats['unit_rect'].center, self.fov_deltoid['origin']['pos'])
        within_degrees = is_degree_in_degree_range(clockwise, counterclock, unit_center_degree)

        focal_point = unit_stats['unit_rect'].center
        dist_origin_to_point = distance_between_positions(self.fov_deltoid['origin']['pos'], unit_stats['unit_rect'].center)
        if dist_origin_to_point <= self.fov_deltoid['stats']['view_distance'] and within_degrees == True:
            within_range = True
            point_sighted = True
            unit_sighted = True
        fov_unit_stats['center'] = (unit_stats['unit_rect'].center, point_sighted, unit_center_degree, dist_origin_to_point)
            
        for x in range(len(unit_stats['bounding_points'])):
            within_degrees = False
            within_range = False
            focal_point = None
            point_sighted = False
            point_x = unit_stats['bounding_points'][x]
            degree_x = angle_between_points(point_x, self.fov_deltoid['origin']['pos'])
            within_degrees = is_degree_in_degree_range(clockwise, counterclock, degree_x)
            focal_point = point_x
            dist_origin_to_point = distance_between_positions(self.fov_deltoid['origin']['pos'], point_x)
            if dist_origin_to_point <= self.fov_deltoid['stats']['view_distance'] and within_degrees == True:
                within_range = True
                unit_sighted = True
                point_sighted = True
            fov_unit_stats['bounding_points'].append((point_x, point_sighted, degree_x, dist_origin_to_point))
            
        return fov_unit_stats, unit_sighted
    
            #Due to severe framerate reduction introduced as a result of the line-intersection calculation, the automatic-check against
            #all potentially colliding units has been removed, as the fringe cases that it resolves have, after consideration, been
            #determined to be insufficiently limited, as any unit that is within a position that it is detected by the fov-deltoid
            #line-test, but not against its bounding-points, will find a bounding point within sight should the angle of observation
            #adjust. This is coupled with the fact that it is only issuous at the corners of the deltoid, as it is an impossible
            #occurence anywhere else, given the nature of the bounding points. Any unnoticed units that would have been detected using
            #the line-intersection functionality will be observed by any sufficient searching capability consisting of simple rotation.
            #
##        if len(unit_stats['bounding_points']) == 4:
##            pairs = [[unit_stats['bounding_points'][0], unit_stats['bounding_points'][1]], [unit_stats['bounding_points'][0], unit_stats['bounding_points'][2]],
##                     [unit_stats['bounding_points'][2], unit_stats['bounding_points'][3]], [unit_stats['bounding_points'][1], unit_stats['bounding_points'][3]]]
##            fov_lines = [('a', 'origin'), ('b', 'origin'), ('c', 'a'), ('c', 'b')]
##            for x in range(len(fov_lines)):
##                for i in range(len(pairs)):
##                    within_degrees = False
##                    within_range = False
##                    focal_point = None
##                    intersect_check = get_intersect(pairs[i][0], pairs[i][1], self.fov_deltoid[fov_lines[x][0]]['pos'], self.fov_deltoid[fov_lines[x][1]]['pos'])
##                    if intersect_check != (float('inf'), float('inf')):
##                        within_degrees = True
##                        intersect_check = (int(intersect_check[0]), int(intersect_check[1]))
##                        intersect_dist = distance_between_positions(self.fov_deltoid['origin']['pos'], intersect_check)
##                        fov_dist = self.fov_deltoid['stats']['view_distance']
##                        if intersect_dist <= fov_dist:
##                            is_on_check = intersection_point_rect_collision(pairs[i][0], pairs[i][1], intersect_check)
##                            if is_on_check == True:
##                                within_range = True
##                                fov_unit_stats['bounding_lines'].append((intersect_check, True))
##                    if within_degrees == False or within_range == False:
##                        fov_unit_stats['bounding_lines'].append((intersect_check, False))

    def order_sighted_units_dist(self):
        closest_to_furthest = []
        id_key_clone = self.fov_unit_keys[:]
        min_dist = 100000
        min_unit = None
        while len(closest_to_furthest) < len(self.fov_unit_keys):
            for x in range(len(id_key_clone)):
                unit_x = self.fov_unit_stats[id_key_clone[x]]
                if unit_x['los_points']['clockwise_dist'] < min_dist or unit_x['los_points']['counterclock_dist'] < min_dist:
                    min_dist = min([unit_x['los_points']['clockwise_dist'], unit_x['los_points']['counterclock_dist']])
                    min_unit = id_key_clone[x]
            closest_to_furthest.append(min_unit)
            id_key_clone.remove(min_unit)
            min_dist = 100000
            min_unit = None

        self.fov_unit_keys = closest_to_furthest[:]

                
            
        
                                        
    def check_unit_points(self, unit_id):

        fov_x = self.fov_unit_stats[unit_id]

        origin_degree = self.fov_deltoid['origin']['degree_val']
        degree_a = self.fov_deltoid['a']['degree_val']#clockwise
        degree_b = self.fov_deltoid['b']['degree_val']#counterclock

        clockwise_points = []
        counterclock_points = []

        for x in range(len(fov_x['bounding_points'])):
            check_degrees = get_closest_degree_direction(fov_x['center'][2], fov_x['bounding_points'][x][2])
            if check_degrees[0] == 'clockwise':
                clockwise_points.append((fov_x['bounding_points'][x][0], check_degrees[1]))
            else:
                counterclock_points.append((fov_x['bounding_points'][x][0], check_degrees[1]))

        max_clock = max([clockwise_points[x][1] for x in range(len(clockwise_points))])
        max_counter = max([counterclock_points[x][1] for x in range(len(counterclock_points))])

        for x in range(len(clockwise_points)):
            if clockwise_points[x][1] == max_clock:
                max_clock = clockwise_points[x][0]
        for x in range(len(counterclock_points)):
            if counterclock_points[x][1] == max_counter:
                max_counter = counterclock_points[x][0]

        if self.fov_unit_stats[unit_id]['allegiance'] == 'PLAYER':
            self.furthest_points_delete_me.extend([max_clock, max_counter, fov_x['center'][0]])
        #seriously, delete me, I'm only useful for testing purposes. Also, I have a reference within the __init__ for the AI class
        #and near the end of the code as a pygame.draw.circle point

##        lines_to_check = []
##        positions = [max_clock, max_counter, fov_x['center'][0]]
##        for x in range(len(positions)):
##            line_x = create_line(self.fov_deltoid['origin']['pos'], positions[x])
        for x in range(len(fov_x['bounding_points'])):
            if fov_x['bounding_points'][x][0] == max_clock:
                clockwise_dist = fov_x['bounding_points'][x][3]
                clockwise_degree = fov_x['bounding_points'][x][2]
            elif fov_x['bounding_points'][x][0] == max_counter:
                counterclock_dist = fov_x['bounding_points'][x][3]
                counterclock_degree = fov_x['bounding_points'][x][2]

        self.fov_unit_stats[unit_id]['los_points'] = {}

        self.fov_unit_stats[unit_id]['los_points'] = {'clockwise': max_clock, 'clockwise_dist': clockwise_dist, 'clockwise_degree': clockwise_degree,
                                                   'counterclock': max_counter, 'counterclock_dist': counterclock_dist, 'counterclock_degree': counterclock_degree}

        
    def check_target_sighted(self, unit_id):
        fov_x = self.fov_unit_stats[unit_id]

        degrees_to_check = {'c': (fov_x['center'][0], fov_x['center'][2], True), 'a': (fov_x['los_points']['clockwise'], fov_x['los_points']['clockwise_degree'], True), 'b': (fov_x['los_points']['counterclock'], fov_x['los_points']['counterclock_degree'], True)}
        degree_keys = ['c', 'a', 'b']
        
        

        for x in range(len(degree_keys)):
            line_collision = False
            for i in range(len(self.fov_unit_keys)):
                if self.fov_unit_keys[i] == unit_id:
                    break
                unit_i = self.fov_unit_keys[i]
                line_in_degrees = is_degree_in_degree_range(self.fov_unit_stats[unit_i]['los_points']['clockwise_degree'], self.fov_unit_stats[unit_i]['los_points']['counterclock_degree'], degrees_to_check[degree_keys[x]][1])
                if line_in_degrees == True:
                    line_collision = True
                    degrees_to_check[degree_keys[x]] = (degrees_to_check[degree_keys[x]][0], degrees_to_check[degree_keys[x]][1], False)
            if line_collision == False:
                break

        self.currently_sighted['keys'].append(unit_id)
        self.currently_sighted['units'][unit_id] = degrees_to_check

        if line_collision == False:
            self.mark_unit_sighted(unit_id)
        
        

    def mark_unit_sighted(self, unit_id):
        sight_time = pygame.time.get_ticks()
        sight_limit = 10000

        if unit_id not in self.sighted_units_keys:
            self.sighted_units_keys.append(unit_id)
        self.sighted_units[unit_id] = {'sight_timer': sight_time + sight_limit}


    def assess_sighted_units(self):
        current_time = pygame.time.get_ticks()

        remaining_units = []

        for x in range(len(self.sighted_units_keys)):
            if current_time > self.sighted_units[self.sighted_units_keys[x]]['sight_timer']:
                del self.sighted_units[self.sighted_units_keys[x]]
            else:
                remaining_units.append(self.sighted_units_keys[x])

        self.sighted_units_keys = remaining_units
                
                
        
        


    def draw_path(self):
        BUBBLEGUM = (255, 0, 255)
        color = (0, 0, 255)
        

        pathfinding_salvo_rework.draw_node_connections(DISPSURF, self.path_info['tested_nodes'], self.path_info['graph'])
        
        for x in range(len(self.path_info['graph'].nodes_list_omni)):
            if self.path_info['graph'].nodes_list_omni[x].center not in self.path_info['graph'].culled_nodes:
                self.path_info['graph'].nodes_list_omni[x].draw_self(DISPSURF)

        self.path_info['start'].draw_self(DISPSURF)
        self.path_info['goal'].draw_self(DISPSURF)
        self.path_info['start'].draw_connection(DISPSURF)
        self.path_info['goal'].draw_connection(DISPSURF)

        path_keys = [x for x in self.path_info['path'].keys()]
        path_keys_nodes = [self.path_info['graph'].retrieve_node(path_keys[x]) for x in range(len(path_keys))]
        for x in range(len(path_keys_nodes)):
            path_keys_nodes[x].draw_self(DISPSURF, (255, 0, 0))

        closest_start_v = vec(self.path_info['closest_node_start'].center)
        closest_end_v = vec(self.path_info['closest_node_goal'].center)
        current = closest_start_v
        counter = 0
        last_node = None
        max_len = len(self.path_info['path'])
        path_start_drawn = False
        
        while counter < max_len:

            pygame.draw.circle(DISPSURF, BUBBLEGUM, vec2int(current), 3, 0)
            if last_node != None:
                pygame.draw.aaline(DISPSURF, BUBBLEGUM, vec2int(last_node), vec2int(current), True)
            last_node = current
            if vec2int(current) not in self.path_info['path']:
                break
            current = current + self.path_info['path'][vec2int(current)]
            counter += 1
        


    def operations_management(self):
        self.focal_point = None
        self.furthest_points_delete_me = []
        self.currently_sighted = {'keys': [], 'units': {}}
        if self.desired_pos != None:
            if self.path_info['path'] != None and self.path_stats['path_followed'] == False and self.path_stats['path_initiated'] == False:
                self.follow_path()
            self.get_desired_degree_val()
            self.turn_chassis_to_desired()
            self.move_chassis_to_desired()
        self.create_fov()
        self.assess_fov()
        self.assess_sighted_units()

            
            
            


        



#------------------Non-Class Functions

def merge_images(turret_base, turret_class, weapons_list):
    merged_img = turret_base['img'].copy()
    for x in range(len(weapons_list)):
        weapon_x_img = weapons_list[x]['img']
        blit_pos = (weapons_list[x]['offset'][turret_class]['blit_pos'])  
        merged_img.blit(weapon_x_img, blit_pos)
    merged_img.convert_alpha()

    return merged_img


def turret_generator(turret_base, weapons_list):

    turret_class = turret_base['turret_class']
    turret_img = merge_images(turret_base, turret_class, weapons_list)
    tank_turret = {'img': turret_img, 'turret_rotation_speed': turret_base['turret_rotation_speed'], 'rotate_offset': turret_base['rotate_offset'],
                   'weapons': [(weapons_list[x]['offset'][turret_class]['munition_spawn'], weapons_list[x]['designation'], weapons_list[x]['fire_mode'],
                                weapons_list[x]['munition_types'], weapons_list[x]['bounding_offsets'][turret_class][0], weapons_list[x]['bounding_offsets'][turret_class][1]) for x in range(len(weapons_list))]}

    return tank_turret


def distance_between_positions(pos_a, pos_b):
    x_distance = abs(pos_a[0] - pos_b[0])
    y_distance = abs(pos_a[1] - pos_b[1])
    pyth_dist = x_distance**2 + y_distance**2
    pyth_dist = int(sqrt(pyth_dist))

    return pyth_dist


def generate_unit_id():
    alphabet = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
    phonetic_alpha = ['ALPHA', 'BRAVO', 'CHARLIE', 'DELTA', 'ECHO', 'FOXTROT', 'GOLF', 'HOTEL', 'INDIA', 'JULIETT', 'KILO', 'LIMA', 'MIKE',
                      'NOVEMBER', 'OSCAR', 'PAPA', 'QUEBEC', 'ROMEO', 'SIERRA', 'TANGO', 'UNIFORM', 'VICTOR', 'WHISKEY', 'XRAY', 'YANKEE', 'ZULU']

    start_a = random.randint(0, len(alphabet))
    start_b = random.randint(0, len(alphabet))
    
    while True:
        for x in range(start_a, len(alphabet)):
            for i in range(start_b, len(alphabet)):
                yield [alphabet[x] + alphabet[i], random.choice(phonetic_alpha)]
            start_b = 0
        start_a = 0


def generate_sector_id():
    prepend = ''
    prepend_index = 0
    alphabet = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
    while True:
        for x in range(0, 100):
            yield prepend + str(x)
        prepend_index += 1
        prepend = alphabet[prepend_index]
        if prepend_index == len(alphabet) - 1:
            alphabet = [alphabet[x][0]*(len(prepend) + 1) for x in range(len(alphabet))]
            prepend_index = 0
        


def check_weapon_reload(playerTank):
    weapon_reloading = None
    if pygame.mouse.get_pressed()[0] == 1:
        weapon_reloading = 0
    elif pygame.mouse.get_pressed()[1] == 1:
        weapon_reloading = 2
    elif pygame.mouse.get_pressed()[2] == 1:
        weapon_reloading = 1
    if weapon_reloading != None:
        playerTank.initiate_reload_requirement(weapon_reloading)


def generate_obstacle(mouse_pos, obstacle_list, other_units):

    new_obstacle = pygame.Rect(mouse_pos[0] - 50, mouse_pos[1] - 50, 100, 100)
    valid_placement = True
    for x in range(len(other_units)):
        other_unit_rect = other_units[x].rotated_chassis_rect
        if other_unit_rect.colliderect(new_obstacle) == True:
            valid_placement = False
    if valid_placement == True:
        obstacle_list.append(new_obstacle)
    return obstacle_list


def angle_between_points(a, b):
    degree_radians = math.atan2(a[1] - b[1], a[0] - b[0])
    degree_val = math.degrees(degree_radians)
    return degree_val


def pos_from_degrees(pos_a, degree_val, dist):
        '''
        Determines a coordinate position given a starting position, a degree-value and a distance.
        '''
        velocity = pygame.math.Vector2(1, 0).rotate(degree_val) * dist
        pos_b = pos_a + velocity
        return pos_b


###########LIBERATED CODE FROM STACKOVERFLOW###########
def get_intersect(a1, a2, b1, b2):
    """ 
    Returns the point of intersection of the lines passing through a2,a1 and b2,b1.
    a1: [x, y] a point on the first line
    a2: [x, y] another point on the first line
    b1: [x, y] a point on the second line
    b2: [x, y] another point on the second line
    """
    s = numpy.vstack([a1,a2,b1,b2])        # s for stacked
    h = numpy.hstack((s, numpy.ones((4, 1)))) # h for homogeneous
    l1 = numpy.cross(h[0], h[1])           # get first line
    l2 = numpy.cross(h[2], h[3])           # get second line
    x, y, z = numpy.cross(l1, l2)          # point of intersection
    if z == 0:                          # lines are parallel
        return (float('inf'), float('inf'))
    return (x/z, y/z)
############END LIBERATION############


############LIBERATED CODE FROM STACKOVERFLOW#############
def is_on_line(a, b, c):
    "Return true iff point c intersects the line segment from a to b."
    # (or the degenerate case that all 3 points are coincident)
    return (collinear(a, b, c)
            and (within(a.x, c.x, b.x) if a.x != b.x else 
                 within(a.y, c.y, b.y)))

def collinear(a, b, c):
    "Return true iff a, b, and c all lie on the same line."
    return (b.x - a.x) * (c.y - a.y) == (c.x - a.x) * (b.y - a.y)

def within(p, q, r):
    "Return true iff q is between p and r (inclusive)."
    return p <= q <= r or r <= q <= p
##############END LIBERATION#############


###copied code - Bresenham's Algorithm
def create_line(start, end):
    """Bresenham's Line Algorithm
    Produces a list of tuples from start and end
 
    >>> points1 = get_line((0, 0), (3, 4))
    >>> points2 = get_line((3, 4), (0, 0))
    >>> assert(set(points1) == set(points2))
    >>> print points1
    [(0, 0), (1, 1), (1, 2), (2, 3), (3, 4)]
    >>> print points2
    [(3, 4), (2, 3), (1, 2), (1, 1), (0, 0)]
    """
    # Setup initial conditions
    x1, y1 = start
    x2, y2 = end
    dx = x2 - x1
    dy = y2 - y1
 
    # Determine how steep the line is
    is_steep = abs(dy) > abs(dx)
 
    # Rotate line
    if is_steep:
        x1, y1 = y1, x1
        x2, y2 = y2, x2
 
    # Swap start and end points if necessary and store swap state
    swapped = False
    if x1 > x2:
        x1, x2 = x2, x1
        y1, y2 = y2, y1
        swapped = True
 
    # Recalculate differentials
    dx = x2 - x1
    dy = y2 - y1
 
    # Calculate error
    error = int(dx / 2.0)
    ystep = 1 if y1 < y2 else -1
 
    # Iterate over bounding box generating points between start and end
    y = y1
    points = []
    for x in range(x1, x2 + 1):
        coord = (y, x) if is_steep else (x, y)
        points.append(coord)
        error -= abs(dy)
        if error < 0:
            y += ystep
            error += dx
 
    # Reverse the list if the coordinates were swapped
    if swapped:
        points.reverse()
    return points
###end of copied code


def intersection_point_rect_collision(a, b, c):
    """
    Creates a bounding rectangle for points a and b, then checks
    for a collision between the rectangle and point c.
    """
    x_points = [a[0], b[0]]
    y_points = [a[1], b[1]]
    top_left = (min(x_points), min(y_points))
    width = abs(a[0] - b[0])
    height = abs(a[1] - b[1])
    if width != 0 and height != 0:
        bounding_rect = pygame.Rect(top_left[0], top_left[1], width, height)
        return bounding_rect.collidepoint(c)
    if width == 0 and c[1] >= min(y_points) and c[1] <= max(y_points):
        return True
    elif height == 0 and c[0] >= min(x_points) and c[0] <= max(x_points):
        return True
    return False


def is_degree_in_degree_range(degree_a, degree_b, degree_c):
    """
    Checkes whether a given degree-value lies between two bounding
    degree-values, where degree_a and degree_b are the bounding
    degree-limits, with degree_a representing the clockwise oriented degree-value
    and degree_b representing the counterclockwise degree-value.
    Degree_c is the value being checked.
    """
    degrees_omni = [degree_a, degree_b, degree_c]
    for x in range(len(degrees_omni)):
        if degrees_omni[x] > 180:
            degrees_omni[x] -= 360
        elif degrees_omni[x] <= -180:
            degrees_omni[x] += 360
    degree_a = degrees_omni[0]
    degree_b = degrees_omni[1]
    degree_c = degrees_omni[2]

    clockwise = degree_a
    counterclock = degree_b

    if clockwise > counterclock:
        if degree_c <= clockwise and degree_c >= counterclock:
            return True
    elif clockwise < counterclock and clockwise < 0 and counterclock > 0:
        if degree_c >= counterclock or degree_c <= clockwise:
            return True
    return False


def get_closest_degree_direction(degree_a, degree_b):
        """
        Returns the direction, counterclock or clockwise, that
        is the closest to degree_a from degree_b,
        along with the distance
        """

        a_360 = degree_a
        b_360 = degree_b
        if a_360 < 0:
            a_360 = a_360 + 360
        if b_360 < 0:
            b_360 = b_360 + 360     

        clockwise_dist = 0
        counterclock_dist = 0
        direction = None

        if b_360 > a_360:
            clockwise_dist = b_360 - a_360
            counterclock_dist = a_360 + (360 - b_360)
        elif b_360 < a_360:
            clockwise_dist = (360 - a_360) + b_360
            counterclock_dist = a_360 - b_360

        if clockwise_dist < counterclock_dist:
            direction = 'clockwise'
            dist = clockwise_dist
        elif clockwise_dist > counterclock_dist:
            direction = 'counterclock'
            dist = counterclock_dist
        elif clockwise_dist == counterclock_dist:
            direction = 'clockwise'
            dist = clockwise_dist

        return (direction, dist)


def get_degree_diff(degree_a, degree_b):
    '''
    Returns the difference between degrees a and b, from the perspective of degree_a.
    If the direction from degree_a to degree_b is clockwise, a positive value will be returned,
    otherwise a negative value.
    '''

    a_360 = degree_a
    b_360 = degree_b
    if a_360 >= 360 or a_360 <= -360:
        if a_360 >= 360:
            a_360 = a_360 % 360
        else:
            a_360 = a_360 % -360
    if a_360 < 0:
        a_360 += 360
    if b_360 >= 360 or b_360 <= -360:
        if b_360 >= 360:
            b_360 = b_360 % 360
        else:
            b_360 = b_360 % -360
    if b_360 < 0:
        b_360 += 360

    if b_360 > a_360:
        clockwise_dist = b_360 - a_360
        counterclock_dist = -(a_360 + (360 - b_360))
    else:
        clockwise_dist = b_360 + (360 - a_360)
        counterclock_dist = b_360 - a_360

    if abs(clockwise_dist) > abs(counterclock_dist):
        return counterclock_dist
    else:
        return clockwise_dist


def polarize_degree(degree_x):
    '''Receives a degree-value in the form of a float, returning the opposite degree-value.
    e.g, 0 returns 180, 90 returns 270, etc.
    '''
    
    if degree_x > 180 or degree_x <= -180:
        if degree_x > 180:
            degree_x = degree_x % 180
            degree_x -= 180
        else:
            degree_x = degree_x % -180
            degree_x += 180
    if degree_x > 0:
        degree_x -= 180
    else:
        degree_x += 180

    return degree_x


def trig_calc(sides):
    '''
    Receives a tuple containing four sides, a, b, c and second_c in order to calculate
    a final side (second_a) utilizing the trigonometric laws of sine and cosine. Side_a being an
    angular reference point for the final side, which is utilized to calculate a point on the same line
    (though not the same position) as side_a, from the origin-point of side_b. This is utilized strictly
    for the relocation of bounding-points from bounding-box to bounding-box, and may be prone to errors if utilized otherwise.
    collisions.
    Arguments: sides (tuple comprising four ints that must represent a viable triangle)
    '''
    side_a = sides[0]
    side_b = sides[1]
    side_c = sides[2]
    second_c = sides[3]
    try:
        angle_c = math.acos((side_a**2 + side_b**2 - side_c**2) / (2 * side_a * side_b))
        side_c = second_c
        try:
            angle_b = math.asin((math.sin(angle_c) * side_b) / side_c)
        except ValueError:
            return None
        angle_a = math.radians(180.00 - math.degrees(angle_b) - math.degrees(angle_c))
        side_a = (math.sin(angle_a) * side_b) / math.sin(angle_b)
        return side_a
    except ZeroDivisionError:
        return None


def vec2int(v):
    return (int(v[0]), int(v[1]))

def int2vec(i):
    return pygame.math.Vector2(i)


def create_circle_sprite(radius):
    '''
    Receives an int(radius) and returns a pygame Surface object with a circle of the radius and 1 pixel width blitted onto the center.
    '''
    radius = int(radius)
    img_surface = pygame.Surface((radius * 2, radius * 2), SRCALPHA)
    img_rect = img_surface.get_rect()
    pygame.draw.circle(img_surface, (0, 0, 0), img_rect.center, radius, 1)
    img_mask = pygame.mask.from_surface(img_surface)


    radius_sprite = gameSprite(img_surface, img_rect, img_mask)
    return radius_sprite

    

def circle_line_intersect(circle, point_a, point_b):
    #Code pilfered from Stackoverflow (or liberated)
    """
    Determines the points of intersection between a line segment and circle
    if one or more intersections exist, returning tuples of the intersect positions,
    or None values for False intersections.

    Arguments: circle: a tuple containing the circle center in (int(x), int(y)) format along
    with the radius of the circle in pixels; point_a: one end of the line segment in tuple (int(x), int(y))
    format, point_b: the opposite end of the line segment from point_a in tuple (int(x), int(y)) format.
    *Note that point_a or point_b may also be position vectors, as this has no effect on the calculation.
    """

    vec_a = int2vec(point_a)
    vec_b = int2vec(point_b)
    
    circle_center = int2vec(circle[0])
    circle_radius = circle[1]
    vector_line = vec_b - vec_a

    a = vector_line.dot(vector_line)
    b = 2 * vector_line.dot(vec_a - circle_center)
    c = vec_a.dot(vec_a) + circle_center.dot(circle_center) - 2 * vec_a.dot(circle_center) - circle_radius**2

    discriminant = b**2 - (4 * a * c)
    if discriminant < 0:
        return None, None
    sqrt_disc = math.sqrt(discriminant)
    coll_a = (-b + sqrt_disc) / (2 * a)
    coll_b = (-b - sqrt_disc) / (2 * a)

    if not (0 <= coll_a <= 1):
        coll_a = None
    else:
        coll_a = vec2int(vec_a + coll_a * vector_line)
    if not (0 <= coll_b <=1):
        coll_b = None
    else:
         coll_b = vec2int(vec_a + coll_b * vector_line)
    if coll_a == None and coll_b == None:
        return None, None
    
    return coll_a, coll_b

    
    


def pygame_quit():
    pygame.quit()
    sys.exit()







#-------------------Main Loop
def main():
    
    global FPSCLOCK, DISPSURF, CURRENT_TIME, ID_GENERATOR, SECTOR_ID
    pygame.init()
    FPSCLOCK = pygame.time.Clock()
    DISPSURF = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))

    DISPSURF.fill(BGCOLOR)

    ID_GENERATOR = generate_unit_id()
    SECTOR_ID = generate_sector_id()

    obstacle_list = []

    master_sector = MasterSector()

    #pygame.display.set_caption('Salvo!')
    
    #Images

    #Blank Image
    blank_img = pygame.image.load('blank_2k.png').convert_alpha()

    #Chassis images
    chassis_img = pygame.image.load('chassis.png').convert_alpha()

    #Turret images
    base_turret_img = pygame.image.load('turret_bare.png').convert_alpha()
    turret_img = pygame.image.load('turret.png').convert_alpha()
    minigun_turret_img = pygame.image.load('minigun_turret.png').convert_alpha()
    minigun_turret_omni_img = pygame.image.load('minigun_turret_omni_short.png').convert_alpha()
    minigun_turret_omni_v2_img = pygame.image.load('minigun_turret_omni.png').convert_alpha()
    minigun_turret_dual_img = pygame.image.load('minigun_turret_dual.png').convert_alpha()

    #Weapon Images
    minigun_left_img = pygame.image.load('minigun_reduced_left.png').convert_alpha()
    minigun_right_img = pygame.image.load('minigun_reduced_right.png').convert_alpha()
    standard_barrel_img = pygame.image.load('standard_barrel.png').convert_alpha()
    minigun_mega_img = pygame.image.load('minigun_mega.png').convert_alpha()
    
    #Munitions images
    standard_shell_img = pygame.image.load('spr_missile_small.png').convert_alpha()
    fortyfour_mm_round_img = pygame.image.load('44_mm.png').convert_alpha()

    #Spritesheets
    explosion_sheet = pygame.image.load('explosion_original.png').convert_alpha()
    explosion_mini_sheet = pygame.image.load('explosion_original_mini.png').convert_alpha()
    exp2_mini_sheet = pygame.image.load('exp2_mini_alpha.png').convert_alpha()
    explosion_large_shockwave_sheet = pygame.image.load('explosion_large_shockwave_spritesheet.png').convert_alpha()
    explosion_skull_sheet = pygame.image.load('explosion_skull_spritesheet_edited.png').convert_alpha()

    #Impact Animations
    explosion_impact = {'impact_animation': explosion_sheet, 'columns_rows': (12, 1), 'impact_offset': (0, 0), 'animation_type': 'dynamic', 'impact_orientation': 'random', 'impact_degree_variance': 0, 'special_degree_fix': 0}
    explosion_mini_impact = {'impact_animation': explosion_mini_sheet, 'columns_rows': (12, 1), 'impact_offset': (0, 0), 'animation_type': 'dynamic', 'impact_orientation': 'random', 'impact_degree_variance': 0, 'special_degree_fix': 0}
    explosion_large_shockwave_impact = {'impact_animation': explosion_large_shockwave_sheet, 'columns_rows': (5, 6), 'impact_offset': (0, 0), 'animation_type': 'dynamic', 'impact_orientation': 'random', 'impact_degree_variance': 0, 'special_degree_fix': 0}
    explosion_skull_impact = {'impact_animation': explosion_skull_sheet, 'columns_rows': (5, 4), 'impact_offset': (100, 0), 'animation_type': 'dynamic', 'impact_orientation': 'inverse', 'impact_degree_variance': 30, 'special_degree_fix': -90}

    #Obs Images
    pine_tree_img = pygame.image.load('tree_pine_1.png').convert_alpha()




    #Turret Variables
    base_turret = {'img': base_turret_img, 'turret_class': 'base_turret', 'turret_rotation_speed': 3, 'rotate_offset': (44, 0)}
            


    #Weapon Variables
    minigun_left = {'img': minigun_left_img, 'offset': {'base_turret': {'blit_pos': (-15, -14), 'munition_spawn': (35, -24)}}, 'designation': 'secondary',
                    'fire_mode': 'auto', 'munition_types': ['fortyfour_mm_round'], 'bounding_offsets': {'base_turret': ([(30, -31), (30, -13), (-20, -31), (-20, -13)], (5, -22))}}

    minigun_right = {'img': minigun_right_img, 'offset': {'base_turret': {'blit_pos': (-15, 29), 'munition_spawn': (35, 24)}}, 'designation': 'secondary',
                     'fire_mode': 'auto', 'munition_types': ['fortyfour_mm_round'], 'bounding_offsets': {'base_turret': ([(30, 31), (30, 13), (-20, 31), (-20, 13)], (5, 24))}}

    standard_barrel = {'img': standard_barrel_img, 'offset': {'base_turret': {'blit_pos': (0, 0), 'munition_spawn': (110, 0)}}, 'designation': 'primary',
                       'fire_mode': 'semi', 'munition_types': ['standard_shell'], 'bounding_offsets': {'base_turret': ([(107, -4), (107, 4), (14, -4), (14, 4)], (55, 0))}}

    minigun_mega = {'img': minigun_mega_img, 'offset': {'base_turret': {'blit_pos': (-69, -18), 'munition_spawn': (75, 0)}}, 'designation': 'secondary',
                    'fire_mode': 'auto', 'munition_types': ['fortyfour_mm_round'], 'bounding_offsets': {'base_turret': ([],)}}

    
    #Tank Variables

    standard_chassis = {'img': chassis_img, 'chassis_move_speed': {'forward': 2, 'reverse': -1.5}, 'chassis_turn_speed': 2,
                             'chassis_direction': {'turn': None, 'move': None}, 'rotate_offset': (44, 0), 'turret_offsets': [(-18, -1)],
                        'node_distance': 100, 'bounding_offsets': [(43, -30), (43, 30), (-45, -30), (-45, 30)],
                        'health': {'mortal': True, 'max_health': 1200, 'health': 1200, 'pen_mod': 450, 'he_mod': 210}}
    
    standard_shell = {'img': standard_shell_img, 'munition_type': 'standard_shell', 'munition_move_speed': 21, 'maximum_distance': 2000, 'designation': 'primary', 'munition_offset': (10, 0), 'degree_variance': 0, 'firing_rate': 1, 'round_capacity': 1, 'maximum_ammo': 30, 'initial_ammo': 15, 'reload_time_ms': 2000, 'impact': explosion_large_shockwave_impact, 'damage': {'direct': {'pen_dmg': 150, 'he_dmg': 300, 'pen_mod': 50, 'he_mod': 200}, 'area': {'pen_dmg': 0, 'he_dmg': 150, 'pen_mod': 0, 'he_mod': 100, 'dist': 75, 'sprite': create_circle_sprite(75)}}}

    fortyfour_mm_round = {'img': fortyfour_mm_round_img.convert_alpha(), 'munition_type': 'fortyfour_mm_round', 'munition_move_speed': 44, 'maximum_distance': 1250, 'designation': 'secondary', 'munition_offset': (5, 0), 'degree_variance': 3, 'firing_rate': 50, 'round_capacity': 75, 'maximum_ammo': 2000, 'initial_ammo': 1000, 'reload_time_ms': 1500, 'impact': explosion_mini_impact, 'damage': {'direct': {'pen_dmg': 80, 'he_dmg': 0, 'pen_mod': 50, 'he_mod': 0}, 'area': None}}
    
    #Obs Sprite Variables
    pine_obs = {'img': pine_tree_img, 'rotate_offset': (44, 0), 'bounding_offsets': [(50, -50), (50, 50), (-50, -50), (-50, 50)], 'health': {'mortal': False}}

    #PlayerTank variables
    
    mouse = {'mouse_x': 0, 'mouse_y': 0}

    chassis_direction = {'turn': None, 'move': None}
    
    chassis_pos = (200, 240)


    player_tank_turret = turret_generator(base_turret, [standard_barrel, minigun_left, minigun_right])
    #playerTank = Tank(standard_chassis, player_tank_turret, [standard_shell, fortyfour_mm_round], {'standard_shell': 100, 'fortyfour_mm_round': 10000}, chassis_pos, 'PLAYER', master_sector)
    playerTank_dict = {'unit_type': 'tank', 'chassis': standard_chassis, 'turret': player_tank_turret, 'munitions': [standard_shell, fortyfour_mm_round], 'ammo': {'standard_shell': 100, 'fortyfour_mm_round': 10000}, 'pos': chassis_pos, 'allegiance': 'PLAYER'}
    playerTank_id = master_sector.instantiate_unit(playerTank_dict)
 


    #SecondTank variables

    e_target = (None, None)
    e_chassis_move_speed = {'forward': 2, 'reverse': -1.5}
    e_chassis_turn_speed = 2
    e_turret_rotation_speed = 3
    e_chassis_direction = {'turn': None, 'move': None}
    e_chassis_pos = (600, 400)
    desired_pos = None

    enemy_tank_turret = turret_generator(base_turret, [standard_barrel])
    #enemyTank = Tank(standard_chassis, enemy_tank_turret, [standard_shell], {}, e_chassis_pos, 'ENEMY', master_sector)
    enemyTank_dict = {'unit_type': 'tank', 'chassis': standard_chassis, 'turret': enemy_tank_turret, 'munitions': [standard_shell], 'ammo': {'standard_shell': 15}, 'pos': e_chassis_pos, 'allegiance': 'ENEMY'}
    enemyTank_id = master_sector.instantiate_unit(enemyTank_dict)
    enemyTank = master_sector.unit_objects[enemyTank_id]
    master_sector.instantiate_artificial(enemyTank_id)
    artificial_enemy = master_sector.artificial_objects[enemyTank_id]


    artificial_enemy.tank.generate_tank(DISPSURF)

    enemy_chassis2 = dict(standard_chassis)
    enemy_tank_turret2 = dict(enemy_tank_turret)

    

    #AuxiliaryTank variables
    aux_tanks = []
    aux_positions = [] #[(500, 300)] #[(200, 450), (625, 350), (800, 450), (500, 300), (75, 100), (575, 75), (925, 75), (900, 575), (60, 500)]
    for x in range(len(aux_positions)):
        #aux_tank = Tank(enemy_chassis2, enemy_tank_turret2, [standard_shell], {}, aux_positions[x], 'ENEMY', master_sector)
        #aux_tanks.append(aux_tank)
        auxTank_dict = dict(enemyTank_dict)
        auxTank_dict['pos'] = aux_positions[x]
        aux_tank = master_sector.instantiate_unit(auxTank_dict)
        aux_tanks.append(aux_tank)

    aux_enemies = []
    for x in range(len(aux_tanks)):
        master_sector.instantiate_artificial(aux_tanks[x])
        aux_enemies.append(aux_tanks[x])

    #Obstacle variables
    obs_omni = []
    obs_positions = [((300, 250), 0)]
    for x in range(len(obs_positions)):
        obs_x_dict = {'unit_type': 'obstacle', 'obstacle': pine_obs, 'pos': obs_positions[x][0], 'degree_val': obs_positions[x][1]}
        obs_x = master_sector.instantiate_unit(obs_x_dict)
        obs_omni.append(obs_x)
    
    

    
    weapon_firing = {'primary': False, 'secondary': False, 'tertiary': False}
    weapon_reloading = False

    rounds_fired = 0

    draw_enemy_sight = False


    running = True
    while running:
        pygame.display.set_caption('{:.2f} {}-fired'.format(FPSCLOCK.get_fps(), rounds_fired))

        CURRENT_TIME = pygame.time.get_ticks()
        
        for event in pygame.event.get():
            if event.type == QUIT or (event.type == KEYUP and event.key == K_ESCAPE):
                pygame_quit()
            elif event.type == MOUSEMOTION:
                mouse['mouse_x'], mouse['mouse_y'] = event.pos
                master_sector.unit_objects[playerTank_id].update_target_via_mouse(mouse)
                artificial_enemy.tank.update_target_via_mouse(mouse)
                for x in range(len(aux_enemies)):
                    if aux_enemies[x] in master_sector.artificial_objects:
                        master_sector.artificial_objects[aux_enemies[x]].tank.update_target_via_mouse(mouse)
            elif event.type == MOUSEBUTTONDOWN:
                if event.button == 1:
                    weapon_firing['primary'] = True
                elif event.button == 2:
                    weapon_firing['tertiary'] = True
                    desired_pos = (mouse['mouse_x'], mouse['mouse_y'])
                    artificial_enemy.change_desired_pos(desired_pos)
                elif event.button == 3:
                    weapon_firing['secondary'] = True
                elif event.button == 4:
                    pass
                elif event.button == 5:
                    pass
            elif event.type == MOUSEBUTTONUP:
                if event.button == 1:
                    weapon_firing['primary'] = False
                elif event.button == 2:
                    weapon_firing['tertiary'] = False
                elif event.button == 3:
                    weapon_firing['secondary'] = False
                elif event.button == 4:
                    pass
                elif event.button == 5:
                    pass                
            elif event.type == KEYDOWN:
                if (event.key == K_LEFT or event.key == K_a):
                    chassis_direction['turn'] = 'counterclock'
                elif (event.key == K_RIGHT or event.key == K_d):
                    chassis_direction['turn'] = 'clockwise'
                elif (event.key == K_DOWN or event.key == K_s):
                    chassis_direction['move'] = 'reverse'
                elif (event.key == K_UP or event.key == K_w):
                    chassis_direction['move'] = 'forward'
                elif (event.key == K_SPACE):
                    weapon_reloading = True
                elif (event.key == K_p):
                    time_start_clock = pygame.time.get_ticks()
                    artificial_enemy.path_info = pathfinding_salvo_rework.main_loop(DISPSURF, artificial_enemy.tank.node_distance, obstacle_list, artificial_enemy.tank.rotated_chassis_rect.center, artificial_enemy.desired_pos)
                    artificial_enemy.path_stats = {'path_followed': False, 'path_gen': None, 'path_initiated': False}
                    time_stop_clock = pygame.time.get_ticks()
                    total_time = time_stop_clock - time_start_clock
                    print(total_time)
            elif event.type == KEYUP:
                if (event.key == K_LEFT or event.key == K_a):
                    if chassis_direction['turn'] == 'counterclock':
                        chassis_direction['turn'] = None
                elif (event.key == K_RIGHT or event.key == K_d):
                    if chassis_direction['turn'] == 'clockwise':
                        chassis_direction['turn'] = None
                elif (event.key == K_DOWN or event.key == K_s):
                    if chassis_direction['move'] == 'reverse':
                        chassis_direction['move'] = None
                elif (event.key == K_UP or event.key == K_w):
                    if chassis_direction['move'] == 'forward':
                        chassis_direction['move'] = None
                elif (event.key == K_SPACE):
                    weapon_reloading = False

        if weapon_reloading == True:
            check_weapon_reload(master_sector.unit_objects[playerTank_id])
            
        master_sector.unit_objects[playerTank_id].update_chassis_direction_via_keys(chassis_direction)
        master_sector.unit_objects[playerTank_id].update_firing_check(weapon_firing)
        master_sector.unit_objects[playerTank_id].weapons_firing_initiate()
                
                    
        DISPSURF.fill(BGCOLOR)

        if artificial_enemy.path_info['path'] != None:
            artificial_enemy.draw_path()
        
        master_sector.unit_objects[playerTank_id].generate_tank(DISPSURF)

        artificial_enemy.operations_management()
        artificial_enemy.tank.generate_tank(DISPSURF)

        for x in range(len(obs_omni)):
            master_sector.unit_objects[obs_omni[x]].generate_obs()
            for i in range(len(master_sector.unit_objects[obs_omni[x]].bounding_points)):
                pygame.draw.circle(DISPSURF, (0, 255, 255), master_sector.unit_objects[obs_omni[x]].bounding_points[i], 3, 0)
            pygame.draw.aaline(DISPSURF, (255, 0, 0), master_sector.unit_objects[obs_omni[x]].bounding_points[0], master_sector.unit_objects[obs_omni[x]].bounding_points[1], True)
            pygame.draw.aaline(DISPSURF, (255, 0, 0), master_sector.unit_objects[obs_omni[x]].bounding_points[0], master_sector.unit_objects[obs_omni[x]].bounding_points[2], True)
            pygame.draw.aaline(DISPSURF, (255, 0, 0), master_sector.unit_objects[obs_omni[x]].bounding_points[1], master_sector.unit_objects[obs_omni[x]].bounding_points[3], True)
            pygame.draw.aaline(DISPSURF, (255, 0, 0), master_sector.unit_objects[obs_omni[x]].bounding_points[2], master_sector.unit_objects[obs_omni[x]].bounding_points[3], True)


        #aux_enemies operations management
        for x in range(len(aux_enemies)):
            if aux_enemies[x] in master_sector.artificial_objects:
                master_sector.artificial_objects[aux_enemies[x]].operations_management()
                master_sector.artificial_objects[aux_enemies[x]].tank.generate_tank(DISPSURF)

        master_sector.generate_munitions()
        master_sector.generate_impacts()
        
        pygame.draw.circle(DISPSURF, (255, 0, 0), enemyTank.rotated_chassis_rect.center, 3, 0)
        if artificial_enemy.desired_pos != None:
            pygame.draw.aaline(DISPSURF, (255, 0, 0), enemyTank.rotated_chassis_rect.center, artificial_enemy.desired_pos, True)

        if artificial_enemy.desired_pos != None:
            pygame.draw.circle(DISPSURF, (255, 0, 255), artificial_enemy.desired_pos, 3, 0)


        for x in range(len(master_sector.sector_keys)):
            master_sector.sectors[master_sector.sector_keys[x]].draw_self(DISPSURF)



        #PLAYERTANK BOUNDING-BOX/IMAGE_RECT
##        pygame.draw.rect(DISPSURF, (0, 255, 0), playerTank.rotated_chassis_rect, 1)
##        for x in range(len(playerTank.bounding_points)):
##            pygame.draw.circle(DISPSURF, (255, 0 ,0), playerTank.bounding_points[x], 3, 0)
##
##        pygame.draw.aaline(DISPSURF, (255, 0, 0), playerTank.bounding_points[0], playerTank.bounding_points[1], True)
##        pygame.draw.aaline(DISPSURF, (255, 0, 0), playerTank.bounding_points[0], playerTank.bounding_points[2], True)
##        pygame.draw.aaline(DISPSURF, (255, 0, 0), playerTank.bounding_points[1], playerTank.bounding_points[3], True)
##        pygame.draw.aaline(DISPSURF, (255, 0, 0), playerTank.bounding_points[2], playerTank.bounding_points[3], True)


        #ENEMY_1 BOUNDING-BOX/IMAGE_RECT
##        pygame.draw.rect(DISPSURF, (0, 255, 0), artificial_enemy.tank.rotated_chassis_rect, 1)
##        for x in range(len(artificial_enemy.tank.bounding_points)):
##            pygame.draw.circle(DISPSURF, (255, 0, 0), artificial_enemy.tank.bounding_points[x], 3, 0)
##        pygame.draw.aaline(DISPSURF, (0, 255, 0), artificial_enemy.tank.bounding_points[0], artificial_enemy.tank.bounding_points[1], True)
##        pygame.draw.aaline(DISPSURF, (0, 255, 0), artificial_enemy.tank.bounding_points[0], artificial_enemy.tank.bounding_points[2], True)
##        pygame.draw.aaline(DISPSURF, (0, 255, 0), artificial_enemy.tank.bounding_points[1], artificial_enemy.tank.bounding_points[3], True)
##        pygame.draw.aaline(DISPSURF, (0, 255, 0), artificial_enemy.tank.bounding_points[2], artificial_enemy.tank.bounding_points[3], True)


##        #PLAYERTANK WEAPON BOUNDING-BOXES (STILL REQUIRES CENTER)
##        for x in range(len(playerTank.weapon_bounding_points)):
##            if len(playerTank.weapon_bounding_points[x]['bounding_points']) > 0:
##                for i in range(len(playerTank.weapon_bounding_points[x]['bounding_points'])):
##                    pygame.draw.circle(DISPSURF, (255, 0, 0), playerTank.weapon_bounding_points[x]['bounding_points'][i], 2, 0)
##                pygame.draw.aaline(DISPSURF, (255, 0, 0), playerTank.weapon_bounding_points[x]['bounding_points'][0], playerTank.weapon_bounding_points[x]['bounding_points'][1], True)
##                pygame.draw.aaline(DISPSURF, (255, 0, 0), playerTank.weapon_bounding_points[x]['bounding_points'][0], playerTank.weapon_bounding_points[x]['bounding_points'][2], True)
##                pygame.draw.aaline(DISPSURF, (255, 0, 0), playerTank.weapon_bounding_points[x]['bounding_points'][1], playerTank.weapon_bounding_points[x]['bounding_points'][3], True)
##                pygame.draw.aaline(DISPSURF, (255, 0, 0), playerTank.weapon_bounding_points[x]['bounding_points'][2], playerTank.weapon_bounding_points[x]['bounding_points'][3], True)
##                pygame.draw.circle(DISPSURF, (0, 255, 255), playerTank.weapon_bounding_points[x]['center'], 2, 0)

            

       #ENEMY_1 FOV

        pygame.draw.polygon(DISPSURF, (255, 0, 0), [artificial_enemy.tank.chassis_turret_pos, artificial_enemy.fov_deltoid['a']['pos'], artificial_enemy.fov_deltoid['c']['pos'], artificial_enemy.fov_deltoid['b']['pos'], artificial_enemy.tank.chassis_turret_pos], 1)
        pygame.draw.rect(DISPSURF, (0, 255, 255), artificial_enemy.fov_rect, 1)
        
        if artificial_enemy.fov_unit_stats != False:
            for x in range(len(artificial_enemy.fov_unit_keys)):
                fov_x = artificial_enemy.fov_unit_stats[artificial_enemy.fov_unit_keys[x]]
                if fov_x['center'][1] == True:
                    pygame.draw.circle(DISPSURF, (0, 255, 0), fov_x['center'][0], 3, 0)
                for i in range(len(fov_x['bounding_points'])):
                    if fov_x['bounding_points'][i][1] == True:
                        pygame.draw.circle(DISPSURF, (0, 255, 0), fov_x['bounding_points'][i][0], 3, 0)

            for x in range(len(aux_enemies)):
                if master_sector.artificial_objects[aux_enemies[x]].tank.unit_id in artificial_enemy.fov_unit_stats:
                    aux_x = master_sector.artificial_objects[aux_enemies[x]]
                    pygame.draw.aaline(DISPSURF, (0, 255, 0), artificial_enemy.fov_unit_stats[aux_x.tank.unit_id]['los_points']['counterclock'], artificial_enemy.fov_unit_stats[aux_x.tank.unit_id]['los_points']['clockwise'], True)


            if playerTank_id in artificial_enemy.currently_sighted['keys']:
                red = (255, 0, 0)
                cyan = (0, 255, 255)
                for x in range(len(['c', 'a', 'b'])):
                    chosen_pos = ['c', 'a', 'b'][x]
                    if artificial_enemy.currently_sighted['units'][playerTank_id][chosen_pos][2] == True:
                        line_color = cyan
                    else:
                        line_color = red
                    pygame.draw.circle(DISPSURF, line_color, artificial_enemy.currently_sighted['units'][playerTank_id][chosen_pos][0], 3, 0)
                    pygame.draw.aaline(DISPSURF, line_color, artificial_enemy.currently_sighted['units'][playerTank_id][chosen_pos][0], artificial_enemy.fov_deltoid['origin']['pos'], True)

##
##        
##        #AUX_ENEMIES FOV
##        aux_enemies_ids = [aux_enemies[x].tank.unit_id for x in range(len(aux_enemies))]
##        for x in range(len(aux_enemies)):
##            pygame.draw.polygon(DISPSURF, (255, 0, 0), [aux_enemies[x].tank.chassis_turret_pos, aux_enemies[x].fov_deltoid['a']['pos'], aux_enemies[x].fov_deltoid['c']['pos'], aux_enemies[x].fov_deltoid['b']['pos'], aux_enemies[x].tank.chassis_turret_pos], 1)
##            pygame.draw.rect(DISPSURF, (0, 255, 255), aux_enemies[x].fov_rect, 1)
##                    
##            if aux_enemies[x].fov_unit_stats != False:
##                for i in range(len(aux_enemies[x].fov_unit_keys)):
##                    fov_i = aux_enemies[x].fov_unit_stats[aux_enemies[x].fov_unit_keys[i]]
##                    if fov_i['center'][1] == True:
##                        pygame.draw.circle(DISPSURF, (0, 255, 0), fov_i['center'][0], 3, 0)
##                    for y in range(len(fov_i['bounding_points'])):
##                        if fov_i['bounding_points'][y][1] == True:
##                            pygame.draw.circle(DISPSURF, (0, 255, 0), fov_i['bounding_points'][y][0], 3, 0)
##
##
##            if enemyTank.unit_id in aux_enemies[x].fov_unit_stats:
##                pygame.draw.aaline(DISPSURF, (0, 255, 0), aux_enemies[x].fov_unit_stats[enemyTank.unit_id]['los_points']['counterclock'], aux_enemies[x].fov_unit_stats[enemyTank.unit_id]['los_points']['clockwise'], True)
##            for i in range(len(aux_enemies_ids)):
##                if aux_enemies_ids[x] in aux_enemies[x].fov_unit_stats:
##                    pygame.draw.aaline(DISPSURF, (0, 255, 0), aux_enemies[x].fov_unit_stats[aux_enemies_ids[x]]['los_points']['counterclock'], aux_enemies[x].fov_unit_stats[aux_enemies_ids[x]]['los_points']['clockwise'], True)
##
##            if playerTank.unit_id in aux_enemies[x].currently_sighted['keys']:
##                red = (255, 0, 0)
##                cyan = (0, 255, 255)
##                for i in range(len(['c', 'a', 'b'])):
##                    chosen_pos = ['c', 'a', 'b'][i]
##                    if aux_enemies[x].currently_sighted['units'][playerTank.unit_id][chosen_pos][2] == True:
##                        line_color = cyan
##                    else:
##                        line_color = red
##                    pygame.draw.circle(DISPSURF, line_color, aux_enemies[x].currently_sighted['units'][playerTank.unit_id][chosen_pos][0], 3, 0)
##                    pygame.draw.aaline(DISPSURF, line_color, aux_enemies[x].currently_sighted['units'][playerTank.unit_id][chosen_pos][0], aux_enemies[x].fov_deltoid['origin']['pos'], True)

       


#######################TANK CHASSIS COLLISION CORRECTION
####
        tank_degree_pos = pos_from_degrees(master_sector.unit_objects[playerTank_id].rotated_chassis_rect.center, master_sector.unit_objects[playerTank_id].chassis_degree_val, 50)
        pygame.draw.aaline(DISPSURF, (255, 255, 255), master_sector.unit_objects[playerTank_id].rotated_chassis_rect.center, tank_degree_pos, True)

            
        closest_points = []
        point_distances = []
        point_info = []
        for x in range(len(master_sector.units[master_sector.unit_objects[playerTank_id].unit_id]['bounding_points'])):
            point_x = master_sector.units[master_sector.unit_objects[playerTank_id].unit_id]['bounding_points'][x]
            point_dist = distance_between_positions(artificial_enemy.tank.rotated_chassis_rect.center, master_sector.units[master_sector.unit_objects[playerTank_id].unit_id]['bounding_points'][x])
            point_distances.append(point_dist)
            point_info.append((x, point_dist, point_x))
        closest_point = min(point_distances)
        closest_point = [(point_info[i][2], point_info[i][0]) for i in range(len(point_info)) if point_info[i][1] == closest_point][0]
        closest_points.append(closest_point)
        for x in range(len(closest_points)):
            pygame.draw.circle(DISPSURF, (255, 0, 0), closest_points[x][0], 3, 0)
            connections_indexes = master_sector.units[playerTank_id]['bounding_connections'][closest_points[x][1]]
            connections_indexes = [connections_indexes['clockwise_index'], connections_indexes['counterclock_index']]
            connections_points = [master_sector.units[playerTank_id]['bounding_points'][connections_indexes[i]] for i in range(len(connections_indexes))]
            for i in range(len(connections_points)):
                pygame.draw.circle(DISPSURF, (0, 255, 0), connections_points[i], 3, 0)
                pygame.draw.aaline(DISPSURF, (0, 0, 255), connections_points[i], closest_points[x][0], True)

        closest_point = artificial_enemy.tank.bounding_points[0]
        point_dist_lowest = 100000
        for x in range(len(artificial_enemy.tank.bounding_points)):
            point_dist = distance_between_positions(artificial_enemy.tank.bounding_points[x], master_sector.unit_objects[playerTank_id].rotated_chassis_rect.center)
            if point_dist < point_dist_lowest:
                closest_point = artificial_enemy.tank.bounding_points[x]
                point_dist_lowest = point_dist
                connection_indexes = master_sector.units[artificial_enemy.tank.unit_id]['bounding_connections'][x]
                connection_indexes = [connection_indexes['clockwise_index'], connection_indexes['counterclock_index']]
        pygame.draw.circle(DISPSURF, (255, 100, 50), closest_point, 3, 0)
        for x in range(len(connection_indexes)):
            pygame.draw.aaline(DISPSURF, (0, 255, 0), closest_point, master_sector.units[artificial_enemy.tank.unit_id]['bounding_points'][connection_indexes[x]], True)

####
####
##
##        player_chassis_deg = copy.deepcopy(playerTank.chassis_degree_val)
##        player_rect = copy.deepcopy(playerTank.rotated_chassis_rect)
##        player_chassis_bounding = copy.deepcopy(master_sector.units[playerTank.unit_id]['bounding_points'])
##        player_chassis_connections = copy.deepcopy(master_sector.units[playerTank.unit_id]['bounding_connections'])
##
##        playerTank.chassis_degree_val = playerTank.degree_val
##        playerTank.rotated_chassis_rect.center = playerTank.chassis_turret_pos
##
##            
##        degree_rotation_change = 0.0
##        degrees_to_change = 0.0
##        enemy_center_degree = angle_between_points(artificial_enemy.tank.rotated_chassis_rect.center, playerTank.rotated_chassis_rect.center)
##        directional_rotate = get_closest_degree_direction(playerTank.chassis_degree_val, enemy_center_degree)[0]
##        enemy_center_direction = directional_rotate
##        if directional_rotate == 'clockwise':
##            directional_rotate = 'counterclock'
##        else:
##            directional_rotate = 'clockwise'
##
##        
##
##            
##        #for x in range(len(master_sector.units[playerTank.unit_id]['bounding_points'])):
##
##                
##        for x in range(len(master_sector.turrets[playerTank.unit_id]['weapon_bounding_points'])):
##            master_sector.units[playerTank.unit_id]['bounding_points'] = master_sector.turrets[playerTank.unit_id]['weapon_bounding_points'][x]['bounding_points']
##            master_sector.units[playerTank.unit_id]['bounding_connections'] = master_sector.turrets[playerTank.unit_id]['weapon_bounding_connections'][x]
##            bounding_x = master_sector.units[playerTank.unit_id]['bounding_points']
##            bounding_connections = master_sector.units[playerTank.unit_id]['bounding_connections']
##            bounding_collision_a, bounding_collision_b = master_sector.check_bounding_box_collision((bounding_x, bounding_connections), (master_sector.units[artificial_enemy.tank.unit_id]['bounding_points'], master_sector.units[artificial_enemy.tank.unit_id]['bounding_connections']), center_a=playerTank.rotated_chassis_rect.center)
##
##            polar_degree_val = polarize_degree(playerTank.chassis_degree_val)
##            collision_reassignment = (False, None, None)
##
##            weapon_rect = master_sector.create_rect_from_points(bounding_x)
##
##
##            #-------------------CLASS-A COLLISION
##
##            alternate_degrees_on = False
##
##
##
##
##            if bounding_collision_a != False:
##
##                #Testing MasterSector integration for class-A collision correction
##                unit_dict = master_sector.get_unit_stats(playerTank.unit_id)
##                obs_dict = master_sector.get_unit_stats(artificial_enemy.tank.unit_id)
##
##                #degree_adjustment_class_a_alt, collision_reassignment_alt = master_sector.bounding_collision_a(unit_dict, obs_dict, bounding_collision_a)
##    
##                degree_adjustment = 0.0
##
##                
##                pygame.draw.circle(DISPSURF, (255, 0, 255), bounding_collision_a[0], 3, 0)
##                pygame.draw.circle(DISPSURF, (0, 255, 255), bounding_collision_a[1], 3, 0)
##
##                #CIRCLE INDICATING CLASS-A
##                pygame.draw.circle(DISPSURF, (255, 0, 0), (10, 10), 5, 0)
##
##                for i in range(len(bounding_x)):
##                    if bounding_collision_a[0] == bounding_x[i]:
##                        bounding_index = i
##                        break
##
##
##                counter_conn_degrees = get_degree_diff(angle_between_points(bounding_x[bounding_connections[bounding_index]['counterclock_index']], bounding_collision_a[0]), angle_between_points(bounding_collision_a[1], bounding_collision_a[0]))
##                clock_conn_degrees = get_degree_diff(angle_between_points(bounding_x[bounding_connections[bounding_index]['clockwise_index']], bounding_collision_a[0]), angle_between_points(bounding_collision_a[1], bounding_collision_a[0]))
##
##                counter_conn_dist = distance_between_positions(bounding_x[bounding_connections[bounding_index]['counterclock_index']], bounding_collision_a[1])
##                clock_conn_dist = distance_between_positions(bounding_x[bounding_connections[bounding_index]['clockwise_index']], bounding_collision_a[1])
##                bounding_point_dist = distance_between_positions(bounding_collision_a[0], bounding_collision_a[1])
##
##                counter_dist_viable = True
##                clock_dist_viable = True
##                if counter_conn_dist < 10 and bounding_point_dist < 10:
##                    counter_dist_viable = False
##                if clock_conn_dist < 10 and bounding_point_dist < 10:
##                    clock_dist_viable = False
##
##                if abs(counter_conn_degrees) < abs(clock_conn_degrees) and counter_dist_viable == True or clock_dist_viable == False:
##                    chosen_index = 'counterclock_index'
##                else:
##                    chosen_index = 'clockwise_index'
##
##                    
##                tank_center_to_bounding = angle_between_points(bounding_collision_a[0], playerTank.rotated_chassis_rect.center)
##                tank_center_to_conn = angle_between_points(bounding_x[bounding_connections[bounding_index][chosen_index]], playerTank.rotated_chassis_rect.center)
##                diff_tank_deg_bounding = get_degree_diff(playerTank.chassis_degree_val, tank_center_to_bounding)
##                diff_tank_pol_bounding = get_degree_diff(polar_degree_val, tank_center_to_bounding)
##                if abs(diff_tank_deg_bounding) < abs(diff_tank_pol_bounding):
##                    chosen_degree_line = playerTank.chassis_degree_val
##                else:
##                    chosen_degree_line = polar_degree_val
##                tank_center_to_obs_bound = angle_between_points(bounding_collision_a[1], playerTank.rotated_chassis_rect.center)
##                
##                tank_bounding_deg_dir = get_closest_degree_direction(tank_center_to_obs_bound, tank_center_to_bounding)[0]
##                tank_conn_deg_dir = [['clockwise', 'counterclock'][i] for i in range(len(['clockwise', 'counterclock'])) if ['clockwise', 'counterclock'][i] != tank_bounding_deg_dir][0]
##                tank_bounding_deg_stats = (tank_bounding_deg_dir, tank_center_to_bounding)
##                tank_conn_deg_stats = (tank_conn_deg_dir, tank_center_to_conn)
##                tank_bounding_conn_deg_stats = [tank_bounding_deg_stats, tank_conn_deg_stats]
##                tank_deg_stats_omni = {tank_bounding_conn_deg_stats[i][0]: tank_bounding_conn_deg_stats[i][1] for i in range(len(tank_bounding_conn_deg_stats))}
##
##                if tank_deg_stats_omni['clockwise'] == tank_center_to_bounding:
##                    bounding_chosen_color = (255, 0, 0)
##                    conn_chosen_color = (0, 255, 255)
##                    bounding_deg_range_dir = 'clockwise'
##                else:
##                    bounding_chosen_color = (0, 255, 255)
##                    conn_chosen_color = (255, 0, 0)
##                    bounding_deg_range_dir = 'counterclock'
##                degrees_in_range = is_degree_in_degree_range(tank_deg_stats_omni['clockwise'], tank_deg_stats_omni['counterclock'], chosen_degree_line)
##
##                #ATTEMPTING TO RECALIBRATE HEAD-ON CLASS-A COLLISIONS BY CHECKING BOTH CONNECTION-POINTS FOR DEGREE-FIELD OVERLAP
##                for i in range(len(master_sector.units[artificial_enemy.tank.unit_id]['bounding_points'])):
##                    if master_sector.units[artificial_enemy.tank.unit_id]['bounding_points'][i] == bounding_collision_a[1]:
##                        enemy_index = i
##                        break
##                obs_bounding_points = master_sector.units[artificial_enemy.tank.unit_id]['bounding_points']
##                obs_bounding_connections = master_sector.units[artificial_enemy.tank.unit_id]['bounding_connections'][enemy_index]
##                obs_bounding_connections = [obs_bounding_connections['clockwise_index'], obs_bounding_connections['counterclock_index']]
##                obs_bounding_connections = [obs_bounding_points[obs_bounding_connections[0]], obs_bounding_points[obs_bounding_connections[1]]]
##
##
##                if degrees_in_range == True:
##                    chassis_center_obs_center = angle_between_points(artificial_enemy.tank.rotated_chassis_rect.center, playerTank.rotated_chassis_rect.center)
##                    obs_center_in_range = is_degree_in_degree_range(tank_deg_stats_omni['clockwise'], tank_deg_stats_omni['counterclock'], chassis_center_obs_center)
##
##                    obs_conn_a_deg = angle_between_points(obs_bounding_connections[0], playerTank.rotated_chassis_rect.center)
##                    obs_conn_a_in_range = is_degree_in_degree_range(tank_deg_stats_omni['clockwise'], tank_deg_stats_omni['counterclock'], obs_conn_a_deg)
##                    obs_conn_b_deg = angle_between_points(obs_bounding_connections[1], playerTank.rotated_chassis_rect.center)
##                    obs_conn_b_in_range = is_degree_in_degree_range(tank_deg_stats_omni['clockwise'], tank_deg_stats_omni['counterclock'], obs_conn_b_deg)
##
##                    coll_bound_prox = get_degree_diff(tank_center_to_bounding, tank_center_to_obs_bound)
##                    coll_conn_prox = get_degree_diff(tank_center_to_conn, tank_center_to_obs_bound)
##
##                    if abs(coll_bound_prox) < 5 or abs(coll_conn_prox) < 5:
##                        proximity_alert = True
##                    else:
##                        proximity_alert = False
##
##                    if obs_center_in_range == False or proximity_alert == True:
##                        degrees_in_range = False
##                    else:
##                        pygame.draw.circle(DISPSURF, (255, 0, 0), playerTank.rotated_chassis_rect.center, 8, 0)
##                        pygame.draw.aaline(DISPSURF, bounding_chosen_color, playerTank.rotated_chassis_rect.center, bounding_x[bounding_connections[bounding_index][chosen_index]], True)
##                        pygame.draw.aaline(DISPSURF, conn_chosen_color, playerTank.rotated_chassis_rect.center, bounding_collision_a[0], True)
##
##                    
##
##                
##
##
##
##                if degrees_in_range == False:
##                    diff_tank_deg_conn = get_degree_diff(playerTank.chassis_degree_val, tank_center_to_conn)
##                    conn_point = bounding_x[bounding_connections[bounding_index][chosen_index]]
##                    selected_point_change = False
##
##                    dist_to_bounding = distance_between_positions(bounding_collision_a[0], bounding_collision_a[1])
##                    dist_to_conn = distance_between_positions(conn_point, bounding_collision_a[1])
##
##
##                    if dist_to_bounding < dist_to_conn:
##                        conn_adjust = get_degree_diff(angle_between_points(bounding_collision_a[0], conn_point), angle_between_points(bounding_collision_a[1], conn_point))
##                        degree_adjustment = abs(conn_adjust)
##                    else:
##                        conn_adjust = get_degree_diff(angle_between_points(conn_point, bounding_collision_a[0]), angle_between_points(bounding_collision_a[1], bounding_collision_a[0]))
##                        degree_adjustment = abs(conn_adjust)               
##
##                    bounding_dir = get_closest_degree_direction(angle_between_points(conn_point, bounding_collision_a[0]), angle_between_points(bounding_collision_a[1], bounding_collision_a[0]))[0]
##                    if dist_to_bounding < dist_to_conn:
##                        if bounding_dir == 'clockwise':
##                            bounding_dir = 'counterclock'
##                        else:
##                            bounding_dir = 'clockwise'
##
##
##                    if bounding_dir == 'counterclock':
##                        degree_adjustment = degree_adjustment * -1
##                        
##
##                    pygame.draw.circle(DISPSURF, (0, 0, 0), conn_point, 4, 0)
##
##                    new_point = pos_from_degrees(playerTank.rotated_chassis_rect.center, playerTank.chassis_degree_val + degree_adjustment, 100)
##                    pygame.draw.aaline(DISPSURF, (255, 0, 0), playerTank.rotated_chassis_rect.center, new_point, True)
##
##                    if abs(degree_adjustment) > abs(degree_rotation_change) or degree_rotation_change == 0.0:
##                        degree_rotation_change = degree_adjustment
##
##                        degree_adjustment_class_a_act = degree_adjustment
##
##                else:
##                    if bounding_collision_b != False:
##                    
##                        pygame.draw.circle(DISPSURF, (0, 0, 0), playerTank.rotated_chassis_rect.center, 5, 0)
##                    #else:
##                    bounding_collision_b = (bounding_collision_a[1], bounding_collision_a[0])
##                    collision_reassignment = (True, bounding_x[bounding_connections[bounding_index][chosen_index]], chosen_degree_line)
##                    degree_adjustment_class_a_act = 0.0
##                #print('old_adj:{}, new_adj:{}, old_reas:{}, new_reas:{}'.format(degree_adjustment, degree_adjustment_alt, collision_reassignment, collision_reassignment_alt))
##
##
##
##
#################################################################################
#################################################################################
#################################################################################
#################################################################################
##            #-----------------CLASS-B COLLISION
##
##            if bounding_collision_b != False:
##
##                unit_dict = master_sector.get_unit_stats(playerTank.unit_id)
##                obs_dict = master_sector.get_unit_stats(artificial_enemy.tank.unit_id)
##
##                #degree_rotation_change_alt = master_sector.bounding_collision_b(unit_dict, obs_dict, bounding_collision_b, collision_reassignment)#degree_rotation_change_alt, trig_omni_dict = master_sector.bounding_collision_b(unit_dict, obs_dict, bounding_collision_b, collision_reassignment)
##
##
##                #CIRCLE INDICATING CLASS-B
##                pygame.draw.circle(DISPSURF, (0, 255, 255), (20, 10), 5, 0)
##                
##        
##                #The bounding_collision_b workaround is not yet successful at collision correction in all-encompassing manner.
##                #Currently, it will inappropriately reassign the bounding_collision_b[0] (obs_bounding_point), if for example
##                #the player-tank is slightly North of the obstacle-tank, with the centre to the West by a small margin and the
##                #selected obstacle_bounding_point being the North-West (top_left) point, with the player-tank rotation clockwise,
##                #it will inappropriately reassign the obstacle-point to be the connecting-point, when leaving the selected-point as it
##                #was would have remedied the collision. The deterministic-criteria for reassignment are not yet completely reliable and
##                #must be redesigned to resolve this issue.
##                pygame.draw.circle(DISPSURF, (255, 0, 255), bounding_collision_b[0], 3, 0)
##                pygame.draw.circle(DISPSURF, (0, 255, 255), bounding_collision_b[1], 3, 0)
##
##                for x in range(len(master_sector.units[artificial_enemy.tank.unit_id]['bounding_points'])):
##                    if master_sector.units[artificial_enemy.tank.unit_id]['bounding_points'][x] == bounding_collision_b[0]:
##                        enemy_index = x
##                        break
##                for x in range(len(bounding_x)):
##                    if bounding_x[x] == bounding_collision_b[1]:
##                        bounding_index = x
##                        break
##
##                enemy_bounding_points = master_sector.units[artificial_enemy.tank.unit_id]['bounding_points']
##                enemy_bounding_connections = master_sector.units[artificial_enemy.tank.unit_id]['bounding_connections'][enemy_index]
##                bounding_connections = [enemy_bounding_connections['clockwise_index'], enemy_bounding_connections['counterclock_index']]
##                bounding_connections = [enemy_bounding_points[bounding_connections[0]], enemy_bounding_points[bounding_connections[1]]]
##                pygame.draw.circle(DISPSURF, (255, 0, 255), bounding_collision_b[1], 3, 0)
##                pygame.draw.circle(DISPSURF, (0, 255, 0), bounding_collision_b[0], 3, 0)
##                for x in range(len(bounding_connections)):
##                    pygame.draw.circle(DISPSURF, (0, 0, 0), bounding_connections[x], 3, 0)
##                    pygame.draw.aaline(DISPSURF, (0, 0, 0), bounding_connections[x], bounding_collision_b[0], True)
##                connection_a_degree = angle_between_points(bounding_connections[0], bounding_collision_b[0])
##                connection_b_degree = angle_between_points(bounding_connections[1], bounding_collision_b[0])
##                colliding_point_degree = angle_between_points(bounding_collision_b[1], bounding_collision_b[0])
##
##                tank_bounding_connections = master_sector.units[playerTank.unit_id]['bounding_connections'][bounding_index]
##                tank_bounding_connections = [tank_bounding_connections['clockwise_index'], tank_bounding_connections['counterclock_index']]
##                tank_bounding_connections = [bounding_x[tank_bounding_connections[0]], bounding_x[tank_bounding_connections[1]]]
##
##                tank_center_bounding = angle_between_points(bounding_collision_b[1], playerTank.rotated_chassis_rect.center)
##                bounding_to_degree_val = get_degree_diff(playerTank.chassis_degree_val, tank_center_bounding)
##                bounding_to_polar_val = get_degree_diff(polar_degree_val, tank_center_bounding)
##
##                if abs(bounding_to_degree_val) < abs(bounding_to_polar_val):
##                    bounding_rotation_dir = get_closest_degree_direction(tank_center_bounding, playerTank.chassis_degree_val)[0]
##                    degree_dir_selected = 'degree'
##                    selected_deg_val = playerTank.chassis_degree_val
##                else:
##                    bounding_rotation_dir = get_closest_degree_direction(tank_center_bounding, polar_degree_val)[0]
##                    degree_dir_selected = 'polar'
##                    selected_deg_val = polar_degree_val
##
##                tank_chassis_center_conn_a = angle_between_points(tank_bounding_connections[0], playerTank.rotated_chassis_rect.center)
##                tank_chassis_center_conn_b = angle_between_points(tank_bounding_connections[1], playerTank.rotated_chassis_rect.center)
##
##                sel_deg_tank_conn_a_diff = get_degree_diff(selected_deg_val, tank_chassis_center_conn_a)
##                sel_deg_tank_conn_b_diff = get_degree_diff(selected_deg_val, tank_chassis_center_conn_b)
##                if abs(sel_deg_tank_conn_a_diff) < abs(sel_deg_tank_conn_b_diff):
##                    tank_chassis_selected_conn = tank_bounding_connections[0]
##                else:
##                    tank_chassis_selected_conn = tank_bounding_connections[1]
##
##                sel_conn_in_obs_bound_deg_field = is_degree_in_degree_range(connection_a_degree, connection_b_degree, angle_between_points(tank_chassis_selected_conn, bounding_collision_b[0]))
##                if sel_conn_in_obs_bound_deg_field == True:
##                    collision_reassignment = (True, tank_chassis_selected_conn, selected_deg_val)
##                    pygame.draw.circle(DISPSURF, (0, 0, 0), playerTank.rotated_chassis_rect.center, 200, 1)
##                    
##                #if collision_reassignment[0] == False:
##                        ####TEST CODE####
##                obs_bounding_chassis_center = angle_between_points(playerTank.rotated_chassis_rect.center, bounding_collision_b[0])
##                connection_a_degree_difference = get_degree_diff(obs_bounding_chassis_center, connection_a_degree)
##                connection_b_degree_difference = get_degree_diff(obs_bounding_chassis_center, connection_b_degree)
##                connection_differences = [abs(connection_a_degree_difference), abs(connection_b_degree_difference)]
##                lowest_degree_difference = min(connection_differences)
##                if min(connection_differences) == abs(connection_a_degree_difference):
##                    selected_connection_point = bounding_connections[0]
##                else:
##                    selected_connection_point = bounding_connections[1]
##                true_lowest_deg_diff = lowest_degree_difference
##                if true_lowest_deg_diff == abs(connection_a_degree_difference):
##                    true_selected_conn = bounding_connections[0]
##                else:
##                    true_selected_conn = bounding_connections[1]
##
##                bounding_dist_to_conn_a = distance_between_positions(bounding_collision_b[0], bounding_connections[0])
##                bounding_dist_to_conn_b = distance_between_positions(bounding_collision_b[0], bounding_connections[1])
##
#######TEST CODE SAMPLE
##                obs_bound_coll_chassis_dir = get_closest_degree_direction(colliding_point_degree, obs_bounding_chassis_center)[0]
##                obs_bound_coll_conn_a_dir = get_closest_degree_direction(colliding_point_degree, connection_a_degree)[0]
##                obs_bound_coll_conn_b_dir = get_closest_degree_direction(colliding_point_degree, connection_b_degree)[0]
##
####                bounding_obs_center = angle_between_points(artificial_enemy.tank.rotated_chassis_rect.center, bounding_collision_b[0])
####
####                obs_center_obs_bounding = angle_between_points(bounding_collision_b[0], artificial_enemy.tank.rotated_chassis_rect.center)
####                obs_center_colliding = angle_between_points(bounding_collision_b[1], artificial_enemy.tank.rotated_chassis_rect.center)
####
####                obs_center_bounding_colliding_diff = abs(get_degree_diff(obs_center_obs_bounding, obs_center_colliding))
####
####                if obs_center_bounding_colliding_diff < 5:
####
####                    degree_val_point = pos_from_degrees(playerTank.rotated_chassis_rect.center, selected_deg_val, distance_between_positions(playerTank.rotated_chassis_rect.center, bounding_collision_b[1]))
####                    obs_center_degree_point = angle_between_points(degree_val_point, artificial_enemy.tank.rotated_chassis_rect.center)
####
####                    obs_bounding_obs_center_polar = polarize_degree(bounding_obs_center)
####                    obs_center_conn_a = angle_between_points(bounding_connections[0], artificial_enemy.tank.rotated_chassis_rect.center)
####                    obs_center_conn_b = angle_between_points(bounding_connections[1], artificial_enemy.tank.rotated_chassis_rect.center)
####                    obs_center_conn_a_dir = get_closest_degree_direction(obs_center_obs_bounding, obs_center_conn_a)[0]
####                    obs_center_conn_b_dir = get_closest_degree_direction(obs_center_obs_bounding, obs_center_conn_b)[0]
####                    obs_center_degree_point_dir = get_closest_degree_direction(obs_center_obs_bounding, obs_center_degree_point)[0]
####
####                    obs_bounding_conn_a_dir = get_closest_degree_direction(bounding_obs_center, connection_a_degree)[0]
####                    obs_bounding_conn_b_dir = get_closest_degree_direction(bounding_obs_center, connection_b_degree)[0]
####
####                    #conn_a_diff = get_degree_diff(colliding_point_degree, connection_a_degree)
####                    #conn_b_diff = get_degree_diff(colliding_point_degree, connection_b_degree)
####
####                    temp_bounding_deg_change = 10
####
####                    if bounding_rotation_dir == 'clockwise':
####                        new_bounding_deg = tank_center_bounding + temp_bounding_deg_change
####                    else:
####                        new_bounding_deg = tank_center_bounding - temp_bounding_deg_change
####                    
####                    tank_center_coll_dist = distance_between_positions(playerTank.rotated_chassis_rect.center, bounding_collision_b[1])
####                    new_coll_temp = pos_from_degrees(playerTank.rotated_chassis_rect.center, new_bounding_deg, tank_center_coll_dist)
####                    new_coll_temp = (int(new_coll_temp[0]), int(new_coll_temp[1]))
####                    pygame.draw.circle(DISPSURF, (0, 0, 0), new_coll_temp, 3, 0)
####
####
####
####                    obs_bounding_new_coll_deg = angle_between_points(new_coll_temp, bounding_collision_b[0])
####                    conn_a_diff = get_degree_diff(connection_a_degree, obs_bounding_new_coll_deg)
####                    conn_b_diff = get_degree_diff(connection_b_degree, obs_bounding_new_coll_deg)
####                    conn_a_diff_inverse = get_degree_diff(obs_bounding_new_coll_deg, connection_a_degree)
####                    conn_b_diff_inverse = get_degree_diff(obs_bounding_new_coll_deg, connection_b_degree)
####
####                    if obs_center_conn_a_dir == 'counterclock':
####                        conn_a_dir_temp_var = 'counterclock'
####                        coll_point_conn_a_field = is_degree_in_degree_range(obs_bonding_obs_center_polar, bounding_obs_center, obs_bounding_new_coll_deg)
####                    else:
####                        conn_a_dir_temp_var = 'clockwise'
####                        coll_point_conn_a_field = is_degree_in_degree_range(bounding_obs_center, obs_bounding_obs_center_polar, obs_bounding_new_coll_deg)
####                    if obs_center_conn_b_dir == 'counterclock':
####                        conn_b_dir_temp_var = 'counterclock'
####                        coll_point_conn_b_field = is_degree_in_degree_range(obs_bounding_obs_center_polar, bounding_obs_center, obs_bounding_new_coll_deg)
####                    else:
####                        conn_b_dir_temp_var = 'clockwise'
####                        coll_point_conn_b_field = is_degree_in_degree_range(bounding_obs_center, obs_bounding_obs_center_polar, obs_bounding_new_coll_deg)
####
####                    #print('a_field:{}, b_field:{}, a_dir:{}, b_dir:{}'.format(coll_point_conn_a_field, coll_point_conn_b_field, conn_a_dir_temp_var, conn_b_dir_temp_var))
####                    
####
####                    
####
####                    
####
####                    #if obs_center_degree_point_dir == obs_center_conn_a_dir:
####                    #if abs(conn_a_diff) < abs(conn_b_diff):
####                    if coll_point_conn_a_field == True:
####                        pygame.draw.circle(DISPSURF, (0, 0, 0), bounding_connections[0], 20, 1)
####                        #selected_connection_point = bounding_connections[0]#TEMPTEST10/14/19
####                    elif coll_point_conn_b_field == True:
####                        pygame.draw.circle(DISPSURF, (0, 0, 0), bounding_connections[1], 20, 1)
####                        #selected_connection_point = bounding_connections[1]#TEMPTEST10/14/19
####                    #lowest_degree_difference = true_lowest_deg_diff
##
##                    
##                    #print('conn_a:{}, conn_b:{}, deg_point:{}'.format(obs_center_conn_a_dir, obs_center_conn_b_dir, obs_center_degree_point_dir))
##
##                if obs_bound_coll_conn_a_dir == obs_bound_coll_conn_b_dir:
##                    obs_bound_obs_center = angle_between_points(artificial_enemy.tank.rotated_chassis_rect.center, bounding_collision_b[0])
##                    obs_bound_center_conn_a_dir = get_closest_degree_direction(obs_bound_obs_center, connection_a_degree)
##                    obs_bound_center_conn_b_dir = get_closest_degree_direction(obs_bound_obs_center, connection_b_degree)
##                    obs_bound_center_coll_dir = get_closest_degree_direction(obs_bound_obs_center, colliding_point_degree)
##
##                    if obs_bound_center_conn_a_dir == obs_bound_center_coll_dir:
##                        selected_connection_point = bounding_connections[0]
##                        #print('CONN A DIR SELECTION')
##                    elif obs_bound_center_conn_b_dir == obs_bound_center_coll_dir:
##                        selected_connection_point = bounding_connections[1]
##                        #print('CONN B DIR SELECTED')
##                    if obs_bound_center_conn_a_dir == obs_bound_center_conn_b_dir:
##                        pygame.draw.circle(DISPSURF, (0, 0, 0), playerTank.rotated_chassis_rect.center, 250, 0)
##                        #print('CONNECTION OVERLAP')
##                elif obs_bound_coll_chassis_dir == obs_bound_coll_conn_a_dir:
##                    pygame.draw.circle(DISPSURF, (0, 255, 255), bounding_connections[0], 15, 1)
##                    selected_connection_point = bounding_connections[0]
##                    #lowest_degree_difference = abs(connection_a_degree_difference)
##                elif obs_bound_coll_chassis_dir == obs_bound_coll_conn_b_dir:
##                    pygame.draw.circle(DISPSURF, (0, 255, 0), bounding_connections[1], 15, 1)
##                    selected_connection_point = bounding_connections[1]
##
##
##
#######END TEST CODE SAMPLE
##
##                pygame.draw.circle(DISPSURF, (255, 0, 255), bounding_collision_b[1], 10, 1)
##
##                if selected_connection_point == bounding_connections[0]:
##                    connection_degree = connection_a_degree
##                    connection_point = bounding_connections[0]
##                    connection_dist = bounding_dist_to_conn_a
##                    connection_point_to_chassis_center_dist = distance_between_positions(playerTank.rotated_chassis_rect.center, bounding_connections[0])
##                        
##                else:
##                    connection_degree = connection_b_degree
##                    connection_point = bounding_connections[1]
##                    connection_dist = bounding_dist_to_conn_b
##                    connection_point_to_chassis_center_dist = distance_between_positions(playerTank.rotated_chassis_rect.center, bounding_connections[1])
##
##                if collision_reassignment[0] == True:
##                    obs_bounding_to_obs_center = angle_between_points(artificial_enemy.tank.rotated_chassis_rect.center, bounding_collision_b[0])
##                    connection_dir = get_closest_degree_direction(obs_bounding_to_obs_center, connection_degree)[0]
##                    chassis_bounding_dir = get_closest_degree_direction(obs_bounding_to_obs_center, colliding_point_degree)[0]
##                    chassis_conn_dir = get_closest_degree_direction(obs_bounding_to_obs_center, angle_between_points(collision_reassignment[1], bounding_collision_b[0]))[0]
##
##                    pygame.draw.circle(DISPSURF, (0, 255, 255), bounding_collision_b[1], 20, 1)
##
##
##
##                    chassis_center_conn_a = angle_between_points(bounding_connections[0], playerTank.rotated_chassis_rect.center)
##                    chassis_center_conn_b = angle_between_points(bounding_connections[1], playerTank.rotated_chassis_rect.center)
##                    chassis_center_obs_bound = angle_between_points(bounding_collision_b[0], playerTank.rotated_chassis_rect.center)
##                    obs_bound_obs_center = angle_between_points(artificial_enemy.tank.rotated_chassis_rect.center, bounding_collision_b[0])
##                    obs_bound_polar_center = polarize_degree(obs_bound_obs_center)
##                    obs_bound_chassis_center = polarize_degree(chassis_center_obs_bound)
##
##                    obs_bound_conn_a_dir = get_closest_degree_direction(obs_bound_obs_center, connection_a_degree)[0]
##                    obs_bound_conn_b_dir = get_closest_degree_direction(obs_bound_obs_center, connection_b_degree)[0]
##
##                    chassis_bounding_deg = angle_between_points(bounding_collision_b[1], playerTank.rotated_chassis_rect.center)
##                    chassis_bounding_deg_val_diff = get_degree_diff(chassis_bounding_deg, playerTank.chassis_degree_val)
##                    chassis_bounding_polar_diff = get_degree_diff(chassis_bounding_deg, polar_degree_val)
##
##                    if abs(chassis_bounding_deg_val_diff) < abs(chassis_bounding_polar_diff):
##                        selected_deg_val = playerTank.chassis_degree_val
##                    else:
##                        selected_deg_val = polar_degree_val
##
##                    obs_bound_selected_deg_dir = get_closest_degree_direction(chassis_bounding_deg, selected_deg_val)[0]
##
##
##                    chassis_conn_a_deg_diff = get_degree_diff(chassis_center_obs_bound, chassis_center_conn_a)
##                    chassis_conn_b_deg_diff = get_degree_diff(chassis_center_obs_bound, chassis_center_conn_b)
##
##
##                    if obs_bound_selected_deg_dir == obs_bound_conn_a_dir:
##                        if abs(chassis_conn_a_deg_diff) > 10:
##                        #if True:
##                            selected_connection_point_b = bounding_connections[0]
##                        else:
##                            selected_connection_point_b = bounding_connections[1]
##                    else:
##                        if abs(chassis_conn_b_deg_diff) > 10:
##                        #if True:
##                            selected_connection_point_b = bounding_connections[1]
##                        else:
##                            selected_connection_point_b = bounding_connections[0]
##
##                    if selected_connection_point_b == bounding_connections[0]:
##                        pygame.draw.circle(DISPSURF, (255, 125, 0), bounding_connections[0], 25, 1)
##                        obs_chosen_conn_dir = obs_bound_conn_a_dir
##                        selected_connection_point_b = bounding_connections[0]
##                    else:
##                        pygame.draw.circle(DISPSURF, (125, 255, 0), bounding_connections[1], 25, 1)
##                        obs_chosen_conn_dir = obs_bound_conn_b_dir
##                        selected_connection_point_b = bounding_connections[1]
##
##                    
##
##                    chassis_colliding_deg = angle_between_points(bounding_collision_b[1], playerTank.rotated_chassis_rect.center)
##                    chassis_conn_deg = angle_between_points(collision_reassignment[1], playerTank.rotated_chassis_rect.center)
##
##                    chassis_coll_dir = get_closest_degree_direction(selected_deg_val, chassis_colliding_deg)[0]
##                    chassis_conn_dir = get_closest_degree_direction(selected_deg_val, chassis_conn_deg)[0]
##                    if chassis_coll_dir == obs_chosen_conn_dir:
##                        chassis_selected_bounding = collision_reassignment[1]
##                        selected_coll_point = collision_reassignment[1]
##                    elif chassis_conn_dir == obs_chosen_conn_dir:
##                        chassis_selected_bounding = bounding_collision_b[1]
##                        selected_coll_point = bounding_collision_b[1]
##                    pygame.draw.circle(DISPSURF, (0, 255, 105), chassis_selected_bounding, 20, 1)
##
##                    if selected_coll_point != bounding_collision_b[1]:
##                        selected_colliding_point = collision_reassignment[1]
##                        bounding_collision_b = (bounding_collision_b[0], collision_reassignment[1])
##                        colliding_point_degree = angle_between_points(bounding_collision_b[1], bounding_collision_b[0])
##                        for x in range(len(bounding_x)):
##                            if bounding_x[x] == bounding_collision_b[1]:
##                                bounding_index = x
##                                break
##                    
##
##                    selected_connection_point = selected_connection_point_b
##                    
##                      
##
####                enemy_bounding_points = master_sector.units[artificial_enemy.tank.unit_id]['bounding_points']
####                enemy_bounding_connections = master_sector.units[artificial_enemy.tank.unit_id]['bounding_connections'][enemy_index]
####                bounding_connections = [enemy_bounding_connections['clockwise_index'], enemy_bounding_connections['counterclock_index']]
####                bounding_connections = [enemy_bounding_points[bounding_connections[0]], enemy_bounding_points[bounding_connections[1]]]
####                pygame.draw.circle(DISPSURF, (255, 0, 255), bounding_collision_b[1], 3, 0)
####                pygame.draw.circle(DISPSURF, (0, 255, 0), bounding_collision_b[0], 3, 0)
####                for x in range(len(bounding_connections)):
####                    pygame.draw.circle(DISPSURF, (0, 0, 0), bounding_connections[x], 3, 0)
####                    pygame.draw.aaline(DISPSURF, (0, 0, 0), bounding_connections[x], bounding_collision_b[0], True)
####                connection_a_degree = angle_between_points(bounding_connections[0], bounding_collision_b[0])
####                connection_b_degree = angle_between_points(bounding_connections[1], bounding_collision_b[0])
####                colliding_point_degree = angle_between_points(bounding_collision_b[1], bounding_collision_b[0])
####                obstacle_bounding_to_chassis_center = angle_between_points(playerTank.rotated_chassis_rect.center, bounding_collision_b[0])
##                obstacle_bounding_to_chassis_center_dist = distance_between_positions(bounding_collision_b[0], playerTank.rotated_chassis_rect.center)
##                chassis_center_bounding_degree = angle_between_points(bounding_collision_b[1], playerTank.rotated_chassis_rect.center)
##                chassis_center_bounding_dist = distance_between_positions(playerTank.rotated_chassis_rect.center, bounding_collision_b[1])
####                degree_difference_original_bounding = get_closest_degree_direction(playerTank.chassis_degree_val, chassis_center_bounding_degree)[1]
####                chassis_center_to_obstacle = angle_between_points(bounding_collision_b[0], playerTank.rotated_chassis_rect.center)
####
####                chassis_center_conn_a_degree = angle_between_points(bounding_connections[0], playerTank.rotated_chassis_rect.center)
####                chassis_center_conn_b_degree = angle_between_points(bounding_connections[1], playerTank.rotated_chassis_rect.center)
####                degree_range_conn_a = get_closest_degree_direction(chassis_center_conn_a_degree, chassis_center_to_obstacle)
####                degree_range_conn_b = get_closest_degree_direction(chassis_center_conn_b_degree, chassis_center_to_obstacle)
####
####                obs_bounding_chassis_center = angle_between_points(playerTank.rotated_chassis_rect.center, bounding_collision_b[0])
####
####
####                connection_a_degree_difference = get_degree_diff(obs_bounding_chassis_center, connection_a_degree)#(connection_a_degree, colliding_point_degree)
####                connection_b_degree_difference = get_degree_diff(obs_bounding_chassis_center, connection_b_degree)#(connection_b_degree, colliding_point_degree)
####                
####                dist_to_conn_a = distance_between_positions(playerTank.rotated_chassis_rect.center, bounding_connections[0])
####                dist_to_conn_b = distance_between_positions(playerTank.rotated_chassis_rect.center, bounding_connections[1])
####
####
####                bounding_dist_to_conn_a = distance_between_positions(bounding_collision_b[0], bounding_connections[0])
####                bounding_dist_to_conn_b = distance_between_positions(bounding_collision_b[0], bounding_connections[1])
####
####                connection_differences = [abs(connection_a_degree_difference), abs(connection_b_degree_difference)]
####
####                lowest_degree_difference = min(connection_differences)
##
##                if selected_connection_point == bounding_connections[0]:
##                    connection_degree = connection_a_degree
##                    connection_point = bounding_connections[0]
##                    connection_dist = bounding_dist_to_conn_a
##                    connection_point_to_chassis_center_dist = distance_between_positions(playerTank.rotated_chassis_rect.center, bounding_connections[0])
##                        
##                else:
##                    connection_degree = connection_b_degree
##                    connection_point = bounding_connections[1]
##                    connection_dist = bounding_dist_to_conn_b
##                    connection_point_to_chassis_center_dist = distance_between_positions(playerTank.rotated_chassis_rect.center, bounding_connections[1])
##
##
##                    
##                pygame.draw.polygon(DISPSURF, (255, 0, 0), [playerTank.rotated_chassis_rect.center, bounding_collision_b[0], connection_point, playerTank.rotated_chassis_rect.center], 1)
##
##                trig_a_act = True
##                side_a = connection_dist
##                first_a = side_a
##                side_b = distance_between_positions(bounding_collision_b[0], playerTank.rotated_chassis_rect.center) #obstacle_bounding_to_chassis_center_dist
##                side_c = connection_point_to_chassis_center_dist
##                first_c = side_c
##                mathematical_radians = math.acos((side_a**2 + side_b**2 - side_c**2) / (2 * side_a * side_b))
##                #print(math.degrees(mathematical_radians))
##
##                side_a_act = side_a
##                side_b_act = side_b
##                side_c_act = side_c
##                
##
##                angle_c = mathematical_radians
##                side_c = chassis_center_bounding_dist
##                side_b = obstacle_bounding_to_chassis_center_dist
##
##                try:
##                    angle_b = math.asin((math.sin(angle_c) * side_b) / side_c)
##                except ValueError:
##                    trig_a_act = False
##                    first_trig_dict = None
##                    turret_rotation_value = 0.0
##                if trig_a_act == True:
##                    angle_a = math.radians(180.00 - math.degrees(angle_b) - math.degrees(angle_c))
##                    side_a = (math.sin(angle_a) * side_b) / math.sin(angle_b)
##                        
##                    new_bounding_pos = pos_from_degrees(bounding_collision_b[0], connection_degree, side_a)
##                    new_bounding_pos = (int(new_bounding_pos[0]), int(new_bounding_pos[1]))
##
##
##                    pygame.draw.circle(DISPSURF, (0, 255, 255), new_bounding_pos, 3, 0)
##                    
##                    turret_rotation_value = get_degree_diff(chassis_center_bounding_degree, angle_between_points(new_bounding_pos, playerTank.rotated_chassis_rect.center))
##                    rotation_padding = get_degree_diff(chassis_center_bounding_degree, playerTank.degree_val) / 2
##                    #turret_rotation_value += rotation_padding
##
##
##                    new_degree_val = playerTank.chassis_degree_val + turret_rotation_value
##                    new_degree_val_pos = pos_from_degrees(playerTank.rotated_chassis_rect.center, new_degree_val, 100)
##                    new_degree_val_pos = (int(new_degree_val_pos[0]), int(new_degree_val_pos[1]))
##                    pygame.draw.aaline(DISPSURF, (0, 255, 255), playerTank.rotated_chassis_rect.center, new_degree_val_pos, True)
##                    first_trig_dict = {'first_a': first_a, 'b': side_b, 'first-c': first_c, 'second_c': side_c, 'side_a': side_a, 'angle-c': angle_c, 'angle_b': angle_b, 'angle-a': angle_a, 'pos': new_bounding_pos, 'rot_val': turret_rotation_value}
##
##
##                ######SECOND TRIG FUNC######
##                trig_b_act = True
##                previous_radians = mathematical_radians
##                
##                side_a_b = connection_dist
##                first_a_b = side_a_b
##                side_b_b = distance_between_positions(playerTank.rotated_chassis_rect.center, connection_point)
##                first_b_b = side_b_b
##                side_c_b = obstacle_bounding_to_chassis_center_dist
##                first_c_b = side_c_b
##                mathematical_radians = math.acos((side_a_b**2 + side_b_b**2 - side_c_b**2) / (2 * side_a_b * side_b_b))
##                if mathematical_radians == 0:
##                    mathematical_radians = previous_radians
##                #print(math.degrees(mathematical_radians))
##                #print('a:{}, b:{}, c:{}'.format(side_a, side_b, side_c))
##                angle_c_b = mathematical_radians
##                side_c_b = chassis_center_bounding_dist
##                side_b_b = distance_between_positions(playerTank.rotated_chassis_rect.center, connection_point)
##                try:
##                    angle_b_b = math.asin((math.sin(angle_c_b) * side_b_b) / side_c_b)
##                except ValueError:
##                    trig_b_act = False
##                    second_trig_dict = None
##                    turret_rotation_value_b = 0.0
##                if trig_b_act == True:
##                    angle_a_b = math.radians(180.00 - math.degrees(angle_b_b) - math.degrees(angle_c_b))
##                    side_a_b = (math.sin(angle_a_b) * side_b_b) / math.sin(angle_b_b)
##                        
##                    new_bounding_pos_b = pos_from_degrees(connection_point, polarize_degree(connection_degree), side_a_b)
##                    new_bounding_pos_b = (int(new_bounding_pos_b[0]), int(new_bounding_pos_b[1]))
##
##
##                    pygame.draw.circle(DISPSURF, (255, 188, 0), new_bounding_pos_b, 3, 0)
##                    
##                    turret_rotation_value_b = get_degree_diff(chassis_center_bounding_degree, angle_between_points(new_bounding_pos_b, playerTank.rotated_chassis_rect.center))
##                    rotation_padding = get_degree_diff(chassis_center_bounding_degree, playerTank.degree_val) / 2
##                    #turret_rotation_value_b += rotation_padding
##
##                    new_degree_val_b = playerTank.chassis_degree_val + turret_rotation_value_b
##                    new_degree_val_pos_b = pos_from_degrees(playerTank.rotated_chassis_rect.center, new_degree_val_b, 100)
##                    new_degree_val_pos_b = (int(new_degree_val_pos_b[0]), int(new_degree_val_pos_b[1]))
##                    pygame.draw.aaline(DISPSURF, (255, 188, 0), playerTank.rotated_chassis_rect.center, new_degree_val_pos_b, True)
##                    second_trig_dict = {'first_a': first_a_b, 'first_b': first_b_b, 'b': side_b_b, 'first-c': first_c_b, 'second_c': side_c_b, 'side_a': side_a_b, 'angle-c': angle_c_b, 'angle_b': angle_b_b, 'angle-a': angle_a_b, 'pos': new_bounding_pos_b, 'rot_val': turret_rotation_value_b}
##
##
##                #######END SECOND TRIG FUNC#######
##                trig_point_info = {'bounding_collision_b': bounding_collision_b, 'conn_point': connection_point, 'unit_center': playerTank.rotated_chassis_rect.center, 'conn_deg': connection_degree, 'polar_conn_deg': polarize_degree(connection_degree)}
##                act_trig_omni_dict = {'first_trig': first_trig_dict, 'second_trig': second_trig_dict, 'trig_point_info': trig_point_info}
##
##                new_bounding_a_diff = get_degree_diff(playerTank.chassis_degree_val, new_degree_val)
##                new_bounding_b_diff = get_degree_diff(playerTank.chassis_degree_val, new_degree_val_b)
##
##                #print('act_a_diff:{}, act_b_diff:{}'.format(new_bounding_a_diff, new_bounding_b_diff))
##                
##
##                #print('a_diff:{}, b_diff:{}, a_deg:{}, b_deg:{}, deg_val:{}'.format(new_bounding_a_diff, new_bounding_b_diff, new_degree_val, new_degree_val_b, playerTank.chassis_degree_val))
##                if abs(new_bounding_a_diff) < abs(new_bounding_b_diff) or collision_reassignment[0] == True:
##                    #degree_rotation_change = turret_rotation_value_b
##                    turret_rotation_value = turret_rotation_value
##                    #print('a selected')
##                else:
##                    #degree_rotation_change = turret_rotation_value_b
##                    #print('b selected')
##                    turret_rotation_value = turret_rotation_value_b
##                    
##                
##                if abs(turret_rotation_value) > abs(degree_rotation_change) or degree_rotation_change == 0.0:
##                    degree_rotation_change = turret_rotation_value
##
##            #degree_rotation_change = master_sector.reorient_unit_collisions_omni(playerTank.unit_id)
##                    
##            if bounding_collision_a == False:
##                degree_adjustment_class_a_alt = None
##                degree_adjustment_class_a_act = None
##            if bounding_collision_b == False:
##                degree_rotation_change_alt = None
##                turret_rotation_value = None
##            #print('deg_alt_b:{}, act_b:{} **** deg_alt_a:{}, act_a:{}'.format(degree_rotation_change_alt, turret_rotation_value, degree_adjustment_class_a_alt, degree_adjustment_class_a_act))
##
##            if alternate_degrees_on == True:
##                if degree_rotation_change_alt != turret_rotation_value:
##                    print('********************************************************************')
##                    print('FIRST DICT:')
##                    print(trig_omni_dict['first_trig'])
##                    print(act_trig_omni_dict['first_trig'])
##                    print('********************************************************************')
##                    print('SECOND TRIG:')
##                    print(trig_omni_dict['second_trig'])
##                    print(act_trig_omni_dict['second_trig'])
##                    print('********************************************************************')
##                    print('POINT INFO')
##                    print(trig_omni_dict['trig_point_info'])
##                    print(act_trig_omni_dict['trig_point_info'])
##                    print('Class-B Failure')    
##                    time.sleep(5)
##                    
##                if degree_adjustment_class_a_alt != degree_adjustment_class_a_act:
##                    print('Class-A Failure')
##                    print('deg_alt_a:{}, act_a:{}'.format(degree_adjustment_class_a_alt, degree_adjustment_class_a_act))
##                    #time.sleep(5)
##                
##            #playerTank.degree_val += degree_rotation_change
##            playerTank.check_unit_collision()       
##            
##            
##            playerTank.chassis_degree_val = player_chassis_deg
##            playerTank.rotated_chassis_rect = player_rect
##            master_sector.units[playerTank.unit_id]['bounding_points'] = player_chassis_bounding
##            master_sector.units[playerTank.unit_id]['bounding_connections'] = player_chassis_connections

            #playerTank.check_unit_collision()


            ######################################################################################################

            
        tank_degrees_pos = pos_from_degrees(master_sector.unit_objects[playerTank_id].chassis_turret_pos, master_sector.unit_objects[playerTank_id].degree_val, 50)
        pygame.draw.aaline(DISPSURF, (255, 0, 0), master_sector.unit_objects[playerTank_id].chassis_turret_pos, tank_degrees_pos, True)
        
        
        for x in range(len(master_sector.turrets[master_sector.unit_objects[playerTank_id].unit_id]['weapon_bounding_points'])):
            closest_points = []
            point_distances = []
            point_info = []

            for i in range(len(master_sector.turrets[playerTank_id]['weapon_bounding_points'][x]['bounding_points'])):
                point_i = master_sector.turrets[playerTank_id]['weapon_bounding_points'][x]['bounding_points'][i]
                point_dist = distance_between_positions(artificial_enemy.tank.rotated_chassis_rect.center, point_i)
                point_distances.append(point_dist)
                point_info.append((i, point_dist, point_i))
            closest_point = min(point_distances)
            closest_point = [(point_info[y][2], point_info[y][0]) for y in range(len(point_info)) if point_info[y][1] == closest_point][0]
            closest_points.append(closest_point)
            for i in range(len(closest_points)):
                pygame.draw.circle(DISPSURF, (255, 0, 0), closest_points[i][0], 3, 0)
                connections_indexes = master_sector.turrets[playerTank_id]['weapon_bounding_connections'][x][closest_points[i][1]]
                connections_indexes = [connections_indexes['clockwise_index'], connections_indexes['counterclock_index']]
                connections_points = [master_sector.turrets[playerTank_id]['weapon_bounding_points'][x]['bounding_points'][connections_indexes[y]] for y in range(len(connections_indexes))]
                for y in range(len(connections_points)):
                    pygame.draw.circle(DISPSURF, (0, 255, 0), connections_points[y], 3, 0)
                    pygame.draw.aaline(DISPSURF, (0, 0, 255), connections_points[y], closest_points[i][0], True)

        closest_point = artificial_enemy.tank.bounding_points[0]
        point_dist_lowest = 100000
        for i in range(len(artificial_enemy.tank.bounding_points)):
            point_dist = distance_between_positions(artificial_enemy.tank.bounding_points[i], master_sector.unit_objects[playerTank_id].rotated_turret_rect.center)
            if point_dist < point_dist_lowest:
                closest_point = artificial_enemy.tank.bounding_points[i]
                point_dist_lowest = point_dist
                connection_indexes = master_sector.units[artificial_enemy.tank.unit_id]['bounding_connections'][i]
                connection_indexes = [connection_indexes['clockwise_index'], connection_indexes['counterclock_index']]
        pygame.draw.circle(DISPSURF, (255, 100, 50), closest_point, 3, 0)
        for i in range(len(connection_indexes)):
            pygame.draw.aaline(DISPSURF, (0, 255, 0), closest_point, master_sector.units[artificial_enemy.tank.unit_id]['bounding_points'][connection_indexes[i]], True)






##        tank_collision = master_sector.check_unit_collisions_omni(playerTank.unit_id)
##
##        if tank_collision == True:
##            color_collision = (255, 0, 0)
##            pygame.draw.circle(DISPSURF, color_collision, playerTank.rotated_chassis_rect.center, 15, 0)

        chosen_bounding = master_sector.turrets[playerTank_id]['weapon_bounding_points'][2]['bounding_points'][2]
        other_bounding = master_sector.turrets[playerTank_id]['weapon_bounding_points'][2]['bounding_points'][3]
        other_other_bounding = master_sector.turrets[playerTank_id]['weapon_bounding_points'][2]['bounding_points'][1]
        final_other_bounding = master_sector.turrets[playerTank_id]['weapon_bounding_points'][2]['bounding_points'][0]
        dist_turret_to_chosen_bounding = distance_between_positions(master_sector.unit_objects[playerTank_id].chassis_turret_pos, chosen_bounding)
        dist_to_other_bounding = distance_between_positions(master_sector.unit_objects[playerTank_id].chassis_turret_pos, other_bounding)
        dist_to_other_other_bounding = distance_between_positions(master_sector.unit_objects[playerTank_id].chassis_turret_pos, other_other_bounding)
        dist_to_final_other_bounding = distance_between_positions(master_sector.unit_objects[playerTank_id].chassis_turret_pos, final_other_bounding)
        pygame.draw.circle(DISPSURF, (255, 0, 255), master_sector.unit_objects[playerTank_id].chassis_turret_pos, dist_turret_to_chosen_bounding, 1)
        pygame.draw.circle(DISPSURF, (255, 0, 255), master_sector.unit_objects[playerTank_id].chassis_turret_pos, dist_to_other_bounding, 1)
        #pygame.draw.circle(DISPSURF, (0, 255, 255), playerTank.chassis_turret_pos, dist_to_other_other_bounding, 1)
        #pygame.draw.circle(DISPSURF, (0, 255, 255), playerTank.chassis_turret_pos, dist_to_final_other_bounding, 1)

                
        pygame.display.update()
        FPSCLOCK.tick(FPS)
        print('-----------------------------------------------------------------------------------------------------')



main()
    


    

    

    

    
