# Prompt Memory - mdwarfometer

This file is a persistent in-folder memory of project prompts and key decisions.
Append new entries each work session.

## 2026-04-02
- Prompt: Build an HTML document with embedded Python code for an M-dwarf properties tool.
- Requirements captured:
  - Input field for object name.
  - Resolve with SIMBAD.
  - Import parallax and G/J/H/K magnitudes.
  - If data is missing, show message and allow manual input.
  - Keep a permanent memory of prompts in-folder for this multi-day project.
- Implementation started in index.html (Phase 1).
- Notes:
  - Current approach uses PyScript + SIMBAD TAP query from browser.
  - May require local serving due browser CORS restrictions.

- Bugfix note:
  - SIMBAD TAP 400 for GL699 was caused by selecting `id.main_id` (invalid column in `ident`).
  - Fixed by selecting `b.main_id` from `basic`.

- UI formatting update:
  - Bandpass labels are now italicized in the UI (<em>G</em>, <em>J</em>, <em>H</em>, <em>K</em>).
  - Units are displayed in square brackets (for example [mas], [mag]).

- Metallicty module start:
  - Added photometric [Fe/H] estimate in the web tool.
  - Implemented using a Bonfils et al. (2005) style relation based on M_K and (V-K).
  - Added V magnitude fetch and manual-input support because this calibration requires V and K.
