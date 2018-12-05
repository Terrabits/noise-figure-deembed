from pathlib                      import Path
from rohdeschwarz.instruments.vna import Vna

root_path = Path(__file__).parent
log_file  = str(root_path / 'vna log.txt')

vna = Vna()
vna.open_tcp()
vna.open_log(log_file)

# Do the work

assert not vna.errors
vna.clear_status();
