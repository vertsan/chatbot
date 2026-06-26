import { useState } from "react";
import { useNavigate } from "@tanstack/react-router";
import { useAuth } from "@/hooks/useAuth";
import { useChatStore } from "@/store/chat";
import { Button } from "@/components/ui/button";
import { ScrollArea } from "@/components/ui/scroll-area";
import { Separator } from "@/components/ui/separator";
import { Avatar, AvatarFallback } from "@/components/ui/avatar";
import { cn } from "@/lib/utils";
import { formatDate, truncate } from "@/lib/utils";
import {
  MessageSquare,
  Plus,
  Search,
  Settings,
  LogOut,
  PanelLeftClose,
  PanelLeft,
  Trash2,
} from "lucide-react";
import type { Conversation } from "@/types";

interface SidebarProps {
  collapsed: boolean;
  onToggle: () => void;
}

export function Sidebar({ collapsed, onToggle }: SidebarProps) {
  const navigate = useNavigate();
  const { user, logout } = useAuth();
  const {
    conversations,
    activeConversationId,
    setActiveConversation,
    removeConversation,
  } = useChatStore();
  const [search, setSearch] = useState("");

  const filteredConversations = conversations.filter((c) =>
    c.title.toLowerCase().includes(search.toLowerCase())
  );

  const handleNewChat = () => {
    navigate({ to: "/chat" });
  };

  const handleSelectConversation = (conv: Conversation) => {
    setActiveConversation(conv.id);
    navigate({ to: `/chat/${conv.id}` });
  };

  const handleDelete = (e: React.MouseEvent, id: string) => {
    e.stopPropagation();
    removeConversation(id);
  };

  return (
    <div
      className={cn(
        "flex flex-col h-full bg-sidebar text-sidebar-foreground transition-all duration-300",
        collapsed ? "w-16" : "w-72"
      )}
    >
      <div className="flex items-center justify-between p-4">
        {!collapsed && (
          <h1 className="text-lg font-semibold">Chatbot</h1>
        )}
        <Button
          variant="ghost"
          size="icon"
          onClick={onToggle}
          className="text-sidebar-foreground hover:bg-sidebar-accent"
        >
          {collapsed ? (
            <PanelLeft className="h-5 w-5" />
          ) : (
            <PanelLeftClose className="h-5 w-5" />
          )}
        </Button>
      </div>

      {!collapsed && (
        <>
          <div className="px-4 pb-2">
            <Button
              onClick={handleNewChat}
              className="w-full justify-start gap-2"
              variant="secondary"
            >
              <Plus className="h-4 w-4" />
              New Chat
            </Button>
          </div>

          <div className="px-4 pb-2">
            <div className="relative">
              <Search className="absolute left-2 top-2.5 h-4 w-4 text-muted-foreground" />
              <input
                value={search}
                onChange={(e) => setSearch(e.target.value)}
                placeholder="Search conversations..."
                className="w-full rounded-md border border-sidebar-border bg-sidebar-accent py-2 pl-8 pr-4 text-sm text-sidebar-foreground placeholder:text-sidebar-foreground/50 focus:outline-none focus:ring-1 focus:ring-ring"
              />
            </div>
          </div>

          <ScrollArea className="flex-1 px-2">
            <div className="space-y-1">
              {filteredConversations.map((conv) => (
                <button
                  key={conv.id}
                  onClick={() => handleSelectConversation(conv)}
                  className={cn(
                    "w-full flex items-start gap-3 rounded-lg px-3 py-2 text-left text-sm transition-colors hover:bg-sidebar-accent group",
                    activeConversationId === conv.id && "bg-sidebar-accent"
                  )}
                >
                  <MessageSquare className="mt-0.5 h-4 w-4 shrink-0" />
                  <div className="flex-1 overflow-hidden">
                    <div className="font-medium truncate">
                      {truncate(conv.title, 30)}
                    </div>
                    <div className="text-xs text-sidebar-foreground/60">
                      {formatDate(conv.last_message_at || conv.created_at)}
                    </div>
                  </div>
                  <Button
                    variant="ghost"
                    size="icon"
                    onClick={(e) => handleDelete(e, conv.id)}
                    className="h-6 w-6 shrink-0 opacity-0 group-hover:opacity-100"
                  >
                    <Trash2 className="h-3 w-3" />
                  </Button>
                </button>
              ))}
            </div>
          </ScrollArea>
        </>
      )}

      <Separator className="bg-sidebar-border" />

      <div className="p-4">
        {collapsed ? (
          <Avatar>
            <AvatarFallback className="bg-sidebar-accent text-sidebar-foreground">
              {user?.display_name?.charAt(0)?.toUpperCase() || "U"}
            </AvatarFallback>
          </Avatar>
        ) : (
          <div className="flex items-center gap-3">
            <Avatar>
              <AvatarFallback className="bg-sidebar-accent text-sidebar-foreground">
                {user?.display_name?.charAt(0)?.toUpperCase() || "U"}
              </AvatarFallback>
            </Avatar>
            <div className="flex-1 overflow-hidden">
              <p className="text-sm font-medium truncate">
                {user?.display_name || "User"}
              </p>
              <p className="text-xs text-sidebar-foreground/60 truncate">
                {user?.email}
              </p>
            </div>
            <div className="flex gap-1">
              <Button
                variant="ghost"
                size="icon"
                className="h-8 w-8 text-sidebar-foreground hover:bg-sidebar-accent"
                onClick={() => navigate({ to: "/settings" })}
              >
                <Settings className="h-4 w-4" />
              </Button>
              <Button
                variant="ghost"
                size="icon"
                className="h-8 w-8 text-sidebar-foreground hover:bg-sidebar-accent"
                onClick={logout}
              >
                <LogOut className="h-4 w-4" />
              </Button>
            </div>
          </div>
        )}
      </div>
    </div>
  );
}
