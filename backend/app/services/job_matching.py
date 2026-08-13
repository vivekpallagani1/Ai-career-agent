class JobMatchingService:
    """Placeholder service for future match-score calculation."""

    def score_candidate_job(self, candidate_profile: dict, job: dict) -> dict:
        return {
            'overall_match': 0,
            'matched_skills': [],
            'missing_skills': [],
            'reasoning': [],
            'job': job.get('title', 'Unknown Role'),
            'candidate': candidate_profile.get('name', 'Candidate'),
        }
