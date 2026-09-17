def envelope_postprocessing_hook(result, generator, request, public):
    """
    قلاب پس‌پردازش drf-spectacular برای استانداردسازی تمامی پاسخ‌های موفق API:
    هر پاسخ موفق (200، 201، 204) را به صورت خودکار در پاکت استاندارد زیر قرار می‌دهد:
    {
        "meta": {
            "message": "...",
            "errors": {}
        },
        "data": <دیتای اصلی سریالایزر>
    }
    """
    if "components" not in result:
        result["components"] = {}
    if "schemas" not in result["components"]:
        result["components"]["schemas"] = {}

    # تعریف مدل عمومی Meta در بخش کامپوننت‌های اسکیما
    result["components"]["schemas"]["MetaResponse"] = {
        "type": "object",
        "properties": {
            "message": {
                "type": "string",
                "description": "پیام وضعیت عملیات",
                "example": "Operation successful",
            },
            "errors": {
                "type": "object",
                "description": "جزئیات خطاها در صورت بروز خطا",
                "additionalProperties": True,
                "example": {},
            },
        },
        "required": ["message", "errors"],
    }

    paths = result.get("paths", {})

    for path, path_item in paths.items():
        # مسیرهای سواگر، اسکیما و ادمین را دست‌نخورده باقی بگذار
        if path.startswith("/api/schema") or path.startswith("/admin"):
            continue

        for method, operation in path_item.items():
            if method.lower() not in ["get", "post", "put", "patch", "delete"]:
                continue

            responses = operation.get("responses", {})

            # مدیریت متد DELETE یا پاسخ‌های خالی 204 که در رندرر به 200 تبدیل شده و data: null دارند
            if "204" in responses:
                del responses["204"]
                responses["200"] = {
                    "description": "عملیات با موفقیت انجام شد",
                    "content": {
                        "application/json": {
                            "schema": {
                                "type": "object",
                                "properties": {
                                    "meta": {
                                        "$ref": "#/components/schemas/MetaResponse"
                                    },
                                    "data": {
                                        "nullable": True,
                                        "description": "داده تهی برای عملیات حذف",
                                        "example": None,
                                    },
                                },
                                "required": ["meta", "data"],
                            }
                        }
                    },
                }

            # کادوپیچ کردن پاسخ‌های 200 و 201
            for status_code in ["200", "201"]:
                if status_code in responses:
                    resp = responses[status_code]
                    content = resp.get("content", {})
                    if "application/json" in content:
                        json_content = content["application/json"]
                        if "schema" in json_content:
                            orig_schema = json_content["schema"]

                            # اگر از قبل کادوپیچ شده بود کاری نکن
                            if (
                                orig_schema.get("type") == "object"
                                and "properties" in orig_schema
                                and "meta" in orig_schema["properties"]
                                and "data" in orig_schema["properties"]
                            ):
                                continue

                            json_content["schema"] = {
                                "type": "object",
                                "properties": {
                                    "meta": {
                                        "$ref": "#/components/schemas/MetaResponse"
                                    },
                                    "data": orig_schema,
                                },
                                "required": ["meta", "data"],
                            }

    return result
