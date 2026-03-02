"""
Shortage Predictor Service
Predicts future attendance shortages
"""


class ShortagePredictor:
    """Predict attendance shortage scenarios"""

    @staticmethod
    def predict_scenario(total_classes, classes_attended, scenario_type, min_percentage=75):
        scenarios = {}

        if scenario_type == 'worst_case':
            for miss_count in [5, 10, 15]:
                new_total = total_classes + miss_count
                new_attended = classes_attended
                pct = (new_attended / new_total * 100) if new_total > 0 else 0
                scenarios[f'miss_{miss_count}'] = round(pct, 2)

        elif scenario_type == 'best_case':
            for attend_count in [5, 10, 15]:
                new_total = total_classes + attend_count
                new_attended = classes_attended + attend_count
                pct = (new_attended / new_total * 100) if new_total > 0 else 0
                scenarios[f'attend_{attend_count}'] = round(pct, 2)

        elif scenario_type == 'maintain':
            current_rate = classes_attended / total_classes if total_classes > 0 else 0
            for future_count in [5, 10, 15, 20]:
                new_total = total_classes + future_count
                new_attended = classes_attended + (future_count * current_rate)
                pct = (new_attended / new_total * 100) if new_total > 0 else 0
                scenarios[f'after_{future_count}'] = round(pct, 2)

        return scenarios

    @staticmethod
    def get_shortage_alert(stats):
        """Generate shortage alert if needed"""
        percentage = stats['percentage']
        can_skip = stats['can_skip_safely']
        alerts = []

        if percentage < 75:
            alerts.append({
                'level': 'CRITICAL',
                'message': 'You are currently in shortage! Immediate action required.',
                'action': f"Attend next {stats['classes_needed_to_recover']} classes without fail."
            })
        elif percentage < 80:
            alerts.append({
                'level': 'HIGH',
                'message': 'You are very close to shortage threshold.',
                'action': f'You can only miss {can_skip} more classes. Be very careful!'
            })
        elif percentage < 85:
            alerts.append({
                'level': 'MEDIUM',
                'message': 'Your attendance is in warning zone.',
                'action': f'You can miss up to {can_skip} classes, but try to attend regularly.'
            })

        return alerts

    @staticmethod
    def predict_trend(attendance_records):
        """Analyze attendance trend over time"""
        if len(attendance_records) < 5:
            return {'trend': 'insufficient_data', 'message': 'Need at least 5 records for trend analysis.'}

        recent_records = sorted(attendance_records, key=lambda x: x.date)[-10:]
        recent_present = sum(1 for r in recent_records if r.status == 'Present')
        recent_rate = recent_present / len(recent_records)

        total_present = sum(1 for r in attendance_records if r.status == 'Present')
        overall_rate = total_present / len(attendance_records)

        if recent_rate > overall_rate + 0.1:
            trend = 'improving'
        elif recent_rate < overall_rate - 0.1:
            trend = 'declining'
        else:
            trend = 'stable'

        return {
            'trend': trend,
            'recent_rate': round(recent_rate * 100, 2),
            'overall_rate': round(overall_rate * 100, 2),
            'message': f'Your attendance trend is {trend}.'
        }
