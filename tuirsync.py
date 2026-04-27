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
                textual.widgets.ListItem(textual.widgets.Label("0. New Connection")),
                textual.widgets.ListItem(textual.widgets.Label("1. Load Connection")),
            )

    def on_list_view_selected(self, event: textual.widgets.ListView.Selected) -> None:
        # Handle menu item selection
        if event.list_view.index == 0:
            self.app.push_screen(NewSSHScreen())


class NewSSHScreen(textual.screen.ModalScreen):
    # Screen to input SSH connection settings (url, user, pass)
    BINDINGS = [("escape,q", "dismiss", "Close New SSH Screen")]

    CSS = """
    NewSSHScreen { align: center middle; }
    NewSSHScreen > Container {
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


class LoadSSHScreen(textual.screen.ModalScreen):
    # Screen to load earlier saved SSH settings and show them in RemoteTree
    BINDINGS = [("escape,q", "dismiss", "Close Load SSH Screen")]

    CSS = """
  LoadSSHScreen { align: center middle; }
  LoadSSHScreen > Container {
      width: 50%;
      height: 75%;
  }
  """


class Trees(textual.containers.Horizontal):
    def compose(self) -> textual.app.ComposeResult:
        yield textual.widgets.DirectoryTree("./")
        yield RemoteTree()


class RemoteTree(textual.widgets.Tree):
    def compose(self) -> textual.app.ComposeResult:
        yield textual.widgets.DirectoryTree("./")


if __name__ == "__main__":
    app = RSyncApp()
    app.run()
