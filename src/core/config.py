UPGRADES_CONFIG = [
    {'name': 'strong_fingers', 'base_price': 10, 'price_growth': 1.5, 'icon': 'textures/upgrades/strong_fingers.png', 'effect_type': 'click', 'effect_value': 1, 'unlock_condition': 0},
    {'name': 'auto_clicker', 'base_price': 50, 'price_growth': 1.7, 'icon': 'textures/upgrades/auto_clicker.png', 'effect_type': 'auto', 'effect_value': 1, 'unlock_condition': 1000},
    {'name': 'golden_touch', 'base_price': 200, 'price_growth': 1.8, 'icon': 'textures/upgrades/golden_touch.png', 'effect_type': 'click', 'effect_value': 5, 'unlock_condition': 5000},
    {'name': 'egg_farm', 'base_price': 1000, 'price_growth': 1.9, 'icon': 'textures/upgrades/egg_farm.png', 'effect_type': 'auto', 'effect_value': 10, 'unlock_condition': 20000},
    {'name': 'mega_drill', 'base_price': 5000, 'price_growth': 2.0, 'icon': 'textures/upgrades/mega_drill.png', 'effect_type': 'click', 'effect_value': 50, 'unlock_condition': 50000}
]

MILLIONAIRE_GOAL = 1_000_000

ACHIEVEMENTS_CONFIG = [
    {
        'id': 'first_click',
        'name': 'First Click',
        'description': 'Click the egg once',
        'icon_unlocked': 'textures/achievement/a1.png',
        'icon_locked': 'textures/achievement/an1.png',
        'condition': lambda ctx: ctx.total_clicks >= 1,
    },
    {
        'id': 'upgrade_master',
        'name': 'Upgrade Master',
        'description': 'Buy every upgrade',
        'icon_unlocked': 'textures/achievement/a2.png',
        'icon_locked': 'textures/achievement/an2.png',
        'condition': lambda ctx: ctx.all_upgrades_bought,
    },
    {
        'id': 'reborn',
        'name': 'Reborn!',
        'description': 'Reborn at least once',
        'icon_unlocked': 'textures/achievement/a3.png',
        'icon_locked': 'textures/achievement/an3.png',
        'condition': lambda ctx: ctx.reborn_count >= 1,
    },
    {
        'id': 'millionaire',
        'name': 'Millionaire',
        'description': 'Earn 1,000,000 clicks',
        'icon_unlocked': 'textures/achievement/a4.png',
        'icon_locked': 'textures/achievement/an4.png',
        'condition': lambda ctx: ctx.total_clicks >= MILLIONAIRE_GOAL,
    },
    {
        'id': 'fashionista',
        'name': 'Fashionista',
        'description': 'Buy every egg skin',
        'icon_unlocked': 'textures/achievement/a5.png',
        'icon_locked': 'textures/achievement/an5.png',
        'condition': lambda ctx: ctx.all_skins_unlocked,
    },
]

FPS = 60
TRANSITION_SPEED = 20
BUTTON_SIZE = (632, 144)
EGG_PRESS_DURATION = 100
EGG_SHRINK_FACTOR = 0.95