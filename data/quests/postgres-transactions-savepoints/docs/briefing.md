# The Partial Rollback

Complex migrations require safety nets within safety nets.

In this script, you are going to execute a sequence of queries within a single transaction block. 
1. Give Charlie a raise to `100000`. This is the *Good Update*.
2. Establish a `SAVEPOINT` named `before_disaster`.
3. An automatic *Bad Update* is already in the file. It will incorrectly set everyone's salary to `0`.
4. Run `ROLLBACK TO SAVEPOINT before_disaster` to rewind just the bad update.
5. `COMMIT` the transaction. 

By the end, Charlie should have his new salary, but everyone else's salary should remain untouched by the disaster.
