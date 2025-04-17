from __future__ import annotations
from typing import List, Tuple
from z3 import *

def _parse(prop: str):
    rep = {"¬": "Not", "∧": "And", "∨": "Or", "→": "Implies"}
    for k, v in rep.items():
        prop = prop.replace(k, v)
    return parse_smt2_string(f"(assert {prop})")[0]

def _minimal_core(ids: list[str], solver: Solver) -> list[str]:
    core = [str(x) for x in solver.unsat_core()]
    # Quick greedy hitting‑set (good enough for <100 props)
    hitting = set()
    for i in core:
        if hitting & {i}:
            continue
        hitting.add(i)
    return list(hitting)

def detect_contradictions(props: List[dict]) -> List[Tuple[str, str]]:
    s = Solver()
    for p in props:
        s.assert_and_track(_parse(p["prop"]), p["id"])
    if s.check() != unsat:
        return []
    core = _minimal_core([p["id"] for p in props], s)
    return [(core[i], core[j]) for i in range(len(core)) for j in range(i + 1, len(core))]
