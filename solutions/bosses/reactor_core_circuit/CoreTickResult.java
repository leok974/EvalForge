package ev.forge.reactor.boss;

import ev.forge.reactor.core.ControlAction;
import java.util.Collections;
import java.util.List;
import java.util.Objects;

public final class CoreTickResult {

    private final String coreId;
    private final boolean coreFound;
    private final boolean invalidReading;
    private final ControlAction action;
    private final List<String> alarms;

    public CoreTickResult(
            String coreId,
            boolean coreFound,
            boolean invalidReading,
            ControlAction action,
            List<String> alarms
    ) {
        this.coreId = Objects.requireNonNull(coreId, "coreId");
        this.coreFound = coreFound;
        this.invalidReading = invalidReading;
        this.action = Objects.requireNonNull(action, "action");
        this.alarms = List.copyOf(alarms);
    }

    public String getCoreId() {
        return coreId;
    }

    public boolean isCoreFound() {
        return coreFound;
    }

    public boolean isInvalidReading() {
        return invalidReading;
    }

    public ControlAction getAction() {
        return action;
    }

    public List<String> getAlarms() {
        return Collections.unmodifiableList(alarms);
    }

    @Override
    public String toString() {
        return "CoreTickResult{" +
                "coreId='" + coreId + '\'' +
                ", coreFound=" + coreFound +
                ", invalidReading=" + invalidReading +
                ", action=" + action +
                ", alarms=" + alarms +
                '}';
    }
}
