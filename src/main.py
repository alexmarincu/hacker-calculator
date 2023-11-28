import flet as ft
import pyperclip as pc
from math import *
import webbrowser

safeTokenList = [
    # math
    'e',
    'pi',
    'inf',
    'nan',
    'tau',
    'acos',
    'acosh',
    'asin',
    'asinh',
    'atan',
    'atan2',
    'atanh',
    'cbrt',
    'ceil',
    'comb',
    'copysign',
    'cos',
    'cosh',
    'degrees',
    'dist',
    'erf',
    'erfc',
    'exp',
    'exp2',
    'expm1',
    'fabs',
    'factorial',
    'floor',
    'fmod',
    'frexp',
    'fsum',
    'gamma',
    'gcd',
    'hypot',
    'isclose',
    'isinf',
    'isfinite',
    'isnan',
    'isqrt',
    'lcm',
    'ldexp',
    'lgamma',
    'log',
    'log10',
    'log1p',
    'log2',
    'modf',
    'nextafter',
    'perm',
    'pow',
    'prod',
    'radians',
    'remainder',
    'sin',
    'sinh',
    'sumprod',
    'sqrt',
    'tan',
    'tanh',
    'trunc',
]
safeTokenDict = dict(
    [(k, globals().get(k, None)) for k in safeTokenList]
)
safeTokenDict['abs'] = abs
safeTokenDict['min'] = min
safeTokenDict['max'] = max
safeTokenDict['round'] = round


def main(page: ft.Page) -> None:
    page.title = "Hacker Calculator"
    page.theme_mode = ft.ThemeMode.DARK
    page.window_min_width = 600
    page.window_min_height = 400
    page.window_width = 600
    page.window_height = 400
    page.window_always_on_top = True
    page.appbar = ft.AppBar(
        leading=ft.Container(
            content=ft.Icon(ft.icons.CALCULATE, scale=1.5),
            padding=ft.padding.only(left=20)
        ),
        color=ft.colors.PRIMARY,
        title=ft.Text("Hacker Calculator"),
        actions=[
            ft.IconButton(
                ft.icons.INFO,
                on_click=lambda e:
                webbrowser.open(
                    'https://github.com/alexmarincu/hacker-calculator'
                )
            ),
            ft.VerticalDivider(width=20, color=ft.colors.TRANSPARENT)
        ],
    )
    page.fonts = {
        "JetBrainsMono NF": "fonts/JetBrainsMonoNerdFont-Regular.ttf",
    }
    page.theme = ft.Theme(font_family="JetBrainsMono NF")
    expressionTextField = ft.Ref[ft.TextField]()
    resultDecimalTextButton = ft.Ref[ft.TextButton]()
    resultHexTextButton = ft.Ref[ft.TextButton]()
    resultBinaryTextButton = ft.Ref[ft.TextButton]()

    def on_keyboard(e: ft.KeyboardEvent):
        if e.key == "Escape":
            if expressionTextField.current.value != "":
                expressionTextField.current.value = ""
                expressionTextField.current.update()
                clearAllResults()
                expressionTextField.current.focus()
            else:
                page.window_close()
    page.on_keyboard_event = on_keyboard

    def onResultClick(e: ft.ControlEvent) -> None:
        pc.copy(e.control.text)

    def clearAllResults() -> None:
        resultDecimalTextButton.current.text = "..."
        resultHexTextButton.current.text = ""
        resultBinaryTextButton.current.text = ""
        page.update()

    def clearHexBinResults() -> None:
        resultHexTextButton.current.text = ""
        resultBinaryTextButton.current.text = ""
        page.update()

    def onExpressionChange(e: ft.ControlEvent) -> None:
        try:
            result = eval(
                e.control.value, {"__builtins__": None}, safeTokenDict
            )
            resultDecimalTextButton.current.text = str(result)
            if isinstance(result, int) or result.is_integer():
                resultInt = int(result)
                resultHexTextButton.current.text = str(hex(resultInt))
                resultBinaryTextButton.current.text = str(bin(resultInt))
                page.update()
            else:
                clearHexBinResults()
        except Exception as e:
            clearAllResults()

    page.add(
        ft.Container(
            padding=20,
            content=ft.Column(
                controls=[
                    ft.TextField(
                        ref=expressionTextField,
                        label="Expression",
                        on_change=onExpressionChange
                    ),
                    ft.TextButton(
                        ref=resultDecimalTextButton,
                        text="...",
                        on_click=onResultClick,
                        style=ft.ButtonStyle(
                            shape={
                                ft.MaterialState.DEFAULT:
                                ft.RoundedRectangleBorder(radius=2),
                            },
                        )
                    ),
                    ft.TextButton(
                        ref=resultHexTextButton,
                        text="",
                        on_click=onResultClick,
                        style=ft.ButtonStyle(
                            shape={
                                ft.MaterialState.DEFAULT:
                                ft.RoundedRectangleBorder(radius=2),
                            },
                        )
                    ),
                    ft.TextButton(
                        ref=resultBinaryTextButton,
                        text="",
                        on_click=onResultClick,
                        style=ft.ButtonStyle(
                            shape={
                                ft.MaterialState.DEFAULT:
                                ft.RoundedRectangleBorder(radius=2),
                            },
                        )
                    )
                ],
                horizontal_alignment=ft.CrossAxisAlignment.CENTER
            )
        )
    )
    expressionTextField.current.focus()


if __name__ == "__main__":
    ft.app(target=main, assets_dir="../assets")
