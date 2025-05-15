#!/usr/bin/env python3

import rclpy
from rclpy.node import Node
from turtlesim.srv import TeleportAbsolute, SetPen
from turtlesim.msg import Pose
import math, time, random, sys, argparse

class FractalDrawer(Node):
    def __init__(self, args):
        super().__init__('fractal_drawer')
        
        # Parse command line arguments
        self.depth = args.depth
        self.trunk_length = args.length
        self.angle = args.angle * (math.pi/180)
        self.color_mode = args.color
        self.rainbow = args.rainbow
        self.middle_branch = args.middle_branch
        self.delay = 0.015
        self.pose = Pose()
        self.pose_received = False
        self.timer_called = False
        
        # Create clients and subscriber
        self.teleport = self.create_client(TeleportAbsolute, 'turtle1/teleport_absolute')
        self.set_pen = self.create_client(SetPen, 'turtle1/set_pen')
        self.pose_sub = self.create_subscription(Pose, 'turtle1/pose', self.pose_callback, 10)
        
        # Wait for services
        while not all([self.teleport.wait_for_service(timeout_sec=1.0), 
                      self.set_pen.wait_for_service(timeout_sec=1.0)]):
            self.get_logger().info('Waiting for services...')
            
        # Draw fractal when ready
        self.timer = self.create_timer(1.0, self.draw_fractal)
        
        # Color schemes
        self.color_schemes = {
            'classic': [(34, 139, 34),(139, 69, 19)],
            'autumn': [(165, 42, 42), (255, 140, 0), (255, 215, 0)],
            'winter': [(70, 130, 180), (135, 206, 250), (240, 248, 255)],
            'spring': [(148, 0, 211), (75, 0, 130), (0, 255, 127)],
            'fire': [(139, 0, 0), (255, 69, 0), (255, 215, 0)]
        }
    
    def pose_callback(self, msg):
        self.pose = msg
        self.pose_received = True
    
    def change_pen(self, r, g, b, width, off=0):
        req = SetPen.Request()
        req.r, req.g, req.b, req.width, req.off = r, g, b, width, off
        self.set_pen.call_async(req)
        time.sleep(self.delay)
    
    def teleport_to(self, x, y, theta=0.0):
        req = TeleportAbsolute.Request()
        req.x, req.y, req.theta = x, y, theta
        self.teleport.call_async(req)
        time.sleep(self.delay)
    
    def draw_line(self, x1, y1, x2, y2):
        self.change_pen(0, 0, 0, 0, 1)  # Pen up
        self.teleport_to(x1, y1)
        self.change_pen(self.current_r, self.current_g, self.current_b, self.current_width, 0)
        self.teleport_to(x2, y2)
    
    def get_color(self, depth, max_depth):
        if self.rainbow:
            # Rainbow mode based on HSV conversion
            h = ((depth / max_depth) * 360 + self.branch_count * 17) % 360
            c = 0.72  # s=0.8, v=0.9 => c=0.72
            x = c * (1 - abs((h / 60) % 2 - 1))
            m = 0.09  # v-c = 0.9-0.72
            
            r, g, b = ((c, x, 0) if h < 60 else
                      (x, c, 0) if h < 120 else
                      (0, c, x) if h < 180 else
                      (0, x, c) if h < 240 else
                      (x, 0, c) if h < 300 else
                      (c, 0, x))
                
            return (int((r + m) * 255), int((g + m) * 255), int((b + m) * 255))
        
        elif self.color_mode in self.color_schemes:
            colors = self.color_schemes[self.color_mode]
            ratio = depth / max_depth
            idx = int(ratio * (len(colors) - 1))
            next_idx = min(idx + 1, len(colors) - 1)
            blend = (ratio * (len(colors) - 1)) - idx
            
            return tuple(int(colors[idx][i] * (1 - blend) + colors[next_idx][i] * blend) for i in range(3))
        else:
            return (random.randint(50, 255), random.randint(50, 255), random.randint(50, 255))
    
    def draw_branch(self, x, y, length, angle, depth, max_depth):
        if depth <= 0:
            return
        
        # Calculate endpoint and draw branch
        x2 = x + length * math.cos(angle)
        y2 = y + length * math.sin(angle)
        
        color = self.get_color(depth, max_depth)
        self.current_r, self.current_g, self.current_b = color
        self.current_width = max(int((depth / max_depth) * 6) + 1, 1)
        self.draw_line(x, y, x2, y2)
        
        self.branch_count += 1
        
        # Recursive branches
        new_length = length * 0.7
        self.draw_branch(x2, y2, new_length, angle + self.angle, depth - 1, max_depth)  # Right
        self.draw_branch(x2, y2, new_length, angle - self.angle, depth - 1, max_depth)  # Left
        
        # Middle branch with variation - controlled by middle_branch parameter
        middle_threshold = 1.0 if not self.middle_branch else 0.0
        if depth > 2 and random.random() > middle_threshold:
            middle_angle = angle + (random.random() - 0.5) * self.angle * 0.5
            self.draw_branch(x2, y2, new_length * 0.8, middle_angle, depth - 1, max_depth)
    
    def draw_fractal(self):
        if self.timer_called or not self.pose_received:
            return
        self.timer_called = True
        self.branch_count = 0
        
        # Draw trunk
        start_x, start_y = 5.5, 0.5
        end_y = start_y + self.trunk_length
        
        trunk_color = self.get_color(self.depth, self.depth)
        self.current_r, self.current_g, self.current_b = trunk_color
        self.current_width = 6
        
        self.draw_line(start_x, start_y, start_x, end_y)
        
        # Draw branches
        self.draw_branch(start_x, end_y, self.trunk_length * 0.7, math.pi/2, self.depth, self.depth)
        
        # Add decorative dots
        if self.depth >= 5 and self.rainbow:
            for _ in range(20):
                x = random.uniform(3.0, 8.0)
                y = random.uniform(5.0, 10.0)
                
                r = random.randint(200, 255)
                g = random.randint(200, 255)
                b = random.randint(200, 255)
                
                self.change_pen(0, 0, 0, 0, 1)  # Pen up
                self.teleport_to(x, y)
                self.change_pen(r, g, b, random.randint(1, 3), 0)
                self.teleport_to(x + 0.01, y + 0.01)
        
        self.get_logger().info('Colorful fractal tree completed!')

def main(args=None):
    parser = argparse.ArgumentParser(description='Draw a colorful fractal tree in turtlesim')
    parser.add_argument('--depth', type=int, default=7, help='Recursion depth (default: 7)')
    parser.add_argument('--length', type=float, default=2.0, help='Trunk length (default: 2.0)')
    parser.add_argument('--angle', type=float, default=30.0, help='Branch angle in degrees (default: 30)')
    parser.add_argument('--color', type=str, default='classic', 
                      choices=['classic', 'autumn', 'winter', 'spring', 'fire', 'random'],
                      help='Color scheme (default: classic)')
    parser.add_argument('--rainbow', action='store_true', help='Use rainbow colors')
    parser.add_argument('--middle-branch', action='store_true', help='Add middle branches for denser tree')
    
    parsed_args = parser.parse_args(args=args)
    
    rclpy.init(args=args)
    node = FractalDrawer(parsed_args)
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main(sys.argv[1:])
