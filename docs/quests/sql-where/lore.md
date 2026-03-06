## Query Log: Where Have All the Actives Gone?

> *Connecting to Archive Node 7...*
> *Scanning `users` table...*
> *6 agents found. 2 flagged as inactive.*

In the Archive, `is_active = 0` marks an agent as suspended. Their records persist but must never be surfaced in ops reports.

The data waits. The filter is yours to write.
