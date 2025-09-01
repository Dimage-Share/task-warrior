from typing import TYPE_CHECKING
from scenes.scene_renderer import SceneRenderer
from ..create.days import Days as CreateDaysScene

if TYPE_CHECKING:
    from ui import UIManager
    from state import GameState

class Days(SceneRenderer):
    def show(self, uiManager: 'UIManager', state: 'GameState', is_cursor_visible: bool):
        CreateDaysScene(self.config).show(uiManager, state, is_cursor_visible)