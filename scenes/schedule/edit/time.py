from typing import TYPE_CHECKING
from scenes.scene_renderer import SceneRenderer
from ..create.time import Time as CreateTimeScene

if TYPE_CHECKING:
    from ui import UIManager
    from state import GameState

class Time(SceneRenderer):
    def show(self, uiManager: 'UIManager', state: 'GameState', is_cursor_visible: bool):
        CreateTimeScene(self.config).show(uiManager, state, is_cursor_visible, prompt="じこくをへんしゅう (HH:MM)")