from mcdreforged.api.all import (
    RTextMCDRTranslation, ServerInterface,
    RText, RTextBase, RAction, CommandSource, RTextList
)
from typing import Optional, Any, Callable, Tuple, NamedTuple

"""
实用功能部分
"""

def tr(translation_key: str, *args) -> RTextMCDRTranslation:
	return ServerInterface.get_instance().rtr('saltwood_devtools.{}'.format(translation_key), *args)

def CommandText(message: Any, hover: Any, command: str) -> RTextBase:
    formatted_text: RTextBase = message.copy() if isinstance(message, RTextBase) else RText(message)
    return formatted_text.set_hover_text(hover).set_click_event(RAction.run_command, command)

def send_message(source: CommandSource, msg, tell=True):
	msg = RTextList(msg)
	if source.is_player and not tell:
		source.get_server().say(msg)
	else:
		source.reply(msg)