"""动画媒体能力：读取首个宽高有效的视频流，输出实际像素尺寸。"""

from collections.abc import Mapping
from types import MappingProxyType

from sr.core.contracts.extender import Extender
from sr.core.system import SystemField
from sr.core.values import SystemValue, TokenValue
from sr.plugin.resources import MediaProbe, ResourceValues


class FileResolution(Extender):
    name = "file_resolution"
    input_ports = ()
    output_ports = ("width", "height", "resolution")
    system_bindings = MappingProxyType(
        {
            "path": SystemField.FILE_PATH,
            "suffix": SystemField.FILE_SUFFIX,
        }
    )
    required_resources = ("media",)
    supported_suffixes = frozenset(
        {
            ".mkv",
            ".mp4",
            ".m4v",
            ".avi",
            ".mov",
            ".webm",
            ".ts",
            ".m2ts",
            ".mts",
            ".mpeg",
            ".mpg",
            ".vob",
            ".wmv",
            ".flv",
            ".ogv",
            ".3gp",
            ".3g2",
        }
    )

    def supports(self, system_values: Mapping[str, SystemValue]) -> bool:
        return system_values["suffix"] in self.supported_suffixes

    @classmethod
    def create(cls, *, resources: ResourceValues) -> "FileResolution":
        return cls(resources["media"])

    def __init__(self, media: MediaProbe) -> None:
        self._media = media

    def extend(
        self,
        input_values: Mapping[str, TokenValue],
        system_values: Mapping[str, SystemValue],
        *,
        options: Mapping[str, object] = MappingProxyType({}),
    ) -> Mapping[str, TokenValue]:
        data = self._media.probe(str(system_values["path"]))
        streams = data.get("streams") if isinstance(data, Mapping) else None
        if isinstance(streams, list):
            for stream in streams:
                if (
                    not isinstance(stream, Mapping)
                    or stream.get("codec_type") != "video"
                ):
                    continue
                width, height = stream.get("width"), stream.get("height")
                if (
                    type(width) is int
                    and type(height) is int
                    and width > 0
                    and height > 0
                ):
                    values = {
                        "width": str(width),
                        "height": str(height),
                        "resolution": f"{width}x{height}",
                    }
                    return {
                        port: TokenValue(value=value, raw=value, operations=())
                        for port, value in values.items()
                    }
        raise ValueError("媒体没有可用的视频分辨率")
