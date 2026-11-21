"""动画领域入口：作品信息查询与本地视频分辨率。"""

__version__ = "0.1.0"

from sr.plugin import Domain

from .bangumi import BangumiSearch
from .file_resolution import FileResolution

DOMAIN = Domain(name="anime", extenders=(BangumiSearch, FileResolution))
