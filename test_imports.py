import sys
import sqlite3
from transformers import BertTokenizer, BertModel
import torch
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
import json
from concurrent.futures import ThreadPoolExecutor

print("Paquetes importados exitosamente.")