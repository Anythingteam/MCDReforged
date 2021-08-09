import os
from typing import Optional, TYPE_CHECKING

from mcdreforged.constants import plugin_constant
from mcdreforged.plugin.type.directory_plugin import DirectoryPlugin
from mcdreforged.plugin.type.regular_plugin import RegularPlugin
from mcdreforged.plugin.type.solo_plugin import SoloPlugin
from mcdreforged.plugin.type.zipped_plugin import ZippedPlugin
from mcdreforged.utils import string_util

if TYPE_CHECKING:
	from mcdreforged.plugin.plugin_manager import PluginManager


def __get_suffix(file_path: str):
	index = file_path.rfind('.')
	if index == -1:
		return ''
	return file_path[index:]


def __get_plugin_class_from_path(file_path: str, allow_disabled: bool) -> Optional[type]:
	if os.path.isfile(file_path):
		if file_path.endswith(plugin_constant.DISABLED_PLUGIN_FILE_SUFFIX) and allow_disabled:
			file_path = string_util.remove_suffix(file_path, plugin_constant.DISABLED_PLUGIN_FILE_SUFFIX)
		suffix = __get_suffix(file_path)
		if suffix == plugin_constant.SOLO_PLUGIN_FILE_SUFFIX:  # .py
			return SoloPlugin
		if suffix == plugin_constant.PACKED_PLUGIN_FILE_SUFFIX:  # .mcdr
			return ZippedPlugin
	elif os.path.isdir(file_path) and (allow_disabled or not file_path.endswith(plugin_constant.DISABLED_PLUGIN_FILE_SUFFIX)):
		if os.path.isfile(os.path.join(file_path, plugin_constant.PLUGIN_META_FILE)) and not os.path.isfile(os.path.join(file_path, '__init__.py')):
			return DirectoryPlugin
	return None


def maybe_plugin(file_path: str, *, allow_disabled: bool = False) -> bool:
	return __get_plugin_class_from_path(file_path, allow_disabled) is not None


def create_regular_plugin(plugin_manager: 'PluginManager', file_path: str) -> RegularPlugin:
	cls = __get_plugin_class_from_path(file_path, False)
	if cls is None:
		raise TypeError('Trying to create a regular plugin with invalid path {}'.format(file_path))
	return cls(plugin_manager, file_path)
