# Bellman Shadow Pricing proof-film

This directory contains the authored, deterministic Manim construction for the
silent BGI Open Build proof-film. It is a new film derived from the published
Bellman shadow-pricing narrative and certified Notebook Compiler evidence.

The storyboard preserves the research program's two-level verdict: the bounded FabricPC
predictor did not clear its economic gate, while using FabricPC as a research instrument
exposed the scalar price-to-action defect and recovered Compitum's exact Bellman action
charge. The film does not claim that predictive coding beat backprop, that FabricPC
directly produced zero regret, or that the exact Bellman oracle was learned.

`build_scene_data.py` reads narrative Markdown and public evidence artifacts as
data. It does not import or execute Compitum. `bellman_shadow_pricing.py` renders
the single `BellmanShadowPricingFilm` scene from `scene_data.json`.

## Rebuild

From the repository root on Windows:

```powershell
.\BGI-Open-Build\video\render.ps1
```

The resolved render used Manim Community 0.20.1, Python 3.13.4, FFmpeg 8.0,
MiKTeX 25.4, Segoe UI, and Cascadia Mono. Manim intermediates are written below
the ignored `video/.manim-media/` directory. The final H.264 video and poster are
written to `BGI-Open-Build/media/`.

Run the deterministic data check with:

```powershell
python BGI-Open-Build\video\build_scene_data.py --check
```

The accepted research commits, evidence bundle hash, certificate hashes,
displayed claims, and their source paths are recorded in `scene_data.json`.
