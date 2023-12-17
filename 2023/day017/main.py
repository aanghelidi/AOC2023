import heapq
import sys
from typing import Generator


def n4() -> Generator[tuple[int, int], None, None]:
    return ((0, 1), (0, -1), (1, 0), (-1, 0))


with open(sys.argv[1]) as f:
    data = f.read().splitlines()

grid = [[int(e) for e in line.strip()] for line in data]
n = len(grid)
m = len(grid[0])
for part in (1, 2):
    visited = set()
    pq = [(0, 0, 0, 0, 0, 0)]
    while pq:
        heat_loss, row, col, dr, dc, nb = heapq.heappop(pq)
        if row == n - 1 and col == m - 1:
            print(f"Part {part}: {heat_loss}")
            break
        if (row, col, dr, dc, nb) in visited:
            continue
        visited.add((row, col, dr, dc, nb))
        if part == 1:
            if nb < 3 and (dr, dc) != (0, 0):
                nr, nc = row + dr, col + dc
                if 0 <= nr < n and 0 <= nc < m:
                    heapq.heappush(pq, (heat_loss + grid[nr][nc], nr, nc, dr, dc, nb + 1))
            for ndr, ndc in n4():
                if (ndr, ndc) != (dr, dc) and (ndr, ndc) != (-dr, -dc):
                    nr, nc = row + ndr, col + ndc
                    if 0 <= nr < n and 0 <= nc < m:
                        heapq.heappush(pq, (heat_loss + grid[nr][nc], nr, nc, ndr, ndc, 1))
        else:
            if nb < 10 and (dr, dc) != (0, 0):
                nr, nc = row + dr, col + dc
                if 0 <= nr < n and 0 <= nc < m:
                    heapq.heappush(pq, (heat_loss + grid[nr][nc], nr, nc, dr, dc, nb + 1))
            if (dr == 0 and dc == 0) or nb > 3:
                for ndr, ndc in n4():
                    if (ndr, ndc) != (dr, dc) and (ndr, ndc) != (-dr, -dc):
                        nr, nc = row + ndr, col + ndc
                        if 0 <= nr < n and 0 <= nc < m:
                            heapq.heappush(pq, (heat_loss + grid[nr][nc], nr, nc, ndr, ndc, 1))
