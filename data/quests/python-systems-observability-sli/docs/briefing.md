# Briefing: Observability & SLIs

## The Mission

You can't manage what you can't measure. In production systems, **Service Level
Indicators (SLIs)** are specific metrics that capture how well a service is
performing. An **SLO (Service Level Objective)** is the target value for that
metric — for example, "99% of requests succeed."

In this mission you will implement `calculate_availability(events)`. It receives a
list of event dictionaries, each with a `status_code` key. A response is considered
successful if `200 <= status_code <= 399`. Your function must return the ratio of
successful responses to total events as a `float` rounded to 4 decimal places.

**Objective:** Implement `calculate_availability(events) -> float`.
