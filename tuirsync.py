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
        if event.list_view.index == 1:
            self.app.push_screen(LoadSSHScreen())


class NewSSHScreen(textual.screen.ModalScreen):
    # Screen to input SSH connection settings (host, user, pass)
    BINDINGS = [("escape,q", "dismiss", "Close New SSH Screen")]

    CSS = """
    NewSSHScreen { align: center middle; }
    NewSSHScreen > Container {
        width: 50%;
        height: 75%;
    }
    """

    def action_dismiss(self) -> None:
        self.dismiss()

    def on_mount(self):
        self.notify("New SSH Connection...")

    def compose(self) -> textual.app.ComposeResult:
        yield textual.widgets.Header()
        yield textual.widgets.Footer()
        with textual.containers.Container():
            yield textual.widgets.Label("SSH Connection Settings")
            yield textual.widgets.Input(
                placeholder="host (e.g. example.com)", id="host"
            )
            yield textual.widgets.Input(placeholder="user", id="user")
            yield textual.widgets.Input(placeholder="pass", password=True, id="pass")
            yield textual.widgets.Input(placeholder="path", id="path")
            yield textual.widgets.Button("Save", variant="primary", id="save")


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

    def action_dismiss(self) -> None:
        self.dismiss()

    def on_mount(self):
        self.notify("Load SSH Connection...")

    def compose(self) -> textual.app.ComposeResult:
        yield textual.widgets.Header()
        yield textual.widgets.Footer()
        with textual.containers.Container():
            yield textual.widgets.Label("Load Saved Connection")
            yield textual.widgets.ListView(
                textual.widgets.ListItem(textual.widgets.Label("Connection 1")),
                textual.widgets.ListItem(textual.widgets.Label("Connection 2")),
            )


class Trees(textual.containers.Horizontal):
    def compose(self) -> textual.app.ComposeResult:
        yield textual.widgets.DirectoryTree("./")
        yield RemoteTree()


class RemoteTree(textual.widgets.Tree):
    def __init__(self):
        super().__init__("Remote")
        self.root.expand()

    def on_mount(self):
        self.root.add_leaf("Connect to see remote files ...")


if __name__ == "__main__":
    app = RSyncApp()
    app.run()
