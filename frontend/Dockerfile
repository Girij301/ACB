# =========================
# Build Stage
# =========================
FROM node:22-alpine AS builder

WORKDIR /app

# Install dependencies
COPY package*.json ./

RUN npm ci

# Copy source code
COPY . .

# Build-time environment variables
ARG VITE_API_URL
ARG VITE_WS_URL
ARG VITE_CLERK_PUBLISHABLE_KEY

ENV VITE_API_URL=$VITE_API_URL
ENV VITE_WS_URL=$VITE_WS_URL
ENV VITE_CLERK_PUBLISHABLE_KEY=$VITE_CLERK_PUBLISHABLE_KEY

# Build React application
RUN npm run build


# =========================
# Production Stage
# =========================
FROM nginx:alpine

COPY --from=builder /app/dist /usr/share/nginx/html

# Custom Nginx configuration for React SPA routing
COPY nginx.conf /etc/nginx/conf.d/default.conf

EXPOSE 80

CMD ["nginx", "-g", "daemon off;"]