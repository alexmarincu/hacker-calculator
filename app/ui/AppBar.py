import flet as ft  # pyright: ignore[reportMissingTypeStubs]


class AppBar(ft.AppBar):
    def __init__(self, page: ft.Page):
        self._page: ft.Page = page
        super().__init__(  # pyright: ignore[reportUnknownMemberType]
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

    def _onMaximizeButtonClick(self, _: ft.ControlEvent) -> None:
        self._page.window_maximized = not self._page.window_maximized
        self._page.update()  # pyright: ignore[reportUnknownMemberType]

    def _onMinimizeButtonClick(self, _: ft.ControlEvent) -> None:
        self._page.window_minimized = True
        self._page.update()  # pyright: ignore[reportUnknownMemberType]

    def _onCloseButtonClick(self, _: ft.ControlEvent) -> None:
        self._page.window_close()

    def _onInfoButtonClick(self, _: ft.ControlEvent) -> None:
        self._page.launch_url(
            'https://github.com/alexmarincu/hacker-calculator'
        )
