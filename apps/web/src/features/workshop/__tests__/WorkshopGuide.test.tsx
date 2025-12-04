import React from "react";
import { render, screen, fireEvent } from "@testing-library/react";
import { WorkshopGuide } from "../WorkshopGuide";
import { describe, it, expect, beforeEach } from "vitest";

const STORAGE_KEY = "evalforge:workshop:tutorial-dismissed";

describe("WorkshopGuide", () => {
    beforeEach(() => {
        window.localStorage.clear();
    });

    it("shows by default when not dismissed", () => {
        render(<WorkshopGuide />);

        expect(screen.getByTestId("workshop-guide")).toBeTruthy();
        expect(screen.getByText(/Workshop Primer/i)).toBeTruthy();
        expect(
            screen.getByText(/Workbench/i)
        ).toBeTruthy();
    });

    it("hides after clicking Got it and persists to localStorage", () => {
        render(<WorkshopGuide />);

        const button = screen.getByRole("button", { name: /got it/i });
        fireEvent.click(button);

        expect(screen.queryByTestId("workshop-guide")).toBeNull();
        expect(window.localStorage.getItem(STORAGE_KEY)).toBe("1");
    });

    it("does not render if localStorage says dismissed", () => {
        window.localStorage.setItem(STORAGE_KEY, "1");
        render(<WorkshopGuide />);

        expect(screen.queryByTestId("workshop-guide")).toBeNull();
    });

    it("can be reopened via global openWorkshopGuide helper even after dismissed", async () => {
        window.localStorage.setItem(STORAGE_KEY, "1");
        render(<WorkshopGuide />);

        // Initially hidden
        expect(screen.queryByTestId("workshop-guide")).toBeNull();

        // Fire global open
        // We need to import the helper, but since we are in the same file context in the test environment,
        // we can just dispatch the event manually or import the helper if we had it available.
        // For this test, we'll simulate the event dispatch directly as the helper does.
        window.dispatchEvent(new CustomEvent("evalforge:workshop:guide:open"));

        expect(await screen.findByTestId("workshop-guide")).toBeTruthy();
    });
});
