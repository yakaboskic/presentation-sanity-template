"""Sample manim scene. Render with `npm run manim:build`.

Requires manim (community edition):  pip install manim

Output goes to public/manim/intro.webm and is referenced from slides.md
via <SlidevVideo src="/manim/intro.webm">.
"""

from manim import (  # type: ignore[import-not-found]
    Scene,
    MathTex,
    Transform,
    Write,
    FadeOut,
)


class IntroScene(Scene):
    def construct(self) -> None:
        eq1 = MathTex(r"e^{i\pi} + 1 = 0").scale(1.5)
        eq2 = MathTex(r"\sum_{n=0}^{\infty} \frac{1}{n!} = e").scale(1.5)

        self.play(Write(eq1))
        self.wait(1)
        self.play(Transform(eq1, eq2))
        self.wait(1)
        self.play(FadeOut(eq1))
