run-backend:
	uvicorn app.api.main:app --reload

run-frontend:
	cd frontendReact && npm run dev

test:
	pytest
