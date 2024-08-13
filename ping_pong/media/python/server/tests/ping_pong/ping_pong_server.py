import sys
from se.krka.kahlua.vm import KahluaTable
from zombie.Lua import LuaManager
from zombie.characters import IsoPlayer

Global = LuaManager.GlobalObject

def on_client_command(module_id, command_id, player, args):
    # type: (str, str, IsoPlayer, KahluaTable) -> None
    if module_id != 'pythoid' or command_id != 'ping_pong':
        return
    print('[pythoid:ping_pong]: Player ' + str(player) + ' said: ' + str(args.rawget('message')))
    
    argsOut = LuaManager.platform.newTable()
    argsOut.rawset('message', 'pong')

    Global.sendServerCommand(player, 'pythoid', 'ping_pong', argsOut)


Events['OnClientCommand'].add(on_client_command) # type: ignore
