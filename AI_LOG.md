# AI Usage Log

- **Overlap filter:** asked the assistant for the SQLAlchemy filter to detect
  overlapping time ranges. It gave the half-open `start < end AND end > start` form; I
  verified it with two tests (`tests/test_overlap.py`) — partial overlap rejected,
  adjacent allowed.
- **Status code:** confirmed 409 is right for a booking conflict rather than 400.
- I did not use AI for the CRUD boilerplate — wrote that directly.
