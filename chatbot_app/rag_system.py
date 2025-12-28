# chatbot_app/rag_system.py
# Secure, user-scoped, Persian-first chatbot with RAG over Chroma
from __future__ import annotations

import os
from typing import Dict, Iterable, List, Tuple

from django.conf import settings

# from chromadb import PersistentClient
# from langchain_community.vectorstores import Chroma
# from langchain_openai import OpenAIEmbeddings, ChatOpenAI
# from langchain.prompts import ChatPromptTemplate
# from langchain.memory import ConversationBufferMemory
# from langchain_core.runnables import RunnablePassthrough


def _get_setting(name: str, default=None):
    return getattr(settings, name, os.getenv(name, default))


# class ChatbotSystem:
#     """
#     One singleton per process; conversation memory is kept per (user_id, session_id).
#     Vector collections are restricted to the current user ("user:{id}:*") plus any "public:*".
#     """

#     def __init__(self):
#         # --- Secrets & models (no hard-coded keys) ---
#         api_key = _get_setting("OPENAI_API_KEY")
#         if not api_key:
#             raise RuntimeError(
#                 "OPENAI_API_KEY is not configured. Set it in env or Django settings."
#             )
#         os.environ["OPENAI_API_KEY"] = api_key

#         self.model_name = _get_setting("CHATBOT_MODEL", "gpt-4o-mini")
#         self.emb_model = _get_setting("EMBEDDINGS_MODEL", "text-embedding-3-small")

#         self.llm = ChatOpenAI(
#             model=self.model_name,
#             temperature=_get_setting("CHATBOT_TEMPERATURE", 0.2),
#             streaming=True,
#         )

#         # --- Vector DB ---
#         persist_dir = _get_setting(
#             "VECTORDB_DIR", os.path.join(settings.BASE_DIR, "media", "vector_dbs")
#         )
#         os.makedirs(persist_dir, exist_ok=True)
#         self.client = PersistentClient(path=persist_dir)
#         self.embedding_function = OpenAIEmbeddings(model=self.emb_model)

#         # --- Per-session memories ---
#         self._memories: Dict[Tuple[int, str], ConversationBufferMemory] = {}

#     # ------------ Memory (per user + session) ------------
#     def _memory_for(self, user_id: int, session_id: str) -> ConversationBufferMemory:
#         key = (user_id, session_id)
#         if key not in self._memories:
#             self._memories[key] = ConversationBufferMemory(
#                 memory_key="chat_history",
#                 return_messages=True,
#                 input_key="question",
#                 output_key="response",
#             )
#         return self._memories[key]

#     # ------------ Collections (user + public) ------------
#     def _allowed_collection_names(self, user_id: int) -> List[str]:
#         names = [c.name for c in self.client.list_collections()]
#         prefix_user = f"user:{user_id}:"
#         allowed = [n for n in names if n.startswith(prefix_user) or n.startswith("public:")]
#         return allowed

#     def _build_retrievers(self, user_id: int, k: int = 4):
#         retrievers = []
#         for name in self._allowed_collection_names(user_id):
#             vs = Chroma(
#                 client=self.client,
#                 collection_name=name,
#                 embedding_function=self.embedding_function,
#             )
#             retrievers.append(vs.as_retriever(search_kwargs={"k": k}))
#         return retrievers

#     # ------------ Retrieval ------------
#     @staticmethod
#     def _dedup(docs: Iterable):
#         seen = set()
#         out = []
#         for d in docs:
#             sig = (d.page_content, d.metadata.get("source"), d.metadata.get("page"))
#             if sig not in seen:
#                 seen.add(sig)
#                 out.append(d)
#         return out

#     def retrieve_from_all(self, user_id: int, question: str) -> Tuple[str, str]:
#         docs_all = []
#         citations = []
#         for r in self._build_retrievers(user_id):
#             try:
#                 docs = r.get_relevant_documents(question)
#             except Exception:
#                 docs = []
#             docs_all.extend(docs)

#         docs_all = self._dedup(docs_all)
#         context = "\n\n".join(d.page_content for d in docs_all) if docs_all else ""
#         for d in docs_all:
#             src = d.metadata.get("source", "منبع نامشخص")
#             page = d.metadata.get("page", "N/A")
#             citations.append(f"- {src}، صفحه {page}")

#         references = "\n".join(citations) if citations else ""
#         return context, references

#     # ------------ Prompt ------------
#     def _prompt(self) -> ChatPromptTemplate:
#         return ChatPromptTemplate.from_messages(
#             [
#                 (
#                     "system",
#                     (
#                         "تو دستیار فارسیِ Health WebPlatform هستی.\n"
#                         "پاسخ‌ها را کوتاه، شفاف و مرحله‌ای بده. اگر زمینه (context) داده شده مفید بود از آن استفاده کن و در پایان بخش «منابع» را فهرست کن.\n"
#                         "محدودیت ایمنی: محتوای پزشکی صرفاً آموزشی است و جایگزین تشخیص/درمان نیست؛ در موارد حساس توصیه کن با پزشک مشورت شود.\n"
#                         "اگر پاسخ دقیق نداشتی، عدم قطعیت را شفاف بیان کن."
#                     ),
#                 ),
#                 (
#                     "user",
#                     (
#                         "تاریخچه گفت‌وگو:\n{chat_history}\n\n"
#                         "زمینه (در صورت وجود):\n{context}\n\n"
#                         "پرسش:\n{question}\n\n"
#                         "منابع:\n{references}"
#                     ),
#                 ),
#             ]
#         )

#     # ------------ Streaming ------------
#     def stream_response(self, user, session_id: str, question: str):
#         memory = self._memory_for(user.id, session_id)
#         chat_history = memory.load_memory_variables({}).get("chat_history", [])

#         context, references = self.retrieve_from_all(user.id, question)

#         chain = (
#             RunnablePassthrough.assign(chat_history=lambda _: chat_history)
#             | self._prompt()
#             | self.llm
#         )

#         full = []
#         try:
#             for chunk in chain.stream(
#                 {"question": question, "context": context, "references": references}
#             ):
#                 token = getattr(chunk, "content", "") or ""
#                 full.append(token)
#                 yield token
#         finally:
#             if full:
#                 memory.save_context({"question": question}, {"response": "".join(full)})


# Singleton
# chatbot_system = ChatbotSystem()
