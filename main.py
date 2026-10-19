from abc import ABC, abstractmethod
import random
class Asset(ABC):
    def __init__(self, asset_id, location):
        self.asset_id = asset_id
        self.location = location
        self.__health = 100  # encapsulated

    def get_health(self):
        return self.__health

    def degrade(self, amount):
        self.__health = max(0, self.__health - amount)

    def needs_maintenance(self):
        return self.__health < 60

    @abstractmethod
    def power_output_mw(self):
        pass
class GasTurbine(Asset):
    def __init__(self, asset_id, location, capacity_mw):
        super().__init__(asset_id, location)
        self.capacity_mw = capacity_mw
    def power_output_mw(self):
        return round(self.capacity_mw * self.get_health() / 100, 1)
class WindTurbine(Asset):
    def __init__(self, asset_id, location, rated_mw):
        super().__init__(asset_id, location)
        self.rated_mw = rated_mw

    def power_output_mw(self):
        wind_factor = random.uniform(0.2, 1.0)
        return round(self.rated_mw * wind_factor * self.get_health() / 100, 1)


class Transformer(Asset):
    def __init__(self, asset_id, location, load_mw):
        super().__init__(asset_id, location)
        self.load_mw = load_mw

    def power_output_mw(self):
        efficiency = 0.99 if self.get_health() > 60 else 0.95
        return round(self.load_mw * efficiency, 1)


class GridMonitor:
    def __init__(self):
        self.assets = []

    def add(self, asset):
        self.assets.append(asset)

    def simulate_day(self):
        for a in self.assets:
            a.degrade(random.randint(0, 15))

    def report(self):
        total = 0
        for a in self.assets:
            out = a.power_output_mw()
            total += out
            flag = "MAINTENANCE" if a.needs_maintenance() else "OK"
            print(f"{type(a).__name__:12} {a.asset_id:6} {a.location:10} "
                  f"health={a.get_health():3}%  output={out:6} MW  [{flag}]")
        print(f"Total output: {round(total, 1)} MW\n")
if __name__ == "__main__":
    grid = GridMonitor()
    grid.add(GasTurbine("GT-01", "Jaipur", 500))
    grid.add(WindTurbine("WT-07", "Jaisalmer", 8))
    grid.add(Transformer("TR-03", "Ajmer", 400))

    for day in range(1, 4):
        print(f"--- Day {day} ---")
        grid.simulate_day()
        grid.report()