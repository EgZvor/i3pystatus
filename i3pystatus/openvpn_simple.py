from i3pystatus import IntervalModule
from i3pystatus.core.command import run_through_shell

__author__ = 'egzvor'


class OpenVPN(IntervalModule):
    """
    Monitor OpenVPN connections.

    Formatters:

    * {vpn_name} — Same as setting.
    * {status} — Unicode up or down symbol.
    * {output} — Output of status_command.

    """

    color_up = "#00ff00"
    color_down = "#FF0000"
    status_up = '▲'
    status_down = '▼'
    format = "{vpn_name} {status}"

    status_command = "pgrep -f 'openvpn.*%(vpn_name)s'"

    connected = False
    vpn_name = ''

    settings = (
        ("format", "Format string"),
        ("color_up", "VPN is up"),
        ("color_down", "VPN is down"),
        ("status_down", "Symbol to display when down"),
        ("status_up", "Symbol to display when up"),
        ("vpn_name", "Name of VPN"),
    )

    def init(self):
        if not self.vpn_name:
            raise Exception("vpn_name is required")

    def run(self):
        cmd = self.status_command % {'vpn_name': self.vpn_name}
        command_result = run_through_shell(cmd)
        self.connected = command_result.rc == 0

        if self.connected:
            color, status = self.color_up, self.status_up
        else:
            color, status = self.color_down, self.status_down

        self.output = {
            "full_text": self.format.format(
                vpn_name=self.vpn_name,
                status=status,
            ),
            'color': color,
        }
