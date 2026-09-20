#!/usr/bin/env python3
"""Generate the 11 approved Edgeheart Competency SVG UI glyphs.

These glyphs are derived from the approved Edgeheart Competency concept sheet
and are intentionally redrawn as clean geometric vectors rather than raster
autotraces. The goal is small-size legibility in Daggerheart 1.2.7 UI surfaces.

Output contract:
- 250 x 250 SVG
- viewBox="0 0 250 250"
- currentColor-based monochrome vector art
- no raster embedding
- no external references
- no text
"""

from __future__ import annotations

import argparse
from pathlib import Path

GLYPHS = {
    "network": """<svg xmlns="http://www.w3.org/2000/svg" width="250" height="250" viewBox="0 0 250 250" fill="none" stroke="currentColor" stroke-width="10" stroke-linecap="round" stroke-linejoin="round">
  <path d="M125 84V48 M125 166v36 M84 102 58 80 M166 102l26-22 M84 148l-30 20 M166 148l30 20"/>
  <circle cx="125" cy="125" r="31"/><circle cx="125" cy="125" r="13"/>
  <circle cx="125" cy="35" r="13"/><circle cx="125" cy="215" r="13"/>
  <circle cx="45" cy="69" r="13"/><circle cx="205" cy="69" r="13"/>
  <circle cx="41" cy="177" r="13"/><circle cx="209" cy="177" r="13"/>
</svg>
""",
    "assault": """<svg xmlns="http://www.w3.org/2000/svg" width="250" height="250" viewBox="0 0 250 250" fill="none" stroke="currentColor" stroke-width="10" stroke-linecap="round" stroke-linejoin="round">
  <path d="M52 48 198 194 M43 42l34 11 111 111 19 42-42-19L54 76Z"/>
  <path d="M200 43 85 158 65 194 78 207l36-20L229 72l7-41Z"/>
  <path d="M58 104a75 75 0 0 0 0 45 M192 104a75 75 0 0 1 0 45 M93 57a75 75 0 0 1 64 0 M93 193a75 75 0 0 0 64 0"/>
</svg>
""",
    "chrome": """<svg xmlns="http://www.w3.org/2000/svg" width="250" height="250" viewBox="0 0 250 250" fill="none" stroke="currentColor" stroke-width="10" stroke-linecap="round" stroke-linejoin="round">
  <path d="M61 191c-18-6-28-16-34-28l20-18 18 9 27-24 22 19-25 27 7 18-18 20Z"/>
  <path d="M92 130 144 77l30 23-58 58 M142 78l16-40 24-12 21 18-7 28-22 28Z"/>
  <circle cx="168" cy="84" r="18"/>
  <path d="M44 151l-14 21 M58 160l-13 25 M73 171l-11 24 M180 29l8 32"/>
  <path d="M50 85a82 82 0 0 1 57-42 M197 96a82 82 0 0 1-59 111"/>
</svg>
""",
    "systems": """<svg xmlns="http://www.w3.org/2000/svg" width="250" height="250" viewBox="0 0 250 250" fill="none" stroke="currentColor" stroke-width="9" stroke-linecap="round" stroke-linejoin="round">
  <path d="M78 88 58 68H37 M72 116H25 M79 145 60 164H38 M172 88l20-20h21 M178 116h47 M171 145l20 19h22"/>
  <circle cx="26" cy="68" r="9"/><circle cx="14" cy="116" r="9"/><circle cx="27" cy="164" r="9"/>
  <circle cx="224" cy="68" r="9"/><circle cx="236" cy="116" r="9"/><circle cx="224" cy="164" r="9"/>
  <path d="M125 47v17 M125 186v17 M66 125H49 M201 125h-17"/>
  <path d="M107 64 117 45h16l10 19 21 8 20-7 11 12-7 20 8 20 19 10v16l-19 10-8 20 7 20-11 12-20-7-21 8-10 19h-16l-10-19-21-8-20 7-11-12 7-20-8-20-19-10v-16l19-10 8-20-7-20 11-12 20 7Z"/>
  <path d="M148 92a31 31 0 0 0-38 38l-31 51 14 9 33-50a31 31 0 0 0 32-39l-17 18-16-8-2-18Z"/>
</svg>
""",
    "influence": """<svg xmlns="http://www.w3.org/2000/svg" width="250" height="250" viewBox="0 0 250 250" fill="none" stroke="currentColor" stroke-width="10" stroke-linecap="round" stroke-linejoin="round">
  <path d="M71 86h108a24 24 0 0 1 24 24v35a24 24 0 0 1-24 24h-60l-32 27v-27H71a24 24 0 0 1-24-24v-35a24 24 0 0 1 24-24Z"/>
  <circle cx="92" cy="127" r="6" fill="currentColor" stroke="none"/><circle cx="125" cy="127" r="6" fill="currentColor" stroke="none"/><circle cx="158" cy="127" r="6" fill="currentColor" stroke="none"/>
  <path d="M83 62a64 64 0 0 1 84 0 M69 45a84 84 0 0 1 112 0 M76 191a67 67 0 0 0 98 0 M62 207a88 88 0 0 0 126 0"/>
</svg>
""",
    "ghost": """<svg xmlns="http://www.w3.org/2000/svg" width="250" height="250" viewBox="0 0 250 250" fill="none" stroke="currentColor" stroke-width="10" stroke-linecap="round" stroke-linejoin="round">
  <path d="M125 31 63 92l14 72 48 51 48-51 14-72Z"/>
  <path d="M125 59 78 109l28-12 19-16 19 16 28 12"/>
  <path d="M92 121 113 130 92 136 M158 121 137 130 158 136"/>
  <path d="M72 91a69 69 0 0 1 23-29 M178 91a69 69 0 0 0-23-29"/>
</svg>
""",
    "frontier": """<svg xmlns="http://www.w3.org/2000/svg" width="250" height="250" viewBox="0 0 250 250" fill="none" stroke="currentColor" stroke-width="10" stroke-linecap="round" stroke-linejoin="round">
  <circle cx="125" cy="125" r="82"/>
  <path d="M125 23 137 75 125 67 113 75Z M125 227 137 175 125 183 113 175Z M23 125 75 113 67 125 75 137Z M227 125 175 113 183 125 175 137Z" fill="currentColor" stroke="none"/>
  <path d="M51 151 89 111l31 25 24-22 55 37"/>
  <path d="M45 151h160"/>
  <circle cx="163" cy="102" r="18" fill="currentColor" stroke="none"/>
</svg>
""",
    "medtech": """<svg xmlns="http://www.w3.org/2000/svg" width="250" height="250" viewBox="0 0 250 250" fill="none" stroke="currentColor" stroke-width="10" stroke-linecap="round" stroke-linejoin="round">
  <path d="M103 65h44v38h38v44h-38v38h-44v-38H65v-44h38Z"/>
  <path d="M52 125h44l12-24 16 51 16-39 11 12h47"/>
  <path d="M82 36a93 93 0 0 1 86 0 M36 82a93 93 0 0 0 0 86 M82 214a93 93 0 0 0 86 0 M214 82a93 93 0 0 1 0 86"/>
  <path d="M125 21v18 M125 211v18 M21 125h18 M211 125h18"/>
</svg>
""",
    "aegis": """<svg xmlns="http://www.w3.org/2000/svg" width="250" height="250" viewBox="0 0 250 250" fill="none" stroke="currentColor" stroke-width="10" stroke-linecap="round" stroke-linejoin="round">
  <path d="M125 51 70 72v47c0 43 20 75 55 96 35-21 55-53 55-96V72Z"/>
  <path d="M125 70 88 84v35c0 30 12 54 37 72Z" fill="currentColor" stroke="none"/>
  <path d="M78 36a96 96 0 0 1 94 0 M36 78a96 96 0 0 0 0 94 M78 214a96 96 0 0 0 94 0 M214 78a96 96 0 0 1 0 94"/>
</svg>
""",
    "redline": """<svg xmlns="http://www.w3.org/2000/svg" width="250" height="250" viewBox="0 0 250 250" fill="none" stroke="currentColor" stroke-width="10" stroke-linecap="round" stroke-linejoin="round">
  <path d="M85 189a77 77 0 1 1 111-6"/>
  <path d="M154 94 126 142"/>
  <circle cx="126" cy="142" r="10" fill="currentColor" stroke="none"/>
  <path d="M177 73l12 14 M195 102l16 7 M200 137h18 M190 168l15 9"/>
  <path d="M29 101h58 M20 126h59 M29 151h57 M42 176h57"/>
  <path d="M91 70a77 77 0 0 1 60-11"/>
</svg>
""",
    "blackwall": """<svg xmlns="http://www.w3.org/2000/svg" width="250" height="250" viewBox="0 0 250 250" fill="none" stroke="currentColor" stroke-width="10" stroke-linecap="round" stroke-linejoin="round">
  <path d="M58 49 111 25v59l17 20-17 20 17 20-17 20v61H58Z" fill="currentColor" stroke="none"/>
  <path d="M192 49 139 25v59l-17 20 17 20-17 20 17 20v61h53Z" fill="currentColor" stroke="none"/>
  <path d="M48 65a83 83 0 0 0-28 60 83 83 0 0 0 28 60 M202 65a83 83 0 0 1 28 60 83 83 0 0 1-28 60"/>
  <path d="M45 142h10v10H45z M68 161h11v11H68z M78 139h8v8H78z M195 111h10v10h-10z M172 130h11v11h-11z M188 145h8v8h-8z" fill="currentColor" stroke="none"/>
</svg>
""",
}

def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo", type=Path, default=Path.cwd())
    args = parser.parse_args()
    repo = args.repo.resolve()
    out = repo / "assets/icons/domains"
    out.mkdir(parents=True, exist_ok=True)

    for domain, svg in GLYPHS.items():
        path = out / f"{domain}.svg"
        path.write_text(svg, encoding="utf-8")
        print(f"wrote {path.relative_to(repo)}")

    print(f"generated {len(GLYPHS)} Edgeheart Competency SVG glyphs")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
