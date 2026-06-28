import { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import { getUserProfile } from "../api/users";

function useProfile() {
  const [formData, setFormData] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const navigate = useNavigate();

  useEffect(() => {
    async function fetchProfile() {
      try {
        setLoading(true);
        setFormData(await getUserProfile());
      } catch (err) {
        if (err.status === 401) {
          navigate("/login", { replace: true });
          return;
        }
        setError(err.message);
      } finally {
        setLoading(false);
      }
    }

    fetchProfile();
  }, [navigate]);

  return { formData, loading, error };
}

export default useProfile;
