import Header from "../components/Header";
import { Outlet } from "react-router-dom";

function MainLayout() {
  return (
    <div className="appShell">
      <Header />
      <main className="mainPanel">
        <Outlet />
      </main>
    </div>
  );
}

export default MainLayout;
