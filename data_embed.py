import sys
from gpt4all import Embed4All
import psycopg2 

#receives string to be embedded by gpt4all
def embed_text(text_to_embed:str):

 embedder=Embed4All(device='gpu',model_name='nomic-embed-text-v1.f16.gguf')
 output = embedder.embed(text_to_embed)
 return output
