"""Silent Manim proof-film for Bellman shadow pricing."""

from __future__ import annotations

import json
from pathlib import Path

from manim import (
    BLACK,
    DOWN,
    LEFT,
    RIGHT,
    UP,
    AnimationGroup,
    Arrow,
    Axes,
    BarChart,
    Circle,
    Create,
    DashedLine,
    Dot,
    FadeIn,
    FadeOut,
    GrowArrow,
    LaggedStart,
    Line,
    MathTex,
    Rectangle,
    RoundedRectangle,
    Scene,
    Text,
    Transform,
    VGroup,
    VMobject,
    Write,
    config,
)

config.background_color = "#0c0d0c"

BG = "#0c0d0c"
PANEL = "#151715"
LINE = "#32362f"
INK = "#ece9df"
MUTED = "#9da397"
GOLD = "#d8ae52"
GREEN = "#91c987"
RED = "#d9736a"
BLUE = "#72a8c8"
SANS = "Segoe UI"
MONO = "Cascadia Mono"


class BellmanShadowPricingFilm(Scene):
    """A 75–90 second silent proof-film derived from certified evidence."""

    def construct(self) -> None:
        data = json.loads(
            Path(__file__).with_name("scene_data.json").read_text(encoding="utf-8")
        )
        self.camera.background_color = BG
        self.title_scene()
        self.fabricpc_enters()
        self.scalar_failure()
        self.whole_action_charge()
        self.bellman_equivalence(data)
        self.belief_boundary(data)
        self.experimental_result(data)
        self.closing_card()

    def heading(self, kicker: str, title: str) -> VGroup:
        kicker_text = Text(kicker.upper(), font=MONO, font_size=22, color=GOLD)
        title_text = Text(title, font=SANS, font_size=42, color=INK, weight="BOLD")
        return VGroup(kicker_text, title_text).arrange(DOWN, aligned_edge=LEFT, buff=0.16)

    def clear(self, *objects: VMobject, run_time: float = 0.6) -> None:
        self.play(*[FadeOut(obj) for obj in objects], run_time=run_time)

    def value_curve(self, axes: Axes) -> VMobject:
        points = [
            axes.c2p(0.0, 0.2),
            axes.c2p(1.0, 0.55),
            axes.c2p(2.0, 0.78),
            axes.c2p(3.0, 1.85),
            axes.c2p(4.0, 2.08),
            axes.c2p(5.0, 2.31),
            axes.c2p(6.0, 3.45),
        ]
        curve = VMobject(color=GOLD, stroke_width=6)
        curve.set_points_as_corners(points)
        return curve

    def title_scene(self) -> None:
        title = Text(
            "BELLMAN SHADOW PRICING",
            font=SANS,
            font_size=58,
            color=INK,
            weight="BOLD",
        ).to_edge(UP, buff=0.55)
        subtitle = Text(
            "The missing action-pricing mechanism.",
            font=SANS,
            font_size=31,
            color=GOLD,
        ).next_to(title, DOWN, buff=0.22)
        router = RoundedRectangle(
            width=4.3, height=1.35, corner_radius=0.18, color=LINE, fill_color=PANEL, fill_opacity=1
        ).shift(DOWN * 0.55 + LEFT * 2.3)
        router_text = Text("FEASIBILITY-FIRST ROUTER", font=MONO, font_size=25, color=INK).move_to(router)
        signal = RoundedRectangle(
            width=3.6, height=1.35, corner_radius=0.18, color=MUTED, fill_color=PANEL, fill_opacity=1
        ).shift(DOWN * 0.55 + RIGHT * 2.65)
        signal_text = VGroup(
            Text("shadow-price signal", font=MONO, font_size=23, color=MUTED),
            Text("diagnostic only", font=SANS, font_size=22, color=RED),
            Text("not trusted for selection", font=SANS, font_size=20, color=RED),
        ).arrange(DOWN, buff=0.1).move_to(signal)
        crossed = Line(signal.get_corner(UP + LEFT), signal.get_corner(DOWN + RIGHT), color=RED, stroke_width=4)
        history = VGroup(
            Text("Compitum had prices.", font=SANS, font_size=34, color=INK, weight="BOLD"),
            Text("It did not let them choose.", font=SANS, font_size=34, color=GOLD, weight="BOLD"),
        ).arrange(DOWN, buff=0.16).to_edge(DOWN, buff=0.45)
        self.play(FadeIn(title, shift=DOWN * 0.2), Write(subtitle), run_time=1.3)
        self.play(FadeIn(router), FadeIn(router_text), FadeIn(signal), FadeIn(signal_text), run_time=1.4)
        self.play(Create(crossed), run_time=0.6)
        self.play(FadeIn(history, shift=UP * 0.15), run_time=0.8)
        self.wait(2.1)
        self.clear(title, subtitle, router, router_text, signal, signal_text, crossed, history, run_time=0.8)

    def fabricpc_enters(self) -> None:
        heading = self.heading("The intervention", "Can hidden scarcity become a routing price?")
        heading.to_corner(UP + LEFT, buff=0.55)
        labels = VGroup(
            Text("history", font=MONO, font_size=27, color=INK),
            Text("hidden scarcity belief", font=MONO, font_size=27, color=BLUE),
            Text("routing price", font=MONO, font_size=27, color=GOLD),
            Text("action", font=MONO, font_size=27, color=GREEN),
        ).arrange(RIGHT, buff=1.0).shift(DOWN * 0.35)
        arrows = VGroup(
            *[
                Arrow(labels[i].get_right(), labels[i + 1].get_left(), color=MUTED, buff=0.14)
                for i in range(3)
            ]
        )
        fabricpc = Text("FabricPC", font=SANS, font_size=38, color=BLUE, weight="BOLD")
        fabricpc.next_to(labels[1], UP, buff=0.6)
        fracture = VGroup(
            Line(arrows[2].get_center() + UP * 0.22, arrows[2].get_center() + DOWN * 0.22, color=RED, stroke_width=6),
            Line(arrows[2].get_center() + LEFT * 0.22, arrows[2].get_center() + RIGHT * 0.22, color=RED, stroke_width=6),
        )
        verdict = Text(
            "The predictor was not the whole problem.",
            font=SANS,
            font_size=34,
            color=INK,
            weight="BOLD",
        ).to_edge(DOWN, buff=0.65)
        self.play(FadeIn(heading), FadeIn(fabricpc), run_time=1.0)
        self.play(LaggedStart(*[FadeIn(label) for label in labels], lag_ratio=0.16), run_time=1.4)
        self.play(LaggedStart(*[GrowArrow(arrow) for arrow in arrows], lag_ratio=0.2), run_time=1.4)
        self.play(Create(fracture), run_time=0.7)
        self.play(FadeIn(verdict, shift=UP * 0.15), run_time=0.7)
        self.wait(2.0)
        self.clear(heading, labels, arrows, fabricpc, fracture, verdict, run_time=0.7)
    def scalar_failure(self) -> None:
        heading = self.heading("The defect", "The price-to-action interface was wrong.")
        heading.to_corner(UP + LEFT, buff=0.55)
        axes = Axes(
            x_range=[0, 6, 1],
            y_range=[0, 4, 1],
            x_length=8.1,
            y_length=4.2,
            axis_config={"color": LINE, "include_ticks": False},
        ).shift(DOWN * 0.55 + LEFT * 1.25)
        curve = self.value_curve(axes)
        b_point = axes.c2p(5.5, 2.75)
        after_point = axes.c2p(2.1, 0.88)
        local = Line(axes.c2p(4.7, 2.25), axes.c2p(5.9, 2.52), color=BLUE, stroke_width=5)
        local_label = MathTex(r"\lambda(B)", color=BLUE, font_size=38).next_to(
            local, UP, buff=0.12
        )
        action = Arrow(b_point, after_point, color=RED, buff=0.05, stroke_width=6)
        action_label = MathTex(r"c(a)", color=RED, font_size=38).next_to(action, DOWN)
        approx = MathTex(r"\lambda(B)\,\cdot\,c(a)", color=BLUE, font_size=48)
        approx.to_edge(RIGHT, buff=0.65).shift(DOWN * 0.1)
        actual = MathTex(r"V(B)-V(B-c(a))", color=GOLD, font_size=43)
        actual.next_to(approx, DOWN, buff=0.55)
        not_equal = MathTex(r"\neq", color=RED, font_size=48).move_to(
            (approx.get_bottom() + actual.get_top()) / 2
        )
        lesson = Text(
            "Better belief cannot repair λ × lumpy consumption.",
            font=SANS,
            font_size=30,
            color=INK,
            weight="BOLD",
        ).to_edge(DOWN, buff=0.5)
        self.play(FadeIn(heading), Create(axes), Create(curve), run_time=1.2)
        self.play(Create(local), FadeIn(local_label), run_time=1.0)
        self.play(GrowArrow(action), FadeIn(action_label), run_time=1.2)
        self.play(Write(approx), run_time=0.9)
        self.play(Write(actual), FadeIn(not_equal), run_time=1.1)
        self.play(FadeIn(lesson, shift=UP * 0.15), run_time=0.8)
        self.wait(5.4)
        self.clear(
            heading,
            axes,
            curve,
            local,
            local_label,
            action,
            action_label,
            approx,
            actual,
            not_equal,
            lesson,
        )

    def whole_action_charge(self) -> None:
        heading = self.heading("The correction", "Charge the continuation-value loss.")
        heading.to_corner(UP + LEFT, buff=0.55)
        equation = MathTex(
            r"C_t(a)",
            r"=",
            r"V_{t+1}(B_t,q_{t+1})",
            r"-",
            r"V_{t+1}(B_t-c_t(a),q_{t+1})",
            font_size=45,
            color=INK,
        ).shift(UP * 1.15)
        equation[0].set_color(GOLD)
        left_box = RoundedRectangle(width=3.7, height=1.25, corner_radius=0.15, color=BLUE)
        right_box = left_box.copy().set_color(RED)
        left_box.move_to(LEFT * 3.0 + DOWN * 0.65)
        right_box.move_to(RIGHT * 3.0 + DOWN * 0.65)
        left_label = Text("value before action", font=MONO, font_size=23, color=BLUE)
        right_label = Text("value after action", font=MONO, font_size=23, color=RED)
        left_label.move_to(left_box)
        right_label.move_to(right_box)
        difference = Arrow(
            left_box.get_right(),
            right_box.get_left(),
            color=GOLD,
            stroke_width=6,
            buff=0.12,
        )
        units = VGroup(
            *[
                Rectangle(width=0.65, height=0.65, color=GOLD, fill_opacity=0.16)
                for _ in range(5)
            ]
        ).arrange(RIGHT, buff=0.12)
        units.shift(DOWN * 2.15)
        unit_label = MathTex(
            r"\sum_{j=1}^{k}\lambda_{\mathrm{unit}}[j]",
            color=GOLD,
            font_size=38,
        ).next_to(units, LEFT, buff=0.42)
        collapsed = MathTex(r"V(B,q)-V(B-k\delta,q)", color=GOLD, font_size=42)
        collapsed.move_to(VGroup(unit_label, units))
        payoff = Text(
            "Shadow pricing returns — no longer as a local tangent.",
            font=SANS,
            font_size=34,
            color=GREEN,
            weight="BOLD",
        ).to_edge(DOWN, buff=0.42)
        self.play(FadeIn(heading), Write(equation), run_time=1.5)
        self.play(
            LaggedStart(
                FadeIn(left_box),
                FadeIn(left_label),
                FadeIn(right_box),
                FadeIn(right_label),
                GrowArrow(difference),
                lag_ratio=0.15,
            ),
            run_time=2.0,
        )
        self.play(
            FadeIn(unit_label),
            LaggedStart(*[FadeIn(unit, shift=RIGHT * 0.15) for unit in units], lag_ratio=0.1),
            run_time=1.7,
        )
        unit_group = VGroup(unit_label, units)
        self.play(Transform(unit_group, collapsed), run_time=1.5)
        self.play(FadeIn(payoff, shift=UP * 0.15), run_time=0.8)
        self.wait(5.7)
        self.clear(
            heading,
            equation,
            left_box,
            left_label,
            right_box,
            right_label,
            difference,
            unit_group,
            payoff,
        )

    def bellman_equivalence(self, data: dict[str, object]) -> None:
        mismatch_count = data["online_equivalence"]["mismatch_count"]  # type: ignore[index]
        heading = self.heading("Exact equivalence", "Two rankings. One selected action.")
        heading.to_corner(UP + LEFT, buff=0.55)
        left_panel = RoundedRectangle(
            width=5.5, height=4.1, corner_radius=0.18, color=LINE, fill_color=PANEL, fill_opacity=1
        ).shift(LEFT * 3.0 + DOWN * 0.55)
        right_panel = left_panel.copy().shift(RIGHT * 6.0)
        left_title = Text(
            "Immediate utility − action charge",
            font=SANS,
            font_size=25,
            color=GOLD,
        ).next_to(left_panel.get_top(), DOWN, buff=0.38)
        right_title = Text("Bellman Q", font=SANS, font_size=25, color=BLUE)
        right_title.next_to(right_panel.get_top(), DOWN, buff=0.38)
        actions_left = VGroup(
            *[Text(f"action {name}", font=MONO, font_size=24, color=MUTED) for name in "ABC"]
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.48).move_to(left_panel)
        actions_right = actions_left.copy().move_to(right_panel)
        winner_left = Arrow(
            actions_left[1].get_left() + LEFT * 0.8,
            actions_left[1].get_left() + LEFT * 0.12,
            color=GREEN,
            buff=0,
        )
        winner_right = Arrow(
            actions_right[1].get_left() + LEFT * 0.8,
            actions_right[1].get_left() + LEFT * 0.12,
            color=GREEN,
            buff=0,
        )
        facts = VGroup(
            Text("choices identical", font=MONO, font_size=23, color=GREEN),
            Text("cumulative utility identical", font=MONO, font_size=23, color=GREEN),
            Text(f"mismatches = {mismatch_count}", font=MONO, font_size=23, color=GREEN),
        ).arrange(RIGHT, buff=0.7).to_edge(DOWN, buff=0.5)
        self.play(
            FadeIn(heading),
            FadeIn(left_panel),
            FadeIn(right_panel),
            FadeIn(left_title),
            FadeIn(right_title),
            run_time=1.3,
        )
        self.play(
            LaggedStart(
                *[FadeIn(item, shift=RIGHT * 0.2) for item in actions_left],
                *[FadeIn(item, shift=RIGHT * 0.2) for item in actions_right],
                lag_ratio=0.1,
            ),
            run_time=1.8,
        )
        self.play(GrowArrow(winner_left), GrowArrow(winner_right), run_time=1.0)
        merge_dot = Dot(DOWN * 2.1, color=GREEN, radius=0.12)
        merge_lines = VGroup(
            Line(winner_left.get_end(), merge_dot.get_center(), color=GREEN),
            Line(winner_right.get_end(), merge_dot.get_center(), color=GREEN),
        )
        self.play(Create(merge_lines), FadeIn(merge_dot), run_time=1.1)
        self.play(LaggedStart(*[FadeIn(fact) for fact in facts], lag_ratio=0.2), run_time=1.4)
        self.wait(4.7)
        self.clear(
            heading,
            left_panel,
            right_panel,
            left_title,
            right_title,
            actions_left,
            actions_right,
            winner_left,
            winner_right,
            merge_lines,
            merge_dot,
            facts,
        )

    def belief_boundary(self, data: dict[str, object]) -> None:
        boundary = data["certified_boundary"]  # type: ignore[index]
        heading = self.heading("Certified state", "Belief changes the optimal action.")
        heading.to_corner(UP + LEFT, buff=0.55)
        state = VGroup(
            Text("remaining steps = 1", font=MONO, font_size=23, color=MUTED),
            Text("budget = 4.5", font=MONO, font_size=23, color=MUTED),
            Text("opportunity observed", font=MONO, font_size=23, color=MUTED),
        ).arrange(RIGHT, buff=0.65).next_to(heading, DOWN, aligned_edge=LEFT, buff=0.45)
        low = boundary["low"]  # type: ignore[index]
        high = boundary["high"]  # type: ignore[index]
        low_panel = RoundedRectangle(
            width=4.6, height=2.65, corner_radius=0.2, color=GOLD, fill_color=PANEL, fill_opacity=1
        ).shift(LEFT * 3.2 + DOWN * 0.65)
        high_panel = low_panel.copy().set_stroke(BLUE).set_fill(PANEL).shift(RIGHT * 6.4)
        low_text = VGroup(
            Text(f"q = {low['belief']:.2f}", font=MONO, font_size=34, color=GOLD),
            Text(str(low["action"]).upper(), font=SANS, font_size=46, color=INK, weight="BOLD"),
        ).arrange(DOWN, buff=0.3).move_to(low_panel)
        high_text = VGroup(
            Text(f"q = {high['belief']:.2f}", font=MONO, font_size=34, color=BLUE),
            Text(str(high["action"]).upper(), font=SANS, font_size=42, color=INK, weight="BOLD"),
        ).arrange(DOWN, buff=0.3).move_to(high_panel)
        band = DashedLine(
            low_panel.get_right(),
            high_panel.get_left(),
            dash_length=0.12,
            color=MUTED,
        )
        statement = VGroup(
            Text(
                "Belief crosses a genuine action boundary.",
                font=SANS,
                font_size=31,
                color=GREEN,
                weight="BOLD",
            ),
            Text(
                "Exact transition point not asserted.",
                font=MONO,
                font_size=23,
                color=MUTED,
            ),
        ).arrange(DOWN, buff=0.18).to_edge(DOWN, buff=0.45)
        self.play(FadeIn(heading), FadeIn(state), run_time=1.2)
        self.play(FadeIn(low_panel), FadeIn(low_text), run_time=1.0)
        self.play(Create(band), run_time=0.8)
        self.play(FadeIn(high_panel), FadeIn(high_text), run_time=1.0)
        self.play(FadeIn(statement, shift=UP * 0.15), run_time=0.9)
        self.wait(6.1)
        self.clear(heading, state, low_panel, low_text, high_panel, high_text, band, statement)

    def experimental_result(self, data: dict[str, object]) -> None:
        regrets = data["tranche7_regret"]  # type: ignore[index]
        heading = self.heading("Tranche 7", "One experiment. Two verdicts.")
        heading.to_corner(UP + LEFT, buff=0.55)
        model_panel = RoundedRectangle(
            width=5.7, height=4.7, corner_radius=0.2, color=RED, fill_color=PANEL, fill_opacity=1
        ).shift(LEFT * 3.0 + DOWN * 0.55)
        program_panel = model_panel.copy().set_stroke(GREEN).set_fill(PANEL).shift(RIGHT * 6.0)
        model = VGroup(
            Text("MODEL VERDICT", font=MONO, font_size=22, color=RED),
            Text("Fixed FabricPC topology", font=SANS, font_size=29, color=INK, weight="BOLD"),
            Text("did not clear the gate.", font=SANS, font_size=28, color=RED),
            Text(f"PCN = backprop = {regrets['fabricpc_pcn']:.3f}", font=MONO, font_size=22, color=BLUE),
            Text(f"{data['fabricpc_recoverable_gap_percent']:.1f}% recovered", font=MONO, font_size=25, color=GOLD),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).move_to(model_panel)
        program = VGroup(
            Text("PROGRAM VERDICT", font=MONO, font_size=22, color=GREEN),
            Text("FabricPC exposed", font=SANS, font_size=29, color=INK, weight="BOLD"),
            Text("the missing mechanism.", font=SANS, font_size=28, color=GREEN),
            Text("Exact Bellman charge", font=MONO, font_size=23, color=GOLD),
            Text("recovered the full gap.", font=SANS, font_size=27, color=GREEN, weight="BOLD"),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).move_to(program_panel)
        footer = Text(
            "The predictor failed its gate.  The intervention recovered the right economics.",
            font=SANS,
            font_size=27,
            color=INK,
            weight="BOLD",
        ).to_edge(DOWN, buff=0.35)
        self.play(FadeIn(heading), FadeIn(model_panel), FadeIn(program_panel), run_time=1.2)
        self.play(LaggedStart(*[FadeIn(line, shift=RIGHT * 0.12) for line in model], lag_ratio=0.15), run_time=1.6)
        self.play(LaggedStart(*[FadeIn(line, shift=LEFT * 0.12) for line in program], lag_ratio=0.15), run_time=1.6)
        self.play(FadeIn(footer, shift=UP * 0.12), run_time=0.8)
        self.wait(5.8)
        self.clear(heading, model_panel, program_panel, model, program, footer, run_time=0.7)
    def closing_card(self) -> None:
        model = VGroup(
            Text("THE FABRICPC PREDICTOR", font=SANS, font_size=40, color=INK, weight="BOLD"),
            Text("DID NOT CLEAR THE GATE.", font=SANS, font_size=40, color=RED, weight="BOLD"),
        ).arrange(DOWN, buff=0.08)
        program = VGroup(
            Text("THE FABRICPC INTERVENTION", font=SANS, font_size=40, color=INK, weight="BOLD"),
            Text("RECOVERED THE RIGHT ECONOMICS.", font=SANS, font_size=40, color=GREEN, weight="BOLD"),
        ).arrange(DOWN, buff=0.08)
        resolution = Text(
            "The model lost.  The experiment succeeded.",
            font=SANS,
            font_size=32,
            color=GOLD,
            weight="BOLD",
        )
        provenance = VGroup(
            Text("Compitum × FabricPC", font=MONO, font_size=17, color=MUTED),
            Text("Bellman Shadow Pricing", font=MONO, font_size=17, color=MUTED),
            Text("certified executable evidence", font=MONO, font_size=17, color=GREEN),
        ).arrange(RIGHT, buff=0.35)
        marks = VGroup(
            *[
                VGroup(
                    Circle(radius=0.18, color=GREEN, fill_color=GREEN, fill_opacity=1),
                    Text("✓", font=SANS, font_size=18, color=BLACK),
                )
                for _ in range(4)
            ]
        ).arrange(RIGHT, buff=0.3)
        group = VGroup(model, program, resolution, provenance, marks).arrange(DOWN, buff=0.38)
        self.play(FadeIn(model, shift=DOWN * 0.2), run_time=1.0)
        self.play(FadeIn(program, shift=DOWN * 0.2), run_time=1.0)
        self.play(FadeIn(resolution), run_time=0.8)
        self.play(FadeIn(provenance), LaggedStart(*[FadeIn(mark) for mark in marks], lag_ratio=0.2), run_time=1.1)
        self.wait(4.8)