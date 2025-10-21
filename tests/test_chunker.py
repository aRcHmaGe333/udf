import os
from ref.chunker import manifest_for_file, chunk_iter, DEFAULT_CHUNK_SIZE

def write_tmp(path, data: bytes):
  with open(path, 'wb') as f:
    f.write(data)

def test_fixed_size_chunking(tmp_path):
  data = b"A" * (DEFAULT_CHUNK_SIZE + 10)
  p = tmp_path/"a.bin"
  write_tmp(p, data)
  chunks = list(chunk_iter(str(p)))
  assert len(chunks) == 2
  m = manifest_for_file(str(p))
  assert m['total_size'] == len(data)
  assert len(m['chunks']) == 2

