from sqlalchemy import ForeignKey

from app.database.base import Base
from app.models.user import User, UserSession, UserAPIKey
from app.models.organization import Organization, OrganizationMember
from app.models.role import Role, Permission, RolePermission
from app.models.chat import Chat, Conversation, Message, Attachment
from app.models.provider import AIProvider, AIModel
from app.models.prompt import PromptTemplate
from app.models.knowledge import KnowledgeBase, Document, DocumentChunk
from app.models.vector import VectorIndex
from app.models.settings import SystemSetting, UserSetting
from app.models.audit import AuditLog
from app.models.notification import Notification

__all__ = [
    "Base",
    "User",
    "UserSession",
    "UserAPIKey",
    "Organization",
    "OrganizationMember",
    "Role",
    "Permission",
    "RolePermission",
    "Chat",
    "Conversation",
    "Message",
    "Attachment",
    "AIProvider",
    "AIModel",
    "PromptTemplate",
    "KnowledgeBase",
    "Document",
    "DocumentChunk",
    "VectorIndex",
    "SystemSetting",
    "UserSetting",
    "AuditLog",
    "Notification",
]
