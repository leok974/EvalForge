# Boss: Foundry Systems Architect - Golden Runbook

## 1. Domain Object & Interface (The Boundary)

We define a clean `LogisticsService` protocol (Interface) and a domain entity `Shipment`.

```python
from typing import Protocol, List, Optional
from dataclasses import dataclass
import enum
import uuid

class ShipmentStatus(enum.Enum):
    PENDING = "PENDING"
    SHIPPED = "SHIPPED"
    DELIVERED = "DELIVERED"
    FAILED = "FAILED"

@dataclass
class Shipment:
    id: str
    order_id: str
    destination: str
    status: ShipmentStatus
    retry_count: int = 0

class ISupplierAPI(Protocol):
    async def request_dispatch(self, shipment: Shipment) -> bool:
        ...

class IRepository(Protocol):
    async def save_shipment(self, shipment: Shipment) -> None:
        ...
```

## 2. Resilience Layer (Circuit Breaker)

We implement a decorator-based Circuit Breaker for stability.

```python
import time
from functools import wraps

class CircuitBreakerOpenException(Exception):
    pass

class CircuitBreaker:
    def __init__(self, failure_threshold: int = 3, recovery_timeout: int = 10):
        self.failure_threshold = failure_threshold
        self.recovery_timeout = recovery_timeout
        self.failures = 0
        self.last_failure_time = 0
        self.state = "CLOSED"

    def record_failure(self):
        self.failures += 1
        self.last_failure_time = time.time()
        if self.failures >= self.failure_threshold:
            self.state = "OPEN"

    def record_success(self):
        self.failures = 0
        self.state = "CLOSED"

    def allow_request(self) -> bool:
        if self.state == "CLOSED":
            return True
        if self.state == "OPEN":
            elapsed = time.time() - self.last_failure_time
            if elapsed > self.recovery_timeout:
                self.state = "HALF_OPEN"
                return True
        return False

def resilient(circuit: CircuitBreaker):
    def decorator(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            if not circuit.allow_request():
                raise CircuitBreakerOpenException("Circuit is OPEN")
            try:
                result = await func(*args, **kwargs)
                circuit.record_success()
                return result
            except Exception as e:
                circuit.record_failure()
                raise e
        return wrapper
    return decorator
```

## 3. Observability (Structured Logging)

Context-aware logging.

```python
import logging
import json
import contextvars

trace_id_ctx = contextvars.ContextVar("trace_id", default="no-trace")

class StructuredLogger:
    def info(self, message: str, **kwargs):
        log_entry = {
            "level": "INFO",
            "message": message,
            "trace_id": trace_id_ctx.get(),
            **kwargs
        }
        print(json.dumps(log_entry))

    def error(self, message: str, **kwargs):
        log_entry = {
            "level": "ERROR",
            "message": message,
            "trace_id": trace_id_ctx.get(),
            **kwargs
        }
        print(json.dumps(log_entry))

logger = StructuredLogger()
```

## 4. The Core Logic (Async & Decoupled)

```python
class LogisticsCore:
    def __init__(self, repo: IRepository, supplier: ISupplierAPI):
        self.repo = repo
        self.supplier = supplier

    async def process_order(self, order_id: str, dest: str):
        tid = str(uuid.uuid4())
        trace_id_ctx.set(tid)
        
        logger.info("Processing Order", order_id=order_id)
        
        shipment = Shipment(
            id=str(uuid.uuid4()),
            order_id=order_id,
            destination=dest,
            status=ShipmentStatus.PENDING
        )
        
        await self.repo.save_shipment(shipment)
        
        # Async Dispatch with Resilience
        try:
            success = await self.supplier.request_dispatch(shipment)
            if success:
                shipment.status = ShipmentStatus.SHIPPED
            else:
                logger.error("Supplier rejected dispatch")
        except CircuitBreakerOpenException:
            logger.error("Circuit OPEN. Queuing for retry.")
            # Fallback logic here (e.g. push to DLQ)
        except Exception as e:
            logger.error(f"Unexpected error: {e}")
            
        await self.repo.save_shipment(shipment)
        logger.info("Order Processed", status=shipment.status.value)
```
