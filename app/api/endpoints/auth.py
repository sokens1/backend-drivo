from fastapi import APIRouter, HTTPException, status, Depends
from fastapi.security import OAuth2PasswordRequestForm
from app.models.user import User
from app.schemas.user import UserCreate, UserOut
from app.schemas.token import Token
from app.core.security import get_password_hash, verify_password, create_access_token

router = APIRouter()

@router.post("/signup", response_model=UserOut, status_code=status.HTTP_201_CREATED)
async def signup(user_in: UserCreate):
    try:
        # Vérifier si l'utilisateur existe déjà
        user = await User.find_one(User.email == user_in.email)
        if user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Cet email est déjà utilisé.",
            )
        
        # Déterminer le rôle (agence ou client)
        role = user_in.role if user_in.role in ["client", "agency", "agence"] else "client"
        if role == "agency":
            role = "agence"  # Normaliser

        # Créer le nouvel utilisateur
        new_user = User(
            email=user_in.email,
            password_hash=get_password_hash(user_in.password),
            full_name=user_in.full_name,
            phone=user_in.phone,
            role=role
        )
        
        await new_user.insert()

        # Si c'est une agence, créer le profil agence
        if role == "agence" and user_in.agency_name:
            from app.models.agency import Agency
            agency = Agency(
                user_id=new_user.id,
                name=user_in.agency_name,
                address="",
                phone=user_in.phone
            )
            await agency.insert()

        return new_user
    except HTTPException:
        raise
    except Exception as e:
        print(f"Signup Error: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erreur lors de l'inscription: {str(e)}"
        )

@router.post("/login", response_model=Token)
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    # Trouver l'utilisateur
    user = await User.find_one(User.email == form_data.username)
    if not user or not verify_password(form_data.password, user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Email ou mot de passe incorrect",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    return {
        "access_token": create_access_token(user.id),
        "token_type": "bearer",
    }
