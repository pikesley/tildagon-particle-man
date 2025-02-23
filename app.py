from events.input import BUTTON_TYPES, Buttons
from system.eventbus import eventbus
from system.patterndisplay.events import PatternDisable

import app

from .lib.background import Background
from .lib.particle import Particle


class Collider(app.App):
    """Collider."""

    def __init__(self):
        """Construct."""
        eventbus.emit(PatternDisable())
        self.button_states = Buttons(self)
        self.part = Particle(x=0, y=0, mass=1, speed=1, angle=90)

    def update(self, _):
        """Update."""
        self.scan_buttons()
        self.part.move()

    def draw(self, ctx):
        """Draw."""
        self.overlays = []
        self.overlays.append(Background(colour=(0, 0, 0)))

        self.overlays.append(self.part)

        self.draw_overlays(ctx)

    def scan_buttons(self):
        """Buttons."""
        if self.button_states.get(BUTTON_TYPES["CANCEL"]):
            self.button_states.clear()
            self.minimise()


__app_export__ = Collider
