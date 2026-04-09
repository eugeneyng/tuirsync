import textual.app
import textual.containers
import textual.widgets


class RSyncApp(textual.app.App):
    BINDINGS = [
        ("escape,q", "quit", "Quit"),
        ("d", "dark_toggle", "Toggle Dark Mode"),
        ("m", "menu_toggle", "Toggle Menu"),
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
    BINDINGS = [("escape,q", "dismiss", "Close Menu")]

    CSS = """
    Menu { align: center middle; }
    Menu > Container {
        width: 50%;
        height: 75%;
    }
    """

    def action_dismiss(self) -> None:
        self.dismiss()

    def compose(self) -> textual.app.ComposeResult:
        yield textual.widgets.Header()
        yield textual.widgets.Footer()
        with textual.containers.Container():
            yield textual.widgets.Label("Menu")
            yield textual.widgets.ListView(
                textual.widgets.ListItem(
                    textual.widgets.Label("0. Settings Save Path")
                ),
                textual.widgets.ListItem(textual.widgets.Label("1. New Connection")),
                textual.widgets.ListItem(textual.widgets.Label("2. Load Connection")),
            )

    def on_list_view_selected(self, event: textual.widgets.ListView.Selected) -> None:
        # Handle menu item selection

        if event.list_view.index == 1:
            self.app.push_screen(SSHConnectionScreen())


class SSHConnectionScreen(textual.screen.ModalScreen):
    BINDINGS = [("escape,q", "dismiss", "Close SSH Connection Screen")]

    CSS = """
    SSHConnectionScreen { align: center middle; }
    SSHConnectionScreen > Container {
        width: 50%;
        height: 75%;
    }
    """

    def on_mount(self):
        self.notify("New SSH Connection...")

    def compose(self) -> textual.app.ComposeResult:
        yield textual.widgets.Header()
        yield textual.widgets.Footer()
        with textual.containers.Container():
            yield textual.widgets.Label("SSH Connection Settings")


class Trees(textual.containers.Horizontal):
    def compose(self) -> textual.app.ComposeResult:
        yield textual.widgets.DirectoryTree("./")
        yield textual.widgets.DirectoryTree("./")


class RemoteTree(textual.widgets.Tree):
    def compose(self) -> textual.app.ComposeResult:
        yield textual.widgets.DirectoryTree("./")


if __name__ == "__main__":
    app = RSyncApp()
    app.run()
