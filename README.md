# Make the Computer Draw a Box

**Nand to Tetris – I (ETCCNT301) · Capstone Project**
School of Engineering & Technology, K.R. Mangalam University

A complete Hack computer pipeline: the hardware (HDL), a two-pass assembler written in Python, and an assembly program that draws a black box on the screen while a key is held down.

## At a glance

| | |
|---|---|
| **Student** | Anish Kumar Jha |
| **Roll number** | 2501010273 |
| **Personal number** | **K = 73** (last two digits of the roll number) |
| **Box** | starts at row **73**, **20 rows** tall, **32 pixels** wide (2 words), left edge |
| **Assembler extra feature** | K mod 3 = 1 → clear error messages with line numbers |

### How K decides everything

| Calculation | Result | Meaning |
|---|---|---|
| K mod 3 = 73 mod 3 | **1** | assembler prints `Line N: invalid instruction` style errors instead of crashing |
| K mod 4 = 73 mod 4 | **1** | width = 16 × (1 + 1) = **32 pixels** = 2 screen words |
| First screen address | **18720** | `16384 + 32 × 73` (one screen row = 32 words) |

## Repository layout

```
capstone/
├── CPU.hdl · Memory.hdl · Computer.hdl      Part A – the computer
├── CPU.tst/.cmp · Memory.tst/.cmp           official test scripts + expected output
├── ComputerAdd|Max|Rect .tst/.cmp           official full-computer tests
├── Add.hack · Max.hack · Rect.hack          programs loaded by the Computer tests
├── assembler.py                             Part B – two-pass Hack assembler
├── test_assembler.py                        unit tests for the assembler
├── compare_with_official.py                 compares assembler output with the official one
├── asm-tests/                               Add, Max, Rect, Pong (.asm + official .hack) and a bad-input demo
├── Box.asm · Box.hack                       Part C – the box program and its machine code
├── screenshots/                             test and CPU Emulator screenshots
```

## Part A – The computer

| Chip | What it does |
|---|---|
| `CPU.hdl` | Decodes the instruction, runs the ALU, updates the A and D registers and the program counter, and handles all jump conditions. The ALU result is routed through an internal pin (`aluOut`) as well as to `outM`, because HDL does not allow an output pin to feed another part. |
| `Memory.hdl` | Address map: `0–16383` RAM, `16384–24575` screen, `24576` keyboard. Bits 13–14 of the address select the region. |
| `Computer.hdl` | ROM32K + CPU + Memory wired together. |

Run the official tests in the Nand2Tetris Hardware Simulator (desktop or [web IDE](https://nand2tetris.github.io/web-ide/)): load each `.tst` file and run it.

> **Note on `Memory.tst`:** the official script is interactive. When it asks, click the keyboard icon and hold `K` (uppercase), then later `Y`, until the next message appears. Those two rows cannot pass without a real keypress.

## Part B – The assembler

```bash
python assembler.py Box.asm          # writes Box.hack next to the .asm file
python -m unittest -v test_assembler.py
python compare_with_official.py      # Add, Max, Rect, Pong vs the official assembler
```

**How it works**

1. **First pass** – strips comments and blank lines, records every label like `(LOOP)` with the ROM address of the next instruction.
2. **Second pass** – turns each line into 16 bits. `@number` and symbols become A-instructions; `dest=comp;jump` lines become C-instructions. Unknown symbols are variables and get RAM addresses 16, 17, 18, …
3. Predefined symbols (`SP`, `LCL`, `ARG`, `THIS`, `THAT`, `R0–R15`, `SCREEN`, `KBD`) are loaded first.

**Extra feature (K mod 3 = 1) – readable errors**

```text
$ python assembler.py asm-tests/bad_example.asm
Line 3: invalid instruction
```

The line number is the real line in the source file (comments and blank lines are counted). Bad labels, bad `@` values, out-of-range addresses and malformed `dest=comp;jump` lines are all reported this way instead of crashing.

Destination letters may be written in any order (`DM=` and `MD=` are identical), as the official `Rect.asm` and `Pong.asm` require.

## Part C – The box (`Box.asm`)

* Reads `KBD` in a loop.
* **Key pressed →** writes `-1` (16 black pixels) into 2 words on each of 20 rows, starting at address 18720.
* **No key →** writes `0` into the same words, so the box disappears.
* After each row the pointer moves `+30` words, because 2 words were written and a screen row is 32 words (2 + 30 = 32).

```bash
python assembler.py Box.asm    # uses the project's own assembler, not the official one
```

Load `Box.hack` in the CPU Emulator, set **Animate: No animation**, run, then press and release a key in the keyboard panel.

To move the box, change the start address `18720` (it appears twice: once in the clear section and once in the draw section). New address = `16384 + 32 × row`.

## Verification status

| Check | Result |
|---|---|
| Assembler unit tests | 9 / 9 pass |
| Add, Max, Rect, Pong vs official assembler output | identical (Pong = 27,483 instructions) |
| `Box.hack` equals the assembler's output for `Box.asm` | identical |
| `Box.hack` behaviour (key down / key up) | rows 73–92 filled, 2 words wide; screen fully cleared on release |
| `CPU.tst` | passes (97 / 97 rows) |
| `ComputerAdd`, `ComputerMax`, `ComputerRect` | pass, using this project's own CPU and Memory |
| `Memory.tst` | all RAM and screen rows pass; the 2 keyboard rows need `K` / `Y` held in the GUI |

The hardware checks were run with the official Nand2Tetris web-IDE simulator engine from the command line. Hardware Simulator and CPU Emulator screenshots are stored in [`screenshots/`](screenshots/).

## Tools

Python 3.8+ (no external packages) · Nand2Tetris Hardware Simulator and CPU Emulator

---
*Individual work for ETCCNT301 · K.R. Mangalam University, School of Engineering & Technology*
