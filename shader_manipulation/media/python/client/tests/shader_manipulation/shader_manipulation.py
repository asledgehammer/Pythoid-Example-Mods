# Pythoid Example: Shader Uniform Manipulation
#
# Project Zomboid uses OpenGL and consequently uses GLSL Shaders to shade the game when rendered 
# each frame. With conventional Lua modding, there are zero ways to interact with shaders beyond
# replacing shader files, although this has no way to be modified by Lua code.
#
# In this example, I will replace the Uniform 'LightIntensity' with a 'LightIntensity2' uniform so
# that the uniform is controlled by us exclusively. I will then set the value to increase in a loop
# from 0.0 to 1.0. You should see a bump in lighting in-game.
# 
# NOTE: If a uniform is defined in the shader and no active code (Excludes commented code), doesn't
# reference the uniform, the compiled shader has no reference and the uniform doesn't exist. Make 
# sure to check for this situation with the uniform's location value not being -1 and the 
# Shader.Uniform not being None.
# 
# @author JabDoesThings 

from typing import Any
from com.asledgehammer import Pythoid
from java.lang import Runnable
from java.util import HashMap
from org.lwjgl.opengl import ARBShaderObjects
from zombie.core import Core
from zombie.core.opengl import RenderThread, Shader, ShaderProgram

class ShaderRunnable(Runnable):

    def __init__(self):

        self.valid = False

        # Make sure the shader exists.
        self.shader = Pythoid.getField(Core.getInstance(), "RenderShader") # type: Shader
        if self.shader == None:
            return

        # Shader properties.        
        self.shader_id = self.shader.getID()
        self.shader_program = self.shader.getProgram()
        self.shader_uniforms = Pythoid.getField(self.shader_program, 'uniformsByName') # type: HashMap[str, ShaderProgram.Uniform]

        # Grab the uniform.
        uniform = self.shader_uniforms.get('LightIntensity2') # type: ShaderProgram.Uniform
        # Make sure it exists.
        if uniform == None:
            return
        
        # Our stored value to set.
        self.LightIntensity2 = 0.0

        self.valid = True


    def update(self):
        # Updates the value to set for the uniform.
        self.LightIntensity2 = self.LightIntensity2 + 0.001
        if self.LightIntensity2 > 1.0:
            self.LightIntensity2 = 0.0


    def get_uniform_value(self, field):
        # type: (ShaderRunnable, str) -> Any
        uniform = self.shader_uniforms.get(field) # type: ShaderProgram.Uniform
        return ARBShaderObjects.glGetUniformfARB(self.shader_id, uniform.loc)


    def set_uniform_value(self, field, value):
        # type: (ShaderRunnable, str, Any) -> None
        self.shader_program.Start()
        self.shader_program.setValue(field, value)
        self.shader_program.End()


    def run(self):
        if not self.valid:
            return
        
        # Update the value to set.
        self.update()

        # Set the uniform-value.
        self.set_uniform_value('LightIntensity2', self.LightIntensity2)

        # Use this to see the result.
        #     
        #     print('LightIntensity2: ' + str(self.get_uniform_value('LightIntensity2')))


# This shader only exists when the game is loaded at-least once.
def on_game_start():

    shader_runnable = ShaderRunnable()

    if shader_runnable.valid:
        
        def on_render_tick():
            RenderThread.invokeOnRenderContext(shader_runnable)

        Events['OnRenderTick'].add(on_render_tick) # type: ignore

Events['OnGameStart'].add(on_game_start) # type: ignore

