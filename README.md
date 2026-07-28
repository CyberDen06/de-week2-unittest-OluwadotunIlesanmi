# de-week2-Artificial_Pancreas_System-unittest-OluwadotunIlesanmi

# Artificial Pancreas System Simulation

A Python‑based simulation of an artificial pancreas system for glucose regulation, built to demonstrate robust object‑oriented programming and comprehensive unit testing in a healthcare‑focused context.

> **Important Disclaimer**  
> This project is a **simulation for educational and demonstration purposes only**. It is **not** intended for real‑world medical use, diagnosis, or treatment. Real artificial pancreas systems require FDA approval, extensive clinical trials, and sophisticated safety mechanisms. Never use this code to make health decisions.

## Learning Objectives

By completing this project, I:

- **Practiced Object-Oriented Programming (OOP)** to structure real‑world data logic.
- **Understood** how data inputs (meals, exercise) affect system states.
- **Applied algorithmic reasoning** to keep a value within safe boundaries (a form of regulation).
- **Wrote unit tests** using `pytest` to ensure model stability and correctness.
- **Discovered** the responsibility and ethical considerations when programming healthcare‑related systems.

---

## OOP in This Project

| Concept | How it's applied |
|---------|------------------|
| **Class** | `ArtificialPancreasSystem` is a blueprint for creating glucose‑regulation objects. |
| **Object / Instance** | Each `ArtificialPancreasSystem` instance represents a virtual patient with their own glucose level, sensitivity, and history. |
| **Encapsulation** | Internal state (`glucose_level`, `total_insulin_delivered`) is managed through methods; validation is done inside the class. |
| **Inheritance** | Not used in this simple implementation, but the pattern could be extended (e.g., different patient types). |
| **Polymorphism** | Could be demonstrated by having different insulin‑delivery strategies; here we keep it simple. |
| **Abstraction** | The system hides complex calculations behind simple methods like `meal()`, `exercise()`, and `predict_action()`. |


##  How It Works

The system simulates glucose regulation using three core methods:

### 1. `meal(carbs: float)`
- Increases glucose by `carbs * GLUCOSE_PER_CARB`.
- Validates input (must be non‑negative numeric).

### 2. `exercise(duration: float)`
- Decreases glucose by `duration * GLUCOSE_BURN_PER_MIN`.
- Glucose is **capped at a minimum safe level** (`MIN_GLUCOSE = 50`) to avoid unrealistic lows.
- Validates input.

### 3. `predict_action()`
- Compares current glucose to target range (`target_glucose ± tolerance`).
- If **above** upper bound:
  - Delivers insulin: dose = `(glucose - target_glucose) * insulin_sensitivity`.
  - Reduces glucose accordingly and tracks total insulin delivered.
  - Returns `("deliver_insulin", new_glucose, dose)`.
- If **below** lower bound:
  - Returns `("warn_low_glucose", glucose, 0)` (no action taken in this simulation).
- If **within** range:
  - Returns `("maintain", glucose, 0)`.

---

## Project Structure

```
de-week2-unittest-<yourname>/
├── main/
│   ├── __init__.py
│   └── artificial_pancreas.py
├── tests/
│   ├── __init__.py
│   └── test_artificial_pancreas.py
├── requirements.txt
├── .gitignore
└── README.md
```

##  Getting Started

### 1. Clone the repository
```bash
git clone https://github.com/<your-username>/de-week2-unittest-<yourname>.git
cd de-week2-unittest-<yourname>
```

### 2. Set up a virtual environment (recommended)
```bash
python -m venv .venv
source .venv/bin/activate   # On Windows: .venv\Scripts\activate
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```
*Only `pytest` is required for testing.*

### 4. Quick usage example (interactive)
```python
from main.artificial_pancreas import ArtificialPancreasSystem

# Create a system for a patient
patient = ArtificialPancreasSystem(glucose_level=100)

# Simulate a meal
patient.meal(40)          # glucose rises to 120

# Simulate exercise
patient.exercise(20)      # glucose drops to 114

# Let the system decide action
action, glucose, dose = patient.predict_action()
print(f"Action: {action}, New glucose: {glucose}, Insulin dose: {dose}")
```

### 5. Run the CLI demo (if you have one)
Not required, but you can add a simple `cli.py` if you wish.


## Testing
We use `pytest` for comprehensive unit testing. The test suite validates:

### Core Functional Tests
- Glucose increases after a meal.
- Glucose decreases after exercise.
- Glucose never drops below the defined minimum.
- Correct actions are returned for high, low, and stable glucose.

### Insulin Tracking
- Total insulin delivered increments correctly.

### Sequential Events
- Multiple actions (meal → exercise → prediction) update state correctly.

### Boundary Conditions
- Behaviour exactly at the upper/lower tolerance limits.

### Error Handling
- Negative carbs/exercise durations raise `ValueError`.
- Non‑numeric inputs raise `TypeError`.
- Invalid initial parameters (e.g., negative glucose) raise `ValueError`.

### Running the Tests
From the project root:
```bash
pytest -v
```
Or to run a specific test file:
```bash
pytest tests/test_artificial_pancreas.py
```

**Expected output:** All tests should pass.

---

## Parameter Reference

| Parameter | Description | Example |
|-----------|-------------|---------|
| `glucose_level` | Current glucose reading (mg/dL) | `100` |
| `insulin_sensitivity` | How much insulin reduces glucose per unit | `1.0` |
| `target_glucose` | Ideal glucose value the system aims for | `100` |
| `tolerance` | Range (±) around target considered stable | `10` |

> **Defaults:** `insulin_sensitivity=1.0`, `target_glucose=100`, `tolerance=10`.

---

## Extending the System

This simulation is intentionally simplified. Possible extensions:

- Add **continuous glucose monitoring (CGM)** noise.
- Implement different insulin **delivery profiles** (basal/bolus).
- Support **multiple meals/exercise** with time decay.
- Introduce **patient variability** (e.g., different sensitivities).
- Add a **graphical dashboard** to visualise glucose over time.

---

## Contributing

This project is part of a learning curriculum. Contributions that improve clarity, add test coverage, or extend functionality are welcome. Please open an issue or pull request.

---

## License

This project is for educational purposes. You are free to use, modify, and distribute it, but please retain the disclaimer and credit the original authors.

---

## ❤️ Acknowledgment

This simulation is inspired by the real‑world challenges faced by people with diabetes. It serves as a reminder of how thoughtful programming, rigorous testing, and human‑centred design can contribute to better health outcomes.

**Code with care. Test with rigour.**
```
