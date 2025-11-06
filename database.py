"""
Database models for chat history, workspaces, and user data
"""

from sqlalchemy import create_engine, Column, Integer, String, Text, DateTime, Float, Boolean, ForeignKey, JSON
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from datetime import datetime
import json

Base = declarative_base()


class ChatSession(Base):
    """Chat session/conversation"""
    __tablename__ = 'chat_sessions'

    id = Column(Integer, primary_key=True)
    title = Column(String(255), default="New Conversation")
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    provider = Column(String(50))
    model = Column(String(100))
    mode = Column(String(50), default="chat")

    # Relationships
    messages = relationship("ChatMessage", back_populates="session", cascade="all, delete-orphan")


class ChatMessage(Base):
    """Individual chat message"""
    __tablename__ = 'chat_messages'

    id = Column(Integer, primary_key=True)
    session_id = Column(Integer, ForeignKey('chat_sessions.id'))
    role = Column(String(20))  # user, assistant
    content = Column(Text)
    image_paths = Column(Text)  # JSON array of image paths
    timestamp = Column(DateTime, default=datetime.utcnow)
    tokens_used = Column(Integer, default=0)
    cost = Column(Float, default=0.0)

    # Relationships
    session = relationship("ChatSession", back_populates="messages")


class GeneratedCode(Base):
    """Generated code snippets"""
    __tablename__ = 'generated_code'

    id = Column(Integer, primary_key=True)
    title = Column(String(255))
    framework = Column(String(50), default="html")
    code = Column(Text)
    description = Column(Text)
    image_paths = Column(Text)  # JSON array
    created_at = Column(DateTime, default=datetime.utcnow)
    provider = Column(String(50))
    model = Column(String(100))
    tokens_used = Column(Integer, default=0)
    cost = Column(Float, default=0.0)


class ImageAnalysis(Base):
    """Stored image analyses"""
    __tablename__ = 'image_analyses'

    id = Column(Integer, primary_key=True)
    title = Column(String(255))
    image_path = Column(String(500))
    analysis_type = Column(String(50))  # ocr, design, comparison, etc.
    result = Column(Text)
    metadata = Column(JSON)
    created_at = Column(DateTime, default=datetime.utcnow)


class Workspace(Base):
    """User workspaces for organization"""
    __tablename__ = 'workspaces'

    id = Column(Integer, primary_key=True)
    name = Column(String(255))
    description = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    settings = Column(JSON)  # Workspace-specific settings


class PromptTemplate(Base):
    """Saved prompt templates"""
    __tablename__ = 'prompt_templates'

    id = Column(Integer, primary_key=True)
    name = Column(String(255))
    category = Column(String(100))
    template = Column(Text)
    description = Column(Text)
    is_public = Column(Boolean, default=True)
    use_count = Column(Integer, default=0)
    created_at = Column(DateTime, default=datetime.utcnow)


class UsageLog(Base):
    """Track API usage and costs"""
    __tablename__ = 'usage_logs'

    id = Column(Integer, primary_key=True)
    provider = Column(String(50))
    model = Column(String(100))
    operation = Column(String(100))  # chat, code_gen, analysis, etc.
    tokens_input = Column(Integer, default=0)
    tokens_output = Column(Integer, default=0)
    cost = Column(Float, default=0.0)
    timestamp = Column(DateTime, default=datetime.utcnow)
    success = Column(Boolean, default=True)
    error_message = Column(Text)


class Database:
    """Database manager"""

    def __init__(self, db_path="sqlite:///vlm_demo.db"):
        self.engine = create_engine(db_path)
        Base.metadata.create_all(self.engine)
        self.Session = sessionmaker(bind=self.engine)

    def get_session(self):
        """Get database session"""
        return self.Session()

    def create_chat_session(self, title="New Conversation", provider=None, model=None, mode="chat"):
        """Create new chat session"""
        session = self.get_session()
        chat_session = ChatSession(
            title=title,
            provider=provider,
            model=model,
            mode=mode
        )
        session.add(chat_session)
        session.commit()
        session_id = chat_session.id
        session.close()
        return session_id

    def add_message(self, session_id, role, content, image_paths=None, tokens=0, cost=0.0):
        """Add message to session"""
        session = self.get_session()
        message = ChatMessage(
            session_id=session_id,
            role=role,
            content=content,
            image_paths=json.dumps(image_paths) if image_paths else None,
            tokens_used=tokens,
            cost=cost
        )
        session.add(message)
        session.commit()
        session.close()

    def get_session_history(self, session_id):
        """Get all messages from a session"""
        session = self.get_session()
        messages = session.query(ChatMessage).filter_by(session_id=session_id).order_by(ChatMessage.timestamp).all()
        result = [{
            'role': msg.role,
            'content': msg.content,
            'image_paths': json.loads(msg.image_paths) if msg.image_paths else [],
            'timestamp': msg.timestamp,
            'tokens': msg.tokens_used,
            'cost': msg.cost
        } for msg in messages]
        session.close()
        return result

    def list_chat_sessions(self, limit=50):
        """List all chat sessions"""
        session = self.get_session()
        sessions = session.query(ChatSession).order_by(ChatSession.updated_at.desc()).limit(limit).all()
        result = [{
            'id': s.id,
            'title': s.title,
            'created_at': s.created_at,
            'updated_at': s.updated_at,
            'provider': s.provider,
            'model': s.model,
            'mode': s.mode,
            'message_count': len(s.messages)
        } for s in sessions]
        session.close()
        return result

    def save_generated_code(self, title, code, framework="html", description="", image_paths=None,
                           provider=None, model=None, tokens=0, cost=0.0):
        """Save generated code"""
        session = self.get_session()
        gen_code = GeneratedCode(
            title=title,
            framework=framework,
            code=code,
            description=description,
            image_paths=json.dumps(image_paths) if image_paths else None,
            provider=provider,
            model=model,
            tokens_used=tokens,
            cost=cost
        )
        session.add(gen_code)
        session.commit()
        code_id = gen_code.id
        session.close()
        return code_id

    def log_usage(self, provider, model, operation, tokens_in=0, tokens_out=0, cost=0.0, success=True, error=None):
        """Log API usage"""
        session = self.get_session()
        log = UsageLog(
            provider=provider,
            model=model,
            operation=operation,
            tokens_input=tokens_in,
            tokens_output=tokens_out,
            cost=cost,
            success=success,
            error_message=error
        )
        session.add(log)
        session.commit()
        session.close()

    def get_usage_stats(self, days=30):
        """Get usage statistics"""
        from datetime import timedelta
        session = self.get_session()
        cutoff = datetime.utcnow() - timedelta(days=days)

        logs = session.query(UsageLog).filter(UsageLog.timestamp >= cutoff).all()

        stats = {
            'total_requests': len(logs),
            'total_cost': sum(log.cost for log in logs),
            'total_tokens': sum(log.tokens_input + log.tokens_output for log in logs),
            'by_provider': {},
            'by_operation': {},
            'success_rate': sum(1 for log in logs if log.success) / len(logs) * 100 if logs else 0
        }

        session.close()
        return stats

    def save_prompt_template(self, name, category, template, description="", is_public=True):
        """Save prompt template"""
        session = self.get_session()
        prompt = PromptTemplate(
            name=name,
            category=category,
            template=template,
            description=description,
            is_public=is_public
        )
        session.add(prompt)
        session.commit()
        session.close()

    def get_prompt_templates(self, category=None):
        """Get prompt templates"""
        session = self.get_session()
        query = session.query(PromptTemplate)
        if category:
            query = query.filter_by(category=category)
        templates = query.order_by(PromptTemplate.use_count.desc()).all()
        result = [{
            'id': t.id,
            'name': t.name,
            'category': t.category,
            'template': t.template,
            'description': t.description
        } for t in templates]
        session.close()
        return result


# Global database instance
db = Database()
