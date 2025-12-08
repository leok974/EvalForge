package ev.forge.reactor.boss;

import ev.forge.reactor.core.*;
import org.junit.jupiter.api.Test;

import java.util.ArrayList;
import java.util.List;

import static org.assertj.core.api.Assertions.assertThat;

class StableCoreControllerTest {

    @Test
    void ticksCoreHappyPath() throws Exception {
        FakeRegistry registry = new FakeRegistry();
        FakeCore core = new FakeCore();
        registry.add("core-1", core);

        ReactorController controller = reading -> ControlAction.COOL;
        List<String> raised = new ArrayList<>();
        AlarmSink sink = raised::add;

        StableCoreController stable = new StableCoreController(registry, controller, sink);

        SensorReading reading = new SensorReading(450.0, 1.0, false);

        CoreTickResult result = stable.tickCore("core-1", reading);

        assertThat(result.getCoreId()).isEqualTo("core-1");
        assertThat(result.isCoreFound()).isTrue();
        assertThat(result.isInvalidReading()).isFalse();
        assertThat(result.getAction()).isEqualTo(ControlAction.COOL);
        assertThat(result.getAlarms()).isEmpty();
        assertThat(core.lastAction).isEqualTo(ControlAction.COOL);
    }

    @Test
    void raisesAlarmWhenCoreMissing() {
        FakeRegistry registry = new FakeRegistry();
        ReactorController controller = reading -> ControlAction.HEAT;
        List<String> raised = new ArrayList<>();
        AlarmSink sink = raised::add;

        StableCoreController stable = new StableCoreController(registry, controller, sink);

        SensorReading reading = new SensorReading(450.0, 1.0, false);
        CoreTickResult result = stable.tickCore("missing-core", reading);

        assertThat(result.isCoreFound()).isFalse();
        assertThat(result.getAction()).isEqualTo(ControlAction.SHUTDOWN);
        assertThat(result.getAlarms()).containsExactly("CORE_NOT_FOUND:missing-core");
    }

    // simple fakes…
    static final class FakeCore implements ReactorCore {
        ControlAction lastAction;
        @Override public void applyControl(ControlAction action) {
            this.lastAction = action;
        }
        @Override public CoreStatus getStatus() { return null; }
    }

    static final class FakeRegistry implements ReactorRegistry {
        private final java.util.Map<String, ReactorCore> cores = new java.util.HashMap<>();
        void add(String id, ReactorCore core) { cores.put(id, core); }
        @Override public ReactorCore getCore(String id) { return cores.get(id); }
        // plus other methods as needed
    }
}
