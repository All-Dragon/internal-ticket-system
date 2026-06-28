import { Link } from "react-router-dom";
import useRegisterForm from "../hooks/useRegisterForm";

function RegisterForm() {
  const { formData, errors, error, loading, handleChange, handleSubmit } = useRegisterForm();

  return (
    <section className="authPanel">
      <h1>Create account</h1>
      <p>This public form creates a normal user account.</p>

      <form className="form" onSubmit={handleSubmit}>
        <label>
          Full name
          <input name="full_name" value={formData.full_name} onChange={handleChange} />
          {errors.full_name && <span className="fieldError">{errors.full_name}</span>}
        </label>

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
        <button type="submit" disabled={loading}>{loading ? "Creating..." : "Create account"}</button>
      </form>

      <p className="authSwitch">Already registered? <Link to="/login">Sign in</Link></p>
    </section>
  );
}

export default RegisterForm;
