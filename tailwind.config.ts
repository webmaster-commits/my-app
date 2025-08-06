import type { Config } from "tailwindcss";

export default {
  darkMode: "class",
  content: [
    "./src/app/**/*.{ts,tsx}",
    "./src/components/**/*.{ts,tsx}"
  ],
  theme: {
    extend: {
      colors: {
        brand: {
          DEFAULT: "#10B981",
          dark: "#059669",
          light: "#34D399"
        }
      },
      boxShadow: {
        soft: "0 6px 20px rgba(0,0,0,0.06)"
      }
    },
  },
  plugins: [],
} satisfies Config;
