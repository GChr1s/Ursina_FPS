from ursina import *
from ursina.prefabs.first_person_controller import FirstPersonController
from ursina.shaders import lit_with_shadows_shader
from menu import menu

app = Ursina()
window.vsync = False
random.seed(0)
Entity.default_shader = lit_with_shadows_shader
sun = DirectionalLight()
sun.look_at(Vec3(1,-1,-1))
Sky()


ground = Entity(model='plane', scale=(100,1,100), texture='textures\doro.jpg', texture_scale=(1,1), collider='box')
apt = Entity(model='cube', scale=(5,100,10),position=(15,50,15), collider='box', texture='white_cube')
apt.texture_scale = (apt.scale_z, apt.scale_y)
apt = Entity(model='cube', scale=(1,5,10), x=-2, y=.01, collider='box', color=color.gray)
apt.texture_scale = (apt.scale_z, apt.scale_y)
apt = Entity(model='cube', scale=(5,100,10),position=(15,50,30), collider='box', texture='white_cube')
apt = Entity(model='cube', scale=(5,100,10),position=(30,50,30), collider='box', texture='white_cube')
apt = Entity(model='cube', scale=(5,100,10),position=(30,50,15), collider='box', texture='white_cube')
grass = Entity(model='assets\structure\source\Bush.fbx',scale=0.01,texture='assets\structure\Textures\grass3.png',position=(10,0,10))
grass = Entity(model='assets\structure\source\Bush.fbx',scale=0.01,texture='assets\structure\Textures\grass3.png',position=(8,0,13))
strl = Entity(model='assets\structure\source\Streetlights.fbx',scale=0.1,position=(25,0,6.5),collider='mesh')
strl2 = Entity(model='cube',scale=(0.5,15,0.5),position=(25,0,7.8),collider='box',visible = False)
for i in range(18,51):
    grass = Entity(model='assets\structure\source\Bush.fbx',scale=0.01,texture='assets\structure\Textures\grass3.png',position=(i,0,6.5))
player = FirstPersonController(y=2, origin_y=-.5)
player.gun = None
player.speed = 10
  
gun = Entity(model='assets\m4a1\M4A1.fbx', texture='assets\m4a1\mat0_c.jpg', parent=camera, position=(0.25,-0.15,0.5), scale=0.05, on_cooldown=False)
gullet = Entity(model='cube', parent=camera, scale=0.02, rotation_y=270, position=(0.25,-0.1,0.95), color=color.black, collision=True, visible=False)
suppressor = Entity(model='assets\Suppressor\source\low.obj', texture='assets\Suppressor\Textures\Suppressor_Base_color.png', parent=camera, scale=10)

shootables_parent = Entity()
mouse.traverse_target = shootables_parent  

bullet=None


def aim(self):
    def shoot():
        M4A1_gunfire=Audio("assets\GunSounds\m4a1_gunshot.mp3", volume = 0.75)
        Cartridge=Audio("assets\GunSounds\Cartridge.mp3", volume = 0.75)
        bullet = Entity(parent=gullet, model='cube', scale=(0.75,0.75,2), rotation_y=90, color=color.black, collision=True, collider="box")
        bullet.world_parent = scene
        bullet.animate_position(bullet.position+(bullet.forward*2500), curve=curve.linear, duration=1)
        destroy(bullet, delay=1)
        M4A1_gunfire.play()
        Cartridge.play()
        camera.shake(0.1,0.2)
        gun.shake(0.1,0.025)
    if held_keys['right mouse']:
        player.speed = 5
        gun.rotation=(0,0,0)
        gun.position=(0,-0.124,0.3)
        gullet.position=(0,-0.124,1)
        if held_keys['left mouse']:
            shoot()
    elif not held_keys['right mouse']:
        player.speed = 10
        if held_keys['w']:
            gun.position=(0.1,-0.25,0.4)
            gun.rotation=(25, -70, 0)
        elif held_keys['a']:
            gun.position=(0.1,-0.25,0.4)
            gun.rotation=(25, -70, 0)
        elif held_keys['s']:
            gun.position=(0.1,-0.25,0.4)
            gun.rotation=(25, -70, 0)
        elif held_keys['d']:
            gun.position=(0.1,-0.25,0.4)
            gun.rotation=(25, -70, 0)
        else:
            gun.position=(0.25,-0.15,0.5)
            gun.rotation=(0,0,0)
            gullet.position=(0.25,-0.1,0.95)
            if held_keys['left mouse']:
                shoot()
    elif held_keys['w']:
        gun.position=(0.1,-0.25,0.4)
        gun.rotation=(25, -70, 0)
    elif held_keys['a']:
        gun.position=(0.1,-0.25,0.4)
        gun.rotation=(25, -70, 0)
    elif held_keys['s']:
        gun.position=(0.1,-0.25,0.4)
        gun.rotation=(25, -70, 0)
    elif held_keys['d']:
        gun.position=(0.1,-0.25,0.4)
        gun.rotation=(25, -70, 0)
    else:
        gun.position=(0.25,-0.15,0.5)
        gun.rotation=(0,0,0)
        gullet.position=(0.25,-0.1,0.95)
        if held_keys['left mouse']:
            shoot()

aim = Entity(input=aim)

app.run()

