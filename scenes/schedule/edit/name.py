from typing import TYPE_CHECKING
from scenes.scene_renderer import SceneRenderer
from ..create.name import Name as CreateNameScene

if TYPE_CHECKING:
    from ui import UIManager
    from state import GameState

class Name(SceneRenderer):
    def show(self, uiManager: 'UIManager', state: 'GameState', is_cursor_visible: bool):
        CreateNameScene(self.config).show(uiManager, state, is_cursor_visible, prompt="よていのなまえをへんしゅう")