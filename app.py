# https://thecodingtrain.com/challenges/184-elastic-collisions
from random import randint, random

from events.input import BUTTON_TYPES, Buttons
from system.eventbus import eventbus
from system.patterndisplay.events import PatternDisable
from tildagonos import tildagonos

import app

from .lib.background import Background
from .lib.conf import conf
from .lib.gamma import gamma_corrections
from .lib.particle import Particle
from .pikesley.rgb_from_hue.rgb_from_hue import rgb_from_hue


class ParticleMan(app.App):
    """Particle Man."""

    def __init__(self):
        """Construct."""
        eventbus.emit(PatternDisable())
        self.button_states = Buttons(self)
        self.background_hue = random()
        self.particle_count = conf["particles"]["count"]
        self.annotate = False
        self.fancy_bounce = True
        self.reset_particles()

    def reset_particles(self):
        """Reset the particles."""
        self.background_hue = random()
        self.particles = []
        for _ in range(self.particle_count):
            self.particles.append(
                Particle(
                    x=randint(-100, 100),
                    y=randint(-100, 100),
                    mass=randint(*conf["particles"]["mass-range"]),
                    speed=randint(*conf["particles"]["speed-range"]),
                    angle=random() * 360,
                    hue=self.background_hue,
                    annotate=self.annotate,
                    fancy_bounce=self.fancy_bounce,
                )
            )
        self.kinetic_energy = sum(
            [particle.kinetic_energy for particle in self.particles]
        )

    def update(self, _):
        """Update."""
        self.scan_buttons()
        for particle in self.particles:
            particle.move()

        for i in range(len(self.particles)):
            for j in range(i + 1, len(self.particles)):
                self.particles[i].collide(self.particles[j], self.background_hue)

        self.kinetic_energy = sum(
            [particle.kinetic_energy for particle in self.particles]
        )

        self.light_leds()
        self.background_hue += conf["background-colour"]["rate-of-change"]

    def draw(self, ctx):
        """Draw."""
        self.overlays = []

        self.overlays.append(
            Background(
                colour=[
                    c * conf["background-colour"]["intensity"]
                    for c in rgb_from_hue(self.background_hue)
                ]
            )
        )

        for particle in self.particles:
            self.overlays.append(particle)

        self.draw_overlays(ctx)

        if self.annotate:
            ctx.move_to(0, 0)
            ctx.rgb(*rgb_from_hue(self.background_hue + 0.5))
            ctx.text_align = ctx.CENTER
            ctx.text_baseline = ctx.MIDDLE
            ctx.font_size = 40
            ctx.text(f"{self.kinetic_energy:0.2f}")

    def scan_buttons(self):
        """Buttons."""
        if self.button_states.get(BUTTON_TYPES["CANCEL"]):
            self.button_states.clear()
            self.minimise()

        if self.button_states.get(BUTTON_TYPES["LEFT"]):
            self.button_states.clear()
            self.annotate = not self.annotate
            for particle in self.particles:
                particle.annotate = self.annotate

        if self.button_states.get(BUTTON_TYPES["RIGHT"]):
            self.button_states.clear()
            self.fancy_bounce = not self.fancy_bounce
            for particle in self.particles:
                particle.fancy_bounce = self.fancy_bounce

        if self.button_states.get(BUTTON_TYPES["CONFIRM"]):
            self.button_states.clear()
            self.reset_particles()

    def light_leds(self):
        """Light lights."""
        brightness = conf["led-brightness"]
        if (
            any(particle.colliding_counter > 0 for particle in self.particles)
            and self.fancy_bounce
        ):
            brightness *= 1.05

        colour = [
            gamma_corrections[int(c * brightness * 255)]
            for c in rgb_from_hue(self.background_hue)
        ]

        for index in range(12):
            tildagonos.leds[index + 1] = colour

        tildagonos.leds.write()


__app_export__ = ParticleMan
