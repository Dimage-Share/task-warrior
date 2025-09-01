from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ui import UIManager
    from state import GameState

class SceneRenderer:
    def __init__(self, config):
        self.config = config
        
    def show(self, uiManager: 'UIManager', state: 'GameState', is_cursor_visible: bool):
        pass