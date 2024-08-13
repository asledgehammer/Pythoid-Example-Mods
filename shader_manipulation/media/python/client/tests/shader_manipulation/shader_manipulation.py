from com.asledgehammer import Pythoid
from java.lang import Runnable
from java.util import HashMap
from zombie.core import Core
from zombie.core.opengl import RenderThread, Shader, ShaderProgram

global val
val = 0.0

class DummyRunnable(Runnable):
    
    def run(self):
        shader = Pythoid.getField(Core.getInstance(), "RenderShader") # type: Shader
        if shader == None:
            return
        
        shader_id = shader.getID()
        shaderProgram = shader.getProgram()

        field = 'LightIntensity2'

        uniformsByName = Pythoid.getField(shaderProgram, 'uniformsByName') # type: HashMap[str, ShaderProgram.Uniform]
        _uniform = uniformsByName.get(field) # type: ignore
        uniform = _uniform # type: ShaderProgram.Uniform
        if uniform == None:
            return

        # print(uniform.name)
        # print(ARBShaderObjects.glGetUniformfARB(shader_id, uniform.loc))

        global val
        val = val + 0.001
        if val > 1.0:
            val = 0.0

        shaderProgram.Start()
        shader.getProgram().setValue(field, val)
        shaderProgram.End()        

dummy_runnable = DummyRunnable()

def on_render_tick():
    RenderThread.invokeOnRenderContext(dummy_runnable)

Events['OnRenderTick'].add(on_render_tick) # type: ignore
