import { useEffect, useState } from "react";
import { createItem, deleteItem, getMyItems } from "../api/items";

export function useItems() {
  const [items, setItems] = useState([]);
  const [formData, setFormData] = useState({ title: "", description: "" });
  const [loading, setLoading] = useState(true);
  const [saving, setSaving] = useState(false);
  const [error, setError] = useState(null);

  async function loadItems() {
    try {
      setLoading(true);
      setError(null);
      setItems(await getMyItems());
    } catch (loadError) {
      setError(loadError.message);
    } finally {
      setLoading(false);
    }
  }

  useEffect(() => {
    loadItems();
  }, []);

  function handleChange(event) {
    const { name, value } = event.target;
    setFormData((prev) => ({ ...prev, [name]: value }));
  }

  async function handleSubmit(event) {
    event.preventDefault();
    if (!formData.title.trim()) return;

    try {
      setSaving(true);
      setError(null);
      const created = await createItem(formData);
      setItems((prev) => [created, ...prev]);
      setFormData({ title: "", description: "" });
    } catch (saveError) {
      setError(saveError.message);
    } finally {
      setSaving(false);
    }
  }

  async function handleDelete(id) {
    await deleteItem(id);
    setItems((prev) => prev.filter((item) => item.id !== id));
  }

  return { items, formData, loading, saving, error, handleChange, handleSubmit, handleDelete };
}
