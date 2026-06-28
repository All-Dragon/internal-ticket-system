# Frontend Notes

GTO-style frontend layout:

- `api/config.js`: base URL helper.
- `api/authFetch.js`: authenticated fetch wrapper.
- `api/*.js`: domain API functions.
- `context/AuthContext.jsx`: auth state and user profile.
- `hooks/*`: form and data-loading logic.
- `components/*`: reusable UI pieces.
- `pages/*`: route-level screens.
- `layouts/MainLayout.jsx`: protected app shell.

To add a new entity, copy `items.js`, `useItems.js`, and `ItemsPage.jsx`, then add a route in `App.jsx`.
