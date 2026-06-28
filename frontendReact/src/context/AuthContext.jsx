import { createContext, useContext, useEffect, useState } from "react";
import { createUser, getUserProfile, loginUser } from "../api/users";

const AuthContext = createContext(null);

export function AuthProvider({ children }) {
  const [user, setUser] = useState(null);
  const [loading, setLoading] = useState(true);

  const token = localStorage.getItem("access_token");

  useEffect(() => {
    let isMounted = true;

    async function loadProfile() {
      if (!token) {
        setLoading(false);
        return;
      }

      try {
        const profile = await getUserProfile();
        if (isMounted) setUser(profile);
      } catch {
        localStorage.removeItem("access_token");
        if (isMounted) setUser(null);
      } finally {
        if (isMounted) setLoading(false);
      }
    }

    loadProfile();
    return () => {
      isMounted = false;
    };
  }, [token]);

  async function login(credentials) {
    const data = await loginUser(credentials);
    localStorage.setItem("access_token", data.access_token);
    const profile = await getUserProfile();
    setUser(profile);
    return profile;
  }

  async function register(payload) {
    return createUser(payload);
  }

  function logout() {
    localStorage.removeItem("access_token");
    setUser(null);
  }

  const value = { user, loading, isAuthenticated: Boolean(user), login, register, logout };

  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>;
}

export function useAuth() {
  const value = useContext(AuthContext);
  if (!value) throw new Error("useAuth must be used inside AuthProvider");
  return value;
}
