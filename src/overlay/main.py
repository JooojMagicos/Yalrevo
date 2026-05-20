import sys
import os


sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", ".."))
from src.overlay.data.mock import MockDataSource
import dearpygui.dearpygui as dpg

def main():
    
    source = MockDataSource()
    source.connect()

    dpg.create_context()
    dpg.create_viewport(title='Overlay', width=400, height=300)
    dpg.setup_dearpygui()

    with dpg.window(label="Telemetry", width=400, height=300):

        speed_text = dpg.add_text("Speed: --")
        gear_text = dpg.add_text("Gear: --")
        rpm_text = dpg.add_text("RPM: --")

    
    def update_overlay():
        data = source.read_data()
        dpg.set_value(speed_text, f"Speed: {data['speed_kmh']}")
        dpg.set_value(gear_text, f"Gear: {data['gear']}")
        dpg.set_value(rpm_text, f"RPM: {data['rpm']}")

    dpg.set_frame_callback(1, update_overlay)
    dpg.show_viewport()

    while dpg.is_dearpygui_running():
        update_overlay()
        dpg.render_dearpygui_frame()

    source.disconnect()
    dpg.destroy_context()

if __name__ == "__main__":
    main()