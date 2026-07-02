import enum


class Role(str, enum.Enum):
    ADMIN = "ADMIN"
    SECURITY = "SECURITY"
    HOST_APPROVER = "HOST_APPROVER"


class VehicleType(str, enum.Enum):
    CAR = "CAR"
    TRUCK = "TRUCK"
    MOTORCYCLE = "MOTORCYCLE"
    DELIVERY_VAN = "DELIVERY_VAN"


class PassType(str, enum.Enum):
    VISITOR = "VISITOR"
    VEHICLE = "VEHICLE"
    VISITOR_WITH_VEHICLE = "VISITOR_WITH_VEHICLE"


class PassStatus(str, enum.Enum):
    PENDING = "PENDING"
    APPROVED = "APPROVED"
    REJECTED = "REJECTED"
    ACTIVE = "ACTIVE"
    COMPLETED = "COMPLETED"
    EXPIRED = "EXPIRED"
    REVOKED = "REVOKED"


class Direction(str, enum.Enum):
    ENTRY = "ENTRY"
    EXIT = "EXIT"