# Tutorial: Calculating Availability

## What is availability?

Your task is to implement `calculate_availability(events)` in `task.py`.

Availability is the fraction of requests that succeeded. A response is a success
if its status code is in the 2xx or 3xx range (`200 <= status_code <= 399`).

If 9 out of 10 requests succeeded, availability is `0.9000`.

## Iterating over events

Each event in the list is a dictionary:

```python
{"status_code": 200}
{"status_code": 500}
{"status_code": 301}
```

Loop over the list and count how many events have a successful status code:

```python
successes = 0
for event in events:
    if 200 <= event["status_code"] <= 399:
        successes += 1
```

## Computing the ratio

Divide successes by the total number of events. Round to 4 decimal places:

```python
availability = round(successes / len(events), 4)
```

Be careful: if `events` is empty you would divide by zero. You can assume the
input always contains at least one event for this quest.

## Rounding and precision

`round(value, 4)` returns a float rounded to 4 decimal places. Your function
must return this float directly — `main()` formats it for printing.
