import { useCallback } from "react";
import { useChatStore } from "@/store/chat";
import { ChatWindow } from "@/features/chat/chat-window";

export function ChatPage() {
  const {
    activeConversationId,
    messages,
    isStreaming,
    streamingContent,
    appendMessage,
    appendStreamContent,
    setStreaming,
    clearStreamContent,
  } = useChatStore();

  const handleSend = useCallback(
    async (content: string) => {
      if (!activeConversationId) return;

      // Add user message immediately
      appendMessage(activeConversationId, {
        id: `temp-${Date.now()}`,
        conversation_id: activeConversationId,
        role: "user",
        content,
        model_id: null,
        provider_id: null,
        tool_calls: null,
        tool_call_id: null,
        input_tokens: null,
        output_tokens: null,
        total_tokens: null,
        latency_ms: null,
        finish_reason: null,
        created_at: new Date().toISOString(),
        parent_id: null,
      });

      setStreaming(true);
      clearStreamContent();

      try {
        const response = await fetch(
          `/api/v1/chats/conversations/${activeConversationId}/stream`,
          {
            method: "POST",
            headers: {
              "Content-Type": "application/json",
              Authorization: `Bearer ${JSON.parse(localStorage.getItem("auth") || "{}").access_token}`,
            },
            body: JSON.stringify({ content, role: "user" }),
          }
        );

        const reader = response.body?.getReader();
        if (!reader) return;

        const decoder = new TextDecoder();
        let buffer = "";

        while (true) {
          const { done, value } = await reader.read();
          if (done) break;

          buffer += decoder.decode(value, { stream: true });
          const lines = buffer.split("\n");
          buffer = lines.pop() || "";

          for (const line of lines) {
            if (line.startsWith("event: token")) {
              // Next line has data
            } else if (line.startsWith("data: ")) {
              try {
                const data = JSON.parse(line.slice(6));
                appendStreamContent(data.content || "");
                if (data.done) {
                  setStreaming(false);
                  break;
                }
              } catch {
                // Skip malformed JSON
              }
            } else if (line.startsWith("event: done")) {
              setStreaming(false);
            }
          }
        }
      } catch (error) {
        console.error("Stream error:", error);
        setStreaming(false);
      }
    },
    [activeConversationId, appendMessage, appendStreamContent, setStreaming, clearStreamContent]
  );

  const handleStop = useCallback(() => {
    setStreaming(false);
  }, [setStreaming]);

  return (
    <ChatWindow
      messages={activeConversationId ? (messages[activeConversationId] || []) : []}
      isStreaming={isStreaming}
      streamingContent={streamingContent}
      onSend={handleSend}
      onStop={handleStop}
      activeConversationId={activeConversationId}
    />
  );
}
