import sys
import os
import flet as ft
import pyperclip as pc
from math import *
import webbrowser


def main(page: ft.Page) -> None:
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

    def assetsPath(relativePath) -> str:
        return os.path.join(
            getattr(sys, '_MEIPASS', os.path.abspath('assets')), relativePath
        )

    page.title = "Hacker Calculator"
    page.theme_mode = ft.ThemeMode.DARK
    page.window_min_width = 600
    page.window_min_height = 400
    page.window_width = 600
    page.window_height = 400
    page.window_always_on_top = True
    page.window_title_bar_hidden = True
    page.window_title_bar_buttons_hidden = True
    page.appbar = ft.AppBar(
        leading=ft.Container(
            content=ft.Image(src=assetsPath("icon.png")),
            padding=ft.padding.only(left=20)
        ),
        bgcolor='#202324',
        title=ft.WindowDragArea(
            content=ft.Text("Hacker Calculator"), expand=True
        ),
        actions=[
            ft.IconButton(
                ft.icons.INFO,
                on_click=lambda e:
                webbrowser.open(
                    'https://github.com/alexmarincu/hacker-calculator'
                )
            ),
            ft.IconButton(
                ft.icons.CLOSE,
                on_click=lambda _: page.window_close()
            ),
            ft.VerticalDivider(width=15, color=ft.colors.TRANSPARENT),

        ],
    )
    page.fonts = {
        "JetBrainsMono NF":
        assetsPath("fonts/JetBrainsMonoNerdFont-Regular.ttf"),
    }
    page.theme = ft.Theme(font_family="JetBrainsMono NF")
    expressionTextField = ft.Ref[ft.TextField]()
    resultDecimalTextButton = ft.Ref[ft.TextButton]()
    resultHexTextButton = ft.Ref[ft.TextButton]()
    resultBinaryTextButton = ft.Ref[ft.TextButton]()

    def onKey(ev: ft.KeyboardEvent):
        if ev.key == "Escape":
            if expressionTextField.current.value != "":
                expressionTextField.current.value = ""
                expressionTextField.current.update()
                clearAllResults()
                expressionTextField.current.focus()
            else:
                page.window_close()
    page.on_keyboard_event = onKey

    def onResultClick(ev: ft.ControlEvent) -> None:
        pc.copy(ev.control.text)

    def clearAllResults() -> None:
        resultDecimalTextButton.current.text = "..."
        resultHexTextButton.current.text = ""
        resultBinaryTextButton.current.text = ""
        page.update()

    def clearHexBinResults() -> None:
        resultHexTextButton.current.text = ""
        resultBinaryTextButton.current.text = ""
        page.update()

    def onExpressionChange(ev: ft.ControlEvent) -> None:
        try:
            result = eval(
                ev.control.value, {"__builtins__": None}, safeTokenDict
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
    page.window_center()
    expressionTextField.current.focus()


if __name__ == "__main__":
    ft.app(target=main)
