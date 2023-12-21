import flet as ft  # pyright: ignore[reportMissingTypeStubs]
from .AppLayout import AppLayout
from .AppBar import AppBar


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
        page.window_center()
        page.fonts = {
            "JetBrainsMono NF":
            "fonts/JetBrainsMonoNerdFont-Regular.ttf",
        }
        page.theme = ft.Theme(font_family="JetBrainsMono NF")
        page.on_keyboard_event = self._onKey
        page.appbar = AppBar(page)
        self.appLayout = AppLayout()
        page.add(self.appLayout)  # pyright: ignore[reportUnknownMemberType]
        self.appLayout.expressionTextField.current.focus()

    def _onKey(self, ev: ft.KeyboardEvent):
        if ev.key == "Escape":
            if ((self.appLayout.expressionTextField.current.value != "")
                    or (not self.appLayout.expressionTextFieldFocused)):
                self.appLayout.resetInput()
            else:
                self.page.window_close()
        elif ev.key == "Tab":
            self.appLayout.onTab()
