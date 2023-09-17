import imgui
import glm

LEFT_COL_W = 150
INT_SPEED = 1
FLOAT_SPEED = 0.05
MIN_VALUE = 0
MAX_VALUE = 100


class Tracker:
    stolenPopup = False


def leftCol(label: str):
    imgui.columns(2)
    imgui.set_column_width(0, LEFT_COL_W)
    imgui.text(f"{label}:")
    imgui.next_column()
    imgui.push_item_width(int(imgui.get_column_width(1)*0.9))


def columnsEnd():
    imgui.columns(1)
    imgui.pop_item_width()


def inputFloat(label: str, value: float) -> tuple[bool, float]:
    leftCol(label)
    changed, val = imgui.input_float(f"##{label}:inputFloat", value)
    columnsEnd()
    return changed, val


def dragFloat(label: str, value: float, speed: float = FLOAT_SPEED) -> tuple[bool, float]:
    leftCol(label)
    changed, val = imgui.drag_float(f"##{label}:dragFloat", value, speed)
    columnsEnd()
    return changed, val


def sliderFloat(label: str, value: float, min: float = MIN_VALUE, max: float = MAX_VALUE) -> tuple[bool, float]:
    leftCol(label)
    changed, val = imgui.slider_float(
        f"##{label}:sliderFloat", value, min, max)
    columnsEnd()
    return changed, val


def dragVec2(label: str, vec: glm.vec2, speed: float = FLOAT_SPEED) -> tuple[bool, glm.vec2]:
    leftCol(label)
    changed, values = imgui.drag_float2(
        f"##{label}:dragVec2", vec.x, vec.y, speed)
    columnsEnd()
    if changed:
        return changed, glm.vec2(values[0], values[1])
    return changed, vec


def dragVec3(label: str, vec: glm.vec3, speed: float = FLOAT_SPEED) -> tuple[bool, glm.vec3]:
    leftCol(label)
    changed, values = imgui.drag_float3(
        f"##{label}:dragVec3", vec.x, vec.y, vec.z, speed)
    columnsEnd()
    if changed:
        return changed, glm.vec3(values[0], values[1], values[2])
    return changed, vec


def dragVec4(label: str, vec: glm.vec4, speed: float = FLOAT_SPEED) -> tuple[bool, glm.vec4]:
    leftCol(label)
    changed, values = imgui.drag_float4(
        f"##{label}:dragVec3", vec.x, vec.y, vec.z, vec.w, speed)
    columnsEnd()
    if changed:
        return changed, glm.vec4(values[0], values[1], values[2], values[3])
    return changed, vec


def iterable(label: str, iterableObj: list | tuple, intSpeed: int = INT_SPEED, floatSpeed: int = FLOAT_SPEED) -> list:
    leftCol(label)
    imgui.push_item_width(int(imgui.get_column_width()*0.8))
    iterable = list(iterableObj)
    if imgui.collapsing_header(f"[{len(iterable)} Items]")[0]:
        for i in range(len(iterable)):
            value = iterable[i]
            match value:
                case bool():
                    _, iterable[i] = imgui.checkbox(
                        f"##{label}:{i}:checkbox", value)
                case int():
                    _, iterable[i] = imgui.drag_int(
                        f"##{label}:{i}:dragInt", value, intSpeed)
                case float():
                    _, iterable[i] = imgui.drag_float(
                        f"##{label}:{i}:dragFloat", value, floatSpeed)
                case str():
                    _, iterable[i] = imgui.input_text(
                        f"##{label}:{i}:inputText", value)
                case glm.vec2():
                    changed, values = imgui.drag_float2(
                        f"##{label}:{i}:dragVec2", value.x, value.y, floatSpeed)
                    if changed:
                        iterable[i] = glm.vec2(*values)
                case glm.vec3():
                    changed, values = imgui.drag_float3(
                        f"##{label}:{i}dragVec3", value.x, value.y, value.z, floatSpeed)
                    if changed:
                        iterable[i] = glm.vec3(*values)
                case glm.vec4():
                    changed, values = imgui.drag_float4(
                        f"##{label}:{i}:dragVec3", value.x, value.y, value.z, value.w, floatSpeed)
                    if changed:
                        iterable[i] = glm.vec4(*values)
            imgui.same_line()
            imgui.push_id(f"{label}-{i}-XButton")
            if imgui.button("X"):
                iterable.pop(i)
                i -= 1
            imgui.pop_id()
        if imgui.begin_popup_context_window(f"Add Item"):
            Tracker.stolenPopup = True
            if imgui.menu_item("Add Int")[0]:
                iterable.append(0)
            elif imgui.menu_item("Add Float")[0]:
                iterable.append(0.0)
            elif imgui.menu_item("Add String")[0]:
                iterable.append("")
            elif imgui.menu_item("Add Bool")[0]:
                iterable.append(False)
            elif imgui.menu_item("Add Vec2")[0]:
                iterable.append(glm.vec2())
            elif imgui.menu_item("Add Vec3")[0]:
                iterable.append(glm.vec3())
            elif imgui.menu_item("Add Vec4")[0]:
                iterable.append(glm.vec4())
            imgui.end_popup()
    imgui.pop_item_width()
    columnsEnd()
    return iterable


def enumDropdown(label: str, options: list[str], selected: str) -> tuple[bool, str]:
    leftCol(label)
    changed, index = imgui.combo(
        f"##{label}:enumDropdown", options.index(selected), options)
    columnsEnd()
    return changed, options[index]


def inputInt(label: str, value: int) -> tuple[bool, int]:
    leftCol(label)
    changed, val = imgui.input_int(f"##{label}:inputInt", value)
    columnsEnd()
    return changed, val


def dragInt(label: str, value: int, speed: int = INT_SPEED) -> tuple[bool, int]:
    leftCol(label)
    changed, val = imgui.drag_int(f"##{label}:dragInt", value, speed)
    columnsEnd()
    return changed, val


def sliderInt(label: str, value: int, min: int = MIN_VALUE, max: int = MAX_VALUE) -> tuple[bool, int]:
    leftCol(label)
    changed, val = imgui.slider_int(f"##{label}:sliderInt", value, min, max)
    columnsEnd()
    return changed, val


def colorEdit4(label: str, color: glm.vec4) -> tuple[bool, glm.vec4]:
    leftCol(label)
    changed, col = imgui.color_edit4(
        f"##{label}:colorEdit4", color.x, color.y, color.z, color.w)
    columnsEnd()
    if changed:
        return changed, glm.vec4(*col)
    return changed, color


def inputText(label: str, text: str) -> tuple[bool, str]:
    leftCol(label)
    changed, txt = imgui.input_text(f"##{label}:inputText", text)
    columnsEnd()
    return changed, txt


def checkbox(label: str, value: bool) -> tuple[bool, bool]:
    leftCol(label)
    changed, val = imgui.checkbox(f"##{label}:checkbox", value)
    columnsEnd()
    return changed, val
