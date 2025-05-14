import bpy, mathutils

#initialize join_curves node group
def join_curves_node_group(base_curve):
    #selected curves
    selected_curves = bpy.context.selected_objects
    
    #create node group
    join_curves = bpy.data.node_groups.new(type = 'GeometryNodeTree', name = "JOIN_CURVES")

    join_curves.color_tag = 'NONE'
    join_curves.description = "Join multiple curves together."
    join_curves.default_group_node_width = 140
    

    join_curves.is_modifier = True

    #join_curves interface
    #Socket Geometry
    geometry_socket = join_curves.interface.new_socket(name = "Geometry", in_out='OUTPUT', socket_type = 'NodeSocketGeometry')
    geometry_socket.attribute_domain = 'POINT'
    geometry_socket.description = "Joined curves."

    #Socket Geometry
    geometry_socket_1 = join_curves.interface.new_socket(name = "Geometry", in_out='INPUT', socket_type = 'NodeSocketGeometry')
    geometry_socket_1.attribute_domain = 'POINT'
    geometry_socket_1.description = "Base curve to join curves to."

    #Socket Use Resample
    use_resample_socket = join_curves.interface.new_socket(name = "Use Resample", in_out='INPUT', socket_type = 'NodeSocketBool')
    use_resample_socket.default_value = False
    use_resample_socket.default_attribute_name = "True"
    use_resample_socket.attribute_domain = 'POINT'
    use_resample_socket.description = "Resample Curve to have matching control point counts."

    #Socket Control Points
    control_points_socket = join_curves.interface.new_socket(name = "Control Points", in_out='INPUT', socket_type = 'NodeSocketInt')
    control_points_socket.default_value = 10
    control_points_socket.min_value = 2
    control_points_socket.max_value = 100000
    control_points_socket.subtype = 'NONE'
    control_points_socket.attribute_domain = 'POINT'
    control_points_socket.description = "Point count for curves."


    #initialize join_curves nodes
    #node Group Input
    group_input = join_curves.nodes.new("NodeGroupInput")
    group_input.name = "Group Input"
    group_input.outputs[1].hide = True
    group_input.outputs[2].hide = True
    group_input.outputs[3].hide = True

    #node Group Output
    group_output = join_curves.nodes.new("NodeGroupOutput")
    group_output.name = "Group Output"
    group_output.is_active_output = True
    group_output.inputs[1].hide = True

    #node Join Geometry
    join_geometry = join_curves.nodes.new("GeometryNodeJoinGeometry")
    join_geometry.name = "Join Geometry"

    #node Resample Curve
    resample_curve = join_curves.nodes.new("GeometryNodeResampleCurve")
    resample_curve.name = "Resample Curve"
    resample_curve.keep_last_segment = True
    resample_curve.mode = 'COUNT'
    resample_curve.inputs[1].hide = True
    resample_curve.inputs[3].hide = True
    #Selection
    resample_curve.inputs[1].default_value = True

    #node Switch
    switch = join_curves.nodes.new("GeometryNodeSwitch")
    switch.name = "Switch"
    switch.input_type = 'GEOMETRY'

    #node Group Input.001
    group_input_001 = join_curves.nodes.new("NodeGroupInput")
    group_input_001.name = "Group Input.001"
    group_input_001.outputs[0].hide = True
    group_input_001.outputs[2].hide = True
    group_input_001.outputs[3].hide = True

    #node Group Input.002
    group_input_002 = join_curves.nodes.new("NodeGroupInput")
    group_input_002.name = "Group Input.002"
    group_input_002.outputs[0].hide = True
    group_input_002.outputs[1].hide = True
    group_input_002.outputs[3].hide = True



    #Set locations
    group_input.location = (-340.0, -8.632193565368652)
    group_output.location = (797.864013671875, 80.15608215332031)
    join_geometry.location = (174.24395751953125, 15.843734741210938)
    resample_curve.location = (425.7012023925781, -45.14072036743164)
    switch.location = (611.7518920898438, 80.811767578125)
    group_input_001.location = (612.7174682617188, 143.0477752685547)
    group_input_002.location = (245.43438720703125, -117.15119171142578)

    #Set dimensions
    group_input.width, group_input.height = 140.0, 100.0
    group_output.width, group_output.height = 140.0, 100.0
    join_geometry.width, join_geometry.height = 140.0, 100.0
    resample_curve.width, resample_curve.height = 140.0, 100.0
    switch.width, switch.height = 140.0, 100.0
    group_input_001.width, group_input_001.height = 140.0, 100.0
    group_input_002.width, group_input_002.height = 140.0, 100.0

    #initialize join_curves links
    #switch.Output -> group_output.Geometry
    join_curves.links.new(switch.outputs[0], group_output.inputs[0])
    #join_geometry.Geometry -> resample_curve.Curve
    join_curves.links.new(join_geometry.outputs[0], resample_curve.inputs[0])
    #resample_curve.Curve -> switch.True
    join_curves.links.new(resample_curve.outputs[0], switch.inputs[2])
    #join_geometry.Geometry -> switch.False
    join_curves.links.new(join_geometry.outputs[0], switch.inputs[1])
    #group_input_001.Use Resample -> switch.Switch
    join_curves.links.new(group_input_001.outputs[1], switch.inputs[0])
    #group_input_002.Control Points -> resample_curve.Count
    join_curves.links.new(group_input_002.outputs[2], resample_curve.inputs[2])
    #group_input.Geometry -> join_geometry.Geometry
    join_curves.links.new(group_input.outputs[0], join_geometry.inputs[0])
    
    #node Object Info for each joined curve
    ct = 1
    for curve in selected_curves:
        if curve.type == 'CURVES':
            if curve.name != base_curve.name:
                object_info = join_curves.nodes.new("GeometryNodeObjectInfo")
                object_info.name = f"Object Info_{ct}"
                object_info.transform_space = 'RELATIVE'
                object_info.inputs[0].hide = True
                object_info.inputs[1].hide = True
                object_info.outputs[0].hide = True
                object_info.outputs[1].hide = True
                object_info.outputs[2].hide = True
                object_info.outputs[3].hide = True
                object_info.inputs[0].default_value = curve
                #As Instance
                object_info.inputs[1].default_value = False
                #Location
                object_info.location = (-340.0, -ct * 100.0)
                object_info.width, object_info.height = 140.0, 100.0
                #object_info.Geometry -> join_geometry.Geometry
                join_curves.links.new(object_info.outputs[4], join_geometry.inputs[0])
                ct += 1

    return join_curves


def join_curves_to_active():
    base_curve = bpy.context.view_layer.objects.active
    join_curves = join_curves_node_group(base_curve)
    mod = base_curve.modifiers.new(name = "JOIN_CURVES", type = 'NODES')
    mod.node_group = join_curves
    return mod

