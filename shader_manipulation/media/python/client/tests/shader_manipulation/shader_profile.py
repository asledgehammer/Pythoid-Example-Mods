from synchronize import make_synchronized # type: ignore
from com.asledgehammer import Pythoid # type: ignore
from java.util import HashMap # type: ignore
from org.lwjgl.opengl import ARBShaderObjects # type: ignore
from zombie.core import SpriteRenderer # type: ignore
from zombie.core.opengl import ShaderProgram # type: ignore

class ShaderProfile:
    
    @make_synchronized
    def apply_render_thread(self, shader_id):
        # type: (ShaderProfile, int) -> None

        if self.apply_only_once and self.applied:
            raise Exception('The profile is already applied.')
        
        try:
            if self.cache_values:
                if len(self.map_field_queue) != 0:
                    for field in self.map_field_queue:
                        loc = ARBShaderObjects.glGetUniformLocationARB(shader_id, field)
                        if loc == -1:
                            continue
                        self.map_field_to_loc[field] = loc
                        self.map_loc_to_value[loc] = self.map_field_queue[field]
                    self.map_field_queue.clear()

                # Apply the set cached value(s).
                for loc in self.map_loc_to_value:
                    if loc == None:
                        continue
                    value = self.map_loc_to_value[loc]
                    if type(value[0]) == int:
                        ARBShaderObjects.glUniform1iARB(loc, value[0])
                    elif type(value[0]) == float:
                        ARBShaderObjects.glUniform1fARB(loc, value[0])
            else:
                if len(self.map_field_queue) != 0:
                    for field in self.map_field_queue:
                        loc = ARBShaderObjects.glGetUniformLocationARB(shader_id, field)
                        if loc == -1:
                            continue
                        value = self.map_field_queue[field]
                        if type(value[0]) == int:
                            ARBShaderObjects.glUniform1iARB(loc, value[0])
                        elif type(value[0]) == float:
                            ARBShaderObjects.glUniform1fARB(loc, value[0])
        except Exception:
            print('##### Failed to Apply injected uniform(s).')
        finally:
            self.applied = True
    
    
    @make_synchronized
    def revert_render_thread(self, shader_id):
        # type: (ShaderProfile, int) -> None
        try:
            if self.cache_values:
                if len(self.map_field_queue) != 0:
                    for field in self.map_field_queue:
                        loc = ARBShaderObjects.glGetUniformLocationARB(shader_id, field)
                        if loc == -1:
                            continue
                        self.map_field_to_loc[field] = loc
                        self.map_loc_to_value[loc] = self.map_field_queue[field]
                    self.map_field_queue.clear()
                
                # Revert to the original value(s)
                for loc in self.map_loc_to_value:
                    if loc == None:
                        continue
                    value = self.map_field_queue[field]
                    if type(value[1]) == int:
                        ARBShaderObjects.glUniform1iARB(loc, value[1])
                    elif type(value[1]) == float:
                        ARBShaderObjects.glUniform1fARB(loc, value[1])
            else:
                if len(self.map_field_queue) != 0:
                    for field in self.map_field_queue:
                        loc = ARBShaderObjects.glGetUniformLocationARB(shader_id, field)
                        if loc == -1:
                            continue
                        value = self.map_field_queue[field]
                        if type(value[1]) == int:
                            ARBShaderObjects.glUniform1iARB(loc, value[1])
                        elif type(value[1]) == float:
                            ARBShaderObjects.glUniform1fARB(loc, value[1])
        except Exception:
            print('##### Failed to Apply injected uniform(s).')
        finally:
            self.applied = False
    

    def apply_main_thread(self, shader):
        # type: (ShaderProfile, ShaderProgram) -> None
        try:
            shader_id = shader.getShaderID()
            
            if self.cache_values:
                if len(self.map_field_queue) != 0:
                    uniformsByName = Pythoid.getField(shader, 'uniformsByName') # type: HashMap[str, ShaderProgram.Uniform]
                    for field in self.map_field_queue:
                        uniform = uniformsByName.get(field) # type: ignore # type: ShaderProgram.Uniform
                        if uniform == None:
                            continue
                        _loc = uniform.loc # type: ignore
                        loc = _loc # type: int
                        if loc == -1:
                            continue
                        self.map_field_to_loc[field] = loc
                        self.map_loc_to_value[loc] = self.map_field_queue[field]
                    self.map_field_queue.clear()
                for loc in self.map_loc_to_value:
                    if loc == None:
                        continue
                    value = self.map_loc_to_value[loc]
                    if type(value[0]) == int:
                        SpriteRenderer.instance.ShaderUpdate1i(shader_id, loc, value[0])
                    elif type(value[0]) == float:
                        SpriteRenderer.instance.ShaderUpdate1f(shader_id, loc, value[0])
            else:
                if len(self.map_field_queue) != 0:
                    uniformsByName = Pythoid.getField(shader, 'uniformsByName') # type: HashMap[str, ShaderProgram.Uniform]
                    for field in self.map_field_queue:
                        value = self.map_field_queue[field]
                        uniform = uniformsByName.get(field) # type: ignore type: ShaderProgram.Uniform
                        if uniform == None:
                            continue
                        _loc = uniform.loc # type: ignore
                        loc = _loc # type: int
                        if loc == -1:
                            continue
                    if type(value[0]) == int:
                        SpriteRenderer.instance.ShaderUpdate1i(shader_id, loc, value[0])
                    elif type(value[0]) == float:
                        SpriteRenderer.instance.ShaderUpdate1f(shader_id, loc, value[0])
        except Exception:
            print('##### Failed to Apply injected uniform(s).')
        finally:
            self.applied = True
    

    def revert_main_thread(self, shader):
        # type: (ShaderProfile, ShaderProgram) -> None
        try:
            shader_id = shader.getShaderID()
            if self.cache_values:
                if len(self.map_field_queue) != 0:
                    uniformsByName = Pythoid.getField(shader, 'uniformsByName') # type: HashMap[str, ShaderProgram.Uniform]
                    for field in self.map_field_queue:
                        uniform = uniformsByName.get(field) # type: ignore
                        if uniform == None:
                            continue
                        _loc = uniform.loc # type: ignore
                        loc = _loc # type: int
                        if loc == -1:
                            continue

                        self.map_field_to_loc[field] = loc
                        self.map_loc_to_value[loc] = self.map_field_queue[field]
                    self.map_field_queue.clear()
                
                for loc in self.map_loc_to_value:
                    if loc == None:
                        continue
                    value = self.map_field_to_loc[loc]
                    if type(value[1] == int):
                        SpriteRenderer.instance.ShaderUpdate1i(shader_id, loc, value[1])
                    elif type(value[1] == float):
                        SpriteRenderer.instance.ShaderUpdate1f(shader_id, loc, value[1])
            else:
                if len(self.map_field_queue) != 0:
                    uniformsByName = Pythoid.getField(shader, 'uniformsByName') # type: HashMap[str, ShaderProgram.Uniform]
                    for field in self.map_field_queue:
                        value = self.map_field_queue[field]
                        uniform = uniformsByName.get(field) # type: ignore
                        if uniform == None:
                            continue
                        _loc = uniform.loc # type: ignore
                        loc = _loc # type: int
                        if loc == -1:
                            continue
                        if type(value[1] == int):
                            SpriteRenderer.instance.ShaderUpdate1i(shader_id, loc, value[1])
                        elif type(value[1] == float):
                            SpriteRenderer.instance.ShaderUpdate1f(shader_id, loc, value[1])
        except Exception:
            print('##### Failed to Apply injected uniform(s).')
        finally:
            self.applied = False
    

    @make_synchronized
    def set(self, field, to_set, to_revert):
        try:
            if self.cache_values:
                if self.map_field_to_loc[field] != None:
                    self.map_loc_to_value[self.map_field_to_loc[field]] = [to_set, to_revert]
                else:
                    self.map_field_queue[field] = [to_set, to_revert]
            else:
                self.map_field_queue[field] = [to_set, to_revert]
        except Exception:
            print('##### Failed to inject uniform(s).')
    

    def setFloat1(self, field, to_set, to_revert):
        # type: (ShaderProfile, str, float, float) -> None
        self.set(field, to_set, to_revert)
    

    def setInt1(self, field, to_set, to_revert):
        # type: (ShaderProfile, str, int, int) -> None
        self.set(field, to_set, to_revert)


    def remove(self, field):
        # type: (ShaderProfile, str) -> None
        if self.map_field_to_loc[field] != None:
            loc = self.map_field_to_loc[field]
            del self.map_loc_to_value[loc]
        del self.map_field_queue[field]
    

    def __init__(self, apply_only_once, cache_values):
        # type: (ShaderProfile, bool, bool) -> None
        self.apply_only_once = apply_only_once
        self.cache_values = cache_values
        self.applied = False
        self.map_field_to_loc = dict()
        self.map_loc_to_value = dict()
        self.map_field_queue = dict()
