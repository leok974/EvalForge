"The network was unstable," Elara said, pointing to a shimmering, jagged green line on the telemetry display. "We were migrating the core schema from orbital relay Alpha to Beta. Three million rows."

She traced the peak of the jagged line. "Right there, a micro-meteorite knocked out the connection for exactly 1.4 seconds. The migration failed."

She turned from the screen. "If we hadn't used Savepoints, the entire three-million row transaction would have failed. It would have taken another twelve hours to restart from scratch. But because we had planted a `SAVEPOINT` every hundred thousand rows, we just rolled back the last batch and kept going."

She tapped her holoscreen, dismissing the graph. "A transaction protects your data from the universe. A Savepoint protects your transaction from itself."
