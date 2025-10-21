from ref.operators import apply_fir

def test_apply_fir():
  vals = [1.0, 2.0, 3.0, 4.0]
  coeffs = [0.5, 0.5]
  out = apply_fir(vals, coeffs)
  # simple moving average of window 2 on prefix
  assert out[0] == 0.5
  assert abs(out[1] - 1.5) < 1e-9
  assert abs(out[2] - 2.5) < 1e-9

