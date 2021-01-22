from typing import Any, Dict, List

from lib.observable import ObservableMessage
from lib.observer import Observer
from lib.types import Instruction


class Ui(Observer):

    def __init__(self):
        # TODO start listening for controller keys
        super(Ui, self).__init__()

    def update(self, msg_type: ObservableMessage, msg_data: Any):
        pass

    def start(self,
              instructions: List[Instruction],
              label_table: Dict[str, int],
              opts: Dict[str, Any]):
        # TODO create and register observable
        # TODO start interpreting
        pass

    def terminate(self):
        # TODO Stop interpreter, listening for keyboard and exit program
        pass
