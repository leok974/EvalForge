## Python Loop

> [!NOTE]
> **What you'll build:** process a list of sensor readings using a loop.

---

## 1) What You'll Build
You'll write a function that loops through readings, filters invalid values, and returns a count.

## 2) The Concept in 30 Seconds
A loop repeats a block of logic across a sequence (lists, strings, ranges). It's one of the most common patterns in real code.

## 3) Key Terms
- **loop**
- **iteration**
- **filter**
- **counter**

---

## 4) Step-by-Step Walkthrough

### **Setup**
- Read the starter code.
- Identify the input list and the expected output.

### **Implementation**
- Loop through the readings
- Ignore negative values
- Count valid values and return the count

### **Testing**
- Click **Run**
- Confirm there are no errors
- Try 1–2 different input lists

---

## 5) Example Implementation
```py
# Example: Count positive numbers
def count_positives(numbers):
    count = 0
    for n in numbers:
        if n > 0:
            count += 1
    return count
```

---

## 6) Common Pitfalls

> [!WARNING]
>
> * Not reading the error messages carefully
> * Forgetting edge cases (like 0)
> * Missing import statements (not needed here but good to know)

---

## 7) Check Yourself

* [ ] Does your code run without errors?
* [ ] Did you test with different inputs?
* [ ] Does it match the expected output?
