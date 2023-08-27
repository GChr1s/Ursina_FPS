from ursina import *
from ursina.prefabs.first_person_controller import FirstPersonController
from ursina.shaders import lit_with_shadows_shader

app = Ursina()

random.seed(0)
Entity.default_shader = lit_with_shadows_shader

ground = Entity(model='plane', collider='box', scale=900, texture='grass', texture_scale=(4,4))
ruined = Entity(model="ruined_portal.obj", collider = "mesh", position=(0,0,0),scale = "30")

editor_camera = EditorCamera(enabled=False, ignore_paused=True)
player = FirstPersonController(model='cube', z=-10, color=color.orange, origin_y=-.5, speed=30, collider='box')
player.collider = BoxCollider(player, Vec3(0,1,0), Vec3(1,2,1))



def pause_input(key):
    if key == 'm':    # 미니맵
        camera.position(player.position, player.position, player.position+10) # BROKEN
        

pause_handler = Entity(ignore_paused=True, input=pause_input)


Sky()


app.run()