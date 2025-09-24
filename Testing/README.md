# RAG System Frontend - Medical Recommendation Interface

A modern, responsive web interface for testing RAG (Retrieval-Augmented Generation) systems focused on medical treatment recommendations and lifestyle guidance.

## Features

### 🏥 Treatment Recommendation Page
- Patient information collection (age, gender, medical history)
- Symptom description and allergy tracking
- Real-time treatment recommendations
- Confidence scoring and source attribution
- Medical disclaimer and safety warnings

### 🌱 Lifestyle Guidance Page  
- Personal health profile setup
- Activity level and health goals selection
- Comprehensive lifestyle recommendations across:
  - Nutrition advice
  - Exercise planning
  - Sleep optimization
  - Mental wellness guidance
- Personalized tips and progress tracking

### 🎨 Modern UI/UX Features
- Responsive design for all devices
- Smooth animations and transitions
- Loading states and error handling
- Accessibility-friendly interface
- Clean, medical-themed design

## Quick Start

1. **Open the website**: Simply open `treatment-recommendation.html` in your web browser
2. **Navigate**: Use the navigation bar to switch between Treatment and Lifestyle pages
3. **Test the interface**: Fill out the forms to see mock recommendations (no backend required for testing)

## File Structure

```
├── treatment-recommendation.html  # Treatment recommendation page
├── lifestyle-guidance.html       # Lifestyle guidance page  
├── styles.css                   # Comprehensive styling
├── script.js                    # Interactive functionality
├── BACKEND_API_STRUCTURE.md     # Backend implementation guide
└── README.md                    # This file
```

## Backend Integration

The frontend is designed to work with a RESTful API backend. See `BACKEND_API_STRUCTURE.md` for:
- Complete API endpoint specifications
- Request/response formats
- RAG system integration requirements
- Database schema suggestions
- Security and deployment considerations

### API Configuration
Update the API configuration in `script.js`:
```javascript
const API_CONFIG = {
    baseUrl: 'http://your-backend-url/api',
    endpoints: {
        treatmentRecommendation: '/treatment-recommendation',
        lifestyleGuidance: '/lifestyle-guidance'
    }
};
```

## Testing Mode

The current implementation includes mock responses for testing the interface without a backend. The forms will:
- Validate user input
- Show loading states
- Display formatted mock recommendations
- Demonstrate error handling

## Browser Compatibility

- ✅ Chrome (latest)
- ✅ Firefox (latest)  
- ✅ Safari (latest)
- ✅ Edge (latest)
- ✅ Mobile browsers

## Customization

### Styling
- Modify `styles.css` for visual customization
- CSS custom properties for easy theme changes
- Responsive breakpoints for different screen sizes

### Functionality  
- Update `script.js` for behavior modifications
- Add new form fields or validation rules
- Customize API integration logic

### Content
- Edit HTML files for content changes
- Update medical disclaimers as needed
- Modify form labels and instructions

## Security Notes

⚠️ **Important**: This is a testing interface. For production use:
- Implement proper input sanitization
- Add HTTPS enforcement
- Include CSRF protection
- Follow medical data privacy regulations
- Add proper error logging and monitoring

## Contributing

This is a testing interface for RAG system development. Feel free to:
- Customize the UI for your specific use case
- Add new form fields or recommendation categories
- Integrate with your RAG backend system
- Enhance accessibility features

## License

This project is provided as-is for testing and development purposes.
