<?php

namespace App\Http\Controllers;

use Illuminate\Http\Request;
use App\Models\User;
use Illuminate\Support\Facades\Hash;
use Illuminate\Validation\ValidationException;

class RegistrationController extends Controller
{
    public function register(Request $request)
    {
        // Validate the input data
        $request->validate([
            'name' => 'required|string',
            'email' => 'required|string|email|unique:users,email',
            'password' => 'required|string|confirmed',
            'role' => 'required|string|in:admin,doctor,patient', // Ensure the role is one of the valid options
        ]);

        // Create the new user with the provided data
        $user = User::create([
            'name' => $request->name,
            'email' => $request->email,
            'password' => Hash::make($request->password),
            'role' => $request->role, // Set the role based on the user's input
        ]);

        // Return a success message
        return response()->json(['message' => 'User registered successfully', 'user' => $user], 201);
    }
}
