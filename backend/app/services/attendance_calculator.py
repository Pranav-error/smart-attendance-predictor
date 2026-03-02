"""
Attendance Calculator Service
Handles all attendance-related calculations
"""
import math

class AttendanceCalculator:
    """Calculate attendance statistics and predictions"""
    
    @staticmethod
    def calculate_percentage(total_classes, classes_attended):
        """Calculate current attendance percentage"""
        if total_classes == 0:
            return 0.0
        return round((classes_attended / total_classes) * 100, 2)
    
    @staticmethod
    def classes_can_skip(total_classes, classes_attended, min_percentage=75):
        """
        Calculate how many classes can be skipped safely
        Formula: max_absences = floor((total × min% - attended) / (1 - min%))
        """
        if total_classes == 0:
            return 0
        
        current_percentage = (classes_attended / total_classes) * 100
        
        if current_percentage < min_percentage:
            return 0  # Cannot skip any if already below threshold
        
        # Calculate maximum absences while maintaining min percentage
        min_ratio = min_percentage / 100
        numerator = (total_classes * min_ratio) - classes_attended
        denominator = 1 - min_ratio
        
        if denominator == 0:
            return 0
        
        max_absences = math.floor(numerator / denominator)
        return max(0, max_absences)
    
    @staticmethod
    def classes_needed_to_recover(total_classes, classes_attended, min_percentage=75):
        """
        Calculate classes needed to reach minimum percentage
        Formula: needed = ceil((min% × (total + x) - attended) / 1)
        where x is classes needed
        """
        if total_classes == 0:
            return 0
        
        current_percentage = (classes_attended / total_classes) * 100
        
        if current_percentage >= min_percentage:
            return 0  # Already at or above threshold
        
        # Calculate classes needed
        min_ratio = min_percentage / 100
        classes_needed = 0
        
        # Iteratively find the number of classes needed
        for x in range(1, 1000):  # Max 1000 iterations for safety
            future_total = total_classes + x
            future_attended = classes_attended + x
            future_percentage = (future_attended / future_total) * 100
            
            if future_percentage >= min_percentage:
                classes_needed = x
                break
        
        return classes_needed
    
    @staticmethod
    def predict_future_percentage(total_classes, classes_attended, future_classes=10):
        """
        Predict attendance percentage after future_classes
        Assumes student maintains current attendance rate
        """
        if total_classes == 0:
            return 0.0
        
        current_rate = classes_attended / total_classes
        predicted_attended = classes_attended + (future_classes * current_rate)
        predicted_total = total_classes + future_classes
        
        return round((predicted_attended / predicted_total) * 100, 2)
    
    @staticmethod
    def get_attendance_stats(attendance_records, min_percentage=75):
        """
        Get comprehensive attendance statistics
        """
        total_classes = len(attendance_records)
        classes_attended = sum(1 for record in attendance_records if record.status == 'Present')
        classes_absent = total_classes - classes_attended
        
        percentage = AttendanceCalculator.calculate_percentage(total_classes, classes_attended)
        can_skip = AttendanceCalculator.classes_can_skip(total_classes, classes_attended, min_percentage)
        need_to_attend = AttendanceCalculator.classes_needed_to_recover(total_classes, classes_attended, min_percentage)
        future_prediction = AttendanceCalculator.predict_future_percentage(total_classes, classes_attended, 10)
        
        return {
            'total_classes': total_classes,
            'classes_attended': classes_attended,
            'classes_absent': classes_absent,
            'percentage': percentage,
            'can_skip_safely': can_skip,
            'classes_needed_to_recover': need_to_attend,
            'predicted_percentage_10_classes': future_prediction,
            'minimum_required': min_percentage
        }
