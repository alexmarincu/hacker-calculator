import flet as ft
from .AppLayout import AppLayout


class App():
    def __init__(self, page: ft.Page) -> None:
        self.page = page
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
                    on_click=self._onInfoButtonClick
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
                    on_click=self._onMinimizeButtonClick
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
                    on_click=self._onMaximizeButtonClick
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
                    on_click=self._onCloseButtonClick
                ),
                ft.VerticalDivider(width=10, color=ft.colors.TRANSPARENT)
            ]
        )
        page.fonts = {
            "JetBrainsMono NF":
            "fonts/JetBrainsMonoNerdFont-Regular.ttf",
        }
        page.theme = ft.Theme(font_family="JetBrainsMono NF")
        page.on_keyboard_event = self._onKey
        self.appLayout = AppLayout()
        page.add(self.appLayout)
        self.page.window_center()
        self.appLayout.expressionTextField.current.focus()

    def _onMaximizeButtonClick(self, _) -> None:
        self.page.window_maximized = not self.page.window_maximized
        self.page.update()

    def _onMinimizeButtonClick(self, _) -> None:
        self.page.window_minimized = True
        self.page.update()

    def _onCloseButtonClick(self, _) -> None:
        self.page.window_close()

    def _onInfoButtonClick(self, _) -> None:
        self.page.launch_url(
            'https://github.com/alexmarincu/hacker-calculator'
        )

    def _onKey(self, ev: ft.KeyboardEvent):
        if ev.key == "Escape":
            if (self.appLayout.expressionTextField.current.value != "")\
                    or (not self.appLayout.expressionTextFieldFocused):
                self.appLayout.resetInput()
            else:
                self.page.window_close()
