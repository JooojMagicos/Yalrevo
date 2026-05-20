import sys
import os
import time
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", ".."))
from src.overlay.data.mock import MockDataSource
import dearpygui.dearpygui as dpg
from src.overlay.window import make_overlay

def main():
    
    source = MockDataSource()
    source.connect()

    dpg.create_context()
    dpg.create_viewport(title='Overlay', width=400, height=300, decorated=False, clear_color=[0, 0, 0, 0], always_on_top=True)
    dpg.setup_dearpygui()
    

    with dpg.theme() as widget_theme:
        with dpg.theme_component(dpg.mvWindowAppItem):
            dpg.add_theme_color(dpg.mvThemeCol_WindowBg, (12, 17, 28, 255))

    with dpg.window(label="Telemetry", width=400, height=300, no_title_bar=True):

        speed_text = dpg.add_text("Speed: --")
        gear_text = dpg.add_text("Gear: --")
        rpm_text = dpg.add_text("RPM: --")

    dpg.bind_item_theme(dpg.last_item(), widget_theme)

    
    def update_overlay():
        data = source.read_data()
        dpg.set_value(speed_text, f"Speed: {data['speed_kmh']}")
        dpg.set_value(gear_text, f"Gear: {data['gear']}")
        dpg.set_value(rpm_text, f"RPM: {data['rpm']}")

    dpg.set_frame_callback(1, update_overlay)
    dpg.show_viewport()
    time.sleep(1)  
    make_overlay('Overlay')


    while dpg.is_dearpygui_running():
        update_overlay()
        dpg.render_dearpygui_frame()

    source.disconnect()
    dpg.destroy_context()

if __name__ == "__main__":
    main()