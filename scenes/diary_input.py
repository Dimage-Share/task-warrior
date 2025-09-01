import pygame, textwrap
from typing import TYPE_CHECKING
from scenes.scene_renderer import SceneRenderer

if TYPE_CHECKING:
    from ui import UIManager
    from state import GameState

class DiaryInput(SceneRenderer):
    def show(self, uiManager: 'UIManager', state: 'GameState', is_cursor_visible: bool):
        mainRect = pygame.Rect(50, 80, uiManager.screenWidth - 100, 150)
        content_y_start = uiManager.showWindow(mainRect)
        content_x = mainRect.x + uiManager.padding + 12
        uiManager.showText("きょうのできごとをどうぞ", content_x, content_y_start, font=uiManager.fontSmall, color=uiManager.colors['inactive_color'])
        inputRect = pygame.Rect(content_x, content_y_start + 35, mainRect.width - (uiManager.padding + 12) * 2, 40)
        pygame.draw.rect(uiManager.screen, uiManager.colors['background'], inputRect)
        uiManager.showText(state.inputText + "_", inputRect.x + 10, inputRect.y + 5)

        line_y = mainRect.bottom + 20
        # pygame.draw.line(uiManager.screen, uiManager.colors["window_white"], (mainRect.left, line_y), (mainRect.right, line_y), 2)
        
        y_offset = line_y + 20
        for entry in state.recentDiaryEntries:
            date_str = entry['formatted_date']
            date_surf = uiManager.fontSmall.render(date_str, True, uiManager.colors['inactive_color'])
            uiManager.screen.blit(date_surf, (mainRect.left, y_offset))
            
            wrapped_lines = textwrap.wrap(entry['content'], width=60)
            for line in wrapped_lines:
                uiManager.showText(line, mainRect.left + 256, y_offset, font=uiManager.fontSmall)
                y_offset += 10
            
            y_offset += 15
            
            if y_offset > uiManager.screenHeight - 120:
                break