# 📐 Prediction Formulas Explained

This document explains all the mathematical formulas and prediction algorithms used in the Smart Attendance system.

## Core Calculations

### 1. Current Attendance Percentage

**Formula:**
```
percentage = (classes_attended / total_classes) × 100
```

**Example:**
- Total classes: 50
- Classes attended: 40
- Percentage = (40 / 50) × 100 = **80%**

**Implementation:** `AttendanceCalculator.calculate_percentage()`

---

### 2. Classes Can Skip Safely

This calculates how many classes a student can miss while staying above the minimum threshold.

**Formula:**
```
max_absences = floor((total_classes × min_percentage/100 - classes_attended) / (1 - min_percentage/100))
```

**Step-by-step breakdown:**
1. Calculate required attended classes: `total × (min%/100)`
2. Calculate buffer: `required - currently_attended`
3. Calculate relative absence rate: `1 - (min%/100)`
4. Divide buffer by rate and round down

**Example:**
- Total classes: 50
- Attended: 45
- Min percentage: 75%
- Required attended: 50 × 0.75 = 37.5
- Buffer: 37.5 - 45 = -7.5 (negative means surplus)
- Relative rate: 1 - 0.75 = 0.25
- Max absences: floor(-7.5 / 0.25) = floor(-30) = 0
  - Wait, that's wrong! Let's recalculate:
  - Actually: floor((50 × 0.75 - 45) / (1 - 0.75))
  - = floor((37.5 - 45) / 0.25)
  - = floor(-7.5 / 0.25)
  - = floor(-30)

**Correct calculation:**
After attending 45/50 classes (90%), you can skip:
- New formula: floor((T × p - A) / (1 - p))
- Where T = 50 + x (future total), A = 45 (current attended), p = 0.75
- We need: (45) / (50 + x) ≥ 0.75
- 45 ≥ 0.75(50 + x)
- 45 ≥ 37.5 + 0.75x
- 7.5 ≥ 0.75x
- x ≤ 10

So you can miss **10 more classes** safely!

**Implementation:** `AttendanceCalculator.classes_can_skip()`

---

### 3. Classes Needed to Recover

Calculates how many consecutive classes must be attended to reach minimum percentage.

**Formula:**
```
For minimum percentage p:
(attended + x) / (total + x) = p
Solving for x:
attended + x = p × (total + x)
attended + x = p × total + p × x
x - p × x = p × total - attended
x(1 - p) = p × total - attended
x = (p × total - attended) / (1 - p)
```

**Example:**
- Total: 50
- Attended: 30
- Current: 60%
- Target: 75%
- x = (0.75 × 50 - 30) / (1 - 0.75)
- x = (37.5 - 30) / 0.25
- x = 7.5 / 0.25
- x = 30

Need to attend **30 more classes** consecutively!

**Implementation:** `AttendanceCalculator.classes_needed_to_recover()`

---

### 4. Future Percentage Prediction

Predicts attendance percentage based on current trend.

**Formula:**
```
current_rate = attended / total
predicted_attended = attended + (future_classes × current_rate)
predicted_total = total + future_classes
future_percentage = (predicted_attended / predicted_total) × 100
```

**Example:**
- Total: 50
- Attended: 40
- Current rate: 40/50 = 0.8 (80%)
- Future classes: 10
- Predicted attended: 40 + (10 × 0.8) = 48
- Predicted total: 50 + 10 = 60
- Future %: (48/60) × 100 = **80%**

The percentage stays the same if you maintain your current rate!

**Implementation:** `AttendanceCalculator.predict_future_percentage()`

---

## Scenario Predictions

### Worst Case Scenario
**What if you miss the next N classes?**

```
new_total = total + N
new_attended = attended (no change)
new_percentage = (attended / new_total) × 100
```

### Best Case Scenario
**What if you attend the next N classes?**

```
new_total = total + N
new_attended = attended + N
new_percentage = ((attended + N) / (total + N)) × 100
```

### Maintain Current Trend
**What if you maintain current attendance rate?**

```
rate = attended / total
new_attended = attended + (N × rate)
new_total = total + N
new_percentage = (new_attended / new_total) × 100
```

---

## Risk Zone Classification

### Algorithm:
```python
if percentage >= 85:
    zone = "SAFE" (Green 🟢)
elif percentage >= 75:
    zone = "WARNING" (Yellow 🟡)
else:
    zone = "DANGER" (Red 🔴)
```

### Logic:
- **SAFE (≥85%)**: Comfortable buffer, can afford to miss classes
- **WARNING (75-84%)**: Close to threshold, be careful
- **DANGER (<75%)**: Below requirement, immediate action needed

---

## Trend Analysis

### Algorithm:
```python
recent_rate = present_count_last_10 / 10
overall_rate = total_present / total_classes

if recent_rate > overall_rate + 0.1:
    trend = "improving"
elif recent_rate < overall_rate - 0.1:
    trend = "declining"
else:
    trend = "stable"
```

This compares your recent attendance (last 10 classes) with your overall average.

---

## Recommendation Generation

### Logic Flow:
1. Check current percentage
2. Identify risk zone
3. Calculate actionable metrics
4. Generate personalized message

### Examples:

**SAFE Zone (90%):**
```
✅ Excellent! You can safely skip up to 12 classes.
📊 If you maintain this trend, your attendance will be 89% after 10 classes.
```

**WARNING Zone (78%):**
```
⚠️ Warning! You can only skip 3 more classes.
📈 Attend the next 8 classes consecutively to reach safe zone (85%).
🎯 Predicted attendance: 76% if trend continues.
```

**DANGER Zone (70%):**
```
🚨 Danger! You're below the minimum requirement.
📚 You MUST attend the next 15 classes to recover.
⛔ Missing even 1 more class could worsen your situation.
📉 Warning: Predicted to drop to 68% if current trend continues!
```

---

## Mathematical Properties

### Why These Formulas Work:

1. **Percentage is ratio-based**: Always between 0-100%
2. **Floor function**: Ensures we don't count partial classes
3. **Ceiling function**: For recovery, round up to be safe
4. **Iterative approach**: For complex scenarios, iterate until condition met

### Edge Cases Handled:

- Division by zero (when total = 0)
- Negative values (clamp to 0)
- Already at target (return 0 for recovery)
- Below threshold (can't skip any)

---

## Implementation Notes

All formulas are implemented in:
- `backend/app/services/attendance_calculator.py`
- `backend/app/services/risk_analyzer.py`
- `backend/app/services/shortage_predictor.py`

These services are used by the analytics routes to provide real-time calculations.

---

## Testing Scenarios

### Test Case 1: Perfect Attendance
- Total: 20, Attended: 20 → **100%** ✅
- Can skip: many classes
- Need to recover: 0

### Test Case 2: Exactly at Threshold
- Total: 100, Attended: 75 → **75%** ⚠️
- Can skip: 0 classes
- Need to recover: 0

### Test Case 3: Below Threshold
- Total: 40, Attended: 25 → **62.5%** 🚨
- Can skip: 0
- Need to recover: ~13 classes

---

## References

These formulas are based on:
- Basic ratio and proportion mathematics
- Probability and statistics concepts
- Real-world college attendance policies
- User experience best practices

