export function validateEmail(value) {
  if (!value.trim()) return "Email is required";
  if (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(value)) return "Enter a valid email";
  return null;
}

export function validatePassword(value) {
  if (!value.trim()) return "Password is required";
  if (value.length < 8) return "Use at least 8 characters";
  return null;
}

export function validateRequired(value, label) {
  if (!String(value || "").trim()) return `${label} is required`;
  return null;
}
