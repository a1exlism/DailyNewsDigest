from pydantic import BaseModel, Field
from datetime import datetime
from typing import List, Optional


class RetrievalInfo(BaseModel):
    retrieved_date: datetime
    source_type: str


class SourceOutlet(BaseModel):
    name: str
    domain: str


class Category(BaseModel):
    primary: str
    secondary: List[str] = []


class Sentiment(BaseModel):
    label: str
    score: Optional[float] = None


class FactualClaim(BaseModel):
    claim: str
    verification_status: str


class KeyEntities(BaseModel):
    persons: List[str] = []
    organizations: List[str] = []
    locations: List[str] = []


class CoreContent(BaseModel):
    title: str
    url: str
    publication_date: Optional[datetime] = None
    author: List[str] = []
    source_outlet: SourceOutlet
    media_type: str
    language: str
    original_content: str


class AnalysisSummary(BaseModel):
    summary: str
    keywords: List[str] = []
    category: Optional[Category] = None
    sentiment: Optional[Sentiment] = None
    key_entities: Optional[KeyEntities] = None
    factual_claims: List[FactualClaim] = []


class DailyDigest(BaseModel):
    unique_id: str
    retrieval_info: RetrievalInfo
    core_content: CoreContent
    analysis_summary: AnalysisSummary