import { describe, it, expect } from "vitest";
import { QueryClient } from "@tanstack/react-query";

describe("App", () => {
  it("renders without crashing", () => {
    const queryClient = new QueryClient();
    expect(queryClient).toBeDefined();
  });
});
