from sqlalchemy.orm import Session

from app.models.profile import CandidateProfile


class ProfileRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_by_user_id(self, user_id: int) -> CandidateProfile | None:
        return self.db.query(CandidateProfile).filter(CandidateProfile.user_id == user_id).first()

    def create(self, user_id: int, **kwargs) -> CandidateProfile:
        profile = CandidateProfile(user_id=user_id, **kwargs)
        self.db.add(profile)
        self.db.commit()
        self.db.refresh(profile)
        return profile

    def update(self, profile_id: int, **kwargs) -> CandidateProfile | None:
        profile = self.db.query(CandidateProfile).filter(CandidateProfile.id == profile_id).first()
        if profile:
            for key, value in kwargs.items():
                setattr(profile, key, value)
            self.db.commit()
            self.db.refresh(profile)
        return profile
