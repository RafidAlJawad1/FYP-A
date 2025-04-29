# React + Vite

This template provides a minimal setup to get React working in Vite with HMR and some ESLint rules.

Currently, two official plugins are available:

- [@vitejs/plugin-react](https://github.com/vitejs/vite-plugin-react/blob/main/packages/plugin-react) uses [Babel](https://babeljs.io/) for Fast Refresh
- [@vitejs/plugin-react-swc](https://github.com/vitejs/vite-plugin-react/blob/main/packages/plugin-react-swc) uses [SWC](https://swc.rs/) for Fast Refresh

## Expanding the ESLint configuration

If you are developing a production application, we recommend using TypeScript with type-aware lint rules enabled. Check out the [TS template](https://github.com/vitejs/vite/tree/main/packages/create-vite/template-react-ts) for information on how to integrate TypeScript and [`typescript-eslint`](https://typescript-eslint.io) in your project.

# 🩺 Medical Chatbot Frontend

A **React 19** + **Vite** + **TailwindCSS** project providing a sleek frontend interface for a medical chatbot.

---

## 📋 Prerequisites

- **Node.js** (v18 or higher recommended)  
- **npm** (comes with Node.js) or **yarn** (optional alternative)

---

## Getting Started

### 1. Clone the Repository
```bash
git clone https://github.com/your-username/medical-chatbot-frontend.git
cd medical-chatbot-frontend
```

### 2. Install Dependencies

Using **npm**:
```bash
npm install
```

Or using **yarn**:
```bash
yarn install
```

---

### 3. Set Up Environment Variables

Create a `.env` file in the project root (if not already provided).

Example `.env` file:
```
VITE_API_URL=https://your-backend-api.com
VITE_API_KEY="API_KEY"
```

> 🔔 *Refer to `.env.example` in the folder containing an API key (Keep requests at a minimum).*

---

### 4. Run the Development Server

Using **npm**:
```bash
npm run dev
```

Or using **yarn**:
```bash
yarn dev
```

Open your browser and visit the localhost link usually **http://localhost:5000** to view the app.

---



## 🛠️ Additional Notes

- Ensure your `.env` variables are correctly configured (especially `VITE_API_URL`).
- If you face TailwindCSS styling issues, verify that:
  - `postcss.config.js`
  - `tailwind.config.js`
  
  are properly set up.
- For advanced customization or deployment:
  - [Vite Documentation](https://vitejs.dev/)
  - [TailwindCSS Documentation](https://tailwindcss.com/)

---



## Contributions
Rafid Al Jawad 102776293


