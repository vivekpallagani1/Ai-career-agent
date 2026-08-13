class ResumeParserService:
    """Placeholder resume extraction service."""

    def parse(self, resume_text: str) -> dict:
        return {
            'skills': [],
            'education': [],
            'experience': [],
            'projects': [],
            'raw_length': len(resume_text or ''),
        }
