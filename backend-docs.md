# Documentation Backend Drivo

Cette documentation détaille la structure et l'implémentation du backend pour le projet Drivo, une plateforme de vente et location de véhicules au Gabon.

## 1. Stack Technique

- **Framework** : [FastAPI](https://fastapi.tiangolo.com/) (Asynchrone, performant, typé).
- **Base de données** : [MongoDB](https://www.mongodb.com/) (NoSQL, flexible pour les structures de véhicules variées).
- **ODM (Object Data Mapper)** : [Beanie](https://beanie-odm.dev/) (Basé sur Pydantic et Motor pour un typage fort et des requêtes asynchrones).
- **Authentification** : JWT (JSON Web Tokens) avec support OTP (SMS via Twilio ou équivalent local).
- **Validation** : Pydantic v2.
- **Environnement** : Python 3.11+.

## 2. Structure du Projet

```text
drivo-backend/
├── app/
│   ├── main.py              # Point d'entrée de l'application
│   ├── core/                # Configuration, sécurité (JWT), constantes
│   ├── models/              # Modèles Beanie (Collections MongoDB)
│   ├── schemas/             # Schémas Pydantic (Request/Response)
│   ├── api/                 # Routers API (v1)
│   │   ├── endpoints/       # auth.py, vehicles.py, etc.
│   ├── services/            # Logique métier (paiements, notifications)
│   └── utils/               # Helpers (OTP, S3 upload)
├── .env                     # Variables d'environnement
├── pyproject.toml           # Dépendances (Poetry/Pip)
└── docker-compose.yml       # Setup MongoDB & Redis local
```

## 3. Schéma de Données (Collections MongoDB)

### **User** (Collection: `users`)
```python
class User(Document):
    email: str
    password_hash: str
    full_name: str
    phone: str  # Format +241XXXXXXX
    role: str   # "client", "agence", "admin"
    is_verified: bool = False
    favorites: List[PydanticObjectId] = []
    created_at: datetime = Field(default_factory=datetime.utcnow)

    class Settings:
        name = "users"
```

### **Agency** (Collection: `agencies`)
```python
class Agency(Document):
    user_id: PydanticObjectId
    name: str
    logo_url: str
    address: str
    phone: str
    verified: bool = False
    rating: float = 0.0
    
    class Settings:
        name = "agencies"
```

### **Vehicle** (Collection: `vehicles`)
```python
class Vehicle(Document):
    agency_id: PydanticObjectId
    title: str
    brand: str
    model: str
    year: int
    price: float
    price_per_day: Optional[float]
    type: str  # "vente", "location", "both"
    category: str # "suv", "sedan", etc.
    images: List[str]
    km: int
    fuel: str
    transmission: str
    location: str
    features: List[str]
    description: str
    views: int = 0
    available: bool = True
    adapted_roads: bool = False # Spécifique Gabon
    
    class Settings:
        name = "vehicles"
```

### **Reservation** (Collection: `reservations`)
```python
class Reservation(Document):
    vehicle_id: PydanticObjectId
    user_id: PydanticObjectId
    start_date: datetime
    end_date: datetime
    total_price: float
    status: str # "pending", "confirmed", "completed", "cancelled"
    payment_method: str # "orange_money", "airtel_money", "card"
    type: str # "location", "vente"
    
    class Settings:
        name = "reservations"
```

## 4. Endpoints API Prioritaires

| Méthode | Endpoint | Description | Rôle |
| :--- | :--- | :--- | :--- |
| **POST** | `/auth/signup` | Inscription & envoi OTP SMS | Tous |
| **POST** | `/auth/token` | Connexion & Retour JWT | Tous |
| **GET** | `/vehicles` | Liste avec filtres (prix, type, géo) | Tous |
| **POST** | `/vehicles` | Ajout véhicule (upload images) | Agence |
| **POST** | `/bookings/create` | Init réservation & calcul prix | Client |
| **POST** | `/bookings/{id}/pay` | Déclenchement Mobile Money API | Client |
| **GET** | `/agency/dashboard` | Statistiques & gestion stocks | Agence |

## 5. Intégrations Gabon

### **OTP (SMS)**
Pour le Gabon, utilisez **Africa's Talking** ou **Twilio**.
Le format des numéros doit être validé : `+241` suivi de 7 ou 8 chiffres selon l'opérateur (Airtel `07`, Orange `06`).

### **Paiements Mobile Money**
1. **Orange Money Web API** : Intégration via leur portail développeur.
2. **Airtel Money API** : Utilisation du marchand Airtel.
3. **Logic Flow** : 
   - Le frontend envoie le numéro.
   - Le backend initie la transaction (Push USSD).
   - Utilisation d'un `Webhook` pour confirmer le paiement.

## 6. Lancement (Développement)

```bash
# 1. Créer environnement
python -m venv venv
source venv/bin/activate

# 2. Installer deps
pip install fastapi[all] beanie motor pydantic-settings pyjwt

# 3. Lancer application
uvicorn app.main:app --reload
```
