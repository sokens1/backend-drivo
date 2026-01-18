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
- `GET /` : Liste des véhicules (Filtres: `brand`, `type`, `agency_id`, `min_price`, `max_price`, `skip`, `limit`).
- `GET /{id}` : Détails d'un véhicule (Incrémente automatiquement le compteur de vues).
- `POST /` : Ajout d'un véhicule (Agences uniquement).
- `PUT /{id}` : Modification d'un véhicule (Propriétaire uniquement).
- `DELETE /{id}` : Suppression d'un véhicule (Propriétaire uniquement).
- `POST /{id}/images` : Upload de photos (Multipart/form-data, plusieurs fichiers possibles).

### 3. Réservations (`/bookings`)
- `POST /create` : Créer une réservation. Le prix total est calculé automatiquement par le backend.
- `GET /` : Historique des réservations de l'utilisateur connecté.
- `GET /{id}` : Détails d'une réservation spécifique.

### 4. Profil & Favoris (`/users`)
- `GET /me` : Infos de l'utilisateur connecté.
- `PATCH /me` : Mise à jour (nom, téléphone).
- `POST /me/change-password` : Changement de mot de passe.
- `GET /me/favorites` : Liste des IDs des véhicules favoris.
- `POST /me/favorites/{id}` : Ajouter aux favoris.
- `DELETE /me/favorites/{id}` : Retirer des favoris.
- `POST /me/avatar` : Upload d'avatar (Multipart/form-data).

### 5. Module Agence (`/agencies`)
- `GET /` : **Liste publique de toutes les agences** (Pagination: `skip`, `limit`).
- `GET /me` : Profil de l'agence de l'utilisateur connecté.
- `GET /dashboard` : Statistiques (Revenus, Vues, Total véhicules).
- `PATCH /me` : Mise à jour du profil de l'agence.
- `POST /me/logo` : Upload du logo de l'agence (Multipart/form-data).

### 6. Paiements Airtel Money (`/payments`)
- **Important** : Actuellement en **mode simulation**.
- `POST /airtel/collect` : Initier un paiement. Renvoie un `transaction_id`.
- `POST /airtel/callback` : Simuler la validation du paiement (pour tester le changement de statut de la réservation).

### 7. Notifications (`/notifications`)
- `GET /` : Liste des notifications de l'utilisateur (Triées par date décroissante).
- `PATCH /{id}/read` : Marquer une notification comme lue.

### 8. Messages (`/messages`)
- `GET /` : Liste tous les messages envoyés ou reçus par l'utilisateur.
- `POST /` : Envoyer un nouveau message.

---

## 🎯 Cas d'usage spécifiques

### Comment uploader des images pour un nouveau véhicule ?
1. Créer d'abord le véhicule via `POST /vehicles/` (renvoie un `id`).
2. Puis uploader les images via `POST /vehicles/{id}/images`.

### Comment filtrer les véhicules par agence ?
Utilisez le paramètre `agency_id` : `GET /vehicles/?agency_id=5eb7cf5a86d9755df3a6c593`

### Upload multiple d'images
L'endpoint `POST /vehicles/{id}/images` accepte plusieurs fichiers en une seule requête (FormData avec champ `files[]`).

---

## 🛠️ Erreurs Communes
- `401 Unauthorized` : Token manquant ou expiré.
- `403 Forbidden` : L'utilisateur n'a pas les permissions (ex: client essayant d'ajouter un véhicule).
- `422 Unprocessable Entity` : Erreur de validation Pydantic (vérifier le format des données envoyées).

---
**Note** : Le dossier `uploads/` est servi statiquement. Les URLs d'images ressemblent à : `https://backend-drivo.onrender.com/uploads/nom-fichier.jpg`
