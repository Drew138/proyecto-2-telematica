import threading
from time import sleep


class Monitor:
    def __init__(self):
        self.INTERVAL = 10 # TODO
        self.LOAD_SPEED = 5 # TODO
        self.load = 5

        # Simulate the load
        LOAD_SIM = threading.Thread(target=self.simulate_load)
        LOAD_SIM.start()
    
    def heartbeat(self) -> str:
        return "Instance is alive"
    
    def simulate_load(self):
        while True:
            while self.load < 70:
                load += self.LOAD_SPEED
                sleep(self.INTERVAL)
            
            # Wait until deload
            sleep(2*self.INTERVAL)

            while self.load > 10:
                load -= self.LOAD_SPEED
                sleep(self.INTERVAL)
    

    def get_metrics(self) -> int:
        return self.load
        
    def register(self):
        pass
    
    def unregister(self):
        pass