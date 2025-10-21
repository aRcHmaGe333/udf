#!/usr/bin/env python3
import json, hashlib
from typing import Dict, Any, List

def canonical_json(d: Dict[str, Any]) -> bytes:
    return json.dumps(d, sort_keys=True, separators=(',', ':')).encode('utf-8')

def operator_id(spec: Dict[str, Any]) -> str:
    h = hashlib.sha256(canonical_json(spec)).hexdigest()
    return f"urn:udf:operator:sha256:{h}"

def apply_fir(vals: List[float], coeffs: List[float]) -> List[float]:
    # Simple 1D convolution (full), return same length as input (valid via clipping)
    n = len(vals); m = len(coeffs)
    out = [0.0]*n
    for i in range(n):
        acc = 0.0
        for k in range(m):
            j = i - k
            if j < 0:
                break
            acc += coeffs[k] * vals[j]
        out[i] = acc
    return out

