$ErrorActionPreference = "Stop"

$videoDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$repoRoot = (Resolve-Path (Join-Path $videoDir "..\..")).Path
$mediaDir = Join-Path $repoRoot "BGI-Open-Build\media"
$manimOutput = Join-Path $repoRoot ".manim-media\videos\bellman_shadow_pricing\1080p30\BellmanShadowPricingFilm.mp4"
$finalVideo = Join-Path $mediaDir "bellman-shadow-pricing.mp4"
$poster = Join-Path $mediaDir "bellman-shadow-pricing-poster.png"

python (Join-Path $videoDir "build_scene_data.py")
manim --config_file (Join-Path $videoDir "manim.cfg") --resolution 1920,1080 --fps 30 `
  (Join-Path $videoDir "bellman_shadow_pricing.py") BellmanShadowPricingFilm
if ($LASTEXITCODE -ne 0) { throw "Manim render failed with exit code $LASTEXITCODE" }

New-Item -ItemType Directory -Force -Path $mediaDir | Out-Null
ffmpeg -y -i $manimOutput -c:v libx264 -preset slow -crf 20 `
  -pix_fmt yuv420p -movflags +faststart -an $finalVideo
if ($LASTEXITCODE -ne 0) { throw "FFmpeg normalization failed with exit code $LASTEXITCODE" }
ffmpeg -y -ss 00:00:04 -i $finalVideo -frames:v 1 $poster
if ($LASTEXITCODE -ne 0) { throw "Poster extraction failed with exit code $LASTEXITCODE" }

Write-Output "Rendered $finalVideo"
Write-Output "Poster $poster"
