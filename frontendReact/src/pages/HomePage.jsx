import { Link } from "react-router-dom";

function HomePage() {
  return (
    <div className="homePage">
      <section className="homeHero">
        <h1>StarterKit</h1>
        <p>A compact full-stack template for apps with an API, auth, and a React interface.</p>
        <div className="heroActions">
          <Link className="buttonPrimary" to="/register">Create account</Link>
          <Link className="buttonSecondary" to="/login">Sign in</Link>
        </div>
      </section>
    </div>
  );
}

export default HomePage;
