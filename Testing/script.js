// Configuration for API endpoints
const API_CONFIG = {
    baseUrl: 'http://localhost:3000/api', // Replace with your actual backend URL
    endpoints: {
        treatmentRecommendation: '/treatment-recommendation',
        lifestyleGuidance: '/lifestyle-guidance'
    }
};

// Utility functions
const showElement = (element) => {
    element.style.display = 'block';
    element.classList.add('fade-in');
};

const hideElement = (element) => {
    element.style.display = 'none';
    element.classList.remove('fade-in');
};

const showLoading = (button) => {
    const btnText = button.querySelector('.btn-text');
    const spinner = button.querySelector('.loading-spinner');
    
    btnText.textContent = 'Processing...';
    spinner.style.display = 'inline-block';
    button.disabled = true;
};

const hideLoading = (button, originalText) => {
    const btnText = button.querySelector('.btn-text');
    const spinner = button.querySelector('.loading-spinner');
    
    btnText.textContent = originalText;
    spinner.style.display = 'none';
    button.disabled = false;
};

const showMessage = (container, message, type = 'success') => {
    const messageDiv = document.createElement('div');
    messageDiv.className = `${type}-message fade-in`;
    messageDiv.textContent = message;
    
    // Remove any existing messages
    const existingMessages = container.querySelectorAll('.success-message, .error-message');
    existingMessages.forEach(msg => msg.remove());
    
    container.insertBefore(messageDiv, container.firstChild);
    
    // Auto-remove after 5 seconds
    setTimeout(() => {
        if (messageDiv.parentNode) {
            messageDiv.remove();
        }
    }, 5000);
};

// Form validation functions
const validateTreatmentForm = (formData) => {
    const errors = [];
    
    if (!formData.age || formData.age < 1 || formData.age > 120) {
        errors.push('Please enter a valid age between 1 and 120');
    }
    
    if (!formData.gender) {
        errors.push('Please select a gender');
    }
    
    if (!formData.symptoms || formData.symptoms.trim().length < 10) {
        errors.push('Please provide more detailed symptoms (at least 10 characters)');
    }
    
    return errors;
};

const validateLifestyleForm = (formData) => {
    const errors = [];
    
    if (!formData.age || formData.age < 1 || formData.age > 120) {
        errors.push('Please enter a valid age between 1 and 120');
    }
    
    if (!formData.gender) {
        errors.push('Please select a gender');
    }
    
    if (!formData.activityLevel) {
        errors.push('Please select your current activity level');
    }
    
    if (!formData.concerns || formData.concerns.trim().length < 10) {
        errors.push('Please provide more detailed lifestyle concerns (at least 10 characters)');
    }
    
    return errors;
};

// API call functions
const callTreatmentAPI = async (formData) => {
    try {
        // Simulate API call for testing - replace with actual API call
        await new Promise(resolve => setTimeout(resolve, 2000)); // 2 second delay
        
        // Mock response - replace with actual API call
        const mockResponse = {
            recommendations: [
                {
                    category: "Primary Treatment",
                    suggestion: "Based on the symptoms provided, consider consultation with a specialist for proper diagnosis.",
                    priority: "High"
                },
                {
                    category: "Supportive Care",
                    suggestion: "Rest, adequate hydration, and monitoring of symptoms is recommended.",
                    priority: "Medium"
                },
                {
                    category: "Follow-up",
                    suggestion: "Schedule follow-up appointment in 1-2 weeks if symptoms persist or worsen.",
                    priority: "Medium"
                }
            ],
            confidence: 0.75,
            sources: ["Medical Database A", "Clinical Guidelines B"],
            timestamp: new Date().toISOString()
        };
        
        /* 
        // Actual API call would look like this:
        const response = await fetch(`${API_CONFIG.baseUrl}${API_CONFIG.endpoints.treatmentRecommendation}`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(formData)
        });
        
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        
        const data = await response.json();
        return data;
        */
        
        return mockResponse;
    } catch (error) {
        console.error('Treatment API Error:', error);
        throw new Error('Failed to get treatment recommendations. Please try again.');
    }
};

const callLifestyleAPI = async (formData) => {
    try {
        // Simulate API call for testing - replace with actual API call
        await new Promise(resolve => setTimeout(resolve, 2000)); // 2 second delay
        
        // Mock response - replace with actual API call
        const mockResponse = {
            recommendations: {
                nutrition: [
                    "Increase intake of fruits and vegetables to 5-7 servings per day",
                    "Consider reducing processed foods and added sugars",
                    "Stay hydrated with 8-10 glasses of water daily"
                ],
                exercise: [
                    "Aim for 150 minutes of moderate-intensity exercise per week",
                    "Include strength training exercises 2-3 times per week",
                    "Start with 15-20 minute walks if currently sedentary"
                ],
                sleep: [
                    "Maintain consistent sleep schedule (7-9 hours nightly)",
                    "Create a relaxing bedtime routine",
                    "Limit screen time 1 hour before bed"
                ],
                mentalHealth: [
                    "Practice stress-reduction techniques like meditation or deep breathing",
                    "Consider regular social activities and connections",
                    "Take breaks throughout the day for mental wellness"
                ]
            },
            confidence: 0.82,
            personalizedTips: [
                "Based on your goals, focus on gradual changes rather than dramatic lifestyle shifts",
                "Track your progress weekly to stay motivated"
            ],
            timestamp: new Date().toISOString()
        };
        
        /* 
        // Actual API call would look like this:
        const response = await fetch(`${API_CONFIG.baseUrl}${API_CONFIG.endpoints.lifestyleGuidance}`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(formData)
        });
        
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        
        const data = await response.json();
        return data;
        */
        
        return mockResponse;
    } catch (error) {
        console.error('Lifestyle API Error:', error);
        throw new Error('Failed to get lifestyle recommendations. Please try again.');
    }
};

// Results display functions
const displayTreatmentResults = (results) => {
    const resultsContainer = document.getElementById('recommendationResults');
    const confidenceElement = document.getElementById('confidenceScore');
    
    if (!resultsContainer || !confidenceElement) return;
    
    // Display recommendations
    let html = '<div class="recommendations-list">';
    results.recommendations.forEach((rec, index) => {
        html += `
            <div class="recommendation-item">
                <h4>${rec.category} <span class="priority priority-${rec.priority.toLowerCase()}">${rec.priority} Priority</span></h4>
                <p>${rec.suggestion}</p>
            </div>
        `;
    });
    html += '</div>';
    
    if (results.sources && results.sources.length > 0) {
        html += '<div class="sources"><h4>Sources:</h4><ul>';
        results.sources.forEach(source => {
            html += `<li>${source}</li>`;
        });
        html += '</ul></div>';
    }
    
    resultsContainer.innerHTML = html;
    confidenceElement.textContent = `${Math.round(results.confidence * 100)}%`;
    
    // Show results section
    const resultsSection = document.getElementById('resultsSection');
    showElement(resultsSection);
    
    // Scroll to results
    resultsSection.scrollIntoView({ behavior: 'smooth' });
};

const displayLifestyleResults = (results) => {
    const categories = ['nutrition', 'exercise', 'sleep', 'mentalHealth'];
    const confidenceElement = document.getElementById('lifestyleConfidence');
    
    categories.forEach(category => {
        const categoryElement = document.getElementById(`${category}Guidance`);
        if (categoryElement && results.recommendations[category]) {
            const contentDiv = categoryElement.querySelector('.category-content');
            let html = '<ul class="recommendation-list">';
            results.recommendations[category].forEach(item => {
                html += `<li>${item}</li>`;
            });
            html += '</ul>';
            contentDiv.innerHTML = html;
        }
    });
    
    if (confidenceElement) {
        confidenceElement.textContent = `${Math.round(results.confidence * 100)}%`;
    }
    
    // Show results section
    const resultsSection = document.getElementById('lifestyleResults');
    showElement(resultsSection);
    
    // Scroll to results
    resultsSection.scrollIntoView({ behavior: 'smooth' });
};

// Form handlers
const handleTreatmentForm = async (event) => {
    event.preventDefault();
    
    const form = event.target;
    const submitBtn = form.querySelector('.submit-btn');
    const formData = new FormData(form);
    
    // Convert FormData to object
    const data = {};
    for (let [key, value] of formData.entries()) {
        data[key] = value;
    }
    
    // Validate form
    const errors = validateTreatmentForm(data);
    if (errors.length > 0) {
        showMessage(form, errors.join('. '), 'error');
        return;
    }
    
    try {
        showLoading(submitBtn);
        const results = await callTreatmentAPI(data);
        displayTreatmentResults(results);
        showMessage(form, 'Treatment recommendations generated successfully!', 'success');
    } catch (error) {
        showMessage(form, error.message, 'error');
    } finally {
        hideLoading(submitBtn, 'Get Treatment Recommendations');
    }
};

const handleLifestyleForm = async (event) => {
    event.preventDefault();
    
    const form = event.target;
    const submitBtn = form.querySelector('.submit-btn');
    const formData = new FormData(form);
    
    // Convert FormData to object, handling checkboxes
    const data = {};
    const goals = [];
    
    for (let [key, value] of formData.entries()) {
        if (key === 'goals') {
            goals.push(value);
        } else {
            data[key] = value;
        }
    }
    
    data.goals = goals;
    
    // Validate form
    const errors = validateLifestyleForm(data);
    if (errors.length > 0) {
        showMessage(form, errors.join('. '), 'error');
        return;
    }
    
    try {
        showLoading(submitBtn);
        const results = await callLifestyleAPI(data);
        displayLifestyleResults(results);
        showMessage(form, 'Lifestyle recommendations generated successfully!', 'success');
    } catch (error) {
        showMessage(form, error.message, 'error');
    } finally {
        hideLoading(submitBtn, 'Get Lifestyle Recommendations');
    }
};

// Initialize page functionality
const initializePage = () => {
    // Treatment form
    const treatmentForm = document.getElementById('treatmentForm');
    if (treatmentForm) {
        treatmentForm.addEventListener('submit', handleTreatmentForm);
    }
    
    // Lifestyle form
    const lifestyleForm = document.getElementById('lifestyleForm');
    if (lifestyleForm) {
        lifestyleForm.addEventListener('submit', handleLifestyleForm);
    }
    
    // Add smooth scrolling for navigation
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function (e) {
            e.preventDefault();
            const target = document.querySelector(this.getAttribute('href'));
            if (target) {
                target.scrollIntoView({
                    behavior: 'smooth'
                });
            }
        });
    });
    
    // Add form input enhancements
    const inputs = document.querySelectorAll('input, textarea, select');
    inputs.forEach(input => {
        input.addEventListener('focus', function() {
            this.parentElement.classList.add('focused');
        });
        
        input.addEventListener('blur', function() {
            this.parentElement.classList.remove('focused');
        });
    });
};

// Initialize when DOM is loaded
document.addEventListener('DOMContentLoaded', initializePage);

// Add some additional CSS for enhanced form states
const additionalCSS = `
    .form-group.focused label {
        color: #667eea;
    }
    
    .recommendation-item {
        margin-bottom: 20px;
        padding: 15px;
        border-left: 3px solid #667eea;
        background: #f8f9fa;
        border-radius: 8px;
    }
    
    .recommendation-item h4 {
        margin-bottom: 10px;
        color: #333;
        display: flex;
        justify-content: space-between;
        align-items: center;
    }
    
    .priority {
        font-size: 0.8em;
        padding: 4px 8px;
        border-radius: 12px;
        font-weight: normal;
    }
    
    .priority-high {
        background: #ffebee;
        color: #c62828;
    }
    
    .priority-medium {
        background: #fff3e0;
        color: #ef6c00;
    }
    
    .priority-low {
        background: #e8f5e8;
        color: #2e7d32;
    }
    
    .sources {
        margin-top: 25px;
        padding: 15px;
        background: #e3f2fd;
        border-radius: 8px;
    }
    
    .sources h4 {
        color: #1565c0;
        margin-bottom: 10px;
    }
    
    .sources ul {
        margin-left: 20px;
    }
    
    .recommendation-list {
        margin: 0;
        padding-left: 20px;
    }
    
    .recommendation-list li {
        margin-bottom: 8px;
        line-height: 1.5;
    }
`;

// Inject additional CSS
const style = document.createElement('style');
style.textContent = additionalCSS;
document.head.appendChild(style);
