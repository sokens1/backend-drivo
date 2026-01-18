import uuid
import asyncio
from typing import Dict, Any

class AirtelMoneyService:
    """
    Service de simulation pour Airtel Money Gabon.
    Permet de tester le flux de paiement sans clés API.
    """
    
    @staticmethod
    async def initiate_payment(phone: str, amount: float, reference: str) -> Dict[str, Any]:
        # Simulation d'un délai réseau
        await asyncio.sleep(1)
        
        # En mode simulation, on accepte tout
        transaction_id = str(uuid.uuid4())
        return {
            "status": "PENDING",
            "message": "Push USSD envoyé au téléphone",
            "transaction_id": transaction_id,
            "reference": reference
        }

    @staticmethod
    async def verify_transaction(transaction_id: str) -> bool:
        # Dans une simulation, on considère que l'utilisateur valide toujours après un court délai
        await asyncio.sleep(0.5)
        return True
