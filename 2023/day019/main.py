import re
import sys
from collections import deque
from math import prod
from typing import Literal, NamedTuple

with open(sys.argv[1]) as f:
    data = f.read().strip().split("\n\n")


class Part(NamedTuple):
    x: int
    m: int
    a: int
    s: int


class Workflow(NamedTuple):
    name: str
    rules: list[str]


def parse_input(data: list[str]) -> tuple[dict[str, Workflow], list[Part]]:
    workflows = {}
    parts = []

    for w in data[0].split("\n"):
        name, _, rules = w.partition("{")
        rules = rules.removesuffix("}").split(",")
        workflows[name] = Workflow(name, rules)

    nums = re.compile(r"\d+")
    for p in data[1].split("\n"):
        p = p.removeprefix("{").removesuffix("}")
        x, m, a, s = (int(n) for n in nums.findall(p))
        parts.append(Part(x, m, a, s))

    return workflows, parts


workflows, parts = parse_input(data)

Status = Literal["A", "R"]


def apply_rules(p: Part, w: Workflow, workflows: dict[str, Workflow]) -> Workflow | Status:
    splitters = re.compile(r"(>|<|:)")
    for rule in w.rules:
        rule_expr = splitters.split(rule)
        match rule_expr:
            case [part, op, value, _, workflow] if part in ("x", "m", "a", "s"):
                cpart = getattr(p, part)
                if op == ">":
                    if cpart > int(value):
                        if workflow in ("A", "R"):
                            return workflow
                        return workflows[workflow]
                elif op == "<":
                    if cpart < int(value):
                        if workflow in ("A", "R"):
                            return workflow
                        return workflows[workflow]
            case [workflow] if workflow in workflows:
                return workflows[workflow]
            case [status] if status in ("A", "R"):
                return status
            case _:
                raise ValueError(f"Invalid rule: {rule}")


ans = 0
for p in parts:
    workflow = workflows["in"]
    while workflow != "A" and workflow != "R":
        workflow = apply_rules(p, workflow, workflows)
    if workflow == "A":
        ans += sum(p)

print(f"Part 1: {ans}")

# Part 2


def xmas(op: str, value: int, r: range) -> range:
    if op == ">":
        lo = max(r.start, value + 1)
        return range(lo, r.stop)
    elif op == ">=":
        lo = max(r.start, value)
        return range(lo, r.stop)
    elif op == "<":
        hi = min(r.stop, value - 1)
        return range(r.start, hi)
    elif op == "<=":
        hi = min(r.stop, value)
        return range(r.start, hi)
    return r


def xxmas(part: str, op: str, value: int, x: range, m: range, a: range, s: range) -> tuple[range, range, range, range]:
    if part == "x":
        x = xmas(op, value, x)
        return x, m, a, s
    elif part == "m":
        m = xmas(op, value, m)
        return x, m, a, s
    elif part == "a":
        a = xmas(op, value, a)
        return x, m, a, s
    elif part == "s":
        s = xmas(op, value, s)
        return x, m, a, s
    else:
        return x, m, a, s


ans2 = 0
splitters = re.compile(r"(>|<|:)")
Q = deque([("in", range(1, 4000), range(1, 4000), range(1, 4000), range(1, 4000))])
while Q:
    name, x, m, a, s = Q.pop()
    if any(r.start > r.stop for r in (x, m, a, s)):
        continue
    if name == "R":
        continue
    elif name == "A":
        ans2 += prod(len(r) + 1 for r in (x, m, a, s))
        continue
    else:
        w = workflows[name]
        for rule in w.rules:
            rule_expr = splitters.split(rule)
            match rule_expr:
                case [part, op, value, _, workflow] if part in ("x", "m", "a", "s"):
                    f_ranges = xxmas(part, op, int(value), x, m, a, s)
                    Q.append((workflow, *f_ranges))
                    x, m, a, s = xxmas(part, ">=" if op == "<" else "<=", int(value), x, m, a, s)
                case [workflow] if workflow in workflows:
                    Q.append((workflow, x, m, a, s))
                case [status] if status in ("A", "R"):
                    Q.append((status, x, m, a, s))
                case _:
                    raise ValueError(f"Invalid rule: {rule}")

print(f"Part 2: {ans2}")
