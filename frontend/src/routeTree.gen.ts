import { createRootRoute, createRoute, createRouter } from "@tanstack/react-router";
import { ChatLayout } from "@/components/layouts";
import { LoginPage } from "@/pages/login";
import { ChatPage } from "@/pages/chat";
import { SettingsPage } from "@/pages/settings";

const rootRoute = createRootRoute({
  component: ChatLayout,
});

const loginRoute = createRoute({
  getParentRoute: () => rootRoute,
  path: "/login",
  component: LoginPage,
});

const chatRoute = createRoute({
  getParentRoute: () => rootRoute,
  path: "/chat",
  component: ChatPage,
});

const chatConversationRoute = createRoute({
  getParentRoute: () => rootRoute,
  path: "/chat/$conversationId",
  component: ChatPage,
});

const settingsRoute = createRoute({
  getParentRoute: () => rootRoute,
  path: "/settings",
  component: SettingsPage,
});

const indexRoute = createRoute({
  getParentRoute: () => rootRoute,
  path: "/",
  component: ChatPage,
});

const routeTree = rootRoute.addChildren([
  loginRoute,
  chatRoute,
  chatConversationRoute,
  settingsRoute,
  indexRoute,
]);

export { routeTree };
