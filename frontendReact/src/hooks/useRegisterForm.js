import { useState } from "react";
import { useNavigate } from "react-router-dom";
import { useAuth } from "../context/AuthContext";
import { validateEmail, validatePassword, validateRequired } from "../utiles/validation";

function useRegisterForm() {
  const { register } = useAuth();
  const navigate = useNavigate();
  const [formData, setFormData] = useState({ full_name: "", email: "", password: "" });
  const [errors, setErrors] = useState({});
  const [error, setError] = useState(null);
  const [loading, setLoading] = useState(false);

  function validateForm() {
    return {
      full_name: validateRequired(formData.full_name, "Full name"),
      email: validateEmail(formData.email),
      password: validatePassword(formData.password),
    };
  }

  function handleChange(event) {
    const { name, value } = event.target;
    setFormData((prev) => ({ ...prev, [name]: value }));
  }

  async function handleSubmit(event) {
    event.preventDefault();
    const validationErrors = validateForm();
    if (Object.values(validationErrors).some(Boolean)) {
      setErrors(validationErrors);
      return;
    }

    try {
      setLoading(true);
      setError(null);
      await register(formData);
      navigate("/login");
    } catch (submitError) {
      setError(submitError.message);
    } finally {
      setLoading(false);
    }
  }

  return { formData, errors, error, loading, handleChange, handleSubmit };
}

export default useRegisterForm;
