import pytest
from main.artificial_pancreas import ArtificialPancreasSystem
class TestArtificialPancreas:
    
    @pytest.fixture
    def stable_glucose_system(self):
        """Fixture providing a default system for testing"""
        return ArtificialPancreasSystem(glucose_level=100)
    
    @pytest.fixture
    def high_glucose_system(self):
        """Fixture for testing high glucose scenarios"""
        return ArtificialPancreasSystem(glucose_level=150, target_glucose=100, tolerance=10)
    
    @pytest.fixture
    def low_glucose_system(self):
        """Fixture for testing low glucose scenarios"""
        return ArtificialPancreasSystem(glucose_level=80, target_glucose=100, tolerance=10)

    def test_glucose_increases_after_meal(self, stable_glucose_system):
        """Test that glucose increases correctly after a meal"""
        initial_glucose = stable_glucose_system.glucose_level
        carbs = 40
        
        new_glucose = stable_glucose_system.meal(carbs)
        expected_increase = carbs * ArtificialPancreasSystem.GLUCOSE_PER_CARB
        
        assert new_glucose == initial_glucose + expected_increase
        assert stable_glucose_system.glucose_level == initial_glucose + expected_increase

    def test_glucose_decreases_after_exercise(self, stable_glucose_system):
        """Test that glucose decreases correctly after exercise"""
        initial_glucose = stable_glucose_system.glucose_level
        duration = 30
        
        new_glucose = stable_glucose_system.exercise(duration)
        expected_decrease = duration * ArtificialPancreasSystem.GLUCOSE_BURN_PER_MIN
        
        assert new_glucose == initial_glucose - expected_decrease
        assert stable_glucose_system.glucose_level == initial_glucose - expected_decrease

    def test_glucose_never_drops_below_min(self, stable_glucose_system):
        """Test that glucose never falls below the minimum safe level"""
        # Force glucose to very low level with excessive exercise
        stable_glucose_system.glucose_level = 60
        duration = 100  # Enough to push below minimum
        
        stable_glucose_system.exercise(duration)
        
        assert stable_glucose_system.glucose_level == ArtificialPancreasSystem.MIN_GLUCOSE

    def test_correct_action_high_glucose(self, high_glucose_system):
        """Test that high glucose triggers insulin delivery"""
        action, glucose, dose = high_glucose_system.predict_action()
        
        assert action == "deliver_insulin"
        assert dose > 0
        assert glucose < 150  # Should be reduced

    def test_correct_action_low_glucose(self, low_glucose_system):
        """Test that low glucose triggers warning"""
        action, glucose, dose = low_glucose_system.predict_action()
        
        assert action == "warn_low_glucose"
        assert dose == 0
        assert glucose == 80  # Should remain unchanged

    def test_correct_action_maintain(self, stable_glucose_system):
        """Test that glucose in target range returns maintain"""
        stable_glucose_system.glucose_level = 105
        
        action, glucose, dose = stable_glucose_system.predict_action()
        
        assert action == "maintain"
        assert dose == 0
        assert glucose == 105

    def test_insulin_tracking(self, high_glucose_system):
        """Test that insulin delivery is properly tracked"""
        initial_insulin = high_glucose_system.total_insulin_delivered
        
        action, glucose, dose = high_glucose_system.predict_action()
        
        assert high_glucose_system.total_insulin_delivered == initial_insulin + dose
        assert high_glucose_system.total_insulin_delivered > 0

    def test_sequential_events(self, stable_glucose_system):
        """Test multiple sequential events maintain correct state"""
        # Start with meal
        stable_glucose_system.meal(30)  # +15 glucose
        assert stable_glucose_system.glucose_level == 115
        
        # Then exercise
        stable_glucose_system.exercise(10)  # -3 glucose
        assert stable_glucose_system.glucose_level == 112
        
        # Check action (should be high - 112 > 110)
        action, glucose, dose = stable_glucose_system.predict_action()
        assert action == "deliver_insulin"
        assert glucose < 112  # Reduced by insulin

    def test_negative_carbs_raises_error(self, stable_glucose_system):
        """Test that negative carbs raise ValueError"""
        with pytest.raises(ValueError, match="Carbs cannot be negative"):
            stable_glucose_system.meal(-10)

    def test_negative_exercise_raises_error(self, stable_glucose_system):
        """Test that negative exercise duration raises ValueError"""
        with pytest.raises(ValueError, match="Exercise duration cannot be negative"):
            stable_glucose_system.exercise(-5)

    def test_invalid_initial_parameters(self):
        """Test that invalid initial parameters raise errors"""
        with pytest.raises(ValueError):
            ArtificialPancreasSystem(glucose_level=-10)
        
        with pytest.raises(ValueError):
            ArtificialPancreasSystem(glucose_level=100, insulin_sensitivity=0)
        
        with pytest.raises(ValueError):
            ArtificialPancreasSystem(glucose_level=100, tolerance=-5)

    def test_non_numeric_inputs(self, stable_glucose_system):
        """Test that non-numeric inputs raise TypeError"""
        with pytest.raises(TypeError):
            stable_glucose_system.meal("invalid")
        
        with pytest.raises(TypeError):
            stable_glucose_system.exercise("invalid")

    def test_insulin_sensitivity_effect(self):
        """Test that insulin sensitivity affects dose calculation"""
        sensitive_system = ArtificialPancreasSystem(glucose_level=150, insulin_sensitivity=2.0)
        normal_system = ArtificialPancreasSystem(glucose_level=150, insulin_sensitivity=1.0)
        
        action1, glucose1, dose1 = sensitive_system.predict_action()
        action2, glucose2, dose2 = normal_system.predict_action()
        
        # More sensitive system should deliver more insulin
        assert dose1 > dose2
        assert glucose1 < glucose2

    def test_boundary_conditions(self):
        """Test behavior at boundary conditions"""
        # Test upper boundary
        upper_bound_system = ArtificialPancreasSystem(glucose_level=110, target_glucose=100, tolerance=10)
        action, glucose, dose = upper_bound_system.predict_action()
        assert action == "maintain"  # Exactly at upper bound should maintain
        
        # Test lower boundary  
        lower_bound_system = ArtificialPancreasSystem(glucose_level=90, target_glucose=100, tolerance=10)
        action, glucose, dose = lower_bound_system.predict_action()
        assert action == "maintain"  # Exactly at lower bound should maintain

if __name__ == "__main__":
    pytest.main([__file__])