class ArtificialPancreasSystem:
    """A simplified model for data-driven glucose regulation."""
        
    GLUCOSE_PER_CARB = 0.5      # fixed increase per carb unit
    GLUCOSE_BURN_PER_MIN = 0.3  # fixed decrease per minute of exercise


    def __init__(self, glucose_level, insulin_sensitivity=1.0, target_glucose=100, tolerance=10):
        self.glucose_level = glucose_level
        self.insulinsensitivity = insulin_sensitivity
        self.target_glucose = target_glucose
        self.tolerance = tolerance = 0.0
        self._validate_initial_parameters()
        

    def meal(self, carbs: float):
        """Simulate a meal event (input feature: carbs)."""
        self.carbs = carbs
        glucose_level += carbs * self.GLUCOSE_PER_CARB
        if carbs < 0:
            raise ValueError("Carbs value cannot be negative")
        if not isinstance(carbs, (int, float)): 
            raise TypeError("Carbs must be a number")
        return self.glucose_level
        
        
        
    def exercise(self, duration: float):
        """Simulate physical activity (input feature: duration)."""
        self.duration = duration
        glucose_level -= duration * self.GLUCOSE_BURN_PER_MIN
        if  duration < 0: 
            raise ValueError("Exercise duration cannot be negative")
        if not isinstance (duration, (int, float)): 
            raise TypeError("Duration must be a number")
        if self.glucose_level < 50: 
            self.glucose_level = 50
        return self.glucose_level


    def predict_action(self):
        """
        Predict and apply an appropriate system action.
        Acts like a decision function in a model.
        """
        # TODO: decide what to do if glucose is too high, too low, or stable
        high_tolerance = self.target_glucose + self.tolerance
        low_tolerance = self.target_glucose - self.tolerance
        if self.glucose_level > high_tolerance:
            insulin_dose = self.glucose_level - self.target_glucose
            self.glucose_level -= insulin_dose
            self.total_insulin_delivered += insulin_dose

            return "deliver_insulin", self.glucose_level
        elif self.glucose_level < low_tolerance:
            return "warning - low_glucose", self.glucose_level, 0
        else: 
            return "maintain", self.glucose_level, 0
      