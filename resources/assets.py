import itertools

from mcresources import ResourceManager, ItemContext, BlockContext, block_states
from mcresources import utils, loot_tables

from constants import *


def generate(rm: ResourceManager):
    bot_variants = four_rotations_mp('firmalife:block/oven_fire', (90, None, 180, 270), 'lit', True)
    for i in range(1, 5):
        bot_variants += four_rotations_mp('firmalife:block/oven_logs_%s' % i, (90, None, 180, 270), 'logs', i)
    variants = {
        'brick': 'minecraft:block/bricks',
        'rustic': 'firmalife:block/rustic_bricks',
        'tile': 'firmalife:block/tiles',
        'stone': 'firmalife:block/sealed_bricks',
        'clay': 'firmalife:block/unfired_bricks'
    }
    for var, base_tex in variants.items():
        bot_front = 'firmalife:block/%s_oven_bottom' % var
        top_front = 'firmalife:block/%s_oven_top' % var
        surface = 'firmalife:block/%s_oven_surface' % var
        hop_front = 'firmalife:block/%s_oven_hopper_front' % var
        hop_top = 'firmalife:block/%s_oven_hopper_top' % var
        side = 'firmalife:block/%s_oven_side' % var if var != 'clay' else base_tex

        rm.block_model('%s_oven_bottom' % var, parent='firmalife:block/oven_bottom', textures={'main': base_tex, 'side': side, 'front': bot_front, 'top': surface})
        rm.block_model('%s_oven_top' % var, parent='firmalife:block/oven_top', textures={'main': base_tex, 'side': side, 'front': top_front, 'top': base_tex})
        rm.block_model('%s_oven_particle' % var, parent='tfc:block/empty', textures={'particle': base_tex})
        rm.block_model('%s_oven_chimney' % var, parent='firmalife:block/oven_chimney', textures={'cured': base_tex})
        rm.block_model('%s_oven_chimney_alt' % var, parent='firmalife:block/oven_chimney_alt', textures={'cured': base_tex})
        rm.block_model('%s_oven_hopper' % var, parent='minecraft:block/orientable', textures={'top': hop_top, 'side': side, 'front': hop_front})
        if var != 'clay':
            rm.block_model('%s_oven_bottom_insulated' % var, parent='firmalife:block/oven_bottom', textures={'main': base_tex, 'side': 'firmalife:block/oven_insulation', 'front': bot_front + '_insulated', 'top': surface})

        pref = 'cured_%s_' % var
        if var == 'brick':
            pref = 'cured_'
        elif var == 'clay':
            pref = ''

        for bottom_type in ('insulated_', 'cured_'):
            if not (var == 'clay' and bottom_type == 'insulated_'):
                fixed_pref = pref.replace('cured_', bottom_type)
                last_bot_variants = bot_variants.copy()
                last_bot_variants += four_rotations_mp_free('firmalife:block/%s_oven_bottom%s' % (var, '_insulated' if bottom_type == 'insulated_' else ''), (90, None, 180, 270))
                last_bot_variants += [{'model': 'firmalife:block/%s_oven_particle' % var}]
                rm.blockstate_multipart('%soven_bottom' % fixed_pref, *last_bot_variants).with_lang(lang('%sbottom oven', fixed_pref)).with_tag('firmalife:oven_blocks').with_block_loot('firmalife:%soven_bottom' % fixed_pref)
                rm.item_model('%soven_bottom' % fixed_pref, parent='firmalife:block/%s_oven_bottom' % var, no_textures=True)

        rm.blockstate('%soven_top' % pref, variants={**four_rotations('firmalife:block/%s_oven_top' % var, (90, None, 180, 270))}).with_lang(lang('%stop oven', pref)).with_tag('firmalife:oven_blocks').with_block_loot('firmalife:%soven_top' % pref)
        rm.item_model('%soven_top' % pref, parent='firmalife:block/%s_oven_top' % var, no_textures=True)
        rm.blockstate('%soven_chimney' % pref, variants={'alt=true': {'model': 'firmalife:block/%s_oven_chimney_alt' % var}, 'alt=false': {'model': 'firmalife:block/%s_oven_chimney' % var}}).with_lang(lang('%soven chimney', pref)).with_tag('firmalife:oven_blocks').with_tag('firmalife:chimneys').with_block_loot('firmalife:%soven_chimney' % pref)
        rm.item_model('%soven_chimney' % pref, parent='firmalife:block/%s_oven_chimney' % var, no_textures=True)
        rm.blockstate('%soven_hopper' % pref, variants={**four_rotations('firmalife:block/%s_oven_hopper' % var, (90, None, 180, 270))}).with_lang(lang('%soven hopper', pref)).with_tag('firmalife:oven_blocks').with_block_loot('firmalife:%soven_hopper' % pref)
        rm.item_model('%soven_hopper' % pref, parent='firmalife:block/%s_oven_hopper' % var, no_textures=True)

        if var != 'clay':
            block = rm.blockstate('%s_countertop' % var).with_item_model().with_tag('firmalife:oven_blocks').with_tag('minecraft:mineable/pickaxe').with_block_loot('firmalife:%s_countertop' % var).with_lang(lang('%s countertop', var))
            block.with_block_model(parent='minecraft:block/cube_column', textures={'end': 'firmalife:block/%s_countertop' % var, 'side': side})

    block = rm.blockstate('ashtray', variants=dict(('stage=%s' % i, {'model': 'firmalife:block/ashtray_%s' % i}) for i in range(0, 11)))
    block.with_lang(lang('ashtray')).with_tag('minecraft:mineable/pickaxe').with_block_loot('firmalife:ashtray')
    for i in range(0, 11):
        rm.block_model('ashtray_%s' % i, parent='minecraft:block/cube_column', textures={'side': 'firmalife:block/ashtray_side_%s' % i, 'end': 'firmalife:block/ashtray_top'})
    rm.item_model('ashtray', parent='firmalife:block/ashtray_0', no_textures=True)

    block = rm.blockstate('ice_fishing_station', variants={**four_rotations('firmalife:block/ice_fishing_station', (90, None, 180, 270))})
    block.with_block_loot('firmalife:ice_fishing_station').with_item_model().with_lang(lang('ice fishing station')).with_tag('minecraft:mineable/axe')

    block = rm.blockstate('plate').with_item_model().with_lang(lang('plate')).with_tag('minecraft:mineable/axe').with_block_loot('firmalife:plate')

    block = rm.blockstate('jarring_station', variants={**four_rotations('firmalife:block/jarring_station', (90, None, 180, 270))})
    block.with_block_loot('firmalife:jarring_station').with_item_model().with_lang(lang('jarring station')).with_tag('minecraft:mineable/pickaxe')

    rm.blockstate('drying_mat', model='firmalife:block/drying_mat').with_item_model().with_tag('tfc:mineable_with_sharp_tool').with_lang(lang('drying mat')).with_block_loot('firmalife:drying_mat')
    rm.blockstate('solar_drier', model='firmalife:block/solar_drier').with_item_model().with_tag('minecraft:mineable/axe').with_lang(lang('solar drier')).with_block_loot('firmalife:solar_drier')
    rm.blockstate('hollow_shell', model='firmalife:block/hollow_shell').with_lang(lang('hollow shell')).with_block_loot('firmalife:hollow_shell')
    block = rm.blockstate('mixing_bowl', model='firmalife:block/mixing_bowl').with_item_model().with_tag('minecraft:mineable/axe').with_lang(lang('mixing bowl'))
    block.with_block_loot({'name': 'firmalife:mixing_bowl'}, {'name': 'firmalife:spoon', 'conditions': [loot_tables.block_state_property('firmalife:mixing_bowl[spoon=true]')]})

    for fruit in TFC_FRUITS:
        rm.item_model(('not_dried', fruit), 'tfc:item/food/%s' % fruit)
        rm.item_model(('dried', fruit), 'firmalife:item/dried/dried_%s' % fruit)
        item_model_property(rm, 'tfc:food/%s' % fruit, [{'predicate': {'firmalife:dry': 1}, 'model': 'firmalife:item/dried/%s' % fruit}], {'parent': 'firmalife:item/not_dried/%s' % fruit})

    for fruit in FL_FRUITS:
        rm.item_model(('not_dried', fruit), 'firmalife:item/food/%s' % fruit)
        rm.item_model(('dried', fruit), 'firmalife:item/dried/dried_%s' % fruit)
        item_model_property(rm, 'firmalife:food/%s' % fruit, [{'predicate': {'firmalife:dry': 1}, 'model': 'firmalife:item/dried/%s' % fruit}], {'parent': 'firmalife:item/not_dried/%s' % fruit})
        rm.item('food/%s' % fruit).with_lang(lang(fruit))

    for greenhouse in GREENHOUSES:
        greenhouse_slab(rm, greenhouse, 'firmalife:block/greenhouse/%s' % greenhouse, 'firmalife:block/greenhouse/%s_glass' % greenhouse)
        greenhouse_stairs(rm, greenhouse, 'firmalife:block/greenhouse/%s' % greenhouse, 'firmalife:block/greenhouse/%s_glass' % greenhouse)
        greenhouse_wall(rm, greenhouse, 'firmalife:block/greenhouse/%s' % greenhouse, 'firmalife:block/greenhouse/%s_glass' % greenhouse)
        greenhouse_door(rm, greenhouse, 'firmalife:block/greenhouse/%s_door_bottom' % greenhouse, 'firmalife:block/greenhouse/%s_door_top' % greenhouse)

    for planter in ('quad_planter', 'large_planter', 'bonsai_planter', 'hanging_planter'):
        for state in ('wet', 'dry'):
            rm.block_model('%s_%s' % (planter, state), parent='firmalife:block/%s' % planter, textures={'soil': 'firmalife:block/potting_soil_%s' % state})
        rm.blockstate(planter, variants={
            'watered=true': {'model': 'firmalife:block/%s_wet' % planter},
            'watered=false': {'model': 'firmalife:block/%s_dry' % planter}
        }).with_lang(lang(planter)).with_block_loot('firmalife:%s' % planter).with_tag('minecraft:mineable/axe').with_tag('minecraft:mineable/pickaxe')
        rm.item_model(planter, parent='firmalife:block/%s_dry' % planter, no_textures=True)
    rm.blockstate('trellis_planter', model='firmalife:block/trellis_planter').with_lang(lang('trellis planter')).with_block_loot('firmalife:trellis_planter').with_tag('minecraft:mineable/axe').with_tag('minecraft:mineable/pickaxe').with_item_model()
    rm.blockstate('hydroponic_planter', model='firmalife:block/hydroponic_planter').with_lang(lang('hydroponic planter')).with_block_loot('firmalife:hydroponic_planter').with_tag('minecraft:mineable/axe').with_tag('minecraft:mineable/pickaxe').with_item_model()

    rm.blockstate('vat', variants={
        'sealed=false': {'model': 'firmalife:block/vat'},
        'sealed=true': {'model': 'firmalife:block/vat_sealed'},
    }).with_lang(lang('vat')).with_block_loot('firmalife:vat').with_tag('minecraft:mineable/pickaxe').with_item_model()

    rm.blockstate('wool_string', variants={
        'axis=x': {'model': 'firmalife:block/wool_string'},
        'axis=z': {'model': 'firmalife:block/wool_string', 'y': 90}
    }).with_block_model(parent='firmalife:block/string', textures={'string': 'minecraft:block/white_wool'}).with_lang(lang('wool string')).with_tag('tfc:mineable_with_sharp_tool').with_item_model().with_block_loot('tfc:wool_yarn')

    rm.blockstate('climate_station', variants={
        'stasis=true': {'model': 'firmalife:block/climate_station_valid'},
        'stasis=false': {'model': 'firmalife:block/climate_station_invalid'}
    }).with_lang(lang('climate station')).with_tag('minecraft:mineable/axe').with_block_loot('firmalife:climate_station')
    rm.item_model('climate_station', parent='firmalife:block/climate_station_invalid', no_textures=True)
    for variant in ('valid', 'invalid'):
        tex = 'firmalife:block/greenhouse/climate_station/%s' % variant
        rm.block_model('firmalife:climate_station_%s' % variant, {'west': tex, 'east': tex, 'north': tex, 'south': tex, 'particle': tex, 'up': 'firmalife:block/greenhouse/climate_station/top', 'down': 'firmalife:block/greenhouse/climate_station/end'}, 'block/cube')

    trd = 'squirting_moisture_transducer'
    rm.blockstate(trd, variants={
        'stasis=true': {'model': 'firmalife:block/' + trd + '_on'},
        'stasis=false': {'model': 'firmalife:block/' + trd + '_off'}
    }).with_lang(lang(trd)).with_tag('minecraft:mineable/pickaxe').with_block_loot('firmalife:%s' % trd)
    rm.item_model(trd, parent='firmalife:block/' + trd + '_on', no_textures=True)
    for variant in ('on', 'off'):
        tex = 'firmalife:block/%s_%s' % (trd, variant)
        rm.block_model('firmalife:%s_%s' % (trd, variant), {'west': tex, 'east': tex, 'north': tex, 'south': tex, 'particle': tex, 'up': 'firmalife:block/%s_top' % trd, 'down': 'firmalife:block/%s_top' % trd})

    rm.blockstate('stovetop_grill').with_lang(lang('stovetop grill')).with_tag('minecraft:mineable/pickaxe').with_block_loot('tfc:wrought_iron_grill')
    rm.blockstate('stovetop_pot').with_lang(lang('stovetop pot')).with_tag('minecraft:mineable/pickaxe').with_block_loot('tfc:ceramic/pot')

    rm.block_model('dribbler', parent='firmalife:block/sprinkler', textures={'0': 'firmalife:block/metal/full/stainless_steel'})
    rm.blockstate('sprinkler', model='firmalife:block/sprinkler').with_lang(lang('sprinkler')).with_tag('minecraft:mineable/pickaxe').with_block_loot('firmalife:sprinkler')
    rm.item_model('sprinkler', parent='firmalife:block/sprinkler', no_textures=True)
    rm.blockstate('dribbler', model='firmalife:block/dribbler').with_lang(lang('dribbler')).with_tag('minecraft:mineable/pickaxe').with_block_loot('firmalife:dribbler')
    rm.item_model('dribbler', parent='firmalife:block/dribbler', no_textures=True)

    rm.blockstate('beehive', variants={
        **four_rotations('minecraft:block/beehive_honey', (90, None, 180, 270), ',honey=true'),
        **four_rotations('minecraft:block/beehive', (90, None, 180, 270), ',honey=false')
    }).with_lang(lang('wooden beehive')).with_tag('minecraft:mineable/axe').with_block_loot('firmalife:beehive')
    rm.item_model('beehive', parent='minecraft:block/beehive', no_textures=True)

    rm.block_model('iron_composter', parent='tfc:block/composter/composter', textures={'0': 'firmalife:block/iron_composter_bottom', '1': 'firmalife:block/iron_composter_side', 'particle': 'firmalife:block/iron_composter_bottom'})
    states = [({'model': 'firmalife:block/iron_composter'})]
    for i in range(1, 9):
        for age in ('normal', 'ready', 'rotten'):
            states.append(({'type': age, 'stage': i}, {'model': 'tfc:block/composter/%s_%s' % (age, i)}),)
    rm.blockstate_multipart('iron_composter', *states).with_lang(lang('iron composter')).with_block_loot('firmalife:iron_composter').with_tag('minecraft:mineable/pickaxe')
    rm.item_model('iron_composter', parent='firmalife:block/iron_composter', no_textures=True)

    rm.block('sealed').make_door().make_trapdoor().make_wall(texture='firmalife:block/sealed_bricks')
    rm.block('sealed_trapdoor').with_lang(lang('sealed trapdoor')).with_tag('minecraft:mineable/pickaxe').with_block_loot('firmalife:sealed_trapdoor')
    rm.block('sealed_wall').with_lang(lang('sealed wall')).with_tag('minecraft:mineable/pickaxe').with_block_loot('firmalife:sealed_wall').with_item_tag('minecraft:walls').with_tag('minecraft:walls')
    block = rm.block('firmalife:sealed_door').with_tag('minecraft:doors').with_lang(lang('sealed door')).with_tag('minecraft:mineable/pickaxe')
    door_loot(block, 'firmalife:sealed_door')

    rm.blockstate('dark_ladder', variants=four_rotations('firmalife:block/dark_ladder', (90, None, 180, 270))).with_block_model(textures={'texture': 'firmalife:block/dark_ladder', 'particle': 'firmalife:block/dark_ladder'}, parent='minecraft:block/ladder').with_lang(lang('dark ladder')).with_tag('minecraft:mineable/pickaxe').with_block_loot('firmalife:dark_ladder')
    rm.item_model('dark_ladder', 'firmalife:block/dark_ladder')

    rm.blockstate('nutritive_basin', variants={
        'watered=false': {'model': 'firmalife:block/nutritive_basin'},
        'watered=true': {'model': 'firmalife:block/nutritive_basin_water'},
    }).with_block_loot('firmalife:nutritive_basin').with_lang(lang('nutritive basin')).with_tag('minecraft:mineable/axe').with_item_model()

    for cheese in CHEESE_WHEELS:
        for age in ('fresh', 'aged', 'vintage'):
            for i in range(1, 5):
                surf = 'firmalife:block/cheese/%s_wheel_surface_%s' % (cheese, age)
                rm.block_model('cheese/%s_%s_%s' % (cheese, age, i), parent='firmalife:block/cheese_%s' % i, textures={'surface': surf, 'particle': surf, 'down': surf, 'inside': 'firmalife:block/cheese/%s_wheel_inner_%s' % (cheese, age)})
        block = rm.blockstate('%s_wheel' % cheese, variants=dict(
            ('age=%s,count=%s' % (a, c), {'model': 'firmalife:block/cheese/%s_%s_%s' % (cheese, a, c)})
            for a in ('fresh', 'aged', 'vintage') for c in range(1, 5)
        )).with_lang(lang('%s cheese wheel', cheese)).with_tag('cheese_wheels').with_item_tag('cheese_wheels')
        block.with_block_loot([{
            'name': 'firmalife:food/%s' % cheese,
            'functions': [loot_tables.set_count(c)],
            'conditions': [loot_tables.block_state_property('firmalife:%s_wheel[count=%s]' % (cheese, c))]
        } for c in range(1, 5)])
        rm.item_model('firmalife:%s_wheel' % cheese, parent='firmalife:block/cheese/%s_fresh_4' % cheese, no_textures=True)

    ore = 'chromite'
    for grade in ORE_GRADES.keys():
        rm.item_model('firmalife:ore/%s_%s' % (grade, ore)).with_lang(lang('%s %s', grade, ore))
    block = rm.blockstate('ore/small_%s' % ore, variants={"": four_ways('firmalife:block/small_%s' % ore)}, use_default_model=False)
    block.with_lang(lang('small %s', ore)).with_block_loot('firmalife:ore/small_%s' % ore).with_tag('tfc:can_be_snow_piled')
    rm.item_model('ore/small_%s' % ore).with_lang(lang('small %s', ore))
    for rock, data in TFC_ROCKS.items():
        for grade in ORE_GRADES.keys():
            block = rm.blockstate(('ore', grade + '_' + ore, rock), 'firmalife:block/ore/%s_%s/%s' % (grade, ore, rock))
            block.with_block_model({
                'all': 'tfc:block/rock/raw/%s' % rock,
                'particle': 'tfc:block/rock/raw/%s' % rock,
                'overlay': 'firmalife:block/ore/%s_%s' % (grade, ore)
            }, parent='tfc:block/ore')
            block.with_item_model().with_lang(lang('%s %s %s', grade, rock, ore)).with_block_loot('firmalife:ore/%s_%s' % (grade, ore)).with_tag('minecraft:mineable/pickaxe').with_tag('tfc:prospectable')
            rm.block('firmalife:ore/%s_%s/%s/prospected' % (grade, ore, rock)).with_lang(lang(ore))

    for carving in CARVINGS.keys():
        for variant, lang_part in (('lit_pumpkin', 'Jack o\'Lantern'), ('carved_pumpkin', 'Carved Pumpkin')):
            name = '%s/%s' % (variant, carving)
            rm.block_model(name, parent='minecraft:block/carved_pumpkin', textures={'front': 'firmalife:block/%s/%s' % (variant, carving)})
            rm.blockstate(name, variants=four_rotations('firmalife:block/%s' % name, (90, 0, 180, 270))).with_tag('tfc:mineable_with_sharp_tool').with_block_loot('firmalife:carved_pumpkin/%s' % carving).with_lang(lang('%s %s', carving, lang_part))
            rm.item_model('firmalife:%s' % name, parent='firmalife:block/%s' % name, no_textures=True)

    for var in ('rustic_bricks', 'tiles'):
        block = rm.block(var).make_slab().make_stairs().make_wall().with_tag('firmalife:oven_blocks')
        slab_loot(rm.block(var + '_slab'), 'firmalife:%s_slab' % var)
        rm.block_loot('firmalife:%s_stairs' % var, 'firmalife:%s_stairs' % var)
        rm.block_loot('firmalife:%s_wall' % var, 'firmalife:%s_wall' % var)
        for extra in ('_slab', '_stairs', '_wall'):
            rm.block('firmalife:%s%s' % (var, extra)).with_lang(lang('%s%s', var.replace('bricks', 'brick').replace('tiles', 'tile'), extra)).with_tag('firmalife:oven_blocks')

    for variant in ('gold', 'red', 'purple'):
        rm.block_model('plant/butterfly_grass_%s' % variant, parent='firmalife:block/tinted_cross_overlay', textures={'cross': 'firmalife:block/plant/butterfly_grass/base', 'overlay': 'firmalife:block/plant/butterfly_grass/%s' % variant})
    rm.blockstate('plant/butterfly_grass', variants={'': [{'model': 'firmalife:block/plant/butterfly_grass_%s' % variant, 'y': rot} for variant in ('gold', 'red', 'purple') for rot in (None, 90)]}, use_default_model=False).with_lang(lang('butterfly grass'))
    simple_plant_data(rm, 'firmalife:plant/butterfly_grass')
    flower_pot_cross(rm, 'butterfly grass', 'firmalife:plant/potted/butterfly_grass', 'plant/flowerpot/butterfly_grass', 'firmalife:block/plant/butterfly_grass/base', 'firmalife:plant/butterfly_grass', tinted=True)
    rm.item_model('plant/butterfly_grass', 'firmalife:block/plant/butterfly_grass/base')

    lifecycle_to_model = {'healthy': '', 'dormant': 'dry_', 'fruiting': 'fruiting_', 'flowering': 'flowering_'}
    lifecycles = ('healthy', 'dormant', 'fruiting', 'flowering')
    for berry in STILL_BUSHES.keys():
        rm.blockstate('plant/%s_bush' % berry, variants=dict(
            (
                'lifecycle=%s,stage=%d' % (lifecycle, stage),
                {'model': 'firmalife:block/plant/%s%s_bush_%d' % (lifecycle_to_model[lifecycle], berry, stage)}
            ) for lifecycle, stage in itertools.product(lifecycles, range(0, 3))
        )).with_lang(lang('%s Bush', berry)).with_tag('tfc:berry_bushes')

        rm.item_model('plant/%s_bush' % berry, parent='firmalife:block/plant/%s_bush_2' % berry, no_textures=True)
        rm.block_loot('plant/%s_bush' % berry, {'name': 'firmalife:plant/%s_bush' % berry, 'conditions': [loot_tables.match_tag('tfc:sharp_tools')]})
        for lifecycle, stage in itertools.product(lifecycle_to_model.values(), range(0, 3)):
            rm.block_model('plant/%s%s_bush_%d' % (lifecycle, berry, stage), parent='tfc:block/plant/stationary_bush_%d' % stage, textures={'bush': 'firmalife:block/berry_bush/' + lifecycle + '%s_bush' % berry})
        rm.block_tag('tfc:fox_raidable', 'firmalife:plant/%s_bush' % berry)

    for herb in HERBS:
        for stage in ('0', '1'):
            rm.block_model('plant/%s_%s' % (herb, stage), parent='minecraft:block/cross', textures={'cross': 'firmalife:block/plant/%s/%s' % (herb, stage)})
        rm.blockstate('plant/%s' % herb, variants={'stage=0': {'model': 'firmalife:block/plant/%s_0' % herb}, 'stage=1': {'model': 'firmalife:block/plant/%s_1' % herb}}).with_lang(lang(herb)).with_tag('firmalife:butterfly_grass_mutants')
        simple_plant_data(rm, 'firmalife:plant/%s' % herb, straw=False)
        rm.item_model('plant/%s' % herb, 'firmalife:block/plant/%s/1' % herb)
        flower_pot_cross(rm, herb, 'firmalife:plant/potted/%s' % herb, 'plant/flowerpot/%s' % herb, 'firmalife:block/plant/%s/1' % herb, 'firmalife:plant/%s' % herb)

    for wood in TFC_WOODS.keys():
        block = rm.blockstate('firmalife:wood/food_shelf/%s' % wood, variants=four_rotations('firmalife:block/wood/food_shelf/%s' % wood, (270, 180, None, 90))).with_tag('food_shelves').with_item_tag('food_shelves')
        block.with_block_loot('firmalife:wood/food_shelf/%s' % wood).with_lang(lang('%s food shelf', wood)).with_tag('minecraft:mineable/axe')
        rm.item_model('firmalife:wood/food_shelf/%s' % wood, parent='firmalife:block/wood/food_shelf/%s' % wood, no_textures=True)
        rm.block_model('firmalife:wood/food_shelf/%s' % wood, parent='firmalife:block/food_shelf_base', textures={'wood': 'tfc:block/wood/planks/%s' % wood})

        block = rm.blockstate('firmalife:wood/hanger/%s' % wood, model='firmalife:block/wood/hanger/%s' % wood).with_tag('hangers').with_item_tag('hangers')
        block.with_block_loot('firmalife:wood/hanger/%s' % wood).with_lang(lang('%s hanger' % wood)).with_tag('minecraft:mineable/axe')
        rm.item_model('firmalife:wood/hanger/%s' % wood, parent='firmalife:block/wood/hanger/%s' % wood, no_textures=True)
        rm.block_model('firmalife:wood/hanger/%s' % wood, parent='firmalife:block/hanger_base', textures={'wood': 'tfc:block/wood/planks/%s' % wood, 'string': 'minecraft:block/white_wool'})

        block = rm.blockstate('firmalife:wood/jarbnet/%s' % wood, variants={
            **four_rotations('firmalife:block/wood/jarbnet/%s' % wood, (90, None, 180, 270), suffix=',open=true'),
            **four_rotations('firmalife:block/wood/jarbnet/%s_shut' % wood, (90, None, 180, 270), suffix=',open=false'),
        })
        block.with_block_loot('firmalife:wood/jarbnet/%s' % wood).with_lang(lang('%s jarbnet', wood)).with_tag('minecraft:mineable/axe').with_tag('jarbnets').with_item_tag('jarbnets')
        rm.item_model('firmalife:wood/jarbnet/%s' % wood, parent='firmalife:block/wood/jarbnet/%s' % wood, no_textures=True)
        textures = {'planks': 'tfc:block/wood/planks/%s' % wood, 'sheet': 'tfc:block/wood/sheet/%s' % wood, 'log': 'tfc:block/wood/log/%s' % wood}
        rm.block_model('firmalife:wood/jarbnet/%s' % wood, parent='firmalife:block/jarbnet', textures=textures)
        rm.block_model('firmalife:wood/jarbnet/%s_shut' % wood, parent='firmalife:block/jarbnet_shut', textures=textures)

    for fruit in FRUITS.keys():
        for prefix in ('', 'growing_'):
            block = rm.blockstate_multipart('plant/' + fruit + '_' + prefix + 'branch',
                ({'model': 'firmalife:block/plant/%s_branch_core' % fruit}),
                ({'down': True}, {'model': 'firmalife:block/plant/%s_branch_down' % fruit}),
                ({'up': True}, {'model': 'firmalife:block/plant/%s_branch_up' % fruit}),
                ({'north': True}, {'model': 'firmalife:block/plant/%s_branch_side' % fruit, 'y': 90}),
                ({'south': True}, {'model': 'firmalife:block/plant/%s_branch_side' % fruit, 'y': 270}),
                ({'west': True}, {'model': 'firmalife:block/plant/%s_branch_side' % fruit}),
                ({'east': True}, {'model': 'firmalife:block/plant/%s_branch_side' % fruit, 'y': 180})
                ).with_tag('tfc:fruit_tree_branch').with_lang(lang('%s Branch', fruit))
            if prefix == '':
                block.with_block_loot({
                    'name': 'firmalife:plant/%s_sapling' % fruit,
                    'conditions': [{
                        'condition': 'minecraft:alternative',
                        'terms': [loot_tables.block_state_property('firmalife:plant/%s_branch[up=true,%s=true]' % (fruit, direction)) for direction in ('west', 'east', 'north', 'south')]
                    },
                        loot_tables.match_tag('tfc:axes')]
                }, {
                    'name': 'minecraft:stick',
                    'functions': [loot_tables.set_count(1, 4)]
                })
            else:
                block.with_block_loot({'name': 'minecraft:stick', 'functions': [loot_tables.set_count(1, 4)]})
            for part in ('down', 'side', 'up', 'core'):
                rm.block_model('firmalife:plant/%s_branch_%s' % (fruit, part), parent='tfc:block/plant/branch_%s' % part, textures={'bark': 'firmalife:block/fruit_tree/%s_branch' % fruit})
            rm.blockstate('plant/%s_leaves' % fruit, variants={
                'lifecycle=flowering': {'model': 'firmalife:block/plant/%s_flowering_leaves' % fruit},
                'lifecycle=fruiting': {'model': 'firmalife:block/plant/%s_fruiting_leaves' % fruit},
                'lifecycle=dormant': {'model': 'firmalife:block/plant/%s_dry_leaves' % fruit},
                'lifecycle=healthy': {'model': 'firmalife:block/plant/%s_leaves' % fruit}
            }).with_item_model().with_tag('minecraft:leaves').with_tag('tfc:fruit_tree_leaves').with_lang(lang('%s Leaves', fruit)).with_block_loot({
                'name': 'firmalife:food/%s' % fruit if fruit != 'cocoa' else 'firmalife:food/cocoa_beans',
                'conditions': [loot_tables.block_state_property('firmalife:plant/%s_leaves[lifecycle=fruiting]' % fruit)]
            }, {
                'name': 'firmalife:plant/%s_leaves' % fruit,
                'conditions': [{
                    "condition": "minecraft:alternative",
                    "terms": [loot_tables.match_tag('forge:shears'), loot_tables.silk_touch()]
                }]
                # 'conditions': [loot_tables.or_condition(loot_tables.match_tag('forge:shears'), loot_tables.silk_touch())]
            }, {
                'name': 'minecraft:stick',
                'conditions': [loot_tables.match_tag('tfc:sharp_tools'), loot_tables.random_chance(0.2)],
                'functions': [loot_tables.set_count(1, 2)]
            }, {
                'name': 'minecraft:stick',
                'conditions': [loot_tables.random_chance(0.05)],
                'functions': [loot_tables.set_count(1, 2)]
            })
            for life in ('', '_fruiting', '_flowering', '_dry'):
                rm.block_model('firmalife:plant/%s%s_leaves' % (fruit, life), parent='block/leaves', textures={'all': 'firmalife:block/fruit_tree/%s%s_leaves' % (fruit, life)})

            rm.blockstate(('plant', '%s_sapling' % fruit), variants={'saplings=%d' % i: {'model': 'firmalife:block/plant/%s_sapling_%d' % (fruit, i)} for i in range(1, 4 + 1)}).with_lang(lang('%s Sapling', fruit)).with_tag('fruit_tree_sapling')
            rm.block_loot(('plant', '%s_sapling' % fruit), {
                'name': 'firmalife:plant/%s_sapling' % fruit,
                'functions': [list({**loot_tables.set_count(i), 'conditions': [loot_tables.block_state_property('firmalife:plant/%s_sapling[saplings=%s]' % (fruit, i))]} for i in range(1, 5)), loot_tables.explosion_decay()]
            })
            for stage in range(2, 4 + 1):
                rm.block_model(('plant', '%s_sapling_%d' % (fruit, stage)), parent='tfc:block/plant/cross_%s' % stage, textures={'cross': 'firmalife:block/fruit_tree/%s_sapling' % fruit})
            rm.block_model(('plant', '%s_sapling_1' % fruit), {'cross': 'firmalife:block/fruit_tree/%s_sapling' % fruit}, 'block/cross')
            rm.item_model(('plant', '%s_sapling' % fruit), 'firmalife:block/fruit_tree/%s_sapling' % fruit)
            flower_pot_cross(rm, '%s sapling' % fruit, 'firmalife:plant/potted/%s_sapling' % fruit, 'plant/flowerpot/%s_sapling' % fruit, 'firmalife:block/fruit_tree/%s_sapling' % fruit, 'firmalife:plant/%s_sapling' % fruit)

    contained_fluid(rm, 'hollow_shell', 'firmalife:item/hollow_shell', 'firmalife:item/hollow_shell_overlay').with_lang(lang('Hollow Shell')).with_tag('tfc:buckets')

    peel(rm, 'peel', 'firmalife:item/peel')

    for jar, _, texture, _ in JARS:
        make_jar(rm, jar, texture)
    for fruit in TFC_FRUITS:
        make_jar(rm, fruit, 'firmalife:block/jar/%s' % fruit).with_tag('foods/preserves')
    for fruit in FL_FRUITS:
        make_jar(rm, fruit, 'firmalife:block/jar/%s' % fruit).with_tag('foods/preserves')

    for block, tag in SIMPLE_BLOCKS.items():
        rm.blockstate(block).with_block_model().with_tag(tag).with_lang(lang(block)).with_item_model().with_block_loot('firmalife:%s' % block)
    for item in SIMPLE_ITEMS:
        rm.item_model(item).with_lang(lang(item))
    for item in SIMPLE_FOODS:
        rm.item_model('food/%s' % item).with_lang(lang(item))
    for grain in TFC_GRAINS:
        rm.item_model('food/%s_slice' % grain).with_lang(lang('%s slice', grain))
        rm.item_model('food/%s_flatbread' % grain).with_lang(lang('%s flatbread', grain))
        rm.item_model('food/%s_dough' % grain, 'tfc:item/food/%s_dough' % grain).with_lang(lang('%s dough', grain))
        rm.item_model('tfc:food/%s_dough' % grain, 'firmalife:item/food/%s_flatbread_dough' % grain)
        rm.lang('item.tfc.food.%s_dough' % grain, lang('%s flatbread dough', grain))
    for item in SIMPLE_SPICES:
        rm.item_model('spice/%s' % item).with_lang(lang(item))
    for be in BLOCK_ENTITIES:
        rm.lang('firmalife.block_entity.%s' % be, lang(be))
    for fluid in EXTRA_FLUIDS:
        water_based_fluid(rm, fluid)

    for key, value in DEFAULT_LANG.items():
        rm.lang(key, value)


def contained_fluid(rm: ResourceManager, name_parts: utils.ResourceIdentifier, base: str, overlay: str) -> 'ItemContext':
    return rm.custom_item_model(name_parts, 'tfc:contained_fluid', {
        'parent': 'forge:item/default',
        'textures': {
            'base': base,
            'fluid': overlay
        }
    })

def flower_pot_cross(rm: ResourceManager, simple_name: str, name: str, model: str, texture: str, loot: str, tinted: bool = False):
    rm.blockstate(name, model='firmalife:block/%s' % model).with_lang(lang('potted %s', simple_name)).with_tag('minecraft:flower_pots').with_block_loot(loot, 'minecraft:flower_pot')
    rm.block_model(model, parent='minecraft:block/tinted_flower_pot_cross' if tinted else 'minecraft:block/flower_pot_cross', textures={'plant': texture, 'dirt': 'tfc:block/dirt/loam'})

def simple_plant_data(rm: ResourceManager, p: str, bees: bool = True, straw: bool = True):
    rm.block_tag('tfc:plants', p)
    rm.item_tag('tfc:plants', p)
    if bees:
        rm.block_tag('bee_restoration_plants', p)
    loot_alt = ({'name': p, 'conditions': [loot_tables.match_tag('tfc:knives')]}) if not straw else ({'name': p, 'conditions': [loot_tables.match_tag('forge:shears')]}, {'name': 'tfc:straw', 'conditions': [loot_tables.match_tag('tfc:sharp_tools')]})
    rm.block_loot(p, loot_alt)

def make_jar(rm: ResourceManager, jar: str, texture: str, lang_override: str = None) -> ItemContext:
    for i in range(1, 5):
        rm.block_model('jar/%s_%s' % (jar, i), textures={'1': texture}, parent='firmalife:block/jar_%s' % i)
    block = rm.blockstate('%s_jar' % jar, variants=dict(('count=%s' % i, {'model': 'firmalife:block/jar/%s_%s' % (jar, i)}) for i in range(1, 5)))
    block.with_lang(lang('%s jar', jar) if lang_override is None else lang_override)
    loot_pools = []
    for i in range(1, 5):
        loot_pools += [{'name': 'firmalife:%s_jar' % jar, 'conditions': [loot_tables.block_state_property('firmalife:%s_jar[count=%s]' % (jar, i))], 'functions': [loot_tables.set_count(i)]}]
    block.with_block_loot(*loot_pools)
    ctx = rm.item_model('firmalife:%s_jar' % jar, 'firmalife:item/jar/%s' % jar)
    rm.item_tag('jars', 'firmalife:%s_jar' % jar)
    return ctx

def item_model_property(rm: ResourceManager, name_parts: utils.ResourceIdentifier, overrides: utils.Json, data: Dict[str, Any]) -> ItemContext:
    res = utils.resource_location(rm.domain, name_parts)
    rm.write((*rm.resource_dir, 'assets', res.domain, 'models', 'item', res.path), {
        **data,
        'overrides': overrides
    })
    return ItemContext(rm, res)


def four_rotations(model: str, rots: Tuple[Any, Any, Any, Any], suffix: str = '', prefix: str = '') -> Dict[str, Dict[str, Any]]:
    return {
        '%sfacing=east%s' % (prefix, suffix): {'model': model, 'y': rots[0]},
        '%sfacing=north%s' % (prefix, suffix): {'model': model, 'y': rots[1]},
        '%sfacing=south%s' % (prefix, suffix): {'model': model, 'y': rots[2]},
        '%sfacing=west%s' % (prefix, suffix): {'model': model, 'y': rots[3]}
    }

def four_rotations_mp_free(model: str, rots: Tuple[Any, Any, Any, Any]) -> List:
    return [
        [{'facing': 'east'}, {'model': model, 'y': rots[0]}],
        [{'facing': 'north'}, {'model': model, 'y': rots[1]}],
        [{'facing': 'south'}, {'model': model, 'y': rots[2]}],
        [{'facing': 'west'}, {'model': model, 'y': rots[3]}]
    ]

def four_rotations_mp(model: str, rots: Tuple[Any, Any, Any, Any], condition_name: str, condition_value: Any) -> List:
    return [
        [{'facing': 'east', condition_name: condition_value}, {'model': model, 'y': rots[0]}],
        [{'facing': 'north', condition_name: condition_value}, {'model': model, 'y': rots[1]}],
        [{'facing': 'south', condition_name: condition_value}, {'model': model, 'y': rots[2]}],
        [{'facing': 'west', condition_name: condition_value}, {'model': model, 'y': rots[3]}]
    ]

def peel(rm: ResourceManager, name_parts: str, texture: str) -> 'ItemContext':
    rm.item(name_parts).with_lang(lang(name_parts))
    rm.item_model(name_parts + '_in_hand', {'particle': texture}, parent='minecraft:item/trident_in_hand')
    rm.item_model(name_parts + '_gui', texture)
    model = rm.domain + ':item/' + name_parts
    # todo: 1.19 rename to forge:separate_transforms due to deprecation
    return rm.custom_item_model(name_parts, 'forge:separate-perspective', {
        'gui_light': 'front',
        'base': {'parent': model + '_in_hand'},
        'perspectives': {
            'none': {'parent': model + '_gui'},
            'fixed': {'parent': model + '_gui'},
            'ground': {'parent': model + '_gui'},
            'gui': {'parent': model + '_gui'}
        }
    })


def greenhouse_stairs(rm: ResourceManager, name: str, frame: str, glass: str) -> 'BlockContext':
    block_name = '%s_greenhouse_roof' % name
    stair_model = 'firmalife:block/greenhouse/%s_roof' % name
    stair_model_inner = 'firmalife:block/greenhouse/%s_roof_inner' % name
    stair_model_outer = 'firmalife:block/greenhouse/%s_roof_outer' % name

    textures = {'glass': glass, 'steel': frame}
    block = rm.blockstate(block_name, variants=block_states.stairs_variants(stair_model, stair_model_inner, stair_model_outer))
    rm.block_model('greenhouse/%s_roof' % name, textures=textures, parent='firmalife:block/greenhouse_roof')
    rm.block_model('greenhouse/%s_roof_inner' % name, textures=textures, parent='firmalife:block/greenhouse_roof_inner')
    rm.block_model('greenhouse/%s_roof_outer' % name, textures=textures, parent='firmalife:block/greenhouse_roof_outer')
    rm.item_model(block_name, parent='firmalife:block/greenhouse/%s_roof' % name, no_textures=True)
    block.with_block_loot('firmalife:%s' % block_name).with_lang(lang('%s greenhouse roof', name))
    greenhouse_tags(block, name).with_tag('minecraft:stairs')
    return block

def greenhouse_slab(rm: ResourceManager, name: str, frame: str, glass: str) -> 'BlockContext':
    wall = 'firmalife:block/greenhouse/%s_wall_both' % name
    top = 'firmalife:block/greenhouse/%s_roof_top' % name
    top_upper = 'firmalife:block/greenhouse/%s_roof_top_upper' % name
    block_name = '%s_greenhouse_roof_top' % name

    textures = {'glass': glass, 'steel': frame}
    block = rm.blockstate(block_name, variants=block_states.slab_variants(wall, top, top_upper)).with_lang(lang('%s greenhouse roof top', name))
    rm.block_model('greenhouse/%s_roof_top' % name, textures, parent='firmalife:block/greenhouse_roof_top')
    rm.block_model('greenhouse/%s_roof_top_upper' % name, textures, parent='firmalife:block/greenhouse_roof_top_upper')
    rm.item_model(block_name, parent='firmalife:block/greenhouse/%s_roof_top' % name, no_textures=True)
    slab_loot(block, 'firmalife:%s' % block_name)
    greenhouse_tags(block, name).with_tag('minecraft:slabs')
    return block

def greenhouse_wall(rm: ResourceManager, name: str, frame: str, glass: str) -> 'BlockContext':
    rm.block_model('greenhouse/%s_wall' % name, {'glass': glass + '_both', 'steel': frame}, parent='firmalife:block/greenhouse_wall')
    rm.block_model('greenhouse/%s_wall_down' % name, {'glass': glass + '_down', 'steel': frame}, parent='firmalife:block/greenhouse_wall_down')
    rm.block_model('greenhouse/%s_wall_up' % name, {'glass': glass + '_up', 'steel': frame}, parent='firmalife:block/greenhouse_wall_up')
    rm.block_model('greenhouse/%s_wall_both' % name, {'glass': glass, 'steel': frame}, parent='firmalife:block/greenhouse_wall_both')

    block = rm.blockstate('%s_greenhouse_wall' % name, variants={
        'down=false,up=false': {'model': 'firmalife:block/greenhouse/%s_wall' % name},
        'down=true,up=false': {'model': 'firmalife:block/greenhouse/%s_wall_down' % name},
        'down=false,up=true': {'model': 'firmalife:block/greenhouse/%s_wall_up' % name},
        'down=true,up=true': {'model': 'firmalife:block/greenhouse/%s_wall_both' % name}
    }).with_block_loot('firmalife:%s_greenhouse_wall' % name).with_lang(lang('%s greenhouse wall', name))
    rm.item_model('%s_greenhouse_wall' % name, parent='firmalife:block/greenhouse/%s_wall_both' % name, no_textures=True)
    greenhouse_tags(block, name)
    return block

def greenhouse_door(rm: ResourceManager, name: str, bot: str, upper: str) -> 'BlockContext':
    door = '%s_greenhouse_door' % name
    door_model = 'greenhouse/%s_door' % name
    block = 'firmalife:block/greenhouse/%s_door' % name
    bottom = block + '_bottom'
    bottom_hinge = block + '_bottom_hinge'
    top = block + '_top'
    top_hinge = block + '_top_hinge'

    block = rm.blockstate(door, variants=block_states.door_blockstate(bottom, bottom_hinge, top, top_hinge)).with_lang(lang('%s greenhouse door', name))
    rm.block_model(door_model + '_bottom', {'bottom': bot}, parent='block/door_bottom')
    rm.block_model(door_model + '_bottom_hinge', {'bottom': bot}, parent='block/door_bottom_rh')
    rm.block_model(door_model + '_top', {'top': upper}, parent='block/door_top')
    rm.block_model(door_model + '_top_hinge', {'top': upper}, parent='block/door_top_rh')
    rm.item_model(door)
    door_loot(block, 'firmalife:%s' % door)
    greenhouse_tags(block, name).with_tag('minecraft:doors').with_item_tag('minecraft:doors')
    return block

def greenhouse_tags(block: BlockContext, greenhouse_name: str) -> 'BlockContext':
    block.with_tag('%s_greenhouse' % greenhouse_name).with_item_tag('%s_greenhouse' % greenhouse_name)
    if greenhouse_name in ('weathered_treated_wood', 'treated_wood'):
        block.with_tag('minecraft:mineable/axe')
    else:
        block.with_tag('minecraft:mineable/pickaxe')
    return block

def slab_loot(block: BlockContext, loot: str) -> 'BlockContext':
    return block.with_block_loot({
        'name': loot,
        'functions': [{
            'function': 'minecraft:set_count',
            'conditions': [loot_tables.block_state_property(loot + '[type=double]')],
            'count': 2,
            'add': False
        }]
    })

def door_loot(block: BlockContext, loot: str) -> 'BlockContext':
    return block.with_block_loot({'name': loot, 'conditions': [loot_tables.block_state_property(loot + '[half=lower]')]})

def water_based_fluid(rm: ResourceManager, name: str):
    rm.blockstate(('fluid', name)).with_block_model({'particle': 'minecraft:block/water_still'}, parent=None).with_lang(lang(name)).with_tag('tfc:all_fluids')
    rm.fluid_tag(name, 'firmalife:%s' % name, 'firmalife:flowing_%s' % name)
    rm.fluid_tag('minecraft:water', 'firmalife:%s' % name, 'firmalife:flowing_%s' % name)  # Need to use water fluid tag for behavior
    rm.fluid_tag('mixable', 'firmalife:%s' % name, 'firmalife:flowing_%s' % name)

    item = rm.custom_item_model(('bucket', name), 'forge:bucket', {
        'parent': 'forge:item/bucket',
        'fluid': 'firmalife:%s' % name
    })
    item.with_lang(lang('%s bucket', name))
    rm.lang('fluid.firmalife.%s' % name, lang(name))

def four_ways(model: str) -> List[Dict[str, Any]]:
    return [
        {'model': model, 'y': 90},
        {'model': model},
        {'model': model, 'y': 180},
        {'model': model, 'y': 270}
    ]

