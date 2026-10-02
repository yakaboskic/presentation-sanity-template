"""The intro scene, stepped: one segment per click instead of one video.

Subclass manim_slides.Slide and end each segment with `self.next_slide()`.
With `steps: true` on the scene in manifest.yaml, `presentation-sanity
build-manim` cuts the render into public/manim/<key>/NN.webm plus a
segments.json index, and the deck's `layout: manim-steps` plays them on
Slidev clicks. Needs: pip install manim-slides
"""

from manim import FadeOut, Indicate, MathTex, Transform, Write
from manim_slides import Slide


class IntroSteps(Slide):
    # manim-slides reverses every segment with H.264, which a WebM file can't
    # hold. The deck shows the previous checkpoint's last frame on "back"
    # instead of playing backwards, so reversing isn't needed.
    skip_reversing = True

    def construct(self) -> None:
        eq1 = MathTex(r"e^{i\pi} + 1 = 0").scale(1.5)
        eq2 = MathTex(r"\sum_{n=0}^{\infty} \frac{1}{n!} = e").scale(1.5)

        self.play(Write(eq1))
        self.next_slide(notes="Transform into the series for e")

        self.play(Transform(eq1, eq2))
        self.next_slide(loop=True, notes="Loops until the next click")

        self.play(Indicate(eq1))
        self.next_slide(notes="Fade out")

        self.play(FadeOut(eq1))
