"""
Risk Analyzer Service
Analyzes attendance and determines risk zones
"""

class RiskAnalyzer:
    """Analyze attendance risk and provide recommendations"""
    
    SAFE_THRESHOLD = 85
    WARNING_THRESHOLD = 75
    
    @staticmethod
    def get_risk_zone(percentage):
        """
        Determine risk zone based on percentage
        SAFE: >= 85%
        WARNING: 75-84%
        DANGER: < 75%
        """
        if percentage >= RiskAnalyzer.SAFE_THRESHOLD:
            return {
                'zone': 'SAFE',
                'color': '#4CAF50',
                'emoji': '🟢',
                'message': "You're doing great! Keep it up!"
            }
        elif percentage >= RiskAnalyzer.WARNING_THRESHOLD:
            return {
                'zone': 'WARNING',
                'color': '#FF9800',
                'emoji': '🟡',
                'message': "Be careful! You're close to shortage."
            }
        else:
            return {
                'zone': 'DANGER',
                'color': '#F44336',
                'emoji': '🔴',
                'message': "Critical! Immediate action needed!"
            }
    
    @staticmethod
    def generate_recommendation(stats):
        """Generate personalized recommendation message"""
        percentage = stats['percentage']
        can_skip = stats['can_skip_safely']
        need_to_attend = stats['classes_needed_to_recover']
        predicted = stats['predicted_percentage_10_classes']
        
        recommendations = []
        
        if percentage >= RiskAnalyzer.SAFE_THRESHOLD:
            recommendations.append(f"✅ Excellent! You can safely skip up to {can_skip} classes.")
            recommendations.append(f"📊 If you maintain this trend, your attendance will be {predicted}% after 10 classes.")
        elif percentage >= RiskAnalyzer.WARNING_THRESHOLD:
            recommendations.append(f"⚠️ Warning! You can only skip {can_skip} more classes.")
            recommendations.append(f"📈 Attend the next {need_to_attend} classes consecutively to reach safe zone (85%).")
            recommendations.append(f"🎯 Predicted attendance: {predicted}% if trend continues.")
        else:
            recommendations.append(f"🚨 Danger! You're below the minimum requirement.")
            recommendations.append(f"📚 You MUST attend the next {need_to_attend} classes to recover.")
            recommendations.append(f"⛔ Missing even 1 more class could worsen your situation.")
            if predicted < percentage:
                recommendations.append(f"📉 Warning: Predicted to drop to {predicted}% if current trend continues!")
        
        return recommendations
    
    @staticmethod
    def analyze(stats):
        """Perform complete risk analysis"""
        risk_zone = RiskAnalyzer.get_risk_zone(stats['percentage'])
        recommendations = RiskAnalyzer.generate_recommendation(stats)
        
        return {
            'risk_zone': risk_zone,
            'recommendations': recommendations,
            'stats': stats
        }
