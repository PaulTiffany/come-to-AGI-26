$ErrorActionPreference = "Stop"

$videoDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$repoRoot = (Resolve-Path (Join-Path $videoDir "..\..")).Path
$mediaDir = Join-Path $repoRoot "BGI-Open-Build\media"
$manimOutput = Join-Path $repoRoot ".manim-media\videos\bellman_shadow_pricing\1080p30\BellmanShadowPricingFilm.mp4"
$normalizedFilm = Join-Path $repoRoot ".manim-media\bellman-shadow-pricing-base.mp4"
$finalVideo = Join-Path $mediaDir "bellman-shadow-pricing.mp4"
$poster = Join-Path $mediaDir "bellman-shadow-pricing-poster.png"
$closingStill = Join-Path $videoDir "board-mockup-completed.png"

python (Join-Path $videoDir "build_scene_data.py")
manim --config_file (Join-Path $videoDir "manim.cfg") --resolution 1920,1080 --fps 30 `
  (Join-Path $videoDir "bellman_shadow_pricing.py") BellmanShadowPricingFilm
if ($LASTEXITCODE -ne 0) { throw "Manim render failed with exit code $LASTEXITCODE" }

New-Item -ItemType Directory -Force -Path $mediaDir | Out-Null
ffmpeg -y -i $manimOutput -c:v libx264 -preset slow -crf 20 `
  -pix_fmt yuv420p -movflags +faststart -an $normalizedFilm
if ($LASTEXITCODE -ne 0) { throw "FFmpeg normalization failed with exit code $LASTEXITCODE" }
ffmpeg -y -i $normalizedFilm -loop 1 -framerate 30 -t 5.2 -i $closingStill `
  -filter_complex "[0:v]fps=30,format=yuv420p,setpts=PTS-STARTPTS[film];[1:v]scale=1920:1080:force_original_aspect_ratio=decrease,pad=1920:1080:(ow-iw)/2:(oh-ih)/2:color=0x0c0d0c,setsar=1,fps=30,format=yuv420p,setpts=PTS-STARTPTS[still];[film][still]concat=n=2:v=1:a=0[out]" `
  -map "[out]" -t 90 -c:v libx264 -preset slow -crf 20 -pix_fmt yuv420p `
  -movflags +faststart -an $finalVideo
if ($LASTEXITCODE -ne 0) { throw "Closing-still assembly failed with exit code $LASTEXITCODE" }
ffmpeg -y -ss 00:00:04 -i $finalVideo -frames:v 1 $poster
if ($LASTEXITCODE -ne 0) { throw "Poster extraction failed with exit code $LASTEXITCODE" }

Write-Output "Rendered $finalVideo"
Write-Output "Poster $poster"
