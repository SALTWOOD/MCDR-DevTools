import mcdreforged.api.all as mcdr
from .utils import (
    tr, CommandText, send_message
)
import sys
from io import StringIO
import platform

"""
常量定义
"""
PREFIX = "!!dev"
HELP_MESSAGE: mcdr.RTextBase

"""
装饰器
"""
def need_permission(permission):
    def decorator(func):
        def wrapper(source: mcdr.CommandSource, ctx: mcdr.CommandContext):
            if source.has_permission(permission):
                func(source, ctx)
            else:
                send_message(source, tr("error.no_enough_permission"))
        return wrapper
    
    return decorator

"""
工具方法
"""
@mcdr.new_thread('DEV_Help')
def print_help(source: mcdr.CommandSource) -> None:
    with source.preferred_language_context():
        send_message(source, HELP_MESSAGE)
        
def unknown_argument_handler(source: mcdr.CommandSource, error: mcdr.UnknownArgument):
    send_message(source, CommandText(
        tr("register.summary"),
        tr("register.hover"),
        PREFIX
    ))
    
def execute(command: str) -> str:
    origin_std = sys.stdout
    capture_std = StringIO()
    
    sys.stdout = capture_std
    
    try:
        exec(command)
    finally:
        sys.stdout = origin_std
        
    return capture_std.getvalue().strip("\n")
        

"""
注册部分
"""

def register_command(server: mcdr.PluginServerInterface) -> None:
    server.register_command(
        mcdr.Literal(PREFIX)
        .runs(print_help)
        .on_error(mcdr.UnknownArgument, unknown_argument_handler, handled=True)
        # 子命令
        .then(
            mcdr.Literal("python")
            # Python 运行时调试
            .then(
                mcdr.Literal("exec")
                .then(
                   mcdr.Text("command")
                   .runs(need_permission(4)(lambda src, ctx: send_message(src, execute(ctx["command"]), False)))
                )
            )
            .then(
                mcdr.Literal("eval")
                .then(
                    mcdr.Text("expression")
                    .runs(need_permission(4)(lambda src, ctx: send_message(src, eval(ctx["expression"]))))
                )
            )
        )
        .then(
            mcdr.Literal("system")
            .then(
                mcdr.Literal("info")
                .runs(lambda src, ctx: send_message(src, tr(
                    "strings.python.current_version",
                    f"{sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}",
                    platform.system(),
                    platform.version(),
                    platform.machine(),
                    platform.processor(),
                )))
            )
        )
    )

def register_event_listeners(server: mcdr.PluginServerInterface) -> None:
    ...

def on_load(server: mcdr.PluginServerInterface, prev_module) -> None:
    global HELP_MESSAGE
    meta: mcdr.Metadata = server.get_self_metadata()
    
    # 加载 HELP_MESSAGE
    HELP_MESSAGE = tr('help_message', meta.name, meta.version)
    
    server.register_help_message(PREFIX, CommandText(tr('register.summary'), tr('register.hover'), PREFIX))
    
    # 注册
    register_command(server)
    register_event_listeners(server)