###############################
PyHydroQuebec Prometheus Server
###############################

Run
###

::

   PYHQ_USER=email PYHQ_PASSWORD=password PYHQ_CONTRACT=contract_number prometheus_pyhydroquebec

With Docker

::

    docker run -e PYHQ_USER=email -e PYHQ_PASSWORD=password -e PYHQ_CONTRACT=contract_number -e PYHQ_OUTPUT=PROMETHEUS registry.gitlab.com/ttblt-hass/pyhydroquebec:master


Limitation
##########

According `to this GitHub issue` <https://github.com/prometheus/prometheus/issues/7396#issuecomment-649451086>`_,
it's currently not possible to insert data in the past. This is problematic with
this integration considering that it takes HydroQuebec multiple hours before
making the metrics available to us. For that reason, this server has to cheat
to be able to work with Prometheus. All of the metrics are inserted 24 hours
after their real timestamp.

To fix this problem, the metrics need to be offset when querying them. The
current solution is to query every hour the metric from 24 hour in the past.

Prometheus Configuration
########################

In your `prometheus.yml`

::

  - job_name: hydroquebec
    scrape_interval: 1h
    static_configs:
      - targets: ['<Your IP address>:9120']
    metrics_path: /daily
    scrape_timeout: 1m

And if you use docker-compose, you can spawn it like that

::

    prometheus:
        image: prom/prometheus:latest
        container_name: prometheus
        restart: unless-stopped
        command:
            - '--config.file=/etc/prometheus/prometheus.yml'
            - '--storage.tsdb.path=/prometheus'
            - '--web.console.libraries=/usr/share/prometheus/console_libraries'
            - '--web.console.templates=/usr/share/prometheus/consoles'
            - '--enable-feature=promql-negative-offset'
    hydroquebec_exporter:
        image: "drpandemic/pyhydroquebec"
        container_name: pyhydroquebec_exporter
        ports:
            - 9120:8080
        environment:
            - PYHQ_USER
            - PYHQ_PASSWORD
            - PYHQ_CONTRACT
            - PYHQ_OUTPUT=PROMETHEUS

Finally, you can add a `.env` with your HydroQuebec secrets

::
   PYHQ_USER=<Your email>
   PYHQ_PASSWORD=<Your password>
   PYHQ_CONTRACT=<Your contract number>

Prometheus Graphing
###################
As mentioned earlier, you will need to offset your data by 24 hours.

::

   hydroquebec_hourly_total_consumption offset -1d
