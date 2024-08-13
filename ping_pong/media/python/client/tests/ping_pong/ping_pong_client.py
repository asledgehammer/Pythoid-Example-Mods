import sys
from se.krka.kahlua.vm import KahluaTable
from zombie.Lua import LuaManager

Global = LuaManager.GlobalObject

def every_ten_minutes():
    # type: () -> None
    print('[pythoid:ping_pong] Sending ping..')

    # Remove after first execution.
    Events['EveryTenMinutes'].remove(every_ten_minutes) # type: ignore

    argsOut = LuaManager.platform.newTable()
    argsOut.rawset('message', 'ping')

    Global.sendClientCommand('pythoid', 'ping_pong', argsOut)

Events['EveryTenMinutes'].add(every_ten_minutes) # type: ignore

def on_server_command(module_id, command_id, args):
    # type: (str, str, KahluaTable) -> None
    if module_id != 'pythoid' or command_id != 'ping_pong':
        return    
    print('[pythoid:ping_pong]: Server said: ' + str(args.rawget('message')))

Events['OnServerCommand'].add(on_server_command) # type: ignore
