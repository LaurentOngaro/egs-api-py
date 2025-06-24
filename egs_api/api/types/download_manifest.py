"""
Download manifest data structures
"""

import struct
import zlib
import hashlib
import logging
from typing import Dict, List, Optional, Any
from pydantic import BaseModel
import json

logger = logging.getLogger(__name__)


class FileChunkPart(BaseModel):
    guid: str
    link: Optional[str] = None
    offset: int
    size: int


class FileManifestList(BaseModel):
    filename: str
    file_hash: str
    file_chunk_parts: List[FileChunkPart]

    def size(self) -> int:
        """Get file size"""
        return sum(part.size for part in self.file_chunk_parts)


class DownloadManifest(BaseModel):
    manifest_file_version: int
    b_is_file_data: bool
    app_id: int
    app_name_string: str
    build_version_string: str
    uninstall_action_path: Optional[str] = None
    uninstall_action_args: Optional[str] = None
    launch_exe_string: str
    launch_command: str
    prereq_ids: Optional[List[str]] = None
    prereq_name: str
    prereq_path: str
    prereq_args: str
    file_manifest_list: List[FileManifestList]
    chunk_hash_list: Dict[str, int]
    chunk_sha_list: Optional[Dict[str, str]] = None
    data_group_list: Dict[str, int]
    chunk_filesize_list: Dict[str, int]
    custom_fields: Optional[Dict[str, str]] = None

    @staticmethod
    def chunk_dir(version: int) -> str:
        """Get chunk directory based on manifest version"""
        if version >= 15:
            return "ChunksV4"
        elif version >= 6:
            return "ChunksV3"
        elif version >= 3:
            return "ChunksV2"
        else:
            return "Chunks"

    def set_custom_field(self, key: str, value: str) -> None:
        """Set a custom field"""
        if self.custom_fields is None:
            self.custom_fields = {}
        self.custom_fields[key] = value

    def custom_field(self, key: str) -> Optional[str]:
        """Get custom field value"""
        if self.custom_fields:
            return self.custom_fields.get(key)
        return None

    def download_links(self) -> Optional[Dict[str, str]]:
        """Get download links from the manifest"""
        url = self.custom_field("SourceURL")
        if not url:
            base_urls = self.custom_field("BaseUrl")
            if not base_urls:
                return None
            url = base_urls.split(',')[0]

        chunk_dir = self.chunk_dir(self.manifest_file_version)
        result = {}

        for guid, hash_val in self.chunk_hash_list.items():
            group_num = self.data_group_list.get(guid)
            if group_num is None:
                continue

            chunk_url = f"{url}/{chunk_dir}/{group_num:02d}/{hash_val:016X}_{guid.upper()}.chunk"
            result[guid] = chunk_url

        return result

    def files(self) -> Dict[str, FileManifestList]:
        """Get list of files in the manifest"""
        result = {}
        links = self.download_links() or {}

        for file_manifest in self.file_manifest_list:
            updated_parts = []
            for part in file_manifest.file_chunk_parts:
                updated_part = FileChunkPart(guid=part.guid, link=links.get(part.guid), offset=part.offset, size=part.size)
                updated_parts.append(updated_part)

            result[file_manifest.filename
                  ] = FileManifestList(filename=file_manifest.filename, file_hash=file_manifest.file_hash, file_chunk_parts=updated_parts)

        return result

    def total_download_size(self) -> int:
        """Get total size of chunks in the manifest"""
        return sum(self.chunk_filesize_list.values())

    def total_size(self) -> int:
        """Get total size of all files"""
        return sum(f.size() for f in self.file_manifest_list)

    @classmethod
    def parse(cls, data: bytes) -> Optional['DownloadManifest']:
        """Parse DownloadManifest from binary data or JSON"""
        logger.debug("Attempting to parse download manifest from binary data")

        manifest_hash = hashlib.sha1(data).hexdigest()

        # Try binary parsing first
        try:
            manifest = cls.from_bytes(data)
            if manifest:
                manifest.set_custom_field("DownloadedManifestHash", manifest_hash)
                return manifest
        except Exception as e:
            logger.debug(f"Binary parsing failed: {e}")

        # Try JSON parsing
        try:
            manifest_dict = json.loads(data.decode('utf-8'))
            manifest = cls.model_validate(manifest_dict)
            manifest.set_custom_field("DownloadedManifestHash", manifest_hash)
            return manifest
        except Exception as e:
            logger.debug(f"JSON parsing failed: {e}")

        return None

    @classmethod
    def from_bytes(cls, buffer: bytes) -> Optional['DownloadManifest']:
        """Create DownloadManifest from binary data"""
        # This is a simplified version - the full binary parsing would be quite complex
        # For now, we'll focus on JSON parsing
        raise NotImplementedError("Binary parsing not yet implemented in Python version")
