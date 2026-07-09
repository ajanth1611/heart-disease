
import json
import os
from pathlib import Path

from supabase import create_client # type: ignore
import streamlit as st

BASE_DIR = Path(__file__).resolve().parent
LOCAL_PREDICTIONS_FILE = BASE_DIR / "models" / "predictions_local.json"


def _read_secret(key, nested_key=None):
    if nested_key:
        return st.secrets.get(key, {}).get(nested_key) or os.environ.get(nested_key.upper())
    return st.secrets.get(key) or os.environ.get(key.upper())


def _load_supabase_config():
    supabase_secrets = st.secrets.get("supabase", {})
    url = (
        supabase_secrets.get("url")
        or _read_secret("SUPABASE_URL")
        or "https://dlncartnlnticoylvtpe.supabase.co"
    )
    key = (
        supabase_secrets.get("service_role_key")
        or supabase_secrets.get("anon_key")
        or supabase_secrets.get("key")
        or _read_secret("SUPABASE_KEY")
        or "sb_publishable_EQmOPFMJ2BDFS875vF4ADg_kmTYh7iD"
    )
    return url, key


SUPABASE_URL, SUPABASE_KEY = _load_supabase_config()
supabase = None


def _get_supabase_client():
    global supabase
    if supabase is not None:
        return supabase

    if not SUPABASE_URL or not SUPABASE_KEY:
        return None

    try:
        supabase = create_client(SUPABASE_URL, SUPABASE_KEY)
    except Exception:
        supabase = None
    return supabase


def _save_locally(data):
    LOCAL_PREDICTIONS_FILE.parent.mkdir(parents=True, exist_ok=True)
    existing = []
    if LOCAL_PREDICTIONS_FILE.exists():
        try:
            existing = json.loads(LOCAL_PREDICTIONS_FILE.read_text(encoding="utf-8"))
        except (json.JSONDecodeError, IOError):
            existing = []
    existing.append(data)
    LOCAL_PREDICTIONS_FILE.write_text(json.dumps(existing, indent=2), encoding="utf-8")
    return {"data": data, "saved_locally": True}


def save_prediction(data):
    """
    Save a prediction record into the 'predictions' table.
    """
    client = _get_supabase_client()
    if not client:
        return {
            "data": data,
            "saved_locally": True,
            "message": "Supabase client unavailable, saved prediction locally.",
        }

    try:
        response = (
            client
            .table("predictions")
            .insert(data)
            .execute()
        )
    except Exception as err:
        message = str(err)
        if "row-level security" in message.lower() or "could not find" in message.lower():
            fallback = _save_locally(data)
            fallback["saved_locally"] = True
            fallback["message"] = "Prediction saved locally because Supabase insert failed."
            return fallback
        return {"error": message}

    if getattr(response, "error", None):
        error_message = response.error.message if hasattr(response.error, "message") else str(response.error)
        if "row-level security" in error_message.lower() or "could not find" in error_message.lower():
            fallback = _save_locally(data)
            fallback["saved_locally"] = True
            fallback["message"] = "Prediction saved locally because Supabase insert failed."
            return fallback
        return {"error": error_message}

    return {"data": response.data, "message": "Prediction saved to Supabase successfully."}


def get_predictions():
    """
    Fetch all prediction records ordered by latest first.
    """
    client = _get_supabase_client()
    if not client:
        return {"error": "Supabase client unavailable."}

    response = (
        client
        .table("predictions")
        .select("*")
        .order("created_at", desc=True)
        .execute()
    )
    if getattr(response, "error", None):
        return {"error": response.error}
    return {"data": response.data}
