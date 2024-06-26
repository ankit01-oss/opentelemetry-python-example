import time

from opentelemetry.metrics import get_meter_provider, set_meter_provider
from opentelemetry.sdk.metrics import Counter, MeterProvider
from opentelemetry.sdk.metrics.export import (
    AggregationTemporality,
    ConsoleMetricExporter,
    PeriodicExportingMetricReader,
)

temporality_cumulative = {Counter: AggregationTemporality.CUMULATIVE}
temporality_delta = {Counter: AggregationTemporality.DELTA}

# Use console exporters for the example

# The metrics that are exported using this exporter will represent a cumulative value
exporter = ConsoleMetricExporter(
    preferred_temporality=temporality_cumulative,
)

# The metrics that are exported using this exporter will represent a delta value
exporter2 = ConsoleMetricExporter(
    preferred_temporality=temporality_delta,
)

# The PeriodicExportingMetricReader takes the preferred aggregation
# from the passed in exporter
reader = PeriodicExportingMetricReader(
    exporter,
    export_interval_millis=5_000,
)

# The PeriodicExportingMetricReader takes the preferred aggregation
# from the passed in exporter
reader2 = PeriodicExportingMetricReader(
    exporter2,
    export_interval_millis=5_000,
)

provider = MeterProvider(metric_readers=[reader, reader2])
set_meter_provider(provider)

meter = get_meter_provider().get_meter("preferred-temporality", "0.1.2")

counter = meter.create_counter("requests")

# Two metrics are expected to be printed to the console per export interval.
# The metric originating from the metric exporter with a preferred temporality
# of cumulative will keep a running sum of all values added.
# The metric originating from the metric exporter with a preferred temporality
# of delta will have the sum value reset each export interval.
counter.add(5)
time.sleep(10)
counter.add(20)