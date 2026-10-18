"""One source, every printout: the idea behind this project, animated.

A number lives once in manifest.yaml. The deck, the blog post, the PDF and
the PPTX all read it from there, so changing it once changes every printout
together.

Text only (no MathTex), so rendering needs manim's own dependencies but no
LaTeX. `presentation-sanity build-manim` renders it to
public/manim/one_source.webm; the deck shows it full-screen (`layout: manim`,
`scene: one_source`) and the blog inline (`<ManimFigure scene="one_source" />`).
"""

from manim import (  # type: ignore[import-not-found]
    DOWN,
    LEFT,
    RIGHT,
    UP,
    AnimationGroup,
    Arrow,
    FadeIn,
    GrowArrow,
    Indicate,
    LaggedStart,
    RoundedRectangle,
    Scene,
    ShowPassingFlash,
    Text,
    Transform,
    VGroup,
)

OLD, NEW = "11,982", "12,453"

SANS, MONO = "sans-serif", "monospace"
INK = "#e2e8f0"
MUTED = "#94a3b8"
ACCENT = "#7fb3c4"  # the deck's teal, lifted for a black background
FRESH = "#4ade80"

OUTPUTS = ("Slides", "Blog post", "PDF", "PowerPoint")


def number(value: str, color: str = INK) -> Text:
    return Text(value, font=MONO, font_size=30, color=color)


class OneSource(Scene):
    def construct(self) -> None:
        # The source: one line of manifest.yaml.
        source_box = RoundedRectangle(
            width=5.6, height=2.1, corner_radius=0.2, stroke_color=ACCENT, stroke_width=3
        ).shift(LEFT * 3.85)
        filename = Text("manifest.yaml", font=MONO, font_size=22, color=MUTED)
        filename.next_to(source_box.get_top(), DOWN, buff=0.3)
        key = Text("num_samples:", font=MONO, font_size=30, color=INK)
        value = number(OLD, ACCENT)
        line = VGroup(key, value).arrange(RIGHT, buff=0.25).move_to(source_box).shift(DOWN * 0.2)
        source = VGroup(source_box, filename, line)

        # The printouts, each showing the number it read.
        cards, values, arrows = VGroup(), [], VGroup()
        for i, label in enumerate(OUTPUTS):
            box = RoundedRectangle(
                width=4.4, height=1.1, corner_radius=0.16, stroke_color=MUTED, stroke_width=2
            ).move_to(RIGHT * 3.9 + UP * (2.25 - i * 1.5))
            name = Text(label, font=SANS, font_size=26, color=INK)
            name.move_to(box.get_left() + RIGHT * (name.width / 2 + 0.35))
            shown = number(OLD)
            shown.move_to(box.get_right() + LEFT * (shown.width / 2 + 0.35))
            cards.add(VGroup(box, name, shown))
            values.append(shown)
            arrows.add(
                Arrow(
                    source_box.get_right(), box.get_left(), buff=0.15, stroke_width=3,
                    color=MUTED, max_tip_length_to_length_ratio=0.06,
                )
            )

        self.play(FadeIn(source, shift=RIGHT * 0.3), run_time=0.9)
        self.play(
            LaggedStart(
                *(AnimationGroup(GrowArrow(a), FadeIn(c, shift=RIGHT * 0.2)) for a, c in zip(arrows, cards)),
                lag_ratio=0.3,
            ),
            run_time=2.2,
        )
        self.wait(0.8)

        # Edit the one line…
        edit = Text("edit once", font=SANS, font_size=24, color=FRESH)
        edit.next_to(source_box, UP, buff=0.25)
        new_value = number(NEW, FRESH).move_to(value, aligned_edge=LEFT)
        self.play(FadeIn(edit, shift=DOWN * 0.15), Indicate(value, color=FRESH), run_time=0.8)
        self.play(Transform(value, new_value), source_box.animate.set_stroke(FRESH), run_time=0.7)

        # …and every printout follows.
        self.play(
            *(ShowPassingFlash(a.copy().set_color(FRESH), time_width=0.6) for a in arrows),
            run_time=1.0,
        )
        self.play(
            *(
                Transform(v, number(NEW, FRESH).move_to(v, aligned_edge=RIGHT))
                for v in values
            ),
            *(c[0].animate.set_stroke(FRESH) for c in cards),
            run_time=0.8,
        )
        self.wait(2.0)
