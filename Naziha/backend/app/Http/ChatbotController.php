<?php

namespace App\Http\Controllers;

use Illuminate\Http\Request;

class ChatbotController extends Controller
{
    // This method will handle incoming chatbot messages
    public function handleMessage(Request $request)
    {
        // Validate the incoming request
        $request->validate([
            'message' => 'required|string',
        ]);

        $userMessage = $request->input('message');

        // Basic mocked responses based on the user message
        $response = $this->getAIResponse($userMessage);

        return response()->json(['response' => $response]);
    }

    // Function to mock AI response based on user input
    private function getAIResponse($message)
    {
        // Define some basic responses
        $responses = [
            'depression symptoms' => 'Common symptoms of depression include persistent sadness, loss of interest in activities, and changes in sleep or appetite.',
            'cbt for anxiety' => 'Cognitive Behavioral Therapy (CBT) is highly effective for treating anxiety. It helps by addressing negative thought patterns.',
            'stress lifestyle changes' => 'Lifestyle changes like regular exercise, healthy eating, and mindfulness can help manage stress.',
            'default' => 'I can provide general health information, but for personal medical advice, please consult a healthcare professional.',
        ];

        // Return the appropriate response or the default response
        $lowerMessage = strtolower($message);
        foreach ($responses as $key => $response) {
            if (strpos($lowerMessage, strtolower($key)) !== false) {
                return $response;
            }
        }

        return $responses['default'];
    }
}
