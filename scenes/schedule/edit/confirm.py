from typing import TYPE_CHECKING
from scenes.scene_renderer import SceneRenderer
from ..create.confirm import Confirm as CreateConfirmScene

if TYPE_CHECKING:
    from ui import UIManager
    from state import GameState

class Confirm(SceneRenderer):
    def show(self, uiManager: 'UIManager', state: 'GameState', is_cursor_visible: bool):
        CreateConfirmScene(self.config).show(uiManager, state, is_cursor_visible)