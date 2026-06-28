import { Link } from "react-router-dom";
import useLoginForm from "../hooks/useLoginForm";

function LoginForm() {
  const { formData, errors, error, loading, handleChange, handleSubmit } = useLoginForm();

  return (
    <section className="authPanel">
      <h1>Sign in</h1>
      <p>Use your account to access the protected app area.</p>

      <form className="form" onSubmit={handleSubmit}>
        <label>
          Email
          <input name="email" type="email" value={formData.email} onChange={handleChange} />
          {errors.email && <span className="fieldError">{errors.email}</span>}
        </label>

        <label>
          Password
          <input name="password" type="password" value={formData.password} onChange={handleChange} />
          {errors.password && <span className="fieldError">{errors.password}</span>}
        </label>

        {error && <p className="formError">{error}</p>}
        <button type="submit" disabled={loading}>{loading ? "Signing in..." : "Sign in"}</button>
      </form>

      <p className="authSwitch">No account? <Link to="/register">Create one</Link></p>
    </section>
  );
}

export default LoginForm;
