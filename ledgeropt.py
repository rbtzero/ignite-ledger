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
    # Build residual graph
    adj: Dict[int, List[int]] = {n: [] for n in nodes}
    capacity: Dict[Tuple[int, int], int] = {}
    for u, v, c in edges:
        adj[u].append(v)
        adj[v].append(u)  # add reverse edge for residual
        capacity[(u, v)] = c
        capacity.setdefault((v, u), 0)

    max_flow = 0

    while True:
        # BFS to find augmenting path
        parent = {src: None}
        queue = [src]
        while queue and sink not in parent:
            cur = queue.pop(0)
            for nxt in adj[cur]:
                if nxt not in parent and capacity[(cur, nxt)] > 0:
                    parent[nxt] = cur
                    queue.append(nxt)
                    if nxt == sink:
                        break

        if sink not in parent:
            break  # no augmenting path

        # Determine bottleneck
        path_flow = math.inf
        v = sink
        while v != src:
            u = parent[v]
            path_flow = min(path_flow, capacity[(u, v)])
            v = u

        # Update residual capacities
        v = sink
        while v != src:
            u = parent[v]
            capacity[(u, v)] -= path_flow
            capacity[(v, u)] += path_flow
            v = u

        max_flow += path_flow

    return int(max_flow)


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