from abc import ABC, abstractmethod
from typing import Any


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
        current_storage = self.internal_storage.pop(0)
        return (current_rank, current_storage)


class NumericProcessor(DataProcessor):
    def __init__(self):
        print("Testing Numeric Processor...")
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
        print("\nTesting Text Processor...")

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
        print("\nTesting Log Processor...")

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
            raise TypeError("Got exception: Improper numeric data")
        if isinstance(data, list):
            for item in data:
                stri = f"{item['log_level']}: {item['log_message']}"
                self.internal_storage.append(stri)
        else:
            stri = f"{data['log_level']}: {data['log_message']}"
            self.internal_storage.append(stri)


if __name__ == "__main__":
    print("=== Code Nexus - Data Processor ===\n")
    first = NumericProcessor()
    numeric_list = [1, 2, 3, 4, 5]
    text_list = ['Hello', 'Nexus', 'World']
    processing_data = [{"log_level": "NOTICE", "log_message": "Connection \
to server"}, {"log_level": "ERROR", "log_\
message": "Unauthorized access!!"}]
    print(f"Trying to validate input: {first.validate(42)}")
    print(f"Trying to validate input: {first.validate('elias')}")
    try:
        first.ingest("foo")
    except TypeError as e:
        print(e)
    print(f"Processing data: {numeric_list}")
    print("Extracting 3 values...")
    first.ingest(numeric_list)
    for _ in range(3):
        rank, value = first.output()
        print(f"Numeric value {rank}: {value}")
    second = TextProcessor()
    second.ingest(text_list)
    print(f"Trying to validate input: {second.validate(42)}")
    print(f"Processing data: {text_list}")
    print("Extracting 1 value...")
    for _ in range(1):
        rank, value = second.output()
        print(f"Text value {rank}: {value}")
    third = LogProcessor()
    third.ingest(processing_data)
    print(f"Trying to validate input {'hello'}: {third.validate('hello')}")
    print("Extracting 2 values...")
    for _ in range(2):
        rank, value = third.output()
        print(f"Log entry {rank}: {value}")
