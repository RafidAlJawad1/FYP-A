import React, { useState } from "react";

const RegistrationForm = () => {
  const [role, setRole] = useState("");
  const [firstName, setFirstName] = useState("");
  const [lastName, setLastName] = useState("");
  const [email, setEmail] = useState("");
  const [phone, setPhone] = useState("");
  const [dob, setDob] = useState("");
  const [password, setPassword] = useState("");
  const [confirmPassword, setConfirmPassword] = useState("");

  const handleRoleSelection = (selectedRole) => {
    setRole(selectedRole);
  };

  const handleSubmit = async (e) => {
    e.preventDefault();

    // Check if password and confirm password match
    if (password !== confirmPassword) {
      alert("Passwords do not match!");
      return;
    }

    // Data to send to the backend
    const userData = {
      name: `${firstName} ${lastName}`,
      email: email,
      phone: phone,
      dob: dob,
      password: password,
      password_confirmation: confirmPassword,
      role: role,
    };

    try {
      const response = await fetch("http://localhost:8000/api/register", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify(userData),
      });

      const data = await response.json();

      if (response.ok) {
        alert("Registration Complete!");
      } else {
        alert("Registration failed: " + data.message);
      }
    } catch (error) {
      console.error("Error:", error);
      alert("An error occurred while registering.");
    }
  };

  return (
    <form onSubmit={handleSubmit} className="min-h-screen w-full p-8 bg-white flex flex-col justify-center">
      <div className="mb-8">
        <h2 className="text-2xl font-bold text-blue-600">Healthcare Portal Registration</h2>
        <div className="text-sm text-gray-600 mb-4">Create your account by selecting your role and completing the registration form</div>
        <div className="grid grid-cols-3 gap-4 mb-6">
          <button
            className={`p-4 text-center border rounded-lg ${
              role === "admin" ? "bg-blue-200" : "hover:bg-gray-200"
            }`}
            onClick={() => handleRoleSelection("admin")}
          >
            <div className="text-blue-600">Administrator</div>
            <div className="text-sm">Manage the healthcare system, users, and operations</div>
          </button>
          <button
            className={`p-4 text-center border rounded-lg ${
              role === "doctor" ? "bg-green-200" : "hover:bg-gray-200"
            }`}
            onClick={() => handleRoleSelection("doctor")}
          >
            <div className="text-green-600">Doctor</div>
            <div className="text-sm">Provide medical care and manage patient records</div>
          </button>
          <button
            className={`p-4 text-center border rounded-lg ${
              role === "patient" ? "bg-purple-200" : "hover:bg-gray-200"
            }`}
            onClick={() => handleRoleSelection("patient")}
          >
            <div className="text-purple-600">Patient</div>
            <div className="text-sm">Access your health records and schedule appointments</div>
          </button>
        </div>
      </div>

      <div className="mb-8">
        <h3 className="text-xl font-semibold text-gray-700 mb-4">Account Details</h3>
        <form onSubmit={handleSubmit}>
          <div className="mb-4">
            <label htmlFor="firstName" className="block text-gray-600">First Name</label>
            <input
              type="text"
              id="firstName"
              className="w-full p-3 border border-gray-300 rounded-lg"
              value={firstName}
              onChange={(e) => setFirstName(e.target.value)}
              required
            />
          </div>
          <div className="mb-4">
            <label htmlFor="lastName" className="block text-gray-600">Last Name</label>
            <input
              type="text"
              id="lastName"
              className="w-full p-3 border border-gray-300 rounded-lg"
              value={lastName}
              onChange={(e) => setLastName(e.target.value)}
              required
            />
          </div>
          <div className="mb-4">
            <label htmlFor="email" className="block text-gray-600">Email</label>
            <input
              type="email"
              id="email"
              className="w-full p-3 border border-gray-300 rounded-lg"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              required
            />
          </div>
          <div className="mb-4">
            <label htmlFor="phone" className="block text-gray-600">Phone Number</label>
            <input
              type="text"
              id="phone"
              className="w-full p-3 border border-gray-300 rounded-lg"
              value={phone}
              onChange={(e) => setPhone(e.target.value)}
              required
            />
          </div>
          <div className="mb-4">
            <label htmlFor="dob" className="block text-gray-600">Date of Birth</label>
            <input
              type="date"
              id="dob"
              className="w-full p-3 border border-gray-300 rounded-lg"
              value={dob}
              onChange={(e) => setDob(e.target.value)}
              required
            />
          </div>

          <div className="mb-4">
            <label htmlFor="password" className="block text-gray-600">Password</label>
            <input
              type="password"
              id="password"
              className="w-full p-3 border border-gray-300 rounded-lg"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              required
            />
          </div>
          <div className="mb-4">
            <label htmlFor="confirmPassword" className="block text-gray-600">Confirm Password</label>
            <input
              type="password"
              id="password_confirmation"
              className="w-full p-3 border border-gray-300 rounded-lg"
              value={confirmPassword}
              onChange={(e) => setConfirmPassword(e.target.value)}
              required
            />
          </div>

          <button
            type="submit"
            className="w-full p-3 bg-blue-600 text-white rounded-lg mt-4"
          >
            Register
          </button>
        </form>
      </div>
    </form>
  );
};

export default RegistrationForm;