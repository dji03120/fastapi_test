
import os
import io
import cv2
import base64
import PIL.Image as Image

import asyncio
import random
import json
import zipfile
import pickle
import datetime
import math
import inspect
import numpy as np
import pandas as pd
import pyarrow as pa
import pyarrow.parquet as pq
import traceback

from pathlib import Path
from fastapi import APIRouter
from pydantic import BaseModel
from typing import Optional, Tuple, Literal, List
from fastapi.responses import JSONResponse
from fastapi.responses import StreamingResponse
from fastapi import WebSocket, WebSocketDisconnect, APIRouter

import uuid
from functools import wraps


def safe_exec(func):
    """서버 동작 중 에러 발생해도 서버가 죽지 않고 500 에러로 응답하도록 하는 데코레이터"""
    if inspect.iscoroutinefunction(func):
        @wraps(func)
        async def async_wrapper(*args, **kwargs):
            try: return await func(*args, **kwargs)
            except Exception:
                print(traceback.format_exc())
                return JSONResponse(
                    content={"error": "internal server error"},
                    status_code=500
                )
        return async_wrapper
    else:
        @wraps(func)
        def sync_wrapper(*args, **kwargs):
            try: return func(*args, **kwargs)
            except Exception:
                print(traceback.format_exc())
                return JSONResponse(
                    content={"error": "internal server error"},
                    #content={"error": traceback.format_exc()}, # 에러내용을 클라이언트에 반환
                    status_code=500
                )
        return sync_wrapper




def safe_value(value):
    """모든 타입을 안전하게 float/str/list/dict로 변환"""
    # None → None
    if value is None: return None

    # numpy array → list
    if isinstance(value, np.ndarray):
        value = np.nan_to_num(value, nan=0.0, posinf=0.0, neginf=0.0)
        return value.tolist()

    # numpy scalar → 기본 타입
    if isinstance(value, (np.integer, np.floating)):
        v = value.item()
        if isinstance(v, float):
            if math.isnan(v): return "nan"
            if math.isinf(v): return "inf"
        return v

    # bytes → utf-8 string
    if isinstance(value, (bytes, bytearray)):
        try: return value.decode('utf-8')
        except Exception: return str(value)

    # list, dict → 그대로
    if isinstance(value, (list, dict)): 
        return value

    # bool → float 변환 (or str로 원하면 str(value))
    if isinstance(value, bool):
        return float(value)

    # datetime → isoformat 문자열
    if isinstance(value, (datetime.datetime, datetime.date)):
        return value.isoformat()

    # int, float → float로 변환 (NaN/inf 처리)
    if isinstance(value, (int, float)):
        if isinstance(value, float):
            if math.isnan(value): return "nan"
            if math.isinf(value): return "inf"
        return float(value)

    # str → 그대로
    if isinstance(value, str):
        return value

    # tuple, set → list
    if isinstance(value, (tuple, set)):
        return list(value)

    # custom object → JSON 직렬화 시도
    try:
        json.dumps(value)
        return value
    except Exception:
        # JSON 안 되면 문자열로 변환
        return str(value)
