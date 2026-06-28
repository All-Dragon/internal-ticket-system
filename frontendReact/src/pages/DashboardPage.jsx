import { useAuth } from "../context/AuthContext";

function DashboardPage() {
  const { user } = useAuth();

  return (
    <section className="pageSection">
      <div className="pageHeader">
        <div>
          <h1>Dashboard</h1>
          <p>Protected overview screen. Replace these panels with your real app workflow.</p>
        </div>
      </div>

      <div className="metricsGrid">
        <article className="metricCard">
          <span>User</span>
          <strong>{user?.full_name}</strong>
        </article>
        <article className="metricCard">
          <span>Role</span>
          <strong>{user?.role}</strong>
        </article>
        <article className="metricCard">
          <span>Status</span>
          <strong>{user?.is_active ? "Active" : "Inactive"}</strong>
        </article>
      </div>
    </section>
  );
}

export default DashboardPage;
