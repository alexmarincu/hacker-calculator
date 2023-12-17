import flet as ft  # pyright: ignore[reportMissingTypeStubs]
import pyperclip as pc  # pyright: ignore[reportMissingTypeStubs]
import expression_eval as ee
import utils as ut


class AppLayout(ft.Container):
    def __init__(self):
        self.expressionTextField = ft.Ref[ft.TextField]()
        self.expressionTextFieldFocused = False
        self.resultDecimalTextButton = ft.Ref[ft.TextButton]()
        self.resultHexTextButton = ft.Ref[ft.TextButton]()
        self.resultBinaryTextButton = ft.Ref[ft.TextButton]()
        super().__init__(  # pyright: ignore[reportUnknownMemberType]
            padding=20,
            expand=True,
            content=ft.Column(
                controls=[
                    ft.TextField(
                        ref=self.expressionTextField,
                        label="Expression",
                        on_change=self._onExpressionChange,
                        on_focus=self._onExpressionFocus,
                        on_blur=self._onExpressionBlur
                    ),
                    ft.Column(
                        scroll=ft.ScrollMode.AUTO,
                        horizontal_alignment=ft.CrossAxisAlignment.STRETCH,
                        expand=True,
                        controls=[
                            ft.TextButton(
                                ref=self.resultDecimalTextButton,
                                text="...",
                                disabled=True,
                                style=ft.ButtonStyle(
                                    shape={
                                        ft.MaterialState.DEFAULT:
                                        ft.RoundedRectangleBorder(radius=2),
                                    },
                                ),
                                on_click=self._onResultClick
                            ),
                            ft.TextButton(
                                ref=self.resultHexTextButton,
                                text="",
                                disabled=True,
                                style=ft.ButtonStyle(
                                    shape={
                                        ft.MaterialState.DEFAULT:
                                        ft.RoundedRectangleBorder(radius=2),
                                    },
                                ),
                                on_click=self._onResultClick
                            ),
                            ft.TextButton(
                                ref=self.resultBinaryTextButton,
                                text="",
                                disabled=True,
                                style=ft.ButtonStyle(
                                    shape={
                                        ft.MaterialState.DEFAULT:
                                        ft.RoundedRectangleBorder(radius=2),
                                    },
                                ),
                                on_click=self._onResultClick
                            )
                        ]
                    ),
                    ft.Text(value="v0.2.0", size=10)
                ]
            )
        )

    def resetInput(self) -> None:
        self.expressionTextField.current.value = ""
        self.expressionTextField.current.update()
        self._clearAllResults()
        self.expressionTextField.current.focus()

    def _onResultClick(self, ev: ft.ControlEvent) -> None:
        pc.copy(ev.control.text)  # pyright: ignore[reportUnknownMemberType, reportUnknownArgumentType]

    def _clearAllResults(self) -> None:
        self.resultDecimalTextButton.current.text = "..."
        self.resultDecimalTextButton.current.disabled = True
        self.resultDecimalTextButton.current.update()
        self.resultHexTextButton.current.text = ""
        self.resultHexTextButton.current.disabled = True
        self.resultHexTextButton.current.update()
        self.resultBinaryTextButton.current.text = ""
        self.resultBinaryTextButton.current.disabled = True
        self.resultBinaryTextButton.current.update()

    def _clearHexBinResults(self) -> None:
        self.resultHexTextButton.current.text = ""
        self.resultHexTextButton.current.disabled = True
        self.resultHexTextButton.current.update()
        self.resultBinaryTextButton.current.text = ""
        self.resultBinaryTextButton.current.disabled = True
        self.resultBinaryTextButton.current.update()

    def _onExpressionChange(self, ev: ft.ControlEvent) -> None:
        result: ut.Result[float] = (
            ee.ExpressionEvaluator().eval(ev.control.value)  # pyright: ignore[reportUnknownMemberType, reportUnknownArgumentType]
        )
        if (isinstance(result, ut.Success)):
            self.resultDecimalTextButton.current.text = str(result.value)
            self.resultDecimalTextButton.current.disabled = False
            self.resultDecimalTextButton.current.update()
            if result.value.is_integer():
                resultInt = int(result.value)
                self.resultHexTextButton.current.text = str(hex(resultInt))
                self.resultHexTextButton.current.disabled = False
                self.resultHexTextButton.current.update()
                self.resultBinaryTextButton.current.text = str(bin(resultInt))
                self.resultBinaryTextButton.current.disabled = False
                self.resultBinaryTextButton.current.update()
            else:
                self._clearHexBinResults()
        elif (isinstance(result, ut.Failure)):
            self._clearAllResults()

    def _onExpressionFocus(self, _: ft.ControlEvent) -> None:
        self.expressionTextFieldFocused = True

    def _onExpressionBlur(self, _: ft.ControlEvent) -> None:
        self.expressionTextFieldFocused = False
