from enum import StrEnum
class Role(StrEnum):
    ADMIN="admin"
    ANALYST="analyst"
    VIEWER="viewer"
class RunStatus(StrEnum):
    QUEUED="queued"
    RUNNING="running"
    COMPLETED="completed"
    FAILED="failed"
class QualificationMode(StrEnum):
    RAW="raw"
    CALIBRATION="calibration_only"
class QualificationStatus(StrEnum):
    DRAFT="draft"
    APPROVED="approved"
