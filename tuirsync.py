import textual.app
import textual.containers
import textual.widgets


class RSyncApp(textual.app.App):
    BINDINGS = [
        ("d", "dark_toggle", "Toggle Dark Mode"),
        ("m", "menu", "Toggle Menu"),
        ("q", "quit", "Quit"),
    ]

    def compose(self) -> textual.app.ComposeResult:
        yield textual.widgets.Header()
        yield textual.widgets.Footer()
        yield Trees()

    def action_dark_toggle(self) -> None:
        self.theme = (
            "textual-dark" if self.theme == "textual-light" else "textual-light"
        )

    def action_menu_toggle(self) -> None:
        self.push_screen(Menu())


class Menu(textual.screen.ModalScreen):
    def compose(self) -> textual.app.ComposeResult:
        with textual.containers.Container():
            yield textual.widgets.Label("Menu")
            yield textual.widgets.ListView(
                textual.widgets.ListItem(textual.widgets.Label("1. New Connection")),
                textual.widgets.ListItem(textual.widgets.Label("2. Load Connection")),
            )


class Trees(textual.containers.Horizontal):
    def compose(self) -> textual.app.ComposeResult:
        yield textual.widgets.DirectoryTree("./")
        yield textual.widgets.DirectoryTree("./")


if __name__ == "__main__":
    app = RSyncApp()
    app.run()
