import subprocess


class ScanRede:
    
    def __init__(self) -> None:
        subprocess.call(['sh', './scan_rede.sh'])