class MapHosts:
    def __init__(self, know_hosts, arp_hosts) -> None:
        self.knowns = know_hosts
        self.arps = arp_hosts

    def match(self):
        self.matches = list(set(self.knowns) & set(self.arps))
        print(self.matches)
