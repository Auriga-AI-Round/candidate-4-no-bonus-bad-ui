# Reasoning

**Overlap check.** Two 30-minute intervals clash iff `start1 < end2 AND end1 > start2`
(half-open), so adjacent slots are fine but partial overlaps are rejected. I put this in
the booking handler and return 409 (state conflict) rather than 400.

**PostgreSQL.** Chose a real server over SQLite because the task requires it and
concurrent bookings behave better. Indexed `(doctor_id, start_time)` for the overlap
query.

**Trade-off.** I prioritised booking correctness and skipped the analytics dashboard
and a polished UI; the UI is a bare table. Given more time I'd add the dashboard and a
`SELECT ... FOR UPDATE` around the overlap check for concurrency safety.
