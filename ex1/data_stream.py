from abc import ABC, abstractmethod
from typing import Any
import typing


class DataProcessor(ABC):
    def __init__(self):
        super().__init__()
        self.internal_storage = []
        self.rank_counter = 0

    @abstractmethod
    def validate(self, data: Any) -> bool:
        pass

    @abstractmethod
    def ingest(self, data: Any) -> None:
        pass

    def output(self) -> tuple[int, str]:
        current_rank = self.rank_counter
        self.rank_counter += 1
        try: 
            current_storage = self.internal_storage.pop(0)
        except IndexError:
            current_storage = ""
        return (current_rank, current_storage)

class DataStream():
    def __init__(self):
        self.processors :list[DataProcessor] = []

    def register_processor(self, proc: DataProcessor) -> None:
        for data in proc:
            self.processors.append(data)

    def process_stream(self, stream: list[typing.Any]) -> None:
        for data in stream:
            for proc in self.processors:
                check = False
                if data.validate(data):
                    data.ingest(data)
                    check = True
                    break
                else:
                    print(f"DataStream error - Can’t process element in stream: {data}")



    def print_processors_stats(self) -> None:
        pass

class NumericProcessor(DataProcessor):
    def __init__(self):
        super().__init__()

    def validate(self, data: Any) -> bool:
        if isinstance(data, list):
            for item in data:
                if not isinstance(item, (int, float)):
                    return False
                else:
                    pass
        elif isinstance(data, (int, float)):
            return True
        else:
            return False
        return True

    def ingest(self, data: int | float | list[int | float]) -> None:
        if self.validate(data) is False:
            print(f"Test invalid ingestion of string \
'{data}' without prior validation:")
            raise TypeError("Got exception: Improper numeric data")
        if isinstance(data, list):
            for item in data:
                self.internal_storage.append(str(item))
        else:
            self.internal_storage.append(str(data))


class TextProcessor(DataProcessor):
    def __init__(self):
        super().__init__()

    def validate(self, data: Any) -> bool:
        if isinstance(data, list):
            for item in data:
                if not isinstance(item, str):
                    return False
                else:
                    pass
        elif isinstance(data, str):
            return True
        else:
            return False
        return True

    def ingest(self, data: str | list[str]) -> None:
        if self.validate(data) is False:
            print(f"Test invalid ingestion of string \
'{data}' without prior validation:")
            raise TypeError("Got exception: Improper text data")
        if isinstance(data, list):
            for item in data:
                self.internal_storage.append(item)
        else:
            self.internal_storage.append(data)


class LogProcessor(DataProcessor):
    def __init__(self):
        super().__init__()

    def validate(self, data: Any) -> bool:
        if isinstance(data, list):
            for item in data:
                if not isinstance(item, dict):
                    return False
                else:
                    pass
        elif isinstance(data, dict):
            return True
        else:
            return False
        return True

    def ingest(self, data: dict | list[dict]) -> None:
        if self.validate(data) is False:
            print(f"Test invalid ingestion of string \
'{data}' without prior validation:")
            raise TypeError("Got exception: Improper log data")
        if isinstance(data, list):
            for item in data:
                stri = f"{item['log_level']}: {item['log_message']}"
                self.internal_storage.append(stri)
        else:
            stri = f"{data['log_level']}: {data['log_message']}"
            self.internal_storage.append(stri)


if __name__ == "__main__":
    print("=== Code Nexus - Data Stream ===")
    first = DataStream()
    first.register_processor(['Hello world', [3.14, -1,2.71], [{'log_level': 'WARNING', 'log_message': 'Telnet access!Use ssh instead'}, {'log_level': 'INFO', 'log_message': 'User wilis connected'}], 42, ['Hi', 'five']])
    first.process_stream(first.processors)
