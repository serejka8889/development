# Use official Prometheus image
FROM prom/prometheus:v2.38.0

# Copy configuration file into the correct location inside the container
COPY prometheus.yml /etc/prometheus/prometheus.yml

# Define a non-root user to run Prometheus
USER nobody:nogroup

# Expose standard Prometheus port
EXPOSE 9090

# Default entry point
ENTRYPOINT ["/bin/prometheus"]

# Pass arguments directly via CMD
CMD ["--config.file=/etc/prometheus/prometheus.yml"]
