from ursina import *
from ursina.prefabs.first_person_controller import FirstPersonController
from ursina.shaders import lit_with_shadows_shader

app = Ursina()
window.fullscreen_resolution = (1920, 1080)
window.fullscreen = True

random.seed(0)
Entity.default_shader = lit_with_shadows_shader
sun = DirectionalLight()
sun.look_at(Vec3(1,-1,-1))
Sky()

class FirstPersonController(Entity):
    def __init__(self, **kwargs):
        super().__init__()
        self.speed = 5
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
        self.on_destroy = self.on_disable

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


    def on_enable(self):
        mouse.locked = True
        self.cursor.enabled = True


    def on_disable(self):
        mouse.locked = False
        self.cursor.enabled = False

if __name__ == '__main__':
    from ursina.prefabs.first_person_controller import FirstPersonController
    window.vsync = False
    app = Ursina()
    
    ground = Entity(model='plane', scale=(100,1,100), color=color.green, texture='grass', texture_scale=(100,100), collider='box')
    e = Entity(model='cube', scale=(1,5,10), x=2, y=.01, rotation_y=45, collider='box', texture='white_cube')
    e.texture_scale = (e.scale_z, e.scale_y)
    e = Entity(model='cube', scale=(1,5,10), x=-2, y=.01, collider='box', texture='white_cube')
    e.texture_scale = (e.scale_z, e.scale_y)

    player = FirstPersonController(y=2, origin_y=-.5)
    player.gun = None

    gun = Entity(model='assets\Models_Gun\M4A1.fbx', parent=camera, color=color.black, rotation_y=270, position=(0.5,-0.5,0.5), scale=0.005, on_cooldown=False)
    gullet = Entity(model='cube',parent=camera,position=(0.505,-0.18,2.3),scale=0.05,rotation_y=270,color=color.black)
    gun.muzzle_flash = Entity(parent=gun, z=1, world_scale=.5, model='quad', color=color.yellow, enabled=False)

    slope = Entity(model='cube', collider='box', position=(0,0,8), scale=6, rotation=(45,0,0), texture='brick', texture_scale=(8,8))
    slope = Entity(model='cube', collider='box', position=(5,0,10), scale=6, rotation=(80,0,0), texture='brick', texture_scale=(8,8))

    hookshot_target = Button(parent=scene, model='cube', color=color.brown, position=(4,5,5))
    hookshot_target.on_click = Func(player.animate_position, hookshot_target.position, duration=.5, curve=curve.linear)
    

    shootables_parent = Entity()
    mouse.traverse_target = shootables_parent
    

    def shoot():

        bullet = Entity(parent=gullet, model='cube', scale=(0.75,0.75,2),rotation_y=90, color=color.black)
        bullet.world_parent = scene
        bullet.animate_position(bullet.position+(bullet.forward*500), curve=curve.linear, duration=1)
        destroy(bullet, delay=1)
    
    class Enemy(Entity):
        def __init__(self, **kwargs):
            super().__init__(parent=shootables_parent, model='cube', scale_y=2, origin_y=-.5, color=color.light_gray, collider='box', **kwargs)
            self.max_hp = 100
            self.hp = self.max_hp

        @property
        def hp(self):
            return self._hp

        @hp.setter
        def hp(self, value):
            self._hp = value
            if value <= 0:
                destroy(self)
                return
    
    enemies = [Enemy(x=x*4) for x in range(4)]
    
    def aim(key):
        if held_keys['right mouse']:
            gun.position=(0,-0.535,0.5)
            gullet.position=(0,-0.215,2.3)
            if held_keys['left mouse']:
                shoot()
        else:
            gun.position=(0.5,-0.5,0.5)
            gullet.position=(0.505,-0.18,2.3)
            if held_keys['left mouse']:
                shoot()

    aim = Entity(input=aim)

    app.run()