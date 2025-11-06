export default {
  content: ["./index.html", "./src/**/*.{js,ts,jsx,tsx}"],
  theme: {
    extend: {
      colors: {
        primary: {
          light: '#60a5fa',
          DEFAULT: '#6366f1',
          dark: '#7c3aed',
        },
        navy: {
          DEFAULT: '#1A237E',
          light: '#3949AB',
          dark: '#0D1642',
        },
        input: {
          green: '#4CAF50',
          blue: '#5B7FE8',
          orange: '#FFA726',
          purple: '#9C27B0',
          cyan: '#00BCD4',
          pink: '#E91E63',
          darkPurple: '#673AB7',
        },
        status: {
          success: '#4CAF50',
          warning: '#FFA726',
          error: '#E91E63',
          info: '#00BCD4',
          neutral: '#9E9E9E',
        },
        text: {
          primary: '#1A237E',
          secondary: '#666666',
          light: '#BDBDBD',
          white: '#FFFFFF',
        },
        background: {
          light: '#F5F5F5',
          white: '#FFFFFF',
          gray: '#FAFAFA',
        },
        border: {
          light: '#E0E0E0',
          DEFAULT: '#BDBDBD',
          dark: '#9E9E9E',
        },
      },
      backgroundImage: {
        'logo-gradient': 'linear-gradient(to right, #60a5fa, #6366f1, #7c3aed)',
      },
    },
  },
  plugins: [],
}
