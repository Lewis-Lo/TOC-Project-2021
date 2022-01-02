import pygraphviz as pgv

G = pgv.AGraph(strict=False, directed=True)
G.add_node("user", shape="doublecircle", color="coral")  # initial state
G.add_node("setting_area", shape="circle")
G.add_node("setting_city", shape="circle")
G.add_node("change_city", shape="circle")
G.add_node("temperature", shape="circle")
G.add_node("raining", shape="circle")
G.add_node("air", shape="circle")

G.add_edge("user", "setting_area", label="advance[is_going_to_setting]")
G.add_edge("setting_area", "setting_city", label="go_to_city")
G.add_edge("setting_city", "change_city", label="go_to_change_city")
G.add_edge("user", "temperature", label="advance[is_going_to_temperature]")
G.add_edge("user", "raining", label="advance[is_going_to_raining]")
G.add_edge("user", "air", label="advance[is_going_to_air]")

G.add_edge("change_city", "user", label="go_back")
G.add_edge("temperature", "user", label="go_back")
G.add_edge("raining", "user", label="go_back")
G.add_edge("air", "user", label="go_back")



G.layout(prog="dot")  
G.draw("fsm.png")  