from dataclasses import dataclass
from datetime import datetime
from typing import Optional

@dataclass
class Contract:
    municipio: str
    uf: str
    populacao: int
    latitude: float
    longitude: float
    data_criacao: datetime = datetime.now()
    id: Optional[int] = None

    def to_dict(self):
        return {
            'id': self.id,
            'municipio': self.municipio,
            'uf': self.uf,
            'populacao': self.populacao,
            'latitude': self.latitude,
            'longitude': self.longitude,
            'data_criacao': self.data_criacao
        }

    @classmethod
    def from_dict(cls, data: dict):
        return cls(
            id=data.get('id'),
            municipio=data['municipio'],
            uf=data['uf'],
            populacao=data['populacao'],
            latitude=data['latitude'],
            longitude=data['longitude'],
            data_criacao=data.get('data_criacao', datetime.now())
        )
