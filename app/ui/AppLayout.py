import flet as ft  # pyright: ignore[reportMissingTypeStubs]
import pyperclip as pc  # pyright: ignore[reportMissingTypeStubs]
import expression_eval as ee
import utils as ut
import re


class AppLayout(ft.Container):
    def __init__(self):
        self.expressionTextField = ft.Ref[ft.TextField]()
        self.expressionTextFieldFocused = False
        self.resultDecimalTextButton = ft.Ref[ft.TextButton]()
        self.resultHexTextButton = ft.Ref[ft.TextButton]()
        self.resultBinaryTextButton = ft.Ref[ft.TextButton]()
        self.tokenListView = ft.Ref[ft.ListView]()
        self.tokenSuggestionsContainer = ft.Ref[ft.Container]()
        super().__init__(  # pyright: ignore[reportUnknownMemberType]
            padding=20,
            expand=True,
            content=ft.Stack(
                controls=[
                    ft.Column(
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
                    ),
                    ft.Column(
                        controls=[
                            ft.Divider(height=65, color=ft.colors.TRANSPARENT),
                            ft.Container(
                                ref=self.tokenSuggestionsContainer,
                                bgcolor='#202324',
                                border_radius=3,
                                padding=10,
                                visible=False,
                                content=ft.ListView(
                                    ref=self.tokenListView,
                                    width=200,
                                    height=200,
                                    spacing=0
                                )
                            )
                        ]
                    )
                ]
            )
        )

    def resetInput(self) -> None:
        self.expressionTextField.current.value = ""
        self.expressionTextField.current.update()
        self.expressionTextField.current.focus()
        self._clearAllResults()
        self.tokenSuggestionsContainer.current.visible = False
        self.tokenSuggestionsContainer.current.update()

    def _onTokenClick(self, ev: ft.ControlEvent) -> None:
        token = str(ev.control.content.value)  # pyright: ignore[reportUnknownMemberType, reportUnknownArgumentType]
        expression = str(self.expressionTextField.current.value)
        last_index = expression.rfind(self.lastWord)
        newExpression = expression[:last_index]
        self.expressionTextField.current.value = (
            f"{newExpression}{token}"
        )
        self.expressionTextField.current.update()
        self.expressionTextField.current.focus()
        self.tokenSuggestionsContainer.current.visible = False
        self.tokenSuggestionsContainer.current.update()

    def onTab(self) -> None:
        if (self.expressionTextFieldFocused
                and self.tokenSuggestionsContainer.current.visible):
            assert isinstance(
                self.tokenListView.current.controls[0], ft.Container
            )
            assert isinstance(
                self.tokenListView.current.controls[0].content, ft.Text
            )
            token = str(self.tokenListView.current.controls[0].content.value)
            expression = str(self.expressionTextField.current.value)
            last_index = expression.rfind(self.lastWord)
            newExpression = expression[:last_index]
            self.expressionTextField.current.value = (
                f"{newExpression}{token}"
            )
            self.expressionTextField.current.update()
            self.expressionTextField.current.focus()
            self.tokenSuggestionsContainer.current.visible = False
            self.tokenSuggestionsContainer.current.update()

    def _onTokenHover(self, ev: ft.ControlEvent) -> None:
        assert isinstance(ev.control, ft.Container)  # pyright: ignore[reportUnknownMemberType]
        container = ev.control
        container.bgcolor = (
            ft.colors.ON_INVERSE_SURFACE if ev.data == "true" else None
        )
        container.update()

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
        expression = str(ev.control.value)  # pyright: ignore[reportUnknownMemberType, reportUnknownArgumentType]
        words = re.findall(r'[0-9a-zA-Z]+$', expression)
        self.lastWord: str = "."
        if words:
            self.lastWord = words[-1]
        tokens = ee.ExpressionEvaluator.getFilteredTokens(self.lastWord)
        if (tokens):
            self.tokenSuggestionsContainer.current.visible = True
        else:
            self.tokenSuggestionsContainer.current.visible = False
        self.tokenSuggestionsContainer.current.update()
        self.tokenListView.current.controls = [
            ft.Container(
                on_click=self._onTokenClick,
                on_hover=self._onTokenHover,
                padding=5,
                border_radius=2,
                content=ft.Text(value=token)
            )
            for token in tokens
        ]
        self.tokenListView.current.update()
        result: ut.Result[float] = ee.ExpressionEvaluator().eval(expression)
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
