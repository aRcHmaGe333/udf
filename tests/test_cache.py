from ref.cache import put_chunk_to_cache, get_chunk_from_cache

def test_cache_put_get(tmp_path, monkeypatch):
  monkeypatch.setenv('UDF_CACHE_DIR', str(tmp_path))
  h = 'sha256:deadbeef'
  data = b'xyz'
  put_chunk_to_cache(h, data)
  out = get_chunk_from_cache(h)
  assert out == data

