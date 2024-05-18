import math

urdf = '<?xml version="1.0"?> <robot name="Sk8t3rBot">'

BODY_HEIGHT = 0.5
BODY_WIDTH = 0.5
BODY_DEPTH = 0.15
BODY_MASS = 50

UPPER_LEG_HEIGHT = 0.2
UPPER_LEG_WIDTH = 0.2
UPPER_LEG_DEPTH = 0.15
UPPER_LEG_MASS = 10

LOWER_LEG_HEIGHT = 0.2
LOWER_LEG_WIDTH = 0.2
LOWER_LEG_DEPTH = 0.15
LOWER_LEG_MASS = 10

BLADE_HEIGHT = 0.05
BLADE_WIDTH = 0.01
BLADE_LENGTH = 0.4
BLADE_MASS = 2



dummy = ""

def add_box_inertia(mass, lx, ly, lz):
    ixx = 1/12 * mass * (ly**2 + lz**2)
    iyy = 1/12 * mass * (lx**2 + lz**2)
    izz = 1/12 * mass * (lx**2 + ly**2)
    
    return f'<inertia ixx="{ixx}"  ixy="0"  ixz="0" iyy="{iyy}" iyz="0" izz="{izz}" />'

def add_mass(mass):
    return f'<mass value="{mass}" />'
    

def add_color(r, g, b):
    return f'<material> <color rgba="{r} {g} {b} 1" /></material>'
    
def add_box_geometry(lx, ly, lz):
    return f'<geometry> <box size="{lx} {ly} {lz}" /> </geometry>'



urdf += f'<link name="rink"> \
    <origin xyz="0 0 0" />\
\
    <visual>\
        <geometry>\
            <box size="100 100 0.0001" />\
        </geometry>\
        <material>\
            <color rgba="0.86 0.945 0.98 1" />\
        </material>\
    </visual>\
</link>\
<joint name="rink_world" type="fixed">\
    <parent link="world" />\
    <child link="rink" />\
</joint>'






body = ""
body += '<link name="body">';
body += f'<inertial> \
    <origin xyz="0 0 {(BODY_HEIGHT)/2}" /> \
    {add_mass(BODY_MASS)} \
    {add_box_inertia(BODY_MASS, BODY_WIDTH, BODY_DEPTH, BODY_HEIGHT)} </inertial>'
body_collision = f'<origin xyz="0 0 {BODY_HEIGHT/2}" /> {add_box_geometry(BODY_WIDTH, BODY_DEPTH, BODY_HEIGHT)}'
body += f'<visual> <origin xyz="0 0 {(BODY_HEIGHT)/2}" /> {body_collision} {add_color(0,1,0)} </visual>';
#body += f'<collision> {body_collision} </collision>';
body += "</link>"
urdf += body





urdf += f'<link name="inner_hip" /> \
<joint name="inner_hip_joint" type="continuous"> \
    <origin xyz="0 0 0" /> \
    <parent link="inner_hip" /> \
    <child link="body" /> \
    <axis xyz="0 0 1" /> \
</joint> \
<transmission> \
    <joint name="inner_hip_joint" /> \
    <actuator name="inner_hip_act" /> \
    <type>transmission_interface/SimpleTransmission</type> \
</transmission>'

urdf += f'<link name="hip" /> \
<joint name="hip_joint" type="continuous"> \
    <origin xyz="0 0 0" /> \
    <parent link="hip" /> \
    <child link="inner_hip" /> \
    <axis xyz="0 1 0" /> \
</joint> \
<transmission> \
    <joint name="hip_joint" /> \
    <actuator name="hip_act" /> \
    <type>transmission_interface/SimpleTransmission</type> \
</transmission>'



# hip joint, moves leg outwards in right direction
urdf += f'<link name="upper_leg"> \
    <inertial> \
        <origin xyz="0 0 {UPPER_LEG_HEIGHT/2}" /> \
        {add_mass(UPPER_LEG_MASS)} \
        {add_box_inertia(UPPER_LEG_MASS, UPPER_LEG_WIDTH, UPPER_LEG_DEPTH, UPPER_LEG_HEIGHT)} \
    </inertial> \
    <visual> \
        <origin xyz="0 0 {UPPER_LEG_HEIGHT/2}" /> \
        {add_box_geometry(UPPER_LEG_WIDTH, UPPER_LEG_DEPTH, UPPER_LEG_HEIGHT)} \
        {add_color(1,0,0)} \
    </visual> \
</link> \
<joint name="phi" type="continuous"> \
    <origin xyz="0 0 {UPPER_LEG_HEIGHT}" /> \
    <parent link="upper_leg" /> \
    <child link="hip" /> \
    <axis xyz="1 0 0" /> \
</joint> \
<transmission> \
    <joint name="phi" /> \
    <actuator name="phi_act" /> \
    <type>transmission_interface/SimpleTransmission</type> \
</transmission>'


# knee joint
urdf += f'<link name="lower_leg"> \
    <inertial> \
        <origin xyz="0 0 {LOWER_LEG_HEIGHT/2}" /> \
        {add_mass(LOWER_LEG_MASS)} \
        {add_box_inertia(LOWER_LEG_MASS, LOWER_LEG_WIDTH, LOWER_LEG_DEPTH, LOWER_LEG_HEIGHT)} \
    </inertial> \
    <visual> \
        <origin xyz="0 0 {LOWER_LEG_HEIGHT/2}" /> \
        {add_box_geometry(LOWER_LEG_WIDTH, LOWER_LEG_DEPTH, LOWER_LEG_HEIGHT)} \
        {add_color(0,0,1)} \
    </visual> \
</link> \
<joint name="knee" type="continuous"> \
    <origin xyz="0 0 {LOWER_LEG_HEIGHT}" /> \
    <parent link="lower_leg" /> \
    <child link="upper_leg" /> \
    <axis xyz="1 0 0" /> \
</joint> \
<transmission> \
    <joint name="knee" /> \
    <actuator name="knee_act" /> \
    <type>transmission_interface/SimpleTransmission</type> \
</transmission>'

"""
<visual> \
        <origin xyz="0 {BLADE_LENGTH/2 - BLADE_HEIGHT/2} {BLADE_HEIGHT/2}" rpy="0 {math.pi/2} 0" /> \
        <geometry> \
            <cylinder length="{BLADE_WIDTH}" radius="{BLADE_HEIGHT/2}" /> \
        </geometry> \
    </visual> \
    <visual> \
        <origin xyz="0 -{BLADE_LENGTH/2 - BLADE_HEIGHT/2} {BLADE_HEIGHT/2}" rpy="0 {math.pi/2} 0" /> \
        <geometry> \
            <cylinder length="{BLADE_WIDTH}" radius="{BLADE_HEIGHT/2}" /> \
        </geometry> \
    </visual> \
"""

# blade joint
urdf += f'<link name="blade"> \
    <inertial> \
        {add_mass(BLADE_MASS)}, \
        {add_box_inertia(BLADE_MASS, BLADE_WIDTH, BLADE_LENGTH, BLADE_HEIGHT)}, \
    </inertial> \
    <visual> \
        <origin xyz="0 0 {BLADE_HEIGHT/2}" /> \
        {add_box_geometry(BLADE_WIDTH, BLADE_LENGTH, BLADE_HEIGHT)} \
    </visual> \
</link> \
<joint name="ankle" type="continuous"> \
    <origin xyz="0 0 {BLADE_HEIGHT}" /> \
    <parent link="blade" /> \
    <child link="lower_leg" /> \
</joint> \
<transmission> \
    <joint name="ankle" /> \
    <actuator name="ankle_act" /> \
    <type>transmission_interface/SimpleTransmission</type> \
</transmission>'
urdf += "</robot></xml>"

print(urdf)