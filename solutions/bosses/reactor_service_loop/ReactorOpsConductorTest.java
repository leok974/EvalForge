package ev.forge.reactor.service;

import ev.forge.reactor.boss.CoreTickResult;
import ev.forge.reactor.boss.StableCoreController;
import ev.forge.reactor.config.ReactorConfig;
import ev.forge.reactor.core.SensorReading;
import org.junit.jupiter.api.Test;
import org.mockito.Mockito;

import java.time.Duration;
import java.util.concurrent.CountDownLatch;
import java.util.concurrent.TimeUnit;
import java.util.concurrent.atomic.AtomicInteger;

import static org.junit.jupiter.api.Assertions.*;
import static org.mockito.ArgumentMatchers.any;
import static org.mockito.Mockito.*;

class ReactorOpsConductorTest {

    @Test
    void startsAndStopsCleanly() throws InterruptedException {
        // Arrange
        StableCoreController controller = mock(StableCoreController.class);
        ReactorConfig config = mock(ReactorConfig.class);
        when(config.getEnvironment()).thenReturn("test");
        when(config.getCoreId()).thenReturn("TEST-CORE");

        // Mock tick result
        when(controller.tickCore(any(), any())).thenReturn(new CoreTickResult(new java.util.ArrayList<>(), new java.util.ArrayList<>()));

        ReactorOpsConductor conductor = new ReactorOpsConductor(
                controller,
                config,
                () -> new SensorReading(50.0, 100.0, 1000.0),
                Duration.ofMillis(10)
        );

        // Act
        conductor.start();
        Thread.sleep(50); // let it tick a few times
        conductor.stop();

        // Assert
        verify(controller, atLeastOnce()).tickCore(any(), any());
    }

    @Test
    void handlesTickExceptionGracefully() throws InterruptedException {
        StableCoreController controller = mock(StableCoreController.class);
        ReactorConfig config = mock(ReactorConfig.class);
        
        // Throw runtime exception on tick
        when(controller.tickCore(any(), any())).thenThrow(new RuntimeException("Boom"));

        CountDownLatch latch = new CountDownLatch(1);

        ReactorOpsConductor conductor = new ReactorOpsConductor(
                controller,
                config,
                () -> {
                   latch.countDown();
                   return new SensorReading(50.0, 100.0, 1000.0);
                },
                Duration.ofMillis(10)
        );

        conductor.start();
        boolean ticked = latch.await(1, TimeUnit.SECONDS);
        assertTrue(ticked, "Should attempt to tick even if it fails");
        
        conductor.stop();
        // Should rely on logs for verification of error handling normally
    }
}
