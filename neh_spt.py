"""NEH vs SPT heuristics for the permutation flow-shop scheduling problem.

NEH (Nawaz-Enscore-Ham):
    - order jobs by decreasing total processing time,
    - insert jobs one by one into the best position (lowest makespan) of the
      current partial sequence.

SPT (Shortest Processing Time):
    - schedule jobs in increasing order of total processing time.

Both are evaluated on the tutorial instances ``jobs_original`` (5 jobs) and
``jobs_extended`` (25 jobs). BEH consistently wins on makespan.

Coursework: Optimization Implementation in Production and Logistics (OVGU
Magdeburg), Assignment 3 — heuristics for flow-shop scheduling.
"""

from __future__ import annotations

import numpy as np

# Each job maps to its processing time on each of the 4 machines.
JOBS_ORIGINAL: dict[int, list[int]] = {
    1: [31, 41, 25, 30],
    2: [19, 55, 3, 34],
    3: [23, 42, 27, 6],
    4: [13, 22, 14, 13],
    5: [33, 5, 57, 19],
}

JOBS_EXTENDED: dict[int, list[int]] = {
    1: [31, 41, 25, 30],
    2: [19, 55, 3, 34],
    3: [23, 42, 27, 6],
    4: [13, 22, 14, 13],
    5: [33, 5, 57, 19],
    6: [56, 57, 50, 44],
    7: [21, 11, 47, 57],
    8: [19, 10, 31, 23],
    9: [48, 35, 27, 31],
    10: [46, 57, 38, 35],
    11: [8, 18, 28, 44],
    12: [24, 33, 21, 20],
    13: [47, 37, 47, 45],
    14: [33, 58, 38, 32],
    15: [21, 23, 54, 29],
    16: [59, 9, 54, 48],
    17: [16, 51, 21, 34],
    18: [35, 58, 25, 21],
    19: [45, 34, 22, 58],
    20: [54, 46, 41, 46],
    21: [58, 16, 5, 12],
    22: [25, 46, 32, 60],
    23: [6, 57, 24, 13],
    24: [20, 53, 47, 27],
    25: [37, 47, 7, 14],
}


def calculate_makespan(sequence: list[int], jobs: dict[int, list[int]]) -> int:
    """Makespan of ``sequence`` in a permutation flow-shop.

    Standard completion-time DP: job ``i`` can start on machine ``m`` only
    after it finished on ``m-1`` *and* the previous job finished on ``m``.

    Args:
        sequence: order of job ids to schedule (same order on all machines).
        jobs:     ``{job_id: [processing_time_on_each_machine]}``.

    Returns:
        Completion time of the last job on the last machine (makespan).
    """
    n_machines = len(jobs[sequence[0]])
    completion = np.zeros((len(sequence), n_machines), dtype=int)
    for i, job_id in enumerate(sequence):
        for m in range(n_machines):
            if i == 0 and m == 0:
                completion[i, m] = jobs[job_id][m]
            elif i == 0:  # first job: purely cascades down machines
                completion[i, m] = completion[i, m - 1] + jobs[job_id][m]
            elif m == 0:  # first machine: purely cascades across jobs
                completion[i, m] = completion[i - 1, m] + jobs[job_id][m]
            else:
                completion[i, m] = (
                    max(completion[i - 1, m], completion[i, m - 1]) + jobs[job_id][m]
                )
    return int(completion[-1, -1])


def neh_heuristic(jobs: dict[int, list[int]]) -> tuple[list[int], int]:
    """NEH heuristic: best-insertion over jobs sorted by total processing time."""
    job_totals = {job_id: sum(times) for job_id, times in jobs.items()}
    sorted_jobs = sorted(job_totals, key=job_totals.get, reverse=True)

    sequence: list[int] = []
    for job in sorted_jobs:
        # Insert the job at every position; keep the cheapest partial schedule.
        best_seq: list[int] | None = None
        best_makespan: int | None = None
        for i in range(len(sequence) + 1):
            trial_seq = sequence[:i] + [job] + sequence[i:]
            makespan = calculate_makespan(trial_seq, jobs)
            if best_makespan is None or makespan < best_makespan:
                best_makespan = makespan
                best_seq = trial_seq
        sequence = best_seq
    return sequence, best_makespan


def spt_heuristic(jobs: dict[int, list[int]]) -> tuple[list[int], int]:
    """SPT rule: jobs in ascending order of total processing time."""
    sorted_jobs = sorted(jobs, key=lambda job_id: sum(jobs[job_id]))
    makespan = calculate_makespan(sorted_jobs, jobs)
    return sorted_jobs, makespan


def print_completion_matrix(sequence: list[int], jobs: dict[int, list[int]]) -> None:
    """Pretty-print the completion time of each job on each machine."""
    n_machines = len(jobs[sequence[0]])
    completion = np.zeros((len(sequence), n_machines), dtype=int)
    for i, job_id in enumerate(sequence):
        for m in range(n_machines):
            proc_time = jobs[job_id][m]
            if i == 0 and m == 0:
                completion[i, m] = proc_time
            elif i == 0:
                completion[i, m] = completion[i, m - 1] + proc_time
            elif m == 0:
                completion[i, m] = completion[i - 1, m] + proc_time
            else:
                completion[i, m] = (
                    max(completion[i - 1, m], completion[i, m - 1]) + proc_time
                )

    print("\t".join(["Job/Machine"] + [f"M{m + 1}" for m in range(n_machines)]))
    for i, job_id in enumerate(sequence):
        row = [f"Job {job_id}"] + [str(completion[i, m]) for m in range(n_machines)]
        print("\t".join(row))
    print(f"\nFinal Makespan: {completion[-1, -1]}\n")


def main() -> None:
    for name, jobs in (("jobs_original", JOBS_ORIGINAL), ("jobs_extended", JOBS_EXTENDED)):
        neh_seq, neh_mk = neh_heuristic(jobs)
        spt_seq, spt_mk = spt_heuristic(jobs)
        print(f"--- {name} ({len(jobs)} jobs, {len(next(iter(jobs.values())))} machines) ---")
        print(f"NEH sequence : {neh_seq}")
        print(f"NEH makespan : {neh_mk}")
        print(f"SPT sequence : {spt_seq}")
        print(f"SPT makespan : {spt_mk}")
        print(f"=> NEH better by {spt_mk - neh_mk} time units\n")

    # Detail for the smaller instance.
    print("=== NEH completion matrix (jobs_original) ===")
    neh_seq, _ = neh_heuristic(JOBS_ORIGINAL)
    print_completion_matrix(neh_seq, JOBS_ORIGINAL)

    print("=== SPT completion matrix (jobs_original) ===")
    spt_seq, _ = spt_heuristic(JOBS_ORIGINAL)
    print_completion_matrix(spt_seq, JOBS_ORIGINAL)


if __name__ == "__main__":
    main()