import re

HANDLE_PREFIX = "9999"


def make_handle(object_id: str) -> str:
    return f"hdl:{HANDLE_PREFIX}/{object_id}"


def make_mets_id(obj_type: str, object_id: str) -> str:
    return f"dspace-{obj_type}-hdl:{HANDLE_PREFIX}/{object_id}"


def make_zip_name(obj_type: str, object_id: str) -> str:
    return f"{obj_type}@{HANDLE_PREFIX}-{object_id}.zip"


def slugify_id(text: str) -> str:
    return re.sub(r"[^a-z0-9]", "_", text.lower())[:40]


def assign_handle_ids(col_structure: dict) -> tuple[str, dict[str, str]]:
    com_id = col_structure["coleccion"]["internal_id"]
    sub_ids = {
        sub["name_subcollection"]: sub["internal_id"]
        for sub in col_structure.get("subcolecciones", [])
    }
    return com_id, sub_ids
