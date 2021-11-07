from src.constants import TS


def get_abs_mouse(mouse_down, mouse_up):
    width = abs(mouse_up[0] - mouse_down[0])
    height = abs(mouse_up[1] - mouse_down[1])
    start_x = mouse_down[0] if mouse_down[0] < mouse_up[0] else mouse_up[0]
    start_y = mouse_down[1] if mouse_down[1] < mouse_up[1] else mouse_up[1]
    start = (start_x, start_y)
    end = (start_x + width, start_y + height)
    return start, end
