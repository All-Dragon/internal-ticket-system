FROM node:22-alpine AS frontend_build
WORKDIR /frontend
COPY frontendReact/package*.json ./
RUN npm install
COPY frontendReact/ ./
RUN npm run build

FROM nginx:1.27-alpine
COPY nginx/default.conf /etc/nginx/conf.d/default.conf
COPY --from=frontend_build /frontend/dist /usr/share/nginx/html
