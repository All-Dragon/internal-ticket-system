import { NavLink, useNavigate } from "react-router-dom";
import { useAuth } from "../context/AuthContext";

function Header() {
  const { user, logout } = useAuth();
  const navigate = useNavigate();

  function handleLogout() {
    logout();
    navigate("/login");
  }

  return (
    <aside className="sidebar">
      <div className="brand">
        <div className="brandMark">SK</div>
        <div>
          <strong>StarterKit</strong>
          <span>Full-stack template</span>
        </div>
      </div>

      <nav className="navList">
        <NavLink to="/dashboard">Dashboard</NavLink>
        <NavLink to="/items">Items</NavLink>
      </nav>

      <div className="sidebarFooter">
        <span>{user?.email}</span>
        <button type="button" onClick={handleLogout}>Logout</button>
      </div>
    </aside>
  );
}

export default Header;
