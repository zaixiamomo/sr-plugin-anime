"""动画领域 Bangumi 搜索，按标题选条目并发布中文名与放送日期。"""

import re
from collections.abc import Mapping
from datetime import date
from types import MappingProxyType

from sr.core.contracts.extender import Extender
from sr.core.values import SystemValue, TokenValue
from sr.plugin.resources import HttpClient, ResourceValues

SEARCH_URL = "https://api.bgm.tv/v0/search/subjects"


def _norm(text: str) -> str:
    return "".join(text.lower().split())


def _matches_title(title: str, candidate: Mapping) -> bool:
    query = _norm(title)
    return any(
        query == _norm(value)
        for key in ("name", "name_cn")
        if isinstance(value := candidate.get(key), str)
    )


class BangumiSearch(Extender):
    name = "bangumi_search"
    input_ports = ("title",)
    output_ports = ("name_cn", "date")
    required_resources = ("http",)

    @classmethod
    def create(cls, *, resources: ResourceValues) -> "BangumiSearch":
        return cls(resources["http"])

    def __init__(self, http: HttpClient) -> None:
        self._http = http

    def extend(
        self,
        input_values: Mapping[str, TokenValue],
        system_values: Mapping[str, SystemValue],
        *,
        options: Mapping[str, object] = MappingProxyType({}),
    ) -> Mapping[str, TokenValue]:
        title = input_values["title"].value
        if type(title) is not str or not title.strip():
            raise ValueError("Bangumi 标题必须是非空文本")
        data = self._http.post_json(
            SEARCH_URL, payload={"keyword": title, "filter": {"type": [2]}}
        )
        items = data.get("data") if isinstance(data, Mapping) else None
        candidates = (
            [item for item in items if isinstance(item, Mapping)]
            if isinstance(items, list)
            else []
        )
        if not candidates:
            raise ValueError("Bangumi 搜索没有可用条目")
        # 跨语言的字符相似度不能衡量作品相关性；仅精确标题覆盖服务端排序。
        candidate = next(
            (item for item in candidates if _matches_title(title, item)), candidates[0]
        )
        outputs = {}
        for port in self.output_ports:
            raw = candidate.get(port)
            if raw is None or raw == "":
                raise ValueError(f"Bangumi 条目缺少 {port}")
            if type(raw) is not str:
                raise TypeError(f"Bangumi {port} 必须是文本")
            if port == "date":
                if re.fullmatch(r"[0-9]{4}-[0-9]{2}-[0-9]{2}", raw) is None:
                    raise ValueError("Bangumi 日期必须符合 YYYY-MM-DD")
                try:
                    date.fromisoformat(raw)
                except ValueError as exc:
                    raise ValueError(f"Bangumi 日期非法：{raw}") from exc
            elif not raw.strip():
                raise ValueError("Bangumi 中文名为空")
            outputs[port] = TokenValue(value=raw, raw=raw, operations=())
        return outputs
