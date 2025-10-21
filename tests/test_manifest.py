from ref.chunker import manifest_for_file

def test_manifest_fields(tmp_path):
  p = tmp_path/"x.bin"
  p.write_bytes(b"hello world")
  m = manifest_for_file(str(p))
  assert m['version'] == '1.0'
  assert m['id'].startswith('urn:udf:manifest:sha256:') or m['id'].startswith('urn:udf:content-map:sha256:')
  assert m['total_size'] == 11
  assert len(m['chunks']) >= 1

