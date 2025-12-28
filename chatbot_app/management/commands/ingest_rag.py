from __future__ import annotations
import os, pathlib, typing as t
from django.core.management.base import BaseCommand, CommandError
from django.conf import settings
from chromadb import PersistentClient
from langchain_community.vectorstores import Chroma
from langchain_openai import OpenAIEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter

def _load_file(path: str) -> t.List[dict]:
    p = pathlib.Path(path)
    ext = p.suffix.lower()
    if ext in {'.txt', '.md'}:
        text = p.read_text(encoding='utf-8', errors='ignore')
        return [{'page_content': text, 'metadata': {'source': str(p)}}]
    elif ext == '.pdf':
        try:
            from pypdf import PdfReader
        except Exception:
            raise CommandError("برای PDF به pypdf نیاز است: pip install pypdf")
        reader = PdfReader(str(p))
        docs = []
        for i, page in enumerate(reader.pages):
            try:
                docs.append({'page_content': page.extract_text() or '', 'metadata': {'source': str(p), 'page': i+1}})
            except Exception:
                docs.append({'page_content': '', 'metadata': {'source': str(p), 'page': i+1}})
        return docs
    else:
        return []

def _iter_files(input_path: str):
    p = pathlib.Path(input_path)
    if p.is_file():
        yield p
    else:
        for f in p.rglob('*'):
            if f.suffix.lower() in {'.txt', '.md', '.pdf'}:
                yield f

class Command(BaseCommand):
    help = "ایندکس‌سازی اسناد برای Chroma با نام user:{id}:<name> یا public:<name>"

    def add_arguments(self, parser):
        parser.add_argument('--user', type=int, help='شناسه کاربر (برای کلکسیون کاربری)')
        parser.add_argument('--name', required=True, help='نام کلکسیون')
        parser.add_argument('--path', required=True, help='مسیر فایل/پوشه')
        parser.add_argument('--public', action='store_true', help='کلکسیون عمومی')

    def handle(self, *args, **opts):
        user_id = opts.get('user')
        name = opts['name']
        input_path = opts['path']
        is_public = bool(opts.get('public'))

        if not is_public and not user_id:
            raise CommandError("--user لازم است مگر اینکه --public بدهید.")

        collection_name = f"public:{name}" if is_public else f"user:{user_id}:{name}"

        persist_dir = getattr(settings, 'VECTORDB_DIR', os.path.join(settings.BASE_DIR, 'media', 'vector_dbs'))
        os.makedirs(persist_dir, exist_ok=True)

        api_key = getattr(settings, 'OPENAI_API_KEY', os.getenv('OPENAI_API_KEY'))
        if not api_key:
            raise CommandError("OPENAI_API_KEY تنظیم نشده است.")
        os.environ['OPENAI_API_KEY'] = api_key

        embed_model = getattr(settings, 'EMBEDDINGS_MODEL', 'text-embedding-3-small')
        embeddings = OpenAIEmbeddings(model=embed_model)

        client = PersistentClient(path=persist_dir)
        vs = Chroma(client=client, collection_name=collection_name, embedding_function=embeddings)

        splitter = RecursiveCharacterTextSplitter(chunk_size=1200, chunk_overlap=150, separators=['\n\n','\n',' ',''])

        total = 0
        for f in _iter_files(input_path):
            docs = _load_file(str(f))
            for d in docs:
                for chunk in splitter.split_text(d['page_content'] or ''):
                    meta = dict(d.get('metadata', {}))
                    meta.setdefault('source', str(f))
                    vs.add_texts([chunk], metadatas=[meta])
                    total += 1

        self.stdout.write(self.style.SUCCESS(f"✅ {total} تکه به {collection_name} اضافه شد"))
