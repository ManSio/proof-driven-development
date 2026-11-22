# PATTERNS — error classes index

> Rules: one line per class, always with a **source** and a **guard**. A class
> without a guard is an open question, not a pattern. Repeats of the same class
> (≥2) must produce a guard in the same change.

| ID | Sign (how to recognize it) | Guard (what prevents it) | Source |
|---|---|---|---|
| P-001 | test is green but the implementation can be broken without it turning red (mutation) | break a line before shipping; the test must redden | example — replace |
