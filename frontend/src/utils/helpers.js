// Format date to YYYY-MM-DD
export const formatDate = (date) => {
    const d = new Date(date);
    const year = d.getFullYear();
    const month = String(d.getMonth() + 1).padStart(2, '0');
    const day = String(d.getDate()).padStart(2, '0');
    return `${year}-${month}-${day}`;
};

// Get today's date
export const getTodayDate = () => formatDate(new Date());

// Calculate days until date
export const daysUntil = (targetDate) => {
    const today = new Date();
    const target = new Date(targetDate);
    const diffTime = target - today;
    const diffDays = Math.ceil(diffTime / (1000 * 60 * 60 * 24));
    return diffDays;
};

// Validate email
export const isValidEmail = (email) => {
    const re = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    return re.test(email);
};

// Get risk color
export const getRiskColor = (percentage) => {
    if (percentage >= 85) return '#4CAF50';
    if (percentage >= 75) return '#FF9800';
    return '#F44336';
};

// Format percentage
export const formatPercentage = (value) => {
    return typeof value === 'number' ? value.toFixed(2) : '0.00';
};
