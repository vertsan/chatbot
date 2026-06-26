import { useMutation, useQueryClient } from "@tanstack/react-query";
import { useNavigate } from "@tanstack/react-router";
import { api, setAuthTokens, clearAuthTokens } from "@/api/client";
import { useAuthStore } from "@/store/auth";
import type { User, AuthTokens } from "@/types";

export function useAuth() {
  const queryClient = useQueryClient();
  const navigate = useNavigate();
  const { user, isAuthenticated, isLoading, setUser, clearUser } =
    useAuthStore();

  const loginMutation = useMutation({
    mutationFn: async (data: { email: string; password: string }) => {
      const result = await api.post<AuthTokens & { user: User }>(
        "/auth/login",
        data
      );
      return result;
    },
    onSuccess: (data) => {
      setAuthTokens(data);
      setUser(data.user);
      queryClient.invalidateQueries({ queryKey: ["me"] });
      navigate({ to: "/chat" });
    },
  });

  const registerMutation = useMutation({
    mutationFn: async (data: {
      email: string;
      password: string;
      display_name: string;
    }) => {
      const result = await api.post<User>("/auth/register", data);
      return result;
    },
    onSuccess: () => {
      navigate({ to: "/login" });
    },
  });

  const logout = () => {
    clearUser();
    clearAuthTokens();
    queryClient.clear();
    navigate({ to: "/login" });
  };

  return {
    user,
    isAuthenticated,
    isLoading,
    login: loginMutation.mutateAsync,
    register: registerMutation.mutateAsync,
    logout,
    loginError: loginMutation.error,
    isLoggingIn: loginMutation.isPending,
    isRegistering: registerMutation.isPending,
  };
}
