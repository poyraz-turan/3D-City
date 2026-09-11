import tkinter as tk
import math
import random
import time
#if fps is low, I'm sorry I could not solve the performance issue. I even send the code to AI but it couldn't come up with a working solution.
class CityWalker3D:
    def __init__(self, root):
        self.root = root
        self.root.title("3D City Walker")
        self.root.geometry("1024x768")
        self.root.resizable(False, False)
        self.canvas = tk.Canvas(root, width=1024, height=768, bg="#87CEEB")
        root.iconbitmap(bitmap="gray50")
        self.canvas.pack()

        self.running = True

        self.player_x = 0.0
        self.player_z = -10.0
        self.player_angle = 0.0
        self.pitch = -10.0
        self.player_speed = 0.15
        self.walk_cycle = 0
        self.bob_amount = 0

        self.last_mouse_x = None
        self.last_mouse_y = None

        
        self.buildings = []
        self.trees = []
        self.street_lights = []
        self.lamp_posts = []
        self.cars = []  
        self.pedestrians = []  
        
        # Performance Settings
        self.render_distance = 80
        self.fps_counter = 0
        self.last_fps_update = time.time()

        
        self.game_time = 0
        self.time_of_day = 12 
        
        
        self.keys = {}

        
        self.generate_city()
        self.generate_traffic()
        self.generate_pedestrians()

        
        self.create_hud()

        
        self.root.bind("<KeyPress>", self.key_down)
        self.root.bind("<KeyRelease>", self.key_up)
        self.canvas.bind("<B1-Motion>", self.mouse_drag)
        self.canvas.bind("<ButtonPress-1>", self.mouse_down)
        self.canvas.bind("<Motion>", self.mouse_move)
        self.canvas.focus_set()

        # Start animation
        self.animate()

    def create_hud(self):
        """Create HUD overlay"""
        self.time_text = self.canvas.create_text(
            950, 30, 
            text="12:00 PM",
            fill="white",
            font=("Arial", 14, "bold"),
            anchor="ne"
        )
        
        self.canvas.create_text(
            20, 20,
            text="🖱️ Drag to look | WASD to walk",
            fill="white",
            font=("Arial", 12),
            anchor="nw"
        )
        
        self.canvas.create_text(
            20, 40,
            text="🏙️ Explore the city architecture",
            fill="#88ff88",
            font=("Arial", 10),
            anchor="nw"
        )
        
        self.fps_text = self.canvas.create_text(
            950, 60,
            text="FPS: 60",
            fill="#88ff88",
            font=("Arial", 10),
            anchor="ne"
        )

    def generate_city(self):
        """Generate a detailed city with fully rendered buildings"""
        block_size = 14
        road_width = 8
        total_blocks = 6  # 6x6 grid
        
        building_colors = [
            "#E8DCC8", "#D4C8B0", "#F0E4D0", "#C8BCA4", 
            "#DCD0BC", "#E0D4C0", "#D8CCB8", "#E4D8C4"
        ]
        roof_colors = [
            "#8B7B6B", "#9B8B7B", "#7B6B5B", "#AB9B8B",
            "#8A7A6A", "#9A8A7A", "#7A6A5A"
        ]
        accent_colors = [
            "#4A6FA5", "#5D8AA8", "#3B6B9A", "#6B8E9C",
            "#7B9EB3", "#4A7C9E", "#5A8AA8", "#6A9AB8"
        ]
        
        for row in range(total_blocks):
            for col in range(total_blocks):
                bx = (col - total_blocks/2) * (block_size + road_width)
                bz = row * (block_size + road_width) + 15
                
                
                height = random.uniform(8, 25)  
                width = random.uniform(block_size * 0.7, block_size * 0.95)
                depth = random.uniform(block_size * 0.7, block_size * 0.95)
                
                
                building_x = bx + random.uniform(-0.5, 0.5)
                building_z = bz + random.uniform(-0.5, 0.5)
                style = random.choice(["modern", "classic", "glass"])
                
                self.buildings.append({
                    "x": building_x,
                    "z": building_z,
                    "w": width,
                    "d": depth,
                    "h": height,
                    "color": random.choice(building_colors),
                    "roof_color": random.choice(roof_colors),
                    "accent": random.choice(accent_colors),
                    "style": style,
                    "floors": int(height / 3),
                    "has_roof": random.random() > 0.3,
                    "has_balcony": random.random() > 0.6,
                    "window_density": random.uniform(0.6, 1.0)
                })
                

                if row % 2 == 0 and col % 2 == 0:
                    self.lamp_posts.append({
                        "x": bx - block_size/2 - road_width/2,
                        "z": bz - block_size/2 - road_width/2,
                        "height": random.uniform(4, 5.5)
                    })
                
                
                if row % 3 == 0 and col % 2 == 0:
                    tree_x = bx + random.uniform(-block_size/2, block_size/2)
                    tree_z = bz - block_size/2 - road_width/2 - 2
                    self.trees.append({
                        "x": tree_x,
                        "z": tree_z,
                        "size": random.uniform(2.5, 4.5),
                        "type": random.choice(["oak", "pine", "maple"])
                    })

    def generate_traffic(self):
        """Generate very few cars for ambiance"""
        car_colors = ["#FF0000", "#0000FF", "#FFFF00", "#00FF00", "#FFA500", "#FF00FF"]
        
        for i in range(5):  
            road_z = random.randint(0, 5) * 22 + random.uniform(-3, 3)
            road_x = random.uniform(-40, 40)
            
            speed = random.uniform(0.03, 0.06)
            if random.random() > 0.5:
                speed = -speed
            
            self.cars.append({
                "x": road_x,
                "z": road_z,
                "color": random.choice(car_colors),
                "speed": speed,
                "size": random.uniform(1.8, 2.2),
                "type": random.choice(["sedan", "suv"])
            })

    def generate_pedestrians(self):
        for i in range(4): 
            z = random.randint(0, 5) * 22 + random.uniform(-6, 6)
            x = random.uniform(-35, 35)
            
            
            skip = False
            for building in self.buildings:
                if abs(x - building["x"]) < building["w"]/2 + 2:
                    if abs(z - building["z"]) < building["d"]/2 + 2:
                        skip = True
                        break
            if skip:
                continue
                
            self.pedestrians.append({
                "x": x,
                "z": z,
                "speed": random.uniform(0.01, 0.015),
                "dx": random.choice([-1, 1]) * random.uniform(0.01, 0.015),
                "dz": random.choice([-0.5, 0.5]) * random.uniform(0.01, 0.015),
                "color": random.choice(["#FF6B6B", "#4ECDC4", "#45B7D1", "#FFEAA7"]),
                "size": random.uniform(0.5, 0.7),
                "direction_change": random.randint(100, 250)
            })

    def key_down(self, event):
        key = event.keysym.lower()
        self.keys[key] = True
        if key == "escape":
            self.running = False
            self.root.quit()

    def key_up(self, event):
        self.keys[event.keysym.lower()] = False

    def mouse_down(self, event):
        self.last_mouse_x = event.x
        self.last_mouse_y = event.y

    def mouse_move(self, event):
        self.last_mouse_x = event.x
        self.last_mouse_y = event.y

    def mouse_drag(self, event):
        if self.last_mouse_x is None:
            return

        dx = event.x - self.last_mouse_x
        dy = event.y - self.last_mouse_y

        self.player_angle += dx * 0.004
        self.pitch = max(-80, min(80, self.pitch - dy * 0.4))

        self.last_mouse_x = event.x
        self.last_mouse_y = event.y

    def handle_movement(self):
        forward_x = math.sin(self.player_angle)
        forward_z = math.cos(self.player_angle)
        right_x = math.cos(self.player_angle)
        right_z = -math.sin(self.player_angle)

        dx, dz = 0, 0
        moving = False
        
        if self.keys.get("w") or self.keys.get("up"):
            dx += forward_x * self.player_speed
            dz += forward_z * self.player_speed
            moving = True
        if self.keys.get("s") or self.keys.get("down"):
            dx -= forward_x * self.player_speed
            dz -= forward_z * self.player_speed
            moving = True
        if self.keys.get("d") or self.keys.get("right"):
            dx += right_x * self.player_speed
            dz += right_z * self.player_speed
            moving = True
        if self.keys.get("a") or self.keys.get("left"):
            dx -= right_x * self.player_speed
            dz -= right_z * self.player_speed
            moving = True

        new_x = self.player_x + dx
        new_z = self.player_z + dz
        
        
        if abs(new_x) < 55 and new_z > -10 and new_z < 110:
            self.player_x = new_x
            self.player_z = new_z
        

        if moving:
            self.walk_cycle += self.player_speed * 2
            self.bob_amount = abs(math.sin(self.walk_cycle * 8)) * 0.2
        else:
            self.bob_amount *= 0.9

    def update_traffic(self):
        """Update car positions"""
        for car in self.cars:
            car["x"] += car["speed"]
            
            if car["x"] > 50:
                car["speed"] = -abs(car["speed"])
            elif car["x"] < -50:
                car["speed"] = abs(car["speed"])

    def update_pedestrians(self):
        for ped in self.pedestrians:
            ped["x"] += ped["dx"]
            ped["z"] += ped["dz"]
            
            ped["direction_change"] -= 1
            if ped["direction_change"] <= 0:
                ped["direction_change"] = random.randint(100, 250)
                ped["dx"] = random.uniform(-0.012, 0.012)
                ped["dz"] = random.uniform(-0.012, 0.012)
            
            if abs(ped["x"]) > 48:
                ped["dx"] *= -1
            if ped["z"] < 5 or ped["z"] > 105:
                ped["dz"] *= -1

    def update_time(self):
        
        self.game_time += 0.001
        self.time_of_day = (self.time_of_day + 0.001) % 24
        
        hour = int(self.time_of_day)
        minute = int((self.time_of_day - hour) * 60)
        am_pm = "AM" if hour < 12 else "PM"
        hour_display = hour if hour <= 12 else hour - 12
        if hour_display == 0:
            hour_display = 12
        
        time_str = f"{hour_display:02d}:{minute:02d} {am_pm}"
        self.canvas.itemconfig(self.time_text, text=time_str)

    def project_point(self, x, y, z):
        cos_a = math.cos(-self.player_angle)
        sin_a = math.sin(-self.player_angle)

        tx = x - self.player_x
        tz = z - self.player_z
        ty = y + self.bob_amount

        rx = tx * cos_a - tz * sin_a
        rz = tx * sin_a + tz * cos_a

        if rz < 0.1:
            return None, rz

        fov = 550
        sx = int((rx * fov) / rz) + 512
        sy = int((-ty * fov) / rz) + 384 + self.pitch
        return (sx, sy), rz

    def render_scene(self):
        self.canvas.delete("all")
        
        
        hour = self.time_of_day
        if hour < 6 or hour > 20:
            sky_color = "#0A0A2E"
            ground_color = "#1A1A2A"
        elif hour < 8:
            sky_color = "#1A2A5A"
            ground_color = "#2A2A3A"
        elif hour < 10:
            sky_color = "#4A7AC8"
            ground_color = "#3A3A4A"
        elif hour < 16:
            sky_color = "#87CEEB"
            ground_color = "#404040"
        elif hour < 18:
            sky_color = "#F4A460"
            ground_color = "#4A4A3A"
        else:
            sky_color = "#8B4513"
            ground_color = "#3A2A1A"
            
        self.canvas.create_rectangle(0, 0, 1024, 384 + self.pitch, fill=sky_color, outline="")
        self.canvas.create_rectangle(0, 384 + self.pitch, 1024, 768, fill=ground_color, outline="")
        
        
        self.draw_road_grid()
        
        
        render_objects = []
        
        for building in self.buildings:
            dist = math.hypot(building["x"] - self.player_x, building["z"] - self.player_z)
            if dist < self.render_distance:
                render_objects.append((dist, "building", building))
        
        
        for tree in self.trees:
            dist = math.hypot(tree["x"] - self.player_x, tree["z"] - self.player_z)
            if dist < 70:
                render_objects.append((dist, "tree", tree))
        
        
        for lamp in self.lamp_posts:
            dist = math.hypot(lamp["x"] - self.player_x, lamp["z"] - self.player_z)
            if dist < 60:
                render_objects.append((dist, "lamp", lamp))
        
        
        for car in self.cars:
            dist = math.hypot(car["x"] - self.player_x, car["z"] - self.player_z)
            if dist < 40:
                render_objects.append((dist, "car", car))
        
        for ped in self.pedestrians:
            dist = math.hypot(ped["x"] - self.player_x, ped["z"] - self.player_z)
            if dist < 30:
                render_objects.append((dist, "pedestrian", ped))
        
        
        render_objects.sort(key=lambda x: x[0], reverse=True)
        
        for _, obj_type, obj in render_objects:
            if obj_type == "building":
                self.draw_building_full(obj)
            elif obj_type == "tree":
                self.draw_tree(obj)
            elif obj_type == "lamp":
                self.draw_lamp_post(obj)
            elif obj_type == "car":
                self.draw_car(obj)
            elif obj_type == "pedestrian":
                self.draw_pedestrian(obj)
        
        self.fps_counter += 1
        if time.time() - self.last_fps_update > 1:
            self.canvas.itemconfig(self.fps_text, text=f"FPS: {self.fps_counter}")
            self.fps_counter = 0
            self.last_fps_update = time.time()

    def draw_road_grid(self):
        
        road_spacing = 22
        for i in range(-2, 8):
            z = i * road_spacing + 15
        
            for x in range(-55, 56, 6):
                pt1, _ = self.project_point(x, 0.1, z)
                pt2, _ = self.project_point(x + 2, 0.1, z)
                if pt1 and pt2:
                    self.canvas.create_line(pt1[0], pt1[1], pt2[0], pt2[1], 
                                          fill="#FFFF00", width=1)

    def draw_building_full(self, building):
        
        x, z, w, d, h = building["x"], building["z"], building["w"], building["d"], building["h"]
        corners = [
            (x - w/2, 0, z - d/2),  # 0: front-left-bottom
            (x + w/2, 0, z - d/2),  # 1: front-right-bottom
            (x + w/2, 0, z + d/2),  # 2: back-right-bottom
            (x - w/2, 0, z + d/2),  # 3: back-left-bottom
            (x - w/2, h, z - d/2),  # 4: front-left-top
            (x + w/2, h, z - d/2),  # 5: front-right-top
            (x + w/2, h, z + d/2),  # 6: back-right-top
            (x - w/2, h, z + d/2)   # 7: back-left-top
        ]
        
        proj = []
        for cx, cy, cz in corners:
            pt, _ = self.project_point(cx, cy, cz)
            if pt:
                proj.append(pt)
            else:
                proj.append(None)
        
        if not any(proj):
            return
        
        # Define all 6 faces: (indices, color, outline) got help by ai doing this
        faces = [
            # Front face (0,1,5,4)
            (0, 1, 5, 4, building["color"], "#444444"),
            # Right face (1,2,6,5)
            (1, 2, 6, 5, building["color"], "#444444"),
            # Back face (2,3,7,6)
            (2, 3, 7, 6, building["color"], "#444444"),
            # Left face (3,0,4,7)
            (3, 0, 4, 7, building["color"], "#444444"),
            # Roof face (4,5,6,7)
            (4, 5, 6, 7, building["roof_color"], "#555555"),
            # Bottom face (0,1,2,3) - only if visible
            (0, 1, 2, 3, building["color"], "#444444")
        ]
        
        for face in faces:
            pts = [proj[i] for i in face[:4] if proj[i] is not None]
            if len(pts) >= 3:
                flat_pts = [coord for pt in pts for coord in pt]
                self.canvas.create_polygon(flat_pts, fill=face[4], outline=face[5], width=1)
        
        
        self.draw_building_windows(building, proj)

    def draw_building_windows(self, building, proj):
        """Draw detailed windows on building faces"""
        x, z, w, d, h = building["x"], building["z"], building["w"], building["d"], building["h"]
        window_density = building.get("window_density", 0.7)
        floors = building.get("floors", int(h/3))
        
        
        is_night = self.time_of_day < 6 or self.time_of_day > 20
        
        
        for floor in range(floors):
            for wi in range(int(w / 1.5)):
                
                if random.random() > window_density:
                    continue
                    
                wx = x - w/2 + (wi + 0.5) * (w / (int(w/1.5) + 1))
                wy = 1 + (floor + 0.5) * (h / (floors + 1))
                wz = z - d/2 - 0.1
                
                lit = is_night or random.random() > 0.6
                win_color = "#FFE4A0" if lit else "#1A1A3A" if is_night else "#2A2A4A"
                
                win_w = w / 20
                win_h = h / (floors * 3)
                
                win_corners = [
                    (wx - win_w/2, wy - win_h/2, wz),
                    (wx + win_w/2, wy - win_h/2, wz),
                    (wx + win_w/2, wy + win_h/2, wz),
                    (wx - win_w/2, wy + win_h/2, wz)
                ]
                
                win_proj = []
                for cx, cy, cz in win_corners:
                    pt, _ = self.project_point(cx, cy, cz)
                    if pt:
                        win_proj.append(pt)
                
                if len(win_proj) == 4:
                    flat_pts = [coord for pt in win_proj for coord in pt]
                    if is_night and lit:
                        
                        self.canvas.create_polygon(flat_pts, fill=win_color, 
                                                  outline="#FFD700" if lit else "#444444", width=0.5)
                        
                        center_x = sum(pt[0] for pt in win_proj) / 4
                        center_y = sum(pt[1] for pt in win_proj) / 4
                        self.canvas.create_oval(
                            center_x - 8, center_y - 8,
                            center_x + 8, center_y + 8,
                            fill="#FFD700", outline="", stipple="gray50"
                        )
                    else:
                        self.canvas.create_polygon(flat_pts, fill=win_color, 
                                                  outline="#444444", width=0.5)
        
        for floor in range(floors):
            for wi in range(int(d / 1.5)):
                if random.random() > window_density:
                    continue
                    
                wx = x + w/2 + 0.1
                wy = 1 + (floor + 0.5) * (h / (floors + 1))
                wz = z - d/2 + (wi + 0.5) * (d / (int(d/1.5) + 1))
                
                lit = is_night or random.random() > 0.6
                win_color = "#FFE4A0" if lit else "#1A1A3A" if is_night else "#2A2A4A"
                
                win_w = d / 20
                win_h = h / (floors * 3)
                
                win_corners = [
                    (wx, wy - win_h/2, wz - win_w/2),
                    (wx, wy - win_h/2, wz + win_w/2),
                    (wx, wy + win_h/2, wz + win_w/2),
                    (wx, wy + win_h/2, wz - win_w/2)
                ]
                
                win_proj = []
                for cx, cy, cz in win_corners:
                    pt, _ = self.project_point(cx, cy, cz)
                    if pt:
                        win_proj.append(pt)
                
                if len(win_proj) == 4:
                    flat_pts = [coord for pt in win_proj for coord in pt]
                    self.canvas.create_polygon(flat_pts, fill=win_color, 
                                              outline="#444444", width=0.5)

    def draw_tree(self, tree):
        
        x, z, size = tree["x"], tree["z"], tree["size"]
        
        
        pt1, _ = self.project_point(x, 0, z)
        pt2, _ = self.project_point(x, size * 0.6, z)
        if pt1 and pt2:
            self.canvas.create_line(pt1[0], pt1[1], pt2[0], pt2[1], 
                                   fill="#8B6914", width=int(size*1.5))
        
        
        pt3, _ = self.project_point(x, size * 0.6, z)
        if pt3:
            colors = ["#2D8A4E", "#3A9A5E", "#1A7A3E", "#4AAA6E"]
            for i, color in enumerate(colors):
                offset_x = math.sin(i * 2.1 + self.game_time * 0.01) * size * 0.3
                offset_z = math.cos(i * 1.7 + self.game_time * 0.01) * size * 0.3
                radius = size * (1.0 - i * 0.15) * 8
                
                pt4, _ = self.project_point(x + offset_x, size * 0.6 + i * 0.3, z + offset_z)
                if pt4:
                    self.canvas.create_oval(
                        pt4[0] - radius, pt4[1] - radius,
                        pt4[0] + radius, pt4[1] + radius,
                        fill=color, outline="#1A5A2E", width=1
                    )

    def draw_lamp_post(self, lamp):
        
        x, z, height = lamp["x"], lamp["z"], lamp["height"]
        
        #Poles
        pt1, _ = self.project_point(x, 0, z)
        pt2, _ = self.project_point(x, height, z)
        if pt1 and pt2:
            self.canvas.create_line(pt1[0], pt1[1], pt2[0], pt2[1], fill="#555555", width=3)
        
        
        is_night = self.time_of_day < 6 or self.time_of_day > 20
        pt3, _ = self.project_point(x, height + 0.5, z)
        if pt3:
            # Glow effect
            glow_size = 25 if is_night else 8
            color = "#FFE4A0" if is_night else "#CCCCCC"
            self.canvas.create_oval(
                pt3[0] - glow_size, pt3[1] - glow_size,
                pt3[0] + glow_size, pt3[1] + glow_size,
                fill=color, outline=""
            )
            if is_night:
                
                self.canvas.create_oval(
                    pt3[0] - 15, pt3[1] - 15,
                    pt3[0] + 15, pt3[1] + 15,
                    fill="#FFD700", outline="", stipple="gray25"
                )
            
            self.canvas.create_oval(
                pt3[0] - 4, pt3[1] - 4,
                pt3[0] + 4, pt3[1] + 4,
                fill="#FFFF00" if is_night else "#AAAAAA", outline=""
            )

    def draw_car(self, car):
        
        x, z, size = car["x"], car["z"], car["size"]
        
        car_height = size * 0.3
        car_width = size * 0.7
        car_length = size * 1.1
        
        corners = [
            (x - car_width/2, 0.2, z - car_length/2),
            (x + car_width/2, 0.2, z - car_length/2),
            (x + car_width/2, 0.2, z + car_length/2),
            (x - car_width/2, 0.2, z + car_length/2),
            (x - car_width/2, car_height, z - car_length/2),
            (x + car_width/2, car_height, z - car_length/2),
            (x + car_width/2, car_height, z + car_length/2),
            (x - car_width/2, car_height, z + car_length/2)
        ]
        
        proj = []
        for cx, cy, cz in corners:
            pt, _ = self.project_point(cx, cy, cz)
            if pt:
                proj.append(pt)
            else:
                proj.append(None)
        
        if all(proj[:4]):
            # Car body
            faces = [
                (0, 1, 5, 4, car["color"]),
                (1, 2, 6, 5, car["color"]),
                (2, 3, 7, 6, car["color"]),
                (3, 0, 4, 7, car["color"])
            ]
            for face in faces:
                pts = [proj[i] for i in face[:4] if proj[i] is not None]
                if len(pts) == 4:
                    flat_pts = [coord for pt in pts for coord in pt]
                    self.canvas.create_polygon(flat_pts, fill=face[4], outline="#222222", width=1)
            
            # Roof
            roof_corners = [
                (x - car_width/2.5, car_height * 1.3, z - car_length/2.5),
                (x + car_width/2.5, car_height * 1.3, z - car_length/2.5),
                (x + car_width/2.5, car_height * 1.3, z + car_length/2.5),
                (x - car_width/2.5, car_height * 1.3, z + car_length/2.5)
            ]
            
            roof_proj = []
            for cx, cy, cz in roof_corners:
                pt, _ = self.project_point(cx, cy, cz)
                if pt:
                    roof_proj.append(pt)
            
            if len(roof_proj) == 4:
                flat_pts = [coord for pt in roof_proj for coord in pt]
                self.canvas.create_polygon(flat_pts, fill="#4A6A8A", outline="#333333", width=1)

    def draw_pedestrian(self, ped):
        x, z, size = ped["x"], ped["z"], ped["size"]
        
        pt1, _ = self.project_point(x, 0, z)
        pt2, _ = self.project_point(x, size * 1.5, z)
        
        if pt1 and pt2:
            self.canvas.create_oval(
                pt1[0] - size * 5, pt1[1] - size * 8,
                pt2[0] + size * 5, pt2[1] + size * 2,
                fill=ped["color"], outline="#333333"
            )
            
            pt3, _ = self.project_point(x, size * 1.8, z)
            if pt3:
                self.canvas.create_oval(
                    pt3[0] - size * 4, pt3[1] - size * 4,
                    pt3[0] + size * 4, pt3[1] + size * 4,
                    fill="#FFD4A8", outline="#CCB090"
                )
            
            leg_swing = math.sin(self.game_time * 2 + x) * 2
            self.canvas.create_line(
                pt1[0] - size * 2 + leg_swing, pt1[1],
                pt1[0] - size * 1.5 + leg_swing, pt1[1] + size * 8,
                fill="#333333", width=2
            )
            self.canvas.create_line(
                pt1[0] + size * 2 - leg_swing, pt1[1],
                pt1[0] + size * 1.5 - leg_swing, pt1[1] + size * 8,
                fill="#333333", width=2
            )

    def animate(self):
        if not self.running:
            return

        self.handle_movement()
        self.update_traffic()
        self.update_pedestrians()
        self.update_time()
        self.render_scene()

        self.root.after(16, self.animate)

if __name__ == "__main__":
    root = tk.Tk()
    app = CityWalker3D(root)
    root.mainloop()