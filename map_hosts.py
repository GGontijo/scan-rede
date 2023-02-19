class MapHosts:
    def __init__(self, known_hosts) -> None:
        self.knowns_mac = []
        self.known_obj = known_hosts
        for i in known_hosts:
            self.knowns_mac.append(i['mac'])

    def match(self, arp_hosts, old_presence) -> dict:
        self.matches_check = list(set(self.knowns_mac) & set(arp_hosts))
        self.matches_names = []
        for i in self.known_obj:
            if i['mac'] in self.matches_check:
                self.matches_names.append(i['name'])

        return self.diff_calc(old_presence, self.matches_names)

    def diff_calc(self, old, new) -> dict:
        old_set = set(old)
        new_set = set(new)    

        self.diff_saiu = old_set.difference(new_set)

        self.diff_entrou = new_set.difference(old_set)

        self.not_changed = list(set(old_set) & set(new_set))

        self.dict = {}
        for i in self.diff_entrou:
            self.dict[i] = {"action": "Entrou"}
        for i in self.diff_saiu:
            self.dict[i] = {"action": "Saiu"}

        for i in self.not_changed:
            self.dict[i] = {"action": "not_changed"}

        return self.dict
       
        




