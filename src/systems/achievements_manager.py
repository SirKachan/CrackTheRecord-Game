import pygame
from src.entities.achievement import Achievement
from src.core.config import ACHIEVEMENTS_CONFIG

NAME_COLOR = (108, 73, 58)
DESC_COLOR = (143, 99, 79)
LOCKED_NAME_COLOR = (84, 84, 92)
LOCKED_DESC_COLOR = (112, 112, 120)

BAR_ASPECT = 77 / 23
ICON_FRACTION = 0.30
SCROLL_STEP = 70
COLUMNS = 2
H_GAP_FRAC = 0.08
V_GAP_FRAC = 0.20


class AchievementContext:
    def __init__(self, total_clicks, current_clicks, reborn_count,
                 all_upgrades_bought, all_skins_unlocked):
        self.total_clicks = total_clicks
        self.current_clicks = current_clicks
        self.reborn_count = reborn_count
        self.all_upgrades_bought = all_upgrades_bought
        self.all_skins_unlocked = all_skins_unlocked


class AchievementsManager:
    def __init__(self):
        self.achievements = [
            Achievement(d['id'], d['name'], d['description'],
                        d['icon_unlocked'], d['icon_locked'], d['condition'])
            for d in ACHIEVEMENTS_CONFIG
        ]
        self.scroll_offset = 0
        self._max_scroll = 0
        self._font_cache = {}
        self._icon_cache = {}

    def check(self, stats, reborn_system, upgrades_manager, skin_manager):
        context = AchievementContext(
            total_clicks=stats.total_clicks,
            current_clicks=stats.clicks,
            reborn_count=reborn_system.count,
            all_upgrades_bought=all(u.level >= 1 for u in upgrades_manager.upgrades),
            all_skins_unlocked=len(set(skin_manager.unlocked_ids)) >= len(skin_manager.skins),
        )
        for achievement in self.achievements:
            achievement.check(context)

    def to_dict(self):
        return {a.id: a.unlocked for a in self.achievements}

    def load_state(self, data):
        for achievement in self.achievements:
            if data.get(achievement.id):
                achievement.unlocked = True

    def reset_scroll(self):
        self.scroll_offset = 0

    def scroll(self, direction):
        self.scroll_offset -= direction * SCROLL_STEP
        self._clamp_scroll()

    def _clamp_scroll(self):
        self.scroll_offset = max(0, min(self.scroll_offset, self._max_scroll))

    def draw(self, screen, content_rect, alpha=255):
        bar_w, bar_h, h_gap, v_gap = self._compute_layout(content_rect)
        count = len(self.achievements)
        rows = (count + COLUMNS - 1) // COLUMNS
        grid_h = rows * bar_h + (rows - 1) * v_gap

        self._max_scroll = max(0, grid_h - content_rect.height)
        self._clamp_scroll()

        if self._max_scroll == 0:
            grid_top = content_rect.top + (content_rect.height - grid_h) // 2
        else:
            grid_top = content_rect.top - self.scroll_offset

        previous_clip = screen.get_clip()
        screen.set_clip(content_rect)
        for i, achievement in enumerate(self.achievements):
            row, col = divmod(i, COLUMNS)
            items_in_row = min(COLUMNS, count - row * COLUMNS)
            row_w = items_in_row * bar_w + (items_in_row - 1) * h_gap
            x = (content_rect.centerx - row_w // 2) + col * (bar_w + h_gap)
            y = grid_top + row * (bar_h + v_gap)
            if y + bar_h >= content_rect.top and y <= content_rect.bottom:
                self._draw_bar(screen, achievement, x, y, bar_w, bar_h, alpha)
        screen.set_clip(previous_clip)

    def _compute_layout(self, content_rect):
        rows = (len(self.achievements) + COLUMNS - 1) // COLUMNS
        width_limited = content_rect.width / (COLUMNS + (COLUMNS - 1) * H_GAP_FRAC)
        height_limited = BAR_ASPECT * content_rect.height / (rows + (rows - 1) * V_GAP_FRAC)
        bar_w = int(min(width_limited, height_limited))
        bar_h = int(bar_w / BAR_ASPECT)
        return bar_w, bar_h, int(bar_w * H_GAP_FRAC), int(bar_h * V_GAP_FRAC)

    def _draw_bar(self, screen, achievement, x, y, w, h, alpha):
        icon = self._scaled_icon(achievement, w, h)
        if alpha < 255:
            icon = icon.copy()
            icon.fill((255, 255, 255, alpha), special_flags=pygame.BLEND_RGBA_MULT)
        screen.blit(icon, (x, y))

        text_left = x + int(w * ICON_FRACTION)
        avail_w = (x + w) - text_left - int(w * 0.04)

        name_color = NAME_COLOR if achievement.unlocked else LOCKED_NAME_COLOR
        desc_color = DESC_COLOR if achievement.unlocked else LOCKED_DESC_COLOR
        name_surf = self._fit_width(self._font(h * 0.30).render(achievement.name, True, name_color), avail_w)
        desc_surf = self._fit_width(self._font(h * 0.21).render(achievement.description, True, desc_color), avail_w)
        if alpha < 255:
            for surf in (name_surf, desc_surf):
                surf.fill((255, 255, 255, alpha), special_flags=pygame.BLEND_RGBA_MULT)

        gap = int(h * 0.05)
        block_h = name_surf.get_height() + gap + desc_surf.get_height()
        text_y = y + (h - block_h) // 2
        screen.blit(name_surf, (text_left, text_y))
        screen.blit(desc_surf, (text_left, text_y + name_surf.get_height() + gap))

    def _font(self, size):
        size = max(8, int(size))
        if size not in self._font_cache:
            self._font_cache[size] = pygame.font.Font('fonts/Game_Paused_DEMO.ttf', size)
        return self._font_cache[size]

    def _scaled_icon(self, achievement, w, h):
        key = (achievement.id, achievement.unlocked, w, h)
        if key not in self._icon_cache:
            self._icon_cache[key] = pygame.transform.scale(achievement.image, (w, h))
        return self._icon_cache[key]

    @staticmethod
    def _fit_width(surf, max_w):
        if max_w <= 0 or surf.get_width() <= max_w:
            return surf
        ratio = max_w / surf.get_width()
        return pygame.transform.smoothscale(surf, (int(max_w), max(1, int(surf.get_height() * ratio))))
