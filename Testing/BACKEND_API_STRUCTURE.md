# Backend API Structure for RAG System

This document outlines the required backend API structure to support the frontend interface for the RAG-based medical recommendation system.

## Base Configuration

- **Base URL**: `http://localhost:3000/api` (configurable in `script.js`)
- **Content-Type**: `application/json`
- **CORS**: Enable CORS for frontend domain

## API Endpoints

### 1. Treatment Recommendation Endpoint

**Endpoint**: `POST /api/treatment-recommendation`

**Request Body**:
```json
{
  "age": 35,
  "gender": "male|female|other",
  "medicalHistory": "Previous conditions, medications, surgeries...",
  "symptoms": "Current symptoms description...",
  "allergies": "Known allergies..."
}
```

**Response Format**:
```json
{
  "recommendations": [
    {
      "category": "Primary Treatment",
      "suggestion": "Detailed treatment recommendation...",
      "priority": "High|Medium|Low"
    },
    {
      "category": "Supportive Care",
      "suggestion": "Supportive care recommendations...",
      "priority": "Medium"
    }
  ],
  "confidence": 0.85,
  "sources": [
    "Medical Database Reference 1",
    "Clinical Guidelines Reference 2"
  ],
  "timestamp": "2025-09-22T10:30:00Z"
}
```

### 2. Lifestyle Guidance Endpoint

**Endpoint**: `POST /api/lifestyle-guidance`

**Request Body**:
```json
{
  "age": 28,
  "gender": "female",
  "height": 165,
  "weight": 60,
  "activityLevel": "sedentary|light|moderate|active|very-active",
  "goals": ["weight-loss", "cardiovascular", "stress-management"],
  "currentDiet": "Description of current eating habits...",
  "healthConditions": "Existing health conditions...",
  "concerns": "Specific lifestyle concerns..."
}
```

**Response Format**:
```json
{
  "recommendations": {
    "nutrition": [
      "Increase intake of fruits and vegetables...",
      "Consider reducing processed foods...",
      "Stay hydrated with 8-10 glasses of water daily"
    ],
    "exercise": [
      "Aim for 150 minutes of moderate-intensity exercise...",
      "Include strength training exercises...",
      "Start with 15-20 minute walks..."
    ],
    "sleep": [
      "Maintain consistent sleep schedule...",
      "Create a relaxing bedtime routine...",
      "Limit screen time before bed..."
    ],
    "mentalHealth": [
      "Practice stress-reduction techniques...",
      "Consider regular social activities...",
      "Take breaks throughout the day..."
    ]
  },
  "confidence": 0.82,
  "personalizedTips": [
    "Based on your goals, focus on gradual changes...",
    "Track your progress weekly to stay motivated"
  ],
  "timestamp": "2025-09-22T10:30:00Z"
}
```

## Error Handling

### Standard Error Response Format:
```json
{
  "error": true,
  "message": "Human-readable error message",
  "code": "ERROR_CODE",
  "timestamp": "2025-09-22T10:30:00Z"
}
```

### Common HTTP Status Codes:
- `200 OK`: Successful request
- `400 Bad Request`: Invalid input data
- `422 Unprocessable Entity`: Validation errors
- `500 Internal Server Error`: Server-side errors
- `503 Service Unavailable`: RAG system temporarily unavailable

## RAG System Integration Points

### Required RAG System Components:

1. **Document Retrieval System**
   - Medical literature database
   - Clinical guidelines repository
   - Treatment protocols database
   - Lifestyle and wellness knowledge base

2. **Embedding and Similarity Search**
   - Convert user input to embeddings
   - Retrieve relevant documents based on similarity
   - Rank and filter results by relevance

3. **Language Model Integration**
   - Process retrieved documents and user input
   - Generate contextual recommendations
   - Ensure medical accuracy and safety

4. **Confidence Scoring**
   - Calculate recommendation confidence based on:
     - Document relevance scores
     - Model certainty
     - Source credibility
     - Input completeness

## Security Considerations

1. **Input Validation**
   - Sanitize all user inputs
   - Validate data types and ranges
   - Implement rate limiting

2. **Data Privacy**
   - Don't log sensitive medical information
   - Implement proper data encryption
   - Follow HIPAA guidelines if applicable

3. **Medical Disclaimer**
   - Include appropriate medical disclaimers
   - Log recommendation generation for audit trails
   - Implement safety checks for high-risk recommendations

## Database Schema Suggestions

### User Sessions Table:
```sql
CREATE TABLE user_sessions (
    id UUID PRIMARY KEY,
    session_data JSONB,
    created_at TIMESTAMP,
    expires_at TIMESTAMP
);
```

### Recommendations Log:
```sql
CREATE TABLE recommendations_log (
    id UUID PRIMARY KEY,
    session_id UUID REFERENCES user_sessions(id),
    recommendation_type VARCHAR(50), -- 'treatment' or 'lifestyle'
    input_data JSONB,
    recommendations JSONB,
    confidence_score DECIMAL(3,2),
    sources TEXT[],
    created_at TIMESTAMP
);
```

## Implementation Technologies

### Recommended Backend Stack:
- **Framework**: Node.js with Express, Python with FastAPI, or similar
- **Database**: PostgreSQL with JSONB support for flexible data storage
- **RAG Framework**: LangChain, LlamaIndex, or custom implementation
- **Vector Database**: Pinecone, Weaviate, or Chroma for document embeddings
- **LLM**: OpenAI GPT-4, Anthropic Claude, or open-source alternatives

### Environment Variables:
```env
PORT=3000
DATABASE_URL=postgresql://...
OPENAI_API_KEY=sk-...
VECTOR_DB_URL=...
CORS_ORIGIN=http://localhost:8080
LOG_LEVEL=info
```

## Testing Requirements

1. **Unit Tests**
   - Input validation functions
   - RAG retrieval accuracy
   - Response formatting

2. **Integration Tests**
   - End-to-end API workflows
   - Database operations
   - External service integrations

3. **Load Testing**
   - Concurrent user handling
   - Response time benchmarks
   - RAG system performance under load

## Monitoring and Logging

### Key Metrics to Track:
- Response times for each endpoint
- RAG system retrieval accuracy
- Confidence score distributions
- Error rates and types
- User session patterns

### Logging Requirements:
- Request/response logging (sanitized)
- RAG system performance metrics
- Error tracking and alerting
- Usage analytics for system improvement

## Deployment Considerations

1. **Containerization**: Use Docker for consistent deployments
2. **Scaling**: Implement horizontal scaling for RAG components
3. **Caching**: Cache frequent queries and embeddings
4. **Health Checks**: Implement health check endpoints
5. **Documentation**: Provide OpenAPI/Swagger documentation

This structure provides a solid foundation for implementing the backend RAG system that will serve the frontend interface effectively.
