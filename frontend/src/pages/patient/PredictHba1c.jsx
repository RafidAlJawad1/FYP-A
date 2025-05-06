import RiskPredictionForm from '../../components/RiskPredictionForm';
import './patient.css';

function PredictHba1c() {
    return (
        <div className="risk-page">
            <div className="risk-card">
                <h2>HbA1c Prediction Form</h2>
                <RiskPredictionForm />
            </div>
        </div>
    );
}

export default PredictHba1c;
