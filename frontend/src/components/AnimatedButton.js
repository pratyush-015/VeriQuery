import { motion } from "framer-motion";
export default function AnimatedButton({ children, ...props }) {
  return (
    <motion.button
      whileHover={{ scale: 1.04, boxShadow: "0 4px 20px rgba(99, 102, 241, 0.2)" }}
      whileTap={{ scale: 0.97 }}
      className="bg-indigo-600 text-white font-semibold px-6 py-2 rounded-lg shadow transition duration-200 disabled:opacity-60 disabled:cursor-not-allowed"
      {...props}
    >
      {children}
    </motion.button>
  );
}
