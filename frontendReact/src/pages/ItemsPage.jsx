import { useItems } from "../hooks/useItems";

function ItemsPage() {
  const { items, formData, loading, saving, error, handleChange, handleSubmit, handleDelete } = useItems();

  return (
    <section className="pageSection">
      <div className="pageHeader">
        <div>
          <h1>Items</h1>
          <p>Sample protected CRUD entity. Copy this chain when adding real resources.</p>
        </div>
      </div>

      <form className="inlineForm" onSubmit={handleSubmit}>
        <input name="title" placeholder="Title" value={formData.title} onChange={handleChange} />
        <input name="description" placeholder="Description" value={formData.description} onChange={handleChange} />
        <button type="submit" disabled={saving}>{saving ? "Saving..." : "Add"}</button>
      </form>

      {error && <p className="formError">{error}</p>}
      {loading && <p className="pageStatus">Loading items...</p>}

      <div className="itemList">
        {items.map((item) => (
          <article className="itemRow" key={item.id}>
            <div>
              <strong>{item.title}</strong>
              <span>{item.description || "No description"}</span>
            </div>
            <button type="button" aria-label="Delete item" onClick={() => handleDelete(item.id)}>
              Delete
            </button>
          </article>
        ))}
      </div>
    </section>
  );
}

export default ItemsPage;
