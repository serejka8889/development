# Use official Grafana image
FROM grafana/grafana:latest

# Allow specifying additional plugins at startup
ARG GRAFANA_PLUGINS=""

# Install any specified plugins during build-time
RUN if [ ! -z "$GRAFANA_PLUGINS" ]; then \
    echo "Installing Grafana plugins: $GRAFANA_PLUGINS"; \
    grafana-cli plugin install $GRAFANA_PLUGINS || true; \
fi

# Expose Grafana's UI port
EXPOSE 3000

# No need to change ENTRYPOINT since it's handled by the official image