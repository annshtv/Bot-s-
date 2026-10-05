from dataclasses import dataclass, field


@dataclass
class Service:
    name: str
    price: int


@dataclass
class BotConfig:
    token: str
    business_name: str
    description: str
    category: str
    features: dict[str, bool] = field(default_factory=dict)
    services: list[Service] = field(default_factory=list)
    hours: str = ""
    address: str = ""
    channel: str = ""