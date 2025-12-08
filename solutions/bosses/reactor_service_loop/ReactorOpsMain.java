package ev.forge.reactor.service;

import ev.forge.reactor.boss.StableCoreController;
import ev.forge.reactor.boss.AlarmSink;
import ev.forge.reactor.config.ReactorConfig;
import ev.forge.reactor.core.*;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

import java.time.Duration;

public final class ReactorOpsMain {

    private static final Logger log = LoggerFactory.getLogger(ReactorOpsMain.class);

    public static void main(String[] args) {
        int exitCode = 0;

        try {
            ReactorConfig config = ReactorConfig.loadFromEnvironment();

            // Stub registry/controller for now since we don't have the full library in this context
            // In a real scenario, these would come from the user's quest implementations or a DI container
            ReactorRegistry registry = new InMemoryReactorRegistry();
            ReactorController controller = new DefaultReactorController(config);
            
            AlarmSink alarmSink = alarmCode -> log.warn("ALARM {}", alarmCode);
            StableCoreController stable = new StableCoreController(registry, controller, alarmSink);

            var conductor = new ReactorOpsConductor(
                    stable,
                    config,
                    () -> SensorReading.random(config),  // or integrate real source later
                    Duration.ofMillis(config.getTickIntervalMillis())
            );

            Runtime.getRuntime().addShutdownHook(new Thread(conductor::stop, "reactor-shutdown-hook"));

            log.info("Reactor Ops starting up");
            conductor.start();

            // keep main alive until shutdown
            // In a real app we might wait on the conductor thread or a CountDownLatch
            while (true) {
                Thread.sleep(60_000L);
            }

        } catch (Exception ex) {
            log.error("Reactor Ops failed to start", ex);
            exitCode = 1;
        } finally {
            log.info("Reactor Ops exiting with code {}", exitCode);
            System.exit(exitCode);
        }
    }

    private ReactorOpsMain() {}
}

// Minimal stubs to make it compile as a standalone artifact if needed
// In the game, these classes exist in the shared library/classpath
class InMemoryReactorRegistry implements ReactorRegistry {
    // Stub implementation
}
class DefaultReactorController implements ReactorController {
    public DefaultReactorController(ReactorConfig config) {}
    // Stub implementation
}
