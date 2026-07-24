# Offline narrated edition

This directory builds the accessible narrated edition of the locked 90-second Bellman
Shadow Pricing proof-film. The silent certified film remains separately published and is
not replaced or re-encoded: FFmpeg copies its H.264 video stream unchanged into the
narrated MP4.

Narration is synthesized entirely offline with Piper 1.4.2. Matt uses
`en_GB-cori-medium` at `length_scale 1.08`; Ellie uses `en_US-kristin-medium` at
`length_scale 0.98`. The voice model cards identify public-domain LibriVox source
recordings. Piper is GPL-3.0; the Piper voice-model repository is MIT-licensed. The engine
and model files remain local and are not redistributed.

## Rebuild

Use a local Piper 1.4.2 environment and the two verified model files:

```powershell
<voice-python> BGI-Open-Build\narration\render_narration.py `
  --piper-python <voice-python> `
  --model-dir <local-piper-model-directory> `
  --source-commit <narration-source-commit>
```

`script.json` defines every sentence, speaker, scene start time, public caption text, and
pronunciation-only synthesis text. The renderer verifies both model hashes, emits
sentence WAV files and a 90-second narration master, writes SRT and WebVTT captions, and
mixes a separate narrated MP4. `narration_receipt.json` binds models, segments, captions,
audio, the locked silent input, and the narrated result by SHA-256.

Microsoft Edge online TTS is not used.
