import { useQuery, useMutation, useQueryClient } from "@tanstack/react-query";
import { api } from "@/api/client";
import { useChatStore } from "@/store/chat";
import type {
  Conversation,
  Message,
  PaginatedResponse,
} from "@/types";

export function useChat() {
  const queryClient = useQueryClient();
  const {
    conversations,
    activeConversationId,
    messages,
    isStreaming,
    streamingContent,
    setActiveConversation,
    appendMessage,
    setStreaming,
    appendStreamContent,
    clearStreamContent,
    addConversation,
  } = useChatStore();

  const conversationsQuery = useQuery({
    queryKey: ["conversations"],
    queryFn: () =>
      api.get<PaginatedResponse<Conversation>>("/chats/conversations"),
    refetchOnMount: true,
  });

  const createConversation = useMutation({
    mutationFn: (data: { chat_id: string; title: string }) =>
      api.post<Conversation>("/chats/conversations", data),
    onSuccess: (newConversation) => {
      addConversation(newConversation);
      setActiveConversation(newConversation.id);
      queryClient.invalidateQueries({ queryKey: ["conversations"] });
    },
  });

  const sendMessage = useMutation({
    mutationFn: async (data: {
      conversationId: string;
      content: string;
    }) => {
      return api.post<Message>(
        `/chats/conversations/${data.conversationId}/messages`,
        { content: data.content }
      );
    },
    onSuccess: (message) => {
      if (activeConversationId) {
        appendMessage(activeConversationId, message);
      }
    },
  });

  return {
    conversations,
    activeConversationId,
    messages,
    isStreaming,
    streamingContent,
    conversationsQuery,
    setActiveConversation,
    createConversation: createConversation.mutateAsync,
    sendMessage: sendMessage.mutateAsync,
    clearStreamContent,
    appendStreamContent,
    setStreaming,
    appendMessage,
  };
}
