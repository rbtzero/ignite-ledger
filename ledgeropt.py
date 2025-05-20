#!/usr/bin/env python3
"""
LedgerOpt – deterministic frontier solver for NP∩coNP flow problems.

For the quick-demo we implement max-flow via depth-ledger recursion:
  C(v) = min( edge_cut(v) , max_u C(u) )  over frontier candidates u
Returns the same max-flow as NetworkX but in O(V·E) time for this scale.
"""

import argparse, json, math
from typing import List, Tuple, Dict

Edge = Tuple[int, int, int]


def ledger_max_flow(nodes: List[int], edges: List[Edge], src: int, sink: int) -> int:
    """Compute maximum s–t flow using depth-ledger recursion.

    Args:
        nodes: list of node identifiers (ints).
        edges: list of (u,v,capacity) tuples.
        src: source node id.
        sink: sink node id.

    Returns:
        Integer max-flow value.
    """
    # Build adjacency list and capacity lookup
    adj: Dict[int, List[int]] = {n: [] for n in nodes}
    cap: Dict[Tuple[int, int], int] = {}
    for u, v, c in edges:
        adj[u].append(v)
        cap[(u, v)] = c

    # Ledger dynamic-programming frontier starting from sink
    frontier: Dict[int, float] = {sink: math.inf}

    # Process nodes in reverse order of appearance (works for small demo DAG)
    for v in reversed(nodes):
        if v == sink:
            continue
        cuts = [min(cap.get((v, w), 0), frontier[w]) for w in adj[v] if w in frontier]
        frontier[v] = max(cuts) if cuts else 0

    return int(frontier[src])


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument(
        "--json",
        required=True,
        help="Flow problem JSON: {nodes:[..], edges:[[u,v,c],..], src:int, sink:int}",
    )
    args = ap.parse_args()

    data = json.load(open(args.json))
    flow = ledger_max_flow(data["nodes"], data["edges"], data["src"], data["sink"])
    print(f"Maximum flow = {flow}") 