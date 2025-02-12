import chromadb

from .config import get_or_make_chroma_path

from openai import OpenAI
from rich.progress import track
from rich.console import Console


def add_embeddings_to_chroma(subs, openai_client):

    chroma_path = get_or_make_chroma_path()
    chroma_client = chroma_client = chromadb.PersistentClient(path=chroma_path) 
    collection = chroma_client.get_or_create_collection(name="subEmbeddings")

    for sub in track(subs, description="Getting embeddings"):
        channel_id = sub[0]
        video_id = sub[1]
        start_time = sub[2]
        text = sub[3]

        if text == '':
            continue

        embedding = get_embedding(text, "text-embedding-ada-002", openai_client)

        meta_data = {
            "channel_id": channel_id,
            "video_id": video_id,
            "start_time": start_time,
        }

        collection.add(
            documents=[text],
            embeddings=[embedding],
            metadatas=[meta_data],
            ids=[video_id + "_" + str(start_time)],
        )



def get_embedding(text, model="text-embedding-ada-002", client=OpenAI()):
   text = text.replace("\n", " ")
   return client.embeddings.create(input = [text], model=model).data[0].embedding

