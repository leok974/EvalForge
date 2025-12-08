package ev.forge.reactor.service;

import ev.forge.reactor.boss.StableCoreController;
import ev.forge.reactor.core.SensorReading;
import ev.forge.reactor.config.ReactorConfig;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

import java.time.Duration;
import java.util.Objects;
import java.util.concurrent.atomic.AtomicBoolean;
import java.util.function.Supplier;

public final class ReactorOpsConductor implements AutoCloseable {

    private static final Logger log = LoggerFactory.getLogger(ReactorOpsConductor.class);

    private final StableCoreController controller;
    private final ReactorConfig config;
    private final Supplier<SensorReading> readingSupplier;
    private final Duration tickInterval;
    private final AtomicBoolean running = new AtomicBoolean(false);
    private Thread loopThread;

    public ReactorOpsConductor(
            StableCoreController controller,
            ReactorConfig config,
            Supplier<SensorReading> readingSupplier,
            Duration tickInterval
    ) {
        this.controller = Objects.requireNonNull(controller, "controller");
        this.config = Objects.requireNonNull(config, "config");
        this.readingSupplier = Objects.requireNonNull(readingSupplier, "readingSupplier");
        this.tickInterval = Objects.requireNonNull(tickInterval, "tickInterval");
    }

    public void start() {
        if (!running.compareAndSet(false, true)) {
            log.warn("ReactorOpsConductor already running");
            return;
        }

        log.info("Starting ReactorOpsConductor [env={}, tickInterval={}ms]",
                config.getEnvironment(), tickInterval.toMillis());

        loopThread = new Thread(this::runLoop, "reactor-ops-loop");
        loopThread.setDaemon(true);
        loopThread.start();
    }

    private void runLoop() {
        while (running.get()) {
            try {
                SensorReading reading = readingSupplier.get();
                var result = controller.tickCore(config.getCoreId(), reading);
                log.debug("Tick result: {}", result);
            } catch (Exception ex) {
                log.error("Unexpected error in Reactor loop", ex);
            }

            try {
                Thread.sleep(tickInterval.toMillis());
            } catch (InterruptedException ie) {
                Thread.currentThread().interrupt();
                log.warn("Reactor loop interrupted; requesting shutdown");
                running.set(false);
            }
        }

        log.info("ReactorOpsConductor loop exiting");
    }

    public void stop() {
        if (!running.compareAndSet(true, false)) {
            return;
        }
        log.info("Stopping ReactorOpsConductor");
        if (loopThread != null) {
            loopThread.interrupt();
            try {
                loopThread.join(5_000);
            } catch (InterruptedException ignored) {
                Thread.currentThread().interrupt();
            }
        }
        log.info("ReactorOpsConductor stopped");
    }

    @Override
    public void close() {
        stop();
    }
}
