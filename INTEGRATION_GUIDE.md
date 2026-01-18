# Documentation d'Intégration API - Drivo

Cette documentation est destinée à l'équipe Front-End pour l'intégration du backend Drivo.

## 🔗 Informations Générales
- **Base URL (Production)** : `https://backend-drivo.onrender.com/api/v1`
- **Documentation Interactive (Swagger)** : `https://backend-drivo.onrender.com/docs`
- **Format des données** : JSON (UTF-8)

## 🔐 Authentification
Le backend utilise des **JSON Web Tokens (JWT)**.
1. **Login** : `POST /auth/login` (via Form Data: `username` et `password`).
2. **Usage** : Inclure le token dans le header de chaque requête protégée :
   `Authorization: Bearer <votre_token>`

---

## 🚀 Endpoints Principaux

### 1. Authentification (`/auth`)
- `POST /signup` : Inscription d'un nouvel utilisateur.
- `POST /login` : Connexion et récupération du token.

### 2. Catalogue de Véhicules (`/vehicles`)
- `GET /` : Liste des véhicules (Supporte filtres: `brand`, `type`, `min_price`, `max_price`).
- `GET /{id}` : Détails d'un véhicule (Incrémente automatiquement le compteur de vues).
- `POST /` : Ajout d'un véhicule (Agences uniquement).
- `POST /{id}/images` : Upload de photos (Multipart/form-data).

### 3. Réservations (`/bookings`)
- `POST /create` : Créer une réservation. Le prix total est calculé automatiquement par le backend.
- `GET /` : Historique des réservations de l'utilisateur connecté.

### 4. Profil & Favoris (`/users`)
- `GET /me` : Infos de l'utilisateur connecté.
- `PATCH /me` : Mise à jour (nom, téléphone).
- `POST /me/change-password` : Changement de mot de passe.
- `GET /me/favorites` : Liste des IDs des véhicules favoris.
- `POST /me/favorites/{id}` : Ajouter aux favoris.

### 5. Module Agence (`/agencies`)
- `GET /dashboard` : Statistiques (Revenus, Vues, Total véhicules).
- `PATCH /me` : Mise à jour du profil de l'agence.

### 6. Paiements Airtel Money (`/payments`)
- **Important** : Actuellement en **mode simulation**.
- `POST /airtel/collect` : Initier un paiement. Renvoie un `transaction_id`.
- `POST /airtel/callback` : Simuler la validation du paiement (pour tester le changement de statut de la réservation).

---

## 🛠️ Erreurs Communes
- `401 Unauthorized` : Token manquant ou expiré.
- `403 Forbidden` : L'utilisateur n'a pas les permissions (ex: client essayant d'ajouter un véhicule).
- `422 Unprocessable Entity` : Erreur de validation Pydantic (vérifier le format des données envoyées).

---
**Note** : Le dossier `uploads/` est servi statiquement. Les URLs d'images ressemblent à : `https://backend-drivo.onrender.com/uploads/nom-fichier.jpg`
