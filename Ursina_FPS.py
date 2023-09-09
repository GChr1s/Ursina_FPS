from ursina import *
from ursina.prefabs.first_person_controller import FirstPersonController
from ursina.shaders import lit_with_shadows_shader
from ursina import curve

app = Ursina()
window.vsync = False
#import menu
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
    
    texturePath = "assets/wall.png"

    barrier = Entity(model='cube', texture=texturePath, scale = (5,300,100),position=(50,0,0),collider="box")
    barrier = Entity(model='cube', texture=texturePath, scale = (5,300,100),position=(-50,0,0),collider="box")
    barrier = Entity(model='cube', texture=texturePath, scale = (100,300,5),position=(0,0,50),collider="box")
    barrier = Entity(model='cube', texture=texturePath, scale = (100,300,5),position=(0,0,-50),collider="box")
    roof = Entity(model='cube', texture=texturePath, scale = (100,10,100),position=(0,150,0),collider="box")
    ground = Entity(model='plane', scale=(100,1,100), texture='textures\imsidoro.png', texture_scale=(1,1), collider='box')
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
    player = FirstPersonController(y=2, origin_y=-.5)
    player.gun = None
    player.speed = 10
    
    gun = Entity(model='assets\m4a1\M4A1.fbx', texture='assets\m4a1\mat0_c.jpg', parent=camera, position=(0.25,-0.15,0.5), scale=0.05, on_cooldown=False)
    gullet = Entity(model='cube', parent=camera, scale=0.02, rotation_y=270, position=(0.25,-0.1,0.95), color=color.black, collision=True, visible=False)
    suppressor = Entity(model='assets\Suppressor\source\low.obj', texture='assets\Suppressor\Textures\Suppressor_Base_color.png', parent=camera, scale=10)

    shootables_parent = Entity()
    mouse.traverse_target = shootables_parent  

    bullet=None

    def fullauto():
            if not gun.on_cooldown:
                gun.on_cooldown = True
                invoke(setattr, gun, 'on_cooldown', False, delay=.15)

    def aim(self):
        def shoot():
            M4A1_gunfire=Audio("assets\GunSounds\m4a1_gunshot.mp3", volume = 0.75)
            Cartridge=Audio("assets\GunSounds\Cartridge.mp3", volume = 0.75)
            bullet = Entity(parent=gullet, model='cube', scale=(0.75,0.75,2), rotation_y=90, color=color.lime,  collision=True, collider="box")
            bullet.world_parent = scene
            bullet.animate_position(bullet.position+(bullet.forward*1500), curve=curve.linear, duration=1)
            destroy(bullet, delay=1)
            M4A1_gunfire.play()
            Cartridge.play()
            gun.shake(0.1,0.02)
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
    
def start_game():
    menu_parent.enabled = False
    sg()
    destroy(menu)

# main menu content
main_menu.buttons = [
    MenuButton('start', on_click=start_game),
    MenuButton('options', on_click=Func(setattr, state_handler, 'state', 'options_menu')),
    MenuButton('quit', on_click=Sequence(Wait(.01), Func(sys.exit))),
]
for i, e in enumerate(main_menu.buttons):
    e.parent = main_menu
    e.y = (-i-2) * button_spacing

# options menu content
volume_slider = Slider(0, 10, default=10, step=1, text='Volume', parent=options_menu, x=-.25)
def set_volume_multiplier():
    Audio.volume_multiplier = volume_slider.value
volume_slider.on_value_changed = set_volume_multiplier

options_back = MenuButton(parent=options_menu, text='Back', x=-.25, origin_x=-.5, on_click=Func(setattr, state_handler, 'state', 'main_menu'))

for i, e in enumerate((volume_slider, options_back)):
    e.y = -i * button_spacing

# animate the buttons in nicely when changing menu
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