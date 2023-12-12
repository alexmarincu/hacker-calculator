import flet as ft
import pyperclip as pc

from ExpressionEvaluator import ExpressionEvaluator
from Result import Failure, Success


def main(page: ft.Page) -> None:

    def onMaximizeButtonClick(ev: ft.ControlEvent) -> None:
        page.window_maximized = not page.window_maximized
        page.update()

    def onMinimizeButtonClick(ev: ft.ControlEvent) -> None:
        page.window_minimized = True
        page.update()

    def onCloseButtonClick(ev: ft.ControlEvent) -> None:
        page.window_close()

    def onInfoButtonClick(ev: ft.ControlEvent) -> None:
        page.launch_url('https://github.com/alexmarincu/hacker-calculator')

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
        leading=ft.WindowDragArea(
            content=ft.Container(
                padding=ft.padding.only(left=10),
                content=ft.Image(src="icon.png", scale=0.7)
            ),
        ),
        bgcolor='#202324',
        title=ft.WindowDragArea(
            expand=True,
            content=ft.Text("Hacker Calculator")
        ),
        actions=[
            ft.IconButton(
                icon=ft.icons.INFO,
                on_click=onInfoButtonClick
            ),
            ft.IconButton(
                icon=ft.icons.MINIMIZE,
                scale=0.8,
                style=ft.ButtonStyle(
                    shape={
                        ft.MaterialState.DEFAULT:
                        ft.RoundedRectangleBorder(radius=2),
                    },
                ),
                on_click=onMinimizeButtonClick
            ),
            ft.IconButton(
                icon=ft.icons.SQUARE_OUTLINED,
                scale=0.8,
                style=ft.ButtonStyle(
                    shape={
                        ft.MaterialState.DEFAULT:
                        ft.RoundedRectangleBorder(radius=2),
                    },
                ),
                on_click=onMaximizeButtonClick
            ),
            ft.IconButton(
                icon=ft.icons.CLOSE,
                scale=0.8,
                style=ft.ButtonStyle(
                    shape={
                        ft.MaterialState.DEFAULT:
                        ft.RoundedRectangleBorder(radius=2),
                    },
                ),
                on_click=onCloseButtonClick
            ),
            ft.VerticalDivider(width=10, color=ft.colors.TRANSPARENT)
        ]
    )
    page.fonts = {
        "JetBrainsMono NF":
        "fonts/JetBrainsMonoNerdFont-Regular.ttf",
    }
    page.theme = ft.Theme(font_family="JetBrainsMono NF")
    expressionTextField = ft.Ref[ft.TextField]()
    expressionTextFieldFocused = False
    resultDecimalTextButton = ft.Ref[ft.TextButton]()
    resultHexTextButton = ft.Ref[ft.TextButton]()
    resultBinaryTextButton = ft.Ref[ft.TextButton]()

    def resetInput() -> None:
        expressionTextField.current.value = ""
        expressionTextField.current.update()
        clearAllResults()
        expressionTextField.current.focus()

    def onKey(ev: ft.KeyboardEvent):
        if ev.key == "Escape":
            if (expressionTextField.current.value != "")\
                    or (not expressionTextFieldFocused):
                resetInput()
            else:
                page.window_close()
    page.on_keyboard_event = onKey

    def onResultClick(ev: ft.ControlEvent) -> None:
        pc.copy(ev.control.text)

    def clearAllResults() -> None:
        resultDecimalTextButton.current.text = "..."
        resultDecimalTextButton.current.disabled = True
        resultDecimalTextButton.current.update()
        resultHexTextButton.current.text = ""
        resultHexTextButton.current.disabled = True
        resultHexTextButton.current.update()
        resultBinaryTextButton.current.text = ""
        resultBinaryTextButton.current.disabled = True
        resultBinaryTextButton.current.update()

    def clearHexBinResults() -> None:
        resultHexTextButton.current.text = ""
        resultHexTextButton.current.disabled = True
        resultHexTextButton.current.update()
        resultBinaryTextButton.current.text = ""
        resultBinaryTextButton.current.disabled = True
        resultBinaryTextButton.current.update()

    def onExpressionChange(ev: ft.ControlEvent) -> None:
        result = ExpressionEvaluator().eval(ev.control.value)
        match result:
            case Success(value=value):
                resultDecimalTextButton.current.text = str(value)
                resultDecimalTextButton.current.disabled = False
                resultDecimalTextButton.current.update()
                if value.is_integer():
                    resultInt = int(value)
                    resultHexTextButton.current.text = str(hex(resultInt))
                    resultHexTextButton.current.disabled = False
                    resultHexTextButton.current.update()
                    resultBinaryTextButton.current.text = str(bin(resultInt))
                    resultBinaryTextButton.current.disabled = False
                    resultBinaryTextButton.current.update()
                else:
                    clearHexBinResults()
            case Failure(errorMessage=errorMessage):
                clearAllResults()

    def onExpressionFocus(ev: ft.ControlEvent) -> None:
        nonlocal expressionTextFieldFocused
        expressionTextFieldFocused = True

    def onExpressionBlur(ev: ft.ControlEvent) -> None:
        nonlocal expressionTextFieldFocused
        expressionTextFieldFocused = False

    page.add(
        ft.Container(
            expand=True,
            padding=20,
            content=ft.Column(
                controls=[
                    ft.TextField(
                        ref=expressionTextField,
                        label="Expression",
                        on_change=onExpressionChange,
                        on_focus=onExpressionFocus,
                        on_blur=onExpressionBlur
                    ),
                    ft.Column(
                        scroll=ft.ScrollMode.AUTO,
                        horizontal_alignment=ft.CrossAxisAlignment.STRETCH,
                        expand=True,
                        controls=[
                            ft.TextButton(
                                ref=resultDecimalTextButton,
                                text="...",
                                disabled=True,
                                style=ft.ButtonStyle(
                                    shape={
                                        ft.MaterialState.DEFAULT:
                                        ft.RoundedRectangleBorder(radius=2),
                                    },
                                ),
                                on_click=onResultClick
                            ),
                            ft.TextButton(
                                ref=resultHexTextButton,
                                text="",
                                disabled=True,
                                style=ft.ButtonStyle(
                                    shape={
                                        ft.MaterialState.DEFAULT:
                                        ft.RoundedRectangleBorder(radius=2),
                                    },
                                ),
                                on_click=onResultClick
                            ),
                            ft.TextButton(
                                ref=resultBinaryTextButton,
                                text="",
                                disabled=True,
                                style=ft.ButtonStyle(
                                    shape={
                                        ft.MaterialState.DEFAULT:
                                        ft.RoundedRectangleBorder(radius=2),
                                    },
                                ),
                                on_click=onResultClick
                            )
                        ]
                    ),
                    ft.Text(value="v0.2.0", size=10)
                ]
            )
        )
    )
    page.window_center()
    expressionTextField.current.focus()


if __name__ == "__main__":
    ft.app(target=main, assets_dir="assets")
