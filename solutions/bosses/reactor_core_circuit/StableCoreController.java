package ev.forge.reactor.boss;

import ev.forge.reactor.core.*;

import java.util.ArrayList;
import java.util.List;
import java.util.Objects;

public final class StableCoreController {

    private final ReactorRegistry registry;
    private final ReactorController controller;
    private final AlarmSink alarmSink;

    public StableCoreController(
            ReactorRegistry registry,
            ReactorController controller,
            AlarmSink alarmSink
    ) {
        this.registry = Objects.requireNonNull(registry, "registry");
        this.controller = Objects.requireNonNull(controller, "controller");
        this.alarmSink = Objects.requireNonNull(alarmSink, "alarmSink");
    }

    public CoreTickResult tickCore(String coreId, SensorReading reading) {
        List<String> alarms = new ArrayList<>();

        ReactorCore core = registry.getCore(coreId);
        if (core == null) {
            String alarm = "CORE_NOT_FOUND:" + coreId;
            alarmSink.raise(alarm);
            alarms.add(alarm);
            return new CoreTickResult(
                    coreId,
                    false,
                    false,
                    ControlAction.SHUTDOWN,
                    alarms
            );
        }

        ControlAction action;
        boolean invalid = false;

        try {
            action = controller.adjustCore(reading);
        } catch (InvalidReadingException ex) {
            invalid = true;
            String alarm = "INVALID_READING:" + ex.getMessage();
            alarmSink.raise(alarm);
            alarms.add(alarm);
            action = ControlAction.SHUTDOWN;
        }

        // Apply action when reading is valid or we chose a safe default.
        core.applyControl(action);

        if (action == ControlAction.SHUTDOWN) {
            String alarm = "CORE_SHUTDOWN:" + coreId;
            alarmSink.raise(alarm);
            alarms.add(alarm);
        }

        return new CoreTickResult(
                coreId,
                true,
                invalid,
                action,
                alarms
        );
    }
}
