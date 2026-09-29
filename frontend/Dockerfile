# ---------- stage 1: stamp the build number into the page ----------
FROM alpine:3.20 AS stamp
ARG BUILD_NUMBER=dev
COPY index.html /src/index.html
RUN sed -i "s/__BUILD__/${BUILD_NUMBER}/g" /src/index.html

# ---------- stage 2: serve it with a non-root Nginx ----------
FROM nginxinc/nginx-unprivileged:1.27-alpine
COPY --from=stamp /src/index.html /usr/share/nginx/html/index.html
EXPOSE 8080
HEALTHCHECK --interval=15s --timeout=3s CMD wget -qO- http://localhost:8080/ >/dev/null || exit 1
