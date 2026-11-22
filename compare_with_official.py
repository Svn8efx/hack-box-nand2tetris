"""Assemble the official programs in asm-tests/ with assembler.py and compare
the result with the official assembler's output (*.official.hack)."""
from pathlib import Path
from assembler import assemble

folder = Path(__file__).parent / "asm-tests"
all_ok = True
for asm_file in sorted(folder.glob("*.asm")):
    official = asm_file.with_suffix(".official.hack")
    if not official.exists():
        continue
    mine, _ = assemble(asm_file.read_text(encoding="utf-8"))
    expected = [line.strip() for line in official.read_text().splitlines() if line.strip()]
    ok = mine == expected
    all_ok &= ok
    print(f"{asm_file.stem:6} {len(mine):6} instructions  {'MATCH' if ok else 'DIFFERENT'}")
raise SystemExit(0 if all_ok else 1)
