<?php

use Illuminate\Http\Request;
use Illuminate\Support\Facades\Route;
use App\Http\Controllers\RiskPredictionController;
use App\Http\Controllers\AuthController;

Route::post('/predict', [RiskPredictionController::class, 'predict']);

Route::post('/register', [AuthController::class, 'register']);
Route::post('/login', [AuthController::class, 'login']);
