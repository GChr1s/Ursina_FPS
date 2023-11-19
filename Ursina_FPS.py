from ursina import *
from ursina.prefabs.first_person_controller import FirstPersonController
from ursina.shaders import lit_with_shadows_shader
from ursina import curve
from ursina.prefabs.health_bar import HealthBar
import os


app = Ursina()
window.vsync = False
random.seed(0)
Entity.default_shader = lit_with_shadows_shader
sun = DirectionalLight()
sun.look_at(Vec3(1,-1,-1))
Sky()

app = Ursina()
class MenuButton(Button):
    def __init__(self, text='', **kwargs):
        super().__init__(text, scale=(.25, .075), highlight_color=color.azure, **kwargs)

        for key, value in kwargs.items():
            setattr(self, key ,value)

button_spacing = .075 * 1.25
menu_parent = Entity(parent=camera.ui, y=.25)
main_menu = Entity(parent=menu_parent)
options_menu = Entity(parent=menu_parent, y=-.15)

state_handler = Animator({
    'main_menu' : main_menu,
    'options_menu' : options_menu,
    }
)

def sg():
    random.seed(0)
    Entity.default_shader = lit_with_shadows_shader
    sun = DirectionalLight()
    sun.look_at(Vec3(1,-1,-1))
    Sky()
    
    texturePath ="assets\\brick.jpg"

    
    for i in range(0,18,1):
        parkour = Entity(model='cube',scale=(2,2,5),position=(45-5*i,1+2*i,45), collider="box")
        hitbox =Entity(model='cube',scale=(2.5,2,5.5),position=(45-5*i,1+2*i,45),collider="box",visible=False)
    for i in range(0,18,1):
        parkour = Entity(model='cube',scale=(5,2,2),position=(45,1+2*i,45-5*i), collider="box")
        hitbox =Entity(model='cube',scale=(5.5,2,2.5),position=(45,1+2*i,45-5*i),collider="box",visible=False)
    for i in range(0,18,1):
        parkour = Entity(model='cube',scale=(5,2,2),position=(-45,35+2*i,45-5*i), collider="box")
        hitbox =Entity(model='cube',scale=(5.5,2,2.5),position=(-45,35+2*i,45-5*i),collider="box",visible=False)
    parkour = Entity(model='cube',scale=(5,2,5),position=(45,1,45), collider="box")
    hitbox =Entity(model='cube',scale=(5.5,2,5.5),position=(45,1,45),collider="box",visible=False)
    parkour = Entity(model='cube',scale=(5,2,5),position=(-45,35,45), collider="box")
    hitbox =Entity(model='cube',scale=(5.5,2,5.5),position=(-45,35,45),collider="box",visible=False)
    parkour = Entity(model='cube',scale=(5,2,5),position=(45,35,-45), collider="box")
    hitbox =Entity(model='cube',scale=(5.5,2,5.5),position=(45,35,-45),collider="box",visible=False)
    
    barrier = Entity(model='cube', texture=texturePath,texture_scale=(10,10), scale = (5,300,100),position=(50,0,0),collider="box")
    barrier = Entity(model='cube', texture=texturePath,texture_scale=(10,10), scale = (5,300,100),position=(-50,0,0),collider="box")
    barrier = Entity(model='cube', texture=texturePath,texture_scale=(10,10), scale = (100,300,5),position=(0,0,50),collider="box")
    barrier = Entity(model='cube', texture=texturePath,texture_scale=(10,10), scale = (100,300,5),position=(0,0,-50),collider="box")
    roof = Entity(model='cube', texture=texturePath,texture_scale=(10,10), scale = (100,10,100),position=(0,150,0),collider="box")
    ground = Entity(model='plane', scale=(100,1,100), texture='textures\imsidoro.png', collider='box')
    apt = Entity(model='cube', scale=(5,100,10),position=(15,50,15), collider='box', texture='white_cube')
    apt = Entity(model='cube', scale=(5,100,10),position=(15,50,30), collider='box', texture='white_cube')
    apt = Entity(model='cube', scale=(5,100,10),position=(30,50,30), collider='box', texture='white_cube')
    apt = Entity(model='cube', scale=(5,100,10),position=(30,50,15), collider='box', texture='white_cube')
    apt = Entity(model='cube', scale=(5,100,10),position=(-15,50,-15), collider='box', texture='white_cube')
    apt = Entity(model='cube', scale=(5,100,10),position=(-15,50,-30), collider='box', texture='white_cube')
    apt = Entity(model='cube', scale=(5,100,10),position=(-30,50,-30), collider='box', texture='white_cube')
    apt = Entity(model='cube', scale=(5,100,10),position=(-30,50,-15), collider='box', texture='white_cube')
    apt = Entity(model='cube', scale=(5,100,10),position=(-15,50,15), collider='box', texture='white_cube')
    apt = Entity(model='cube', scale=(5,100,10),position=(-15,50,30), collider='box', texture='white_cube')
    apt = Entity(model='cube', scale=(5,100,10),position=(-30,50,30), collider='box', texture='white_cube')
    apt = Entity(model='cube', scale=(5,100,10),position=(-30,50,15), collider='box', texture='white_cube')
    apt = Entity(model='cube', scale=(5,100,10),position=(15,50,-15), collider='box', texture='white_cube')
    apt = Entity(model='cube', scale=(5,100,10),position=(15,50,-30), collider='box', texture='white_cube')
    apt = Entity(model='cube', scale=(5,100,10),position=(30,50,-30), collider='box', texture='white_cube')
    apt = Entity(model='cube', scale=(5,100,10),position=(30,50,-15), collider='box', texture='white_cube')
    
    player = FirstPersonController(model='cube', z=-25, color=color.orange, origin_y=-.5, speed=8, collider='box',visbile=False)
    player.collider = BoxCollider(player, Vec3(0,1,0), Vec3(1,2,1))
    player.gun = None
    player.speed = 10

    shootables_parent = Entity()
    mouse.traverse_target = shootables_parent
    
    gun = Entity(model='assets\m4a1\M4A1.fbx', texture='assets\m4a1\mat0_c.jpg', parent=camera, position=(0.25,-0.15,0.5), scale=0.05, on_cooldown=False)
    gun.muzzle_flash = Entity(parent=gun, position=(0,0.5,9), scale=5, model='quad', color=color.yellow, enabled=False)

    def aim(self):
        def shoot():
            M4A1_gunfire=Audio("assets\GunSounds\m4a1_gunshot.mp3", volume = 0.75)
            Cartridge=Audio("assets\GunSounds\Cartridge.mp3", volume = 0.75)
            gun.muzzle_flash.enabled=True
            M4A1_gunfire.play()
            Cartridge.play()
            gun.shake(0.1,0.03)
            invoke(gun.muzzle_flash.disable, delay=.05)
            if mouse.hovered_entity and hasattr(mouse.hovered_entity, 'hp'):
                mouse.hovered_entity.hp -= 10
                mouse.hovered_entity.blink(color.red)

        def straight():
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
                if held_keys['left mouse']:
                    shoot()
        
        def rm():
            if held_keys['right mouse']:
                player.speed = 5
                gun.rotation=(0,0,0)
                gun.position=(0,-0.124,0.3)
                if held_keys['left mouse']:
                    shoot()

            elif not held_keys['right mouse']:
                player.speed = 10
                straight()
            
        if held_keys['shift']:
            player.speed = 15
            straight()

        if not held_keys['shift']:
            player.speed = 10
            gun.position=(0.25,-0.15,0.5)
            gun.rotation=(0,0,0)
            if held_keys['right mouse']:
                player.speed = 5
                gun.rotation=(0,0,0)
                gun.position=(0,-0.124,0.3)
                if held_keys['left mouse']:
                    shoot()
            if held_keys['left mouse']:
                shoot()

    class Enemy(Entity):
        def __init__(self, **kwargs):
            super().__init__(parent=shootables_parent, model='cube', scale_y=4, origin_y=-.5, color=color.black, collider='box', **kwargs)
            self.health_bar = Entity(parent=self, y=1.3, model='cube', color=color.red, world_scale=(1.5,.1,.1))
            self.max_hp = 100
            self.hp = self.max_hp

        def update(self):
            dist = distance_xz(player.position, self.position)
            if dist > 40:
                return

            self.health_bar.alpha = max(0, self.health_bar.alpha - time.dt)

            self.look_at_2d(player.position, 'y')
            hit_info = raycast(self.world_position + Vec3(0,1,0), self.forward, 30, ignore=(self,))
            if hit_info.entity == player:
                if dist > 0:
                    self.position += self.forward * time.dt * 12
            
            if player.intersects(self):
                exit()

        @property
        def hp(self):
            return self._hp

        @hp.setter
        def hp(self, value):
            self._hp = value
            if value <= 0:
                destroy(self)
                return
            
            self.health_bar.world_scale_x = self.hp / self.max_hp * 1.5
            self.health_bar.alpha = 1

    enemies = [Enemy(x=x+1) for x in range(25)]
    
    aim = Entity(input=aim)
    
def start_game():
    menu_parent.enabled = False
    sg()
    destroy(menu)

main_menu.buttons = [
    MenuButton('start', on_click=start_game),
    MenuButton('options', on_click=Func(setattr, state_handler, 'state', 'options_menu')),
    MenuButton('quit', on_click=Sequence(Wait(.01), Func(sys.exit))),
]
for i, e in enumerate(main_menu.buttons):
    e.parent = main_menu
    e.y = (-i-2) * button_spacing

volume_slider = Slider(0, 10, default=10, step=1, text='Volume', parent=options_menu, x=-.25)
def set_volume_multiplier():
    Audio.volume_multiplier = volume_slider.value
volume_slider.on_value_changed = set_volume_multiplier

options_back = MenuButton(parent=options_menu, text='Back', x=-.25, origin_x=-.5, on_click=Func(setattr, state_handler, 'state', 'main_menu'))

for i, e in enumerate((volume_slider, options_back)):
    e.y = -i * button_spacing

for menu in (main_menu, options_menu):
    def animate_in_menu(menu=menu):
        for i, e in enumerate(menu.children):
            e.original_x = e.x
            e.x += .1
            e.animate_x(e.original_x, delay=i*.05, duration=.1, curve=curve.out_quad)

            e.alpha = 0
            e.animate('alpha', .7, delay=i*.05, duration=.1, curve=curve.out_quad)

            if hasattr(e, 'text_entity'):
                e.text_entity.alpha = 0
                e.text_entity.animate('alpha', 1, delay=i*.05, duration=.1)

    menu.on_enable = animate_in_menu

app.run()
