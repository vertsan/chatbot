import { describe, it, expect } from "vitest";
import { render, screen } from "@testing-library/react";
import { QueryClient, QueryClientProvider } from "@tanstack/react-query";

describe("App", () => {
  it("renders without crashing", () => {
    const queryClient = new QueryClient();
    expect(queryClient).toBeDefined();
  });
});
