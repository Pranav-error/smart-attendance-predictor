import React from 'react';

const RiskIndicator = ({ riskZone }) => {
    if (!riskZone) return null;

    return (
        <div className="risk-indicator" style={{ backgroundColor: riskZone.color }}>
            <span className="risk-emoji">{riskZone.emoji}</span>
            <span className="risk-zone">{riskZone.zone}</span>
        </div>
    );
};

export default RiskIndicator;
