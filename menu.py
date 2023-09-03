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
    class FirstPersonController(Entity):
        def __init__(self, **kwargs):
            super().__init__()
            self.speed = 10
            self.height = 2
            self.camera_pivot = Entity(parent=self, y=self.height)

            camera.parent = self.camera_pivot
            camera.position = (0,0,0)
            camera.rotation = (0,0,0)
            camera.fov = 90
            mouse.locked = True
            self.mouse_sensitivity = Vec2(40, 40)

            self.gravity = 1
            self.grounded = False
            self.jump_height = 2
            self.jump_up_duration = .5
            self.fall_after = .35
            self.jumping = False
            self.air_time = 0

            self.traverse_target = scene
            self.ignore_list = [self, ]

            for key, value in kwargs.items():
                setattr(self, key ,value)

            if self.gravity:
                ray = raycast(self.world_position+(0,self.height,0), self.down, traverse_target=self.traverse_target, ignore=self.ignore_list)
                if ray.hit:
                    self.y = ray.world_point.y

        def update(self):
            self.rotation_y += mouse.velocity[0] * self.mouse_sensitivity[1]

            self.camera_pivot.rotation_x -= mouse.velocity[1] * self.mouse_sensitivity[0]
            self.camera_pivot.rotation_x= clamp(self.camera_pivot.rotation_x, -90, 90)

            self.direction = Vec3(
                self.forward * (held_keys['w'] - held_keys['s'])
                + self.right * (held_keys['d'] - held_keys['a'])
                ).normalized()

            feet_ray = raycast(self.position+Vec3(0,0.5,0), self.direction, traverse_target=self.traverse_target, ignore=self.ignore_list, distance=.5, debug=False)
            head_ray = raycast(self.position+Vec3(0,self.height-.1,0), self.direction, traverse_target=self.traverse_target, ignore=self.ignore_list, distance=.5, debug=False)
                
            if not feet_ray.hit and not head_ray.hit:
                move_amount = self.direction * time.dt * self.speed
                if raycast(self.position+Vec3(-.0,1,0), Vec3(1,0,0), distance=.5, traverse_target=self.traverse_target, ignore=self.ignore_list).hit:
                    move_amount[0] = min(move_amount[0], 0)
                if raycast(self.position+Vec3(-.0,1,0), Vec3(-1,0,0), distance=.5, traverse_target=self.traverse_target, ignore=self.ignore_list).hit:
                    move_amount[0] = max(move_amount[0], 0)
                if raycast(self.position+Vec3(-.0,1,0), Vec3(0,0,1), distance=.5, traverse_target=self.traverse_target, ignore=self.ignore_list).hit:
                    move_amount[2] = min(move_amount[2], 0)
                if raycast(self.position+Vec3(-.0,1,0), Vec3(0,0,-1), distance=.5, traverse_target=self.traverse_target, ignore=self.ignore_list).hit:
                    move_amount[2] = max(move_amount[2], 0)
                self.position += move_amount

            if self.gravity:
                ray = raycast(self.world_position+(0,self.height,0), self.down, traverse_target=self.traverse_target, ignore=self.ignore_list)

                if ray.distance <= self.height+.1:
                    if not self.grounded:
                        self.land()
                    self.grounded = True

                    if ray.world_normal.y > .7 and ray.world_point.y - self.world_y < .5: # walk up slope
                        self.y = ray.world_point[1]
                    return
                else:
                    self.grounded = False

                self.y -= min(self.air_time, ray.distance-.05) * time.dt * 100
                self.air_time += time.dt * .25 * self.gravity

        def input(self, key):
            if key == 'space':
                self.jump()

        def jump(self):
            if not self.grounded:
                return

            self.grounded = False
            self.animate_y(self.y+self.jump_height, self.jump_up_duration, resolution=int(1//time.dt), curve=curve.out_expo)
            invoke(self.start_fall, delay=self.fall_after)

        def start_fall(self):
            self.y_animator.pause()
            self.jumping = False

        def land(self):
            self.air_time = 0
            self.grounded = True

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
    strl = Entity(model='assets\structure\source\Streetlights.fbx',scale=0.1,position=(25,0,6.5))
    for i in range(18,51):
        grass = Entity(model='assets\structure\source\Bush.fbx',scale=0.01,texture='assets\structure\Textures\grass3.png',position=(i,0,6.5))
    player = FirstPersonController(y=2, origin_y=-.5)
    player.gun = None
        
    gun = Entity(model='assets\m4a1\M4A1.fbx', texture='assets\m4a1\mat0_c.jpg', parent=camera, position=(0.25,-0.15,0.5), scale=0.05, on_cooldown=False)
    gullet = Entity(model='cube', parent=camera, scale=0.02, rotation_y=270, position=(0.25,-0.1,0.95), color=color.black, collision=True, visible=False)
    suppressor = Entity(model='assets\Suppressor\source\low.obj', texture='assets\Suppressor\Textures\Suppressor_Base_color.png', parent=camera, scale=10)

    shootables_parent = Entity()
    mouse.traverse_target = shootables_parent  

    bullet=None
    def shoot():
        global bullet
        bullet = Entity(parent=gullet, model='cube', scale=(0.75,0.75,2), rotation_y=90, color=color.black, collision=True, collider="box")
        bullet.world_parent = scene
        bullet.animate_position(bullet.position+(bullet.forward*2500), curve=curve.linear, duration=1)
        destroy(bullet, delay=1)
        M4A1_gunfire.play()
        Cartridge.play()
        camera.shake(0.1,0.2)
        gun.shake(0.1,0.05)

    M4A1_gunfire=Audio("assets\GunSounds\m4a1_gunshot.mp3")
    Cartridge=Audio("assets\GunSounds\Cartridge.mp3")
    Reloading=Audio("assets/GunSounds/reload.mp3")
            
    def reload():
        if held_keys['r']:
            gun.position=(0.1,-0.25,0.4)
            gun.rotation=(25, -70, 0)
            Reloading.play()

    def aim():
        if held_keys['right mouse']:
            gun.animate_rotation((-20, 0, 0), duration = 0.1, curve = curve.linear)
            gun.animate("z", 1.2, duration = 0.03, curve = curve.linear)
            gun.animate("z", 1.5, 0.2, delay = 0.1, curve = curve.linear)
            gun.animate_rotation((-10, 0, 0), 0.2, delay = 0.1, curve = curve.linear)
            gun.animate_rotation((0, 0, 0), 0.4, delay = 0.12, curve = curve.linear)
        else:
            gun.position=(0.25,-0.15,0.5)
            gullet.position=(0.25,-0.1,0.95)
            if held_keys['left mouse']:
                shoot()

    aim = Entity(input=aim)
def start_game():
    menu_parent.enabled = False
    sg()

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
volume_slider = Slider(0, 10, default=5, step=1, text='Volume', parent=options_menu, x=-.25)
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