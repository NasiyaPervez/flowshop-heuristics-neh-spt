# Flow-shop scheduling heuristics: NEH vs SPT

**Short description:** Permutation flow-shop makespan minimization with two
dispatching heuristics — NEH (Nawaz–Enscore–Ham best-insertion) versus SPT
(Shortest Processing Time) — compared on two tutorial instances.

## What this is

Coursework for *Optimization Implementation in Production and Logistics* (OVGU
Magdeburg), Assignment 3. In a permutation flow-shop every job visits all
machines in the same order, and jobs keep that order across machines; the goal
is to minimise the makespan. Two classic heuristics are implemented:

- **NEH** — a dedicated flow-shop heuristic. Jobs are first sorted by *decreasing*
  total processing time, then inserted one-by-one into the partial sequence at
  the position giving the lowest makespan. It is widely regarded as one of the
  best constructive heuristics for the permutation flow-shop.
- **SPT** — a simple dispatching rule that schedules jobs in *increasing* order
  of total processing time.

Both are benchmarked on `jobs_original` (5 jobs) and `jobs_extended` (25 jobs)
with 4 machines each.

## Repository layout

```
.
├── neh_spt.py                          # Clean, reusable implementation
├── Nasiya Pervez - Heuristics - Assign3.ipynb   # Original assignment notebook
├── Algorithm-Sequencejobsoriginal-Makespanjobsoriginal-Sequencejobsextended-Makespanjobsextended.csv
│                                       # Results table exported from the notebook
└── LICENSE
```

## Requirements & setup

Pure `numpy` and the standard library — no solver needed:

```bash
pip install numpy
python neh_spt.py
```

## How it works

- `calculate_makespan(sequence, jobs)` — dynamic-programming completion-time
  table; returns the makespan of a job permutation.
- `neh_heuristic(jobs)` — sorts jobs by total processing time (descending) and
  greedily inserts each into the best position.
- `spt_heuristic(jobs)` — sorts jobs by total processing time (ascending).
- `main()` — runs both on both instances, prints sequences, makespans, and
  detailed completion matrices.

## Results

| Algorithm | Sequence (`jobs_original`)     | Makespan | Sequence (`jobs_extended`) | Makespan |
|---|---|---|---|---|
| **NEH**   | `[4, 2, 5, 1, 3]`             | **213**  | `[23, 4, 8, 12, 11, 3, ...]` | **944**  |
| **SPT**   | `[4, 3, 2, 5, 1]`             | 250      | `[4, 8, 21, 3, 11, 12, ...]` | 1092     |

NEH wins by **37** time units on the small instance and **148** on the large one.

### Why NEH wins

- It is *designed* for flow-shop makespan minimisation (best-insertion search),
  whereas SPT is a generic dispatching rule imported from single-machine theory
  where short processing times are optimal for mean flow time — not for makespan.
- The insertion step always keeps the locally best partial schedule, packing
  jobs so machines stay busier (fewer idle gaps in the Gantt chart).

### Why SPT loses

- Sorting purely by total processing time ignores machine interactions.
  Delaying a short-job-heavy machine sequence with long jobs at the front can
  push the tail of the schedule out, inflating the makespan.

> The original notebook also optionally solves the instances exactly with a
> Gurobi MIP (Manne model) to get the true optimum (219 for `jobs_original`) —
> see the last cells of `Nasiya Pervez - Heuristics - Assign3.ipynb`.

## License

MIT — see [LICENSE](LICENSE). All code in this repository is the author's own;
the tutorial instances were provided by the course instructor.